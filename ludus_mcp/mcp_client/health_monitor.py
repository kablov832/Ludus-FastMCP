"""Health monitoring system for MCP connections.

This module provides health checks and auto-recovery for the MCP server
and Ludus API connectivity.
"""

import asyncio
import sys
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .connection_manager import MCPConnectionManager


class HealthMonitor:
    """Health monitoring and auto-recovery for MCP connections."""

    def __init__(self, connection_manager: "MCPConnectionManager"):
        """Initialize the health monitor.

        Args:
            connection_manager: The connection manager to monitor
        """
        self.connection_manager = connection_manager
        self.last_check: Optional[datetime] = None
        self.consecutive_failures = 0
        self.max_failures = 3
        self._monitoring = False

    async def check_mcp_server(self) -> bool:
        """Check if MCP server is healthy.

        Returns:
            True if healthy, False otherwise
        """
        self.last_check = datetime.now()

        # 1. Check if process is alive
        if not self.connection_manager.is_server_alive():
            print("Health check failed: Server process is not alive", file=sys.stderr)
            self.consecutive_failures += 1
            return False

        # 2. Try to list tools (lightweight operation)
        try:
            tools = await asyncio.wait_for(
                self.connection_manager._send_request("tools/list"),
                timeout=5.0
            )
            if tools and "tools" in tools:
                self.consecutive_failures = 0
                return True
            else:
                print("Health check failed: Invalid tools response", file=sys.stderr)
                self.consecutive_failures += 1
                return False
        except asyncio.TimeoutError:
            print("Health check failed: Server response timeout", file=sys.stderr)
            self.consecutive_failures += 1
            return False
        except Exception as e:
            print(f"Health check failed: {e}", file=sys.stderr)
            self.consecutive_failures += 1
            return False

    async def check_ludus_api(self) -> tuple[bool, Optional[str]]:
        """Check if Ludus API is accessible.

        Returns:
            Tuple of (is_healthy, error_message)
        """
        try:
            from ..core.client import LudusAPIClient
            from utils.config import get_settings

            settings = get_settings()

            # Basic connectivity check
            if not settings.ludus_api_url or not settings.ludus_api_key:
                return False, "Ludus API credentials not configured"

            # Try to connect
            async with LudusAPIClient() as client:
                # Try a lightweight operation
                try:
                    await asyncio.wait_for(
                        client.get_host_info(),
                        timeout=5.0
                    )
                    return True, None
                except asyncio.TimeoutError:
                    return False, "Ludus API timeout"
                except Exception as e:
                    return False, f"Ludus API error: {str(e)}"

        except Exception as e:
            return False, f"Failed to check Ludus API: {str(e)}"

    async def auto_recover(self) -> bool:
        """Attempt automatic recovery.

        Returns:
            True if recovery successful, False otherwise
        """
        if self.consecutive_failures < self.max_failures:
            # Not enough failures yet, don't recover
            return False

        print(f"Attempting auto-recovery after {self.consecutive_failures} failures...", file=sys.stderr)

        try:
            # Step 1: Kill zombie processes
            await self.connection_manager._kill_zombie_processes()

            # Step 2: Restart server
            await self.connection_manager._restart_server()

            # Step 3: Verify recovery
            is_healthy = await self.check_mcp_server()

            if is_healthy:
                print("Auto-recovery successful!", file=sys.stderr)
                self.consecutive_failures = 0
                return True
            else:
                print("Auto-recovery failed", file=sys.stderr)
                return False

        except Exception as e:
            print(f"Auto-recovery error: {e}", file=sys.stderr)
            return False

    async def start_monitoring(self, interval: int = 30) -> None:
        """Start periodic health monitoring.

        Args:
            interval: Check interval in seconds
        """
        if self._monitoring:
            return

        self._monitoring = True
        print(f"Starting health monitoring (interval: {interval}s)...", file=sys.stderr)

        while self._monitoring:
            try:
                # Check MCP server
                is_healthy = await self.check_mcp_server()

                if not is_healthy:
                    # Try auto-recovery if threshold reached
                    if self.consecutive_failures >= self.max_failures:
                        await self.auto_recover()

                # Check Ludus API
                api_healthy, error_msg = await self.check_ludus_api()
                if not api_healthy:
                    print(f"Ludus API health check failed: {error_msg}", file=sys.stderr)

                # Wait for next check
                await asyncio.sleep(interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Health monitoring error: {e}", file=sys.stderr)
                await asyncio.sleep(interval)

        print("Health monitoring stopped", file=sys.stderr)

    def stop_monitoring(self) -> None:
        """Stop periodic health monitoring."""
        self._monitoring = False

    def get_health_status(self) -> dict:
        """Get current health status.

        Returns:
            Health status dictionary
        """
        return {
            "mcp_server_alive": self.connection_manager.is_server_alive(),
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "consecutive_failures": self.consecutive_failures,
            "monitoring_active": self._monitoring,
            "active_clients": self.connection_manager.get_active_client_count(),
        }
