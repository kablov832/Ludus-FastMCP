"""Custom exceptions for Ludus MCP.

This module defines custom exception classes for better error handling
and more informative error messages throughout the application.
"""


class LudusError(Exception):
    """Base exception for all Ludus MCP errors."""

    pass


class LudusAPIError(LudusError):
    """Ludus API returned an error response.

    Attributes:
        status_code: HTTP status code from the API
        message: Error message from the API
        details: Additional error details (endpoint, method, etc.)
    """

    def __init__(
        self, status_code: int, message: str, details: dict[str, any] | None = None
    ):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(f"[{status_code}] {message}")


class LudusConnectionError(LudusError):
    """Failed to connect to Ludus server.

    This is raised when the client cannot establish a connection to the
    Ludus API server (network issues, wrong URL, etc.).
    """

    pass


class LudusAuthenticationError(LudusError):
    """Authentication failed (invalid or missing API key).

    This is raised when the API key is invalid, expired, or missing.
    """

    pass


class LudusValidationError(LudusError):
    """Request validation failed.

    This is raised when request parameters fail validation before
    being sent to the Ludus API.
    """

    pass


class LudusTimeoutError(LudusError):
    """Request timed out.

    This is raised when a request to the Ludus API takes too long
    and exceeds the configured timeout.
    """

    pass


class LudusRateLimitError(LudusError):
    """Rate limit exceeded.

    This is raised when the client has made too many requests and
    hit the rate limit.

    Attributes:
        retry_after: Number of seconds to wait before retrying
    """

    def __init__(self, retry_after: int | None = None):
        self.retry_after = retry_after
        if retry_after:
            super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds")
        else:
            super().__init__("Rate limit exceeded")


class LudusNotFoundError(LudusError):
    """Requested resource not found.

    This is raised when the API returns a 404 status code.
    """

    pass


class LudusPermissionError(LudusError):
    """Insufficient permissions for the requested operation.

    This is raised when the API returns a 403 status code.
    """

    pass


class LudusServerError(LudusError):
    """Ludus server encountered an internal error.

    This is raised when the API returns a 5xx status code.
    """

    pass
