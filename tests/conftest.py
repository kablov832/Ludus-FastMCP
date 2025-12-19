"""Pytest configuration and shared fixtures."""

import pytest
import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

from ludus_mcp.core.client import LudusAPIClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_ludus_client() -> AsyncGenerator[LudusAPIClient, None]:
    """Create a mock Ludus API client for testing.

    This fixture provides a client with mocked HTTP responses.
    """
    client = LudusAPIClient(
        base_url="https://test.ludus.local:8080", api_key="test.api-key"
    )

    # Mock the underlying HTTP client
    client.client = AsyncMock()

    yield client

    # Cleanup
    await client.close()


@pytest.fixture
def mock_range_response() -> dict:
    """Mock response for get_range API call."""
    return {
        "range_id": "test-range-123",
        "user_id": "test-user",
        "status": "deployed",
        "vms": [
            {"name": "DC01", "ip": "10.0.0.10", "status": "running"},
            {"name": "WS01", "ip": "10.0.0.20", "status": "running"},
        ],
        "networks": [{"name": "internal", "cidr": "10.0.0.0/24"}],
    }


@pytest.fixture
def mock_templates_response() -> list:
    """Mock response for list_templates API call."""
    return [
        {
            "name": "kali-linux-2023",
            "description": "Kali Linux 2023",
            "os": "linux",
            "version": "2023.1",
        },
        {
            "name": "windows-server-2022",
            "description": "Windows Server 2022",
            "os": "windows",
            "version": "2022",
        },
        {
            "name": "ubuntu-22.04",
            "description": "Ubuntu 22.04 LTS",
            "os": "linux",
            "version": "22.04",
        },
    ]


@pytest.fixture
def mock_users_response() -> list:
    """Mock response for list_users API call."""
    return [
        {"user_id": "admin", "name": "Administrator", "is_admin": True},
        {"user_id": "user1", "name": "Test User 1", "is_admin": False},
        {"user_id": "user2", "name": "Test User 2", "is_admin": False},
    ]


@pytest.fixture
def mock_snapshots_response() -> list:
    """Mock response for list_snapshots API call."""
    return [
        {
            "vm_name": "DC01",
            "snapshot_name": "clean-state",
            "description": "Initial clean state",
            "created_at": "2024-12-01T10:00:00Z",
        },
        {
            "vm_name": "DC01",
            "snapshot_name": "post-domain-setup",
            "description": "After domain controller setup",
            "created_at": "2024-12-01T11:30:00Z",
        },
        {
            "vm_name": "WS01",
            "snapshot_name": "clean-state",
            "description": "Initial clean state",
            "created_at": "2024-12-01T10:00:00Z",
        },
    ]


@pytest.fixture
def mock_error_response() -> dict:
    """Mock error response from API."""
    return {"error": "Resource not found", "status_code": 404, "details": {}}
