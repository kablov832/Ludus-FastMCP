"""Centralized MCP connection management.

This module provides a singleton connection manager that ensures only one
MCP server instance is running and manages the lifecycle of client connections.
"""

import asyncio
import json
import os
import subprocess
import sys
from typing import Any, Optional
from threading import Lock

from .health_monitor import HealthMonitor
from ..core.client import LudusAPIClient


class MCPConnectionManager:
    """Centralized MCP connection manager (Singleton).

    Ensures only one MCP server process is running and manages all client
    connections to it. Provides automatic cleanup, health monitoring, and
    connection recovery.
    """

    _instance: Optional["MCPConnectionManager"] = None
    _lock = Lock()

    def __init__(self):
        """Initialize the connection manager.

        Note: Use get_instance() instead of direct instantiation.
        """
        if MCPConnectionManager._instance is not None:
            raise RuntimeError("Use MCPConnectionManager.get_instance() instead")

        self._server_process: Optional[subprocess.Popen] = None
        self._server_command = "ludus-fastmcp"
        self._server_env: dict[str, str] = {}
        self._clients: list[Any] = []  # Track active clients
        self._health_monitor = HealthMonitor(self)
        self._is_shutting_down = False
        self._request_id = 0

    @classmethod
    def get_instance(cls) -> "MCPConnectionManager":
        """Get or create the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton (for testing)."""
        with cls._lock:
            if cls._instance is not None:
                # Cleanup existing instance
                if cls._instance._server_process:
                    try:
                        cls._instance._server_process.kill()
                        cls._instance._server_process.wait()
                    except:
                        pass
            cls._instance = None

    def configure(self, command: str = "ludus-fastmcp", env: Optional[dict[str, str]] = None):
        """Configure the MCP server command and environment.

        Args:
            command: Command to run the MCP server
            env: Environment variables for the server process
        """
        self._server_command = command
        self._server_env = env or {}

    def is_server_alive(self) -> bool:
        """Check if the MCP server process is alive."""
        if self._server_process is None:
            return False
        return self._server_process.poll() is None

    async def ensure_connected(self) -> bool:
        """Ensure MCP server is running and connected.

        Returns:
            True if connected, False otherwise
        """
        # Check if server is alive
        if not self.is_server_alive():
            # Try to start server
            try:
                await self._start_server()
            except Exception as e:
                print(f"Failed to start MCP server: {e}", file=sys.stderr)
                return False

        # Run health check
        is_healthy = await self._health_monitor.check_mcp_server()
        if not is_healthy:
            # Try to recover
            print("MCP server unhealthy, attempting recovery...", file=sys.stderr)
            await self._recover_connection()
            is_healthy = await self._health_monitor.check_mcp_server()

        return is_healthy

    async def _start_server(self) -> None:
        """Start the MCP server process."""
        if self.is_server_alive():
            return  # Already running

        # Cleanup any dead process
        if self._server_process is not None:
            try:
                self._server_process.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                pass
            self._server_process = None

        # Merge environment: system env + custom env (custom takes precedence)
        process_env = {**os.environ, **self._server_env} if self._server_env else None

        print(f"Starting MCP server: {self._server_command}", file=sys.stderr)

        try:
            self._server_process = subprocess.Popen(
                [self._server_command],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=process_env,
                bufsize=0,  # Unbuffered for real-time communication
            )
        except FileNotFoundError:
            raise RuntimeError(
                f"MCP server command not found: {self._server_command}. "
                f"Make sure it's installed and in your PATH."
            )

        # Give server time to start
        await asyncio.sleep(0.2)

        # Check if it started successfully
        if not self.is_server_alive():
            stderr_output = ""
            if self._server_process and self._server_process.stderr:
                stderr_output = self._server_process.stderr.read().decode()
            raise RuntimeError(
                f"MCP server failed to start. Exit code: {self._server_process.returncode if self._server_process else 'unknown'}\n"
                f"Stderr: {stderr_output[:500]}"
            )

        # Initialize the server
        await self._initialize_server()

        print("MCP server started successfully", file=sys.stderr)

    async def _initialize_server(self) -> None:
        """Send initialize request to MCP server."""
        init_params = {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "ludus-fastmcp-connection-manager",
                "version": "0.2.0",
            },
        }

        try:
            result = await self._send_request("initialize", init_params)
        except Exception as e:
            # Get stderr for debugging
            stderr_output = ""
            if self._server_process and self._server_process.stderr:
                stderr_output = self._server_process.stderr.read().decode()
            raise RuntimeError(
                f"Server initialization failed: {e}\nServer stderr: {stderr_output[:500]}"
            )

        # Send initialized notification
        notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }
        notification_json = json.dumps(notification) + "\n"
        try:
            self._server_process.stdin.write(notification_json.encode())
            self._server_process.stdin.flush()
        except BrokenPipeError:
            raise RuntimeError("Server closed connection during initialization")

    async def _send_request(
        self, method: str, params: Optional[dict[str, Any]] = None, timeout: float = 10.0
    ) -> dict[str, Any]:
        """Send a JSON-RPC request to the MCP server.

        Args:
            method: JSON-RPC method name
            params: Method parameters
            timeout: Timeout in seconds

        Returns:
            Response from the server
        """
        if not self.is_server_alive():
            raise RuntimeError("Server is not running")

        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
        }

        if params:
            request["params"] = params

        # Write request
        request_json = json.dumps(request) + "\n"
        try:
            self._server_process.stdin.write(request_json.encode())
            self._server_process.stdin.flush()
        except BrokenPipeError:
            raise RuntimeError("Server closed connection (broken pipe)")

        # Read response with timeout
        loop = asyncio.get_event_loop()
        try:
            response_line = await asyncio.wait_for(
                loop.run_in_executor(None, self._server_process.stdout.readline),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            raise RuntimeError(f"Server did not respond within {timeout} seconds")

        if not response_line:
            # Check if process died
            if not self.is_server_alive():
                stderr_output = ""
                if self._server_process.stderr:
                    stderr_output = self._server_process.stderr.read().decode()
                raise RuntimeError(
                    f"Server process exited with code {self._server_process.returncode}. "
                    f"Stderr: {stderr_output[:500]}"
                )
            raise RuntimeError("Server closed connection")

        try:
            response = json.loads(response_line.decode().strip())
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response: {response_line.decode()[:200]}")

        if "error" in response:
            error_info = response["error"]
            error_msg = error_info.get("message", str(error_info))
            raise RuntimeError(f"MCP error: {error_msg}")

        return response.get("result", {})

    async def call_tool(
        self, name: str, arguments: Optional[dict[str, Any]] = None, timeout: float = 120.0
    ) -> dict[str, Any]:
        """Call a tool on the MCP server.

        Args:
            name: Tool name
            arguments: Tool arguments
            timeout: Timeout in seconds

        Returns:
            Tool result
        """
        # Ensure connected
        if not await self.ensure_connected():
            raise RuntimeError("Failed to connect to MCP server")

        if arguments is None:
            arguments = {}

        # Use longer timeout for LLM-based tools
        if "agent" in name or "build" in name or "prompt" in name:
            timeout = max(timeout, 180.0)

        result = await self._send_request("tools/call", {
            "name": name,
            "arguments": arguments,
        }, timeout=timeout)

        # Extract content
        content = result.get("content", [])
        output = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                output.append(item["text"])
            else:
                output.append(str(item))

        return {
            "tool": name,
            "arguments": arguments,
            "result": "\n".join(output),
            "is_error": result.get("isError", False),
        }

    async def list_tools(self) -> list[dict[str, Any]]:
        """List available tools from MCP server.

        Returns:
            List of tool definitions
        """
        # Ensure connected
        if not await self.ensure_connected():
            raise RuntimeError("Failed to connect to MCP server")

        result = await self._send_request("tools/list")
        return result.get("tools", [])

    async def _recover_connection(self) -> None:
        """Attempt to recover the connection."""
        print("Attempting connection recovery...", file=sys.stderr)

        # Kill zombie processes
        await self._kill_zombie_processes()

        # Restart server
        await self._restart_server()

    async def _kill_zombie_processes(self) -> None:
        """Kill any zombie MCP server processes."""
        if self._server_process and not self.is_server_alive():
            try:
                self._server_process.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                self._server_process.kill()
                self._server_process.wait()
            self._server_process = None

        # Also check for orphaned processes (platform-specific)
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and self._server_command in ' '.join(cmdline):
                        # Check if it's not our current process
                        if self._server_process is None or proc.pid != self._server_process.pid:
                            print(f"Killing orphaned process: {proc.pid}", file=sys.stderr)
                            proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except ImportError:
            # psutil not available, skip orphan cleanup
            pass

    async def _restart_server(self) -> None:
        """Restart the MCP server."""
        # Stop current server
        await self.cleanup(graceful=False)

        # Start new server
        await self._start_server()

    async def cleanup(self, graceful: bool = True) -> None:
        """Cleanup all connections and stop the server.

        Args:
            graceful: If True, attempt graceful shutdown. If False, force kill.
        """
        if self._is_shutting_down:
            return

        self._is_shutting_down = True

        print("Cleaning up MCP connections...", file=sys.stderr)

        # Clear client list
        self._clients.clear()

        # Stop server process
        if self._server_process:
            try:
                if graceful:
                    # Try graceful shutdown
                    if self._server_process.stdin:
                        self._server_process.stdin.close()
                    self._server_process.terminate()
                    try:
                        self._server_process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        # Force kill if it doesn't terminate
                        self._server_process.kill()
                        self._server_process.wait()
                else:
                    # Force kill immediately
                    self._server_process.kill()
                    self._server_process.wait()
            except Exception as e:
                print(f"Error during cleanup: {e}", file=sys.stderr)
            finally:
                self._server_process = None

        self._is_shutting_down = False
        print("Cleanup complete", file=sys.stderr)

    def register_client(self, client: Any) -> None:
        """Register a client connection.

        Args:
            client: Client object to register
        """
        if client not in self._clients:
            self._clients.append(client)

    def unregister_client(self, client: Any) -> None:
        """Unregister a client connection.

        Args:
            client: Client object to unregister
        """
        if client in self._clients:
            self._clients.remove(client)

    def get_active_client_count(self) -> int:
        """Get the number of active clients.

        Returns:
            Number of active clients
        """
        return len(self._clients)

    async def __aenter__(self) -> "MCPConnectionManager":
        """Async context manager entry."""
        await self.ensure_connected()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.cleanup()
