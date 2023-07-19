#!/usr/bin/env python3
"""
This module defines a get_page function that obtains the HTML content of a
particular URL and caches it.
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()

def count_url_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a particular URL is accessed.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        redis_client.incr(f'count:{url}')
        result = redis_client.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_client.set(f'count:{url}', 0)
        redis_client.setex(f'result:{url}', 10, result)
        return result
    return wrapper

@count_url_calls
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a particular URL and caches it with an
    expiration time of 10 seconds.

    Args:
        url (str): The URL of the page to be retrieved.

    Returns:
        str: The HTML content of the page.
    """
    return requests.get(url).text
