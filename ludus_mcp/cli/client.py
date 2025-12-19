"""Backwards compatibility shim for client.py.

This module maintains backwards compatibility with existing code.
All new code should use ludus_mcp.mcp_client.unified_client instead.
"""

import warnings
from ludus_mcp.mcp_client.unified_client import UnifiedMCPClient

# Show deprecation warning
warnings.warn(
    "Importing from 'ludus_mcp_client.client' is deprecated. "
    "Please use 'from ludus_mcp.mcp_client import UnifiedMCPClient' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Backwards compatibility alias
LudusMCPClient = UnifiedMCPClient

__all__ = ["LudusMCPClient"]
