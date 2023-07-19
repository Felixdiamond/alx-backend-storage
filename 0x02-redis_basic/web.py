#!/usr/bin/env python3
"""
This module defines a get_page function that obtains the HTML content of a
particular URL and caches it.
"""
import requests
from functools import wraps
import redis

redis_client = redis.Redis()

def count_url_calls(method):
    """
    Decorator that counts how many times a particular URL is accessed.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(url):
        key = f"count:{url}"
        redis_client.incr(key)
        return method(url)
    return wrapper

@count_url_calls
def get_page(url):
    """
    Obtains the HTML content of a particular URL and caches it with an
    expiration time of 10 seconds.

    Args:
        url (str): The URL of the page to be retrieved.

    Returns:
        str: The HTML content of the page.
    """
    cache_key = f"cached:{url}"
    cached_response = redis_client.get(cache_key)

    if cached_response:
        return cached_response.decode('utf-8')

    response = requests.get(url)
    redis_client.setex(cache_key, 10, response.text)

    return response.text
