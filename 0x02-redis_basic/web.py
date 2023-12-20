#!/usr/bin/env python3
"""Web cache and tracker"""

import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """Helper function to track the number of times a URL is accessed."""
    @wraps(method)
    def wrapper(url):
        count_access = f"cached:{url}"
        cached_data = store.get(count_access)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = f"count:{url}"
        html_content = method(url)

        store.incr(count_key)
        store.set(count_access, html_content)
        store.expire(count_access, 10)
        return html_content
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Gets the HTML content of a particular URL,
    tracks the access count, and caches the result.
    """
    count = requests.get(url)
    return count.text
