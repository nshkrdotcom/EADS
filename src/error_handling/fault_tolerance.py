"""Fault tolerance mechanisms for handling service failures.

This module implements fault tolerance patterns designed to work with both direct HTTP
and message queue architectures. All components support asynchronous operation patterns
required for message queue readiness.

Message Queue Ready Design Requirements:
1. Async Operation Pattern:
   - All operations must be async-compatible
   - Long-running operations should return job IDs
   - Status checking endpoints must be provided
   - Results should be retrievable via separate endpoints

2. Decoupled Processing:
   - Services must operate independently
   - State management via databases/caches
   - No direct service-to-service dependencies

3. Configurable Timeouts:
   - All operations must respect timeout configurations
   - Worker processes should be adjustable
   - Async mode must be toggleable

Example Usage with Message Queue Pattern:
    ```python
    @circuit_breaker
    @retry_with_backoff
    @fallback
    async def process_message(message_id: str, payload: dict) -> str:
        # Submit job and return ID for status tracking
        job_id = str(uuid.uuid4())
        asyncio.create_task(process_async(job_id, payload))
        return job_id

    # Status check endpoint
    async def get_job_status(job_id: str) -> dict:
        return await db.get_job_status(job_id)

    # Result retrieval endpoint
    async def get_job_result(job_id: str) -> dict:
        return await db.get_job_result(job_id)
    ```
"""

import asyncio
import functools
import time
from typing import Any, Awaitable, Callable, Generic, TypeVar

from cachetools import TTLCache  # type: ignore

T = TypeVar("T")


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open."""


class CircuitBreaker:
    """Circuit breaker implementation for handling service failures.

    This implementation is message queue ready and supports both direct
    HTTP calls and async message processing patterns.
    """

    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60) -> None:
        """Initialize circuit breaker with configurable parameters.

        Args:
            failure_threshold: Number of failures before opening circuit
            reset_timeout: Time in seconds before attempting reset
        """
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.is_open = False
        self._last_failure_time = 0.0

    def __call__(
        self, func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        """Decorator for applying circuit breaker pattern to async functions.

        This decorator is compatible with both direct function calls and
        message queue processing patterns. When used with message queues,
        it tracks failures at the message processing level.
        """

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            current_time = time.time()

            # Check circuit state
            if self.is_open:
                if current_time - self._last_failure_time >= self.reset_timeout:
                    self.is_open = False
                    self.failures = 0
                else:
                    raise CircuitBreakerError("Circuit breaker is open")

            try:
                result = await func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                self._last_failure_time = current_time
                if self.failures >= self.failure_threshold:
                    self.is_open = True
                raise e

        return wrapper


class RetryWithBackoff:
    """Retry mechanism with exponential backoff.

    This implementation supports both direct HTTP calls and message queue
    processing patterns. When used with message queues, it implements
    retry logic at the message processing level.
    """

    def __init__(
        self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0
    ) -> None:
        """Initialize retry mechanism with configurable parameters.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def __call__(
        self, func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        """Decorator for applying retry pattern with exponential backoff.

        This decorator supports both synchronous HTTP calls and asynchronous
        message queue processing. When used with message queues, failed
        messages can be requeued with appropriate delay.
        """

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            retries = 0
            while retries <= self.max_retries:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    if retries == self.max_retries:
                        raise e
                    delay = min(self.base_delay * (2**retries), self.max_delay)
                    await asyncio.sleep(delay)
                    retries += 1
            raise RuntimeError("Should not reach here")

        return wrapper


class Fallback(Generic[T]):
    """Fallback mechanism with caching for failed operations.

    This implementation supports both direct calls and message queue
    processing patterns. When used with message queues, it provides
    cached responses while failed messages are being reprocessed.
    """

    def __init__(self, ttl: int = 300) -> None:
        """Initialize fallback mechanism with TTL cache.

        Args:
            ttl: Time-to-live for cached results in seconds
        """
        self.cache: TTLCache[str, T] = TTLCache(maxsize=100, ttl=ttl)

    def __call__(
        self, func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        """Decorator for applying fallback pattern with caching.

        This decorator supports both direct calls and message queue
        processing. When used with message queues, it can provide
        cached responses while failed messages are being reprocessed.
        """

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            cache_key = str(args) + str(kwargs)
            try:
                result: T = await func(*args, **kwargs)
                self.cache[cache_key] = result
                return result
            except Exception:
                if cache_key in self.cache:
                    cached_result: T = self.cache[cache_key]
                    return cached_result
                raise

        return wrapper
