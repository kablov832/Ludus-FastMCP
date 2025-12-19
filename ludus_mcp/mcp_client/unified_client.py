"""Unified MCP client implementation.

This consolidates the functionality from simple_client.py and client.py
into a single, robust client that uses the connection manager.
"""

import asyncio
from typing import Any, Optional

from .connection_manager import MCPConnectionManager


class UnifiedMCPClient:
    """Unified MCP client using centralized connection management.

    This client uses the singleton MCPConnectionManager to ensure proper
    connection lifecycle management and automatic recovery.

    Usage:
        async with UnifiedMCPClient() as client:
            tools = await client.list_tools()
            result = await client.call_tool("ludus.get_range", {})
    """

    def __init__(self, command: str = "ludus-fastmcp", env: Optional[dict[str, str]] = None):
        """Initialize the unified MCP client.

        Args:
            command: Command to run the MCP server (default: "ludus-fastmcp")
            env: Environment variables to pass to the server
        """
        self.command = command
        self.env = env or {}
        self.manager = MCPConnectionManager.get_instance()
        self.manager.configure(command=command, env=env)
        self._registered = False

    async def connect(self) -> None:
        """Connect to the MCP server.

        This uses the connection manager, so it may reuse an existing connection.
        """
        await self.manager.ensure_connected()
        if not self._registered:
            self.manager.register_client(self)
            self._registered = True

    async def disconnect(self) -> None:
        """Disconnect from the MCP server.

        Note: This only unregisters this client. The server stays running
        if other clients are connected.
        """
        if self._registered:
            self.manager.unregister_client(self)
            self._registered = False

        # Only cleanup if no other clients
        if self.manager.get_active_client_count() == 0:
            await self.manager.cleanup()

    async def ensure_connected(self) -> bool:
        """Ensure the client is connected.

        Returns:
            True if connected, False otherwise
        """
        if not self._registered:
            await self.connect()
        return await self.manager.ensure_connected()

    async def list_tools(self) -> list[dict[str, Any]]:
        """List all available tools from the MCP server.

        Returns:
            List of tool definitions
        """
        await self.ensure_connected()
        return await self.manager.list_tools()

    async def call_tool(
        self, name: str, arguments: Optional[dict[str, Any]] = None, timeout: float = 120.0
    ) -> dict[str, Any]:
        """Call a tool on the MCP server.

        Args:
            name: Name of the tool to call
            arguments: Arguments to pass to the tool
            timeout: Timeout in seconds (default: 120.0)

        Returns:
            Tool execution result with keys:
            - tool: Tool name
            - arguments: Arguments passed
            - result: Result text
            - is_error: Whether an error occurred
        """
        await self.ensure_connected()
        return await self.manager.call_tool(name, arguments, timeout)

    async def get_health_status(self) -> dict:
        """Get health status of the connection.

        Returns:
            Health status dictionary
        """
        return self.manager._health_monitor.get_health_status()

    async def __aenter__(self) -> "UnifiedMCPClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.disconnect()


# Backwards compatibility aliases
SimpleMCPClient = UnifiedMCPClient
LudusMCPClient = UnifiedMCPClient
