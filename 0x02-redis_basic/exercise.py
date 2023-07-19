#!/usr/bin/env python3
"""
This module defines a Cache class that stores data in a Redis instance.
"""
import redis
from typing import Union, Callable, Optional
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves the data stored at the specified key in the Redis instance
        and returns it. If a callable is provided as the fn argument, it is
        used to convert the data back to the desired format.

        Args:
            key (str): The key of the data to be retrieved.
            fn (Optional[Callable]): A callable used to convert the data back
                to the desired format.

        Returns:
            Union[str, bytes, int, float]: The data stored at the specified key.
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves the data stored at the specified key in the Redis instance,
        converts it to a string using decode("utf-8"), and returns it.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            str: The data stored at the specified key as a string.
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Retrieves the data stored at the specified key in the Redis instance,
        converts it to an integer using int.from_bytes(value, byteorder), and
        returns it.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            int: The data stored at the specified key as an integer.
        """
        value = self._redis.get(key)
        return int.from_bytes(value, byteorder="big")

