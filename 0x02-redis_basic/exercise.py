#!/usr/bin/env python3
"""
This module defines a Cache class that stores data in a Redis instance.
"""
import redis
from typing import Union
from uuid import uuid4


class Cache:
    """
    Cache class that stores data in a Redis instance.
    """

    def __init__(self):
        """
        Initializes a new Cache instance. Creates a new Redis client and
        flushes the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in the Redis instance using a randomly generated
        key and returns the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The key used to store the data.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
