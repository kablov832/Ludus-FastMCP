"""Tests for custom exception classes."""

import pytest
from ludus_mcp.exceptions import (
    LudusError,
    LudusAPIError,
    LudusConnectionError,
    LudusAuthenticationError,
    LudusNotFoundError,
    LudusPermissionError,
    LudusServerError,
    LudusTimeoutError,
    LudusRateLimitError,
    LudusValidationError,
)


class TestExceptions:
    """Test suite for exception classes."""

    def test_base_exception(self):
        """Test base LudusError exception."""
        error = LudusError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_api_error(self):
        """Test LudusAPIError with status code and details."""
        error = LudusAPIError(
            status_code=400,
            message="Bad request",
            details={"field": "value", "endpoint": "/test"},
        )

        assert error.status_code == 400
        assert error.message == "Bad request"
        assert error.details == {"field": "value", "endpoint": "/test"}
        assert "[400]" in str(error)
        assert "Bad request" in str(error)

    def test_api_error_without_details(self):
        """Test LudusAPIError without details."""
        error = LudusAPIError(status_code=500, message="Server error")

        assert error.status_code == 500
        assert error.message == "Server error"
        assert error.details == {}

    def test_connection_error(self):
        """Test LudusConnectionError."""
        error = LudusConnectionError("Cannot connect to server")
        assert str(error) == "Cannot connect to server"
        assert isinstance(error, LudusError)

    def test_authentication_error(self):
        """Test LudusAuthenticationError."""
        error = LudusAuthenticationError("Invalid API key")
        assert str(error) == "Invalid API key"
        assert isinstance(error, LudusError)

    def test_not_found_error(self):
        """Test LudusNotFoundError."""
        error = LudusNotFoundError("Resource not found")
        assert str(error) == "Resource not found"
        assert isinstance(error, LudusError)

    def test_permission_error(self):
        """Test LudusPermissionError."""
        error = LudusPermissionError("Permission denied")
        assert str(error) == "Permission denied"
        assert isinstance(error, LudusError)

    def test_server_error(self):
        """Test LudusServerError."""
        error = LudusServerError("Internal server error")
        assert str(error) == "Internal server error"
        assert isinstance(error, LudusError)

    def test_timeout_error(self):
        """Test LudusTimeoutError."""
        error = LudusTimeoutError("Request timed out")
        assert str(error) == "Request timed out"
        assert isinstance(error, LudusError)

    def test_validation_error(self):
        """Test LudusValidationError."""
        error = LudusValidationError("Invalid input")
        assert str(error) == "Invalid input"
        assert isinstance(error, LudusError)

    def test_rate_limit_error_with_retry_after(self):
        """Test LudusRateLimitError with retry_after."""
        error = LudusRateLimitError(retry_after=60)

        assert error.retry_after == 60
        assert "60 seconds" in str(error)
        assert isinstance(error, LudusError)

    def test_rate_limit_error_without_retry_after(self):
        """Test LudusRateLimitError without retry_after."""
        error = LudusRateLimitError()

        assert error.retry_after is None
        assert "Rate limit exceeded" in str(error)

    def test_exception_inheritance(self):
        """Test that all exceptions inherit from LudusError."""
        exceptions = [
            LudusAPIError(500, "test"),
            LudusConnectionError("test"),
            LudusAuthenticationError("test"),
            LudusNotFoundError("test"),
            LudusPermissionError("test"),
            LudusServerError("test"),
            LudusTimeoutError("test"),
            LudusRateLimitError(),
            LudusValidationError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, LudusError)
            assert isinstance(exc, Exception)
