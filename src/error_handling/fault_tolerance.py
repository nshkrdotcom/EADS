"""Fault tolerance mechanisms for handling service failures."""

import asyncio
import functools
from typing import Any, Awaitable, Callable, Generic, TypeVar

from cachetools import TTLCache  # type: ignore

T = TypeVar("T")


class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open."""

    pass


class CircuitBreaker:
    """Circuit breaker implementation for handling service failures."""

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
        """Decorator for applying circuit breaker pattern to async functions."""

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            if self.is_open:
                if (
                    asyncio.get_event_loop().time() - self._last_failure_time
                    >= self.reset_timeout
                ):
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
                self._last_failure_time = asyncio.get_event_loop().time()
                if self.failures >= self.failure_threshold:
                    self.is_open = True
                raise e

        return wrapper


class RetryWithBackoff:
    """Retry mechanism with exponential backoff."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0) -> None:
        """Initialize retry mechanism with configurable parameters.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay between retries in seconds
        """
        self.max_retries = max_retries
        self.base_delay = base_delay

    def __call__(
        self, func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        """Decorator for applying retry pattern with exponential backoff."""

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
                    delay = self.base_delay * (2**retries)
                    await asyncio.sleep(delay)
                    retries += 1
            raise RuntimeError("Should not reach here")

        return wrapper


class Fallback(Generic[T]):
    """Fallback mechanism with caching for failed operations."""

    def __init__(self, ttl: int = 300) -> None:
        """Initialize fallback mechanism with TTL cache.

        Args:
            ttl: Time-to-live for cached results in seconds
        """
        self.cache: TTLCache[str, T] = TTLCache(maxsize=100, ttl=ttl)

    def __call__(
        self, func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        """Decorator for applying fallback pattern with caching."""

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
