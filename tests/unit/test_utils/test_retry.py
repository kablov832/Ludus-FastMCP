"""Tests for retry utility."""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from ludus_mcp.utils.retry import async_retry


class TestAsyncRetry:
    """Test suite for async_retry decorator."""

    @pytest.mark.asyncio
    async def test_successful_call_no_retry(self):
        """Test that successful calls don't trigger retries."""
        call_count = 0

        @async_retry(max_attempts=3)
        async def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await successful_function()

        assert result == "success"
        assert call_count == 1  # Should only be called once

    @pytest.mark.asyncio
    async def test_retry_on_exception(self):
        """Test that exceptions trigger retries."""
        call_count = 0

        @async_retry(max_attempts=3, initial_delay=0.01)
        async def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "success"

        result = await failing_function()

        assert result == "success"
        assert call_count == 3  # Should be called 3 times

    @pytest.mark.asyncio
    async def test_max_attempts_exceeded(self):
        """Test that max attempts is respected."""
        call_count = 0

        @async_retry(max_attempts=3, initial_delay=0.01)
        async def always_failing_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Permanent error")

        with pytest.raises(ValueError, match="Permanent error"):
            await always_failing_function()

        assert call_count == 3  # Should be called exactly 3 times

    @pytest.mark.asyncio
    async def test_specific_exception_filtering(self):
        """Test that only specified exceptions trigger retries."""
        call_count = 0

        @async_retry(max_attempts=3, exceptions=(ValueError,), initial_delay=0.01)
        async def function_with_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("This should not be retried")

        with pytest.raises(TypeError):
            await function_with_type_error()

        assert call_count == 1  # Should only be called once (no retry)

    @pytest.mark.asyncio
    async def test_exponential_backoff(self):
        """Test that exponential backoff delays are applied."""
        call_times = []

        @async_retry(max_attempts=3, backoff_factor=2.0, initial_delay=0.1)
        async def function_with_delays():
            call_times.append(asyncio.get_event_loop().time())
            raise ValueError("Error")

        with pytest.raises(ValueError):
            await function_with_delays()

        # Check that delays increase exponentially
        assert len(call_times) == 3

        # First retry should be after ~0.1s (initial_delay)
        # Second retry should be after ~0.2s (initial_delay * backoff_factor)
        if len(call_times) >= 3:
            delay1 = call_times[1] - call_times[0]
            delay2 = call_times[2] - call_times[1]

            # Allow some tolerance for timing
            assert 0.08 <= delay1 <= 0.15
            assert 0.15 <= delay2 <= 0.30

    @pytest.mark.asyncio
    async def test_max_delay_cap(self):
        """Test that max_delay caps the exponential backoff."""
        call_times = []

        @async_retry(
            max_attempts=4,
            backoff_factor=10.0,
            initial_delay=0.1,
            max_delay=0.2,  # Cap at 0.2s
        )
        async def function_with_capped_delay():
            call_times.append(asyncio.get_event_loop().time())
            raise ValueError("Error")

        with pytest.raises(ValueError):
            await function_with_capped_delay()

        # All delays should be capped at max_delay
        if len(call_times) >= 3:
            for i in range(1, len(call_times)):
                delay = call_times[i] - call_times[i - 1]
                assert delay <= 0.25  # Allow some tolerance

    @pytest.mark.asyncio
    async def test_retry_preserves_return_value(self):
        """Test that retry preserves the original return value."""

        @async_retry(max_attempts=3)
        async def function_with_complex_return():
            return {"status": "ok", "data": [1, 2, 3]}

        result = await function_with_complex_return()

        assert result == {"status": "ok", "data": [1, 2, 3]}

    @pytest.mark.asyncio
    async def test_retry_with_function_arguments(self):
        """Test retry decorator works with function arguments."""
        call_count = 0

        @async_retry(max_attempts=2, initial_delay=0.01)
        async def function_with_args(a, b, c=10):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First call fails")
            return a + b + c

        result = await function_with_args(1, 2, c=3)

        assert result == 6
        assert call_count == 2
