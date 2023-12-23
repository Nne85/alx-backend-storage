#!/usr/bin/env python3
"""This module obtain the HTML content of a particular URL"""

from functools import wrapper
import redis
import requests

redis_client = redis.Redis()


def count_access(method: Callable) -> Callable:
    """Increments the access count for a URL in Redis using incr."""
    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """Increment access"""
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return method(url, *args, **kwargs)
    return wrapper


def cache_result(expiration_time: int = 10) -> Callable:
    """Returns the cached result if found"""
    def decorator(method: Callable) -> Callable:
        """Checks for a cached result in Redis using get"""
        @wraps(method)
        def wrapper(url: str, *args, **kwargs):
            """caches the new result using setex, and returns it."""
            cache_key = f"result:{url}"
            result = redis_client.get(cache_key)
            if result:
                return result.decode("utf-8")

            result = method(url, *args, **kwargs)
            redis_client.setex(cache_key, expiration_time, result)
            return result
        return wrapper
    return decorator


@count_access
@cache_result(expiration_time=10)
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL using requests.get."""
    response = requests.get(url)response.raise_for_status()
    return response.text
