#!/usr/bin/env python3
"""web cache and tracker"""

import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def count_access(url: str) -> int:
    """
    Helper function to track the number of times
    a URL is accessed.
    """
    count_key = f"count:{url}"
    count = redis_client.incr(count_key)
    redis_client.expire(count_key, 10)
    return count


def cache_result(url: str, result: str) -> None:
    """
    Helper function to cache the result of a
    URL with a 10-second expiration time.
    """
    cache_key = f"cache:{url}"
    redis_client.setex(cache_key, 10, result)


def get_page(url: str) -> str:
    """
    Gets the HTML content of a particular URL,
    tracks the access count, and caches the result.
    """
    cache_key = f"cache:{url}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        count_access(url)
        return cached_result.decode("utf-8")

    response = requests.get(url)
    html_content = response.text

    cache_result(url, html_content)
    count_access(url)

    return html_content


def cache_decorator(func: Callable) -> Callable:
    """
    Decorator to cache the result of a function
    with a 10-second expiration time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = f"cache:{func.__name__}:{args}:{kwargs}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode("utf-8")

        result = func(*args, **kwargs)
        redis_client.setex(cache_key, 10, result)

        return result

    return wrapper
