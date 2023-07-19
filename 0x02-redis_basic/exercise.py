#!/usr/bin/env python3
"""
This module defines a Cache class that stores data in a Redis instance.
"""
import redis
from typing import Union, Callable, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method of the Cache class is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a particular
    function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper


def replay(method: Callable):
    """
    Displays the history of calls of a particular function.

    Args:
        method (Callable): The method whose call history is to be displayed.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for input_, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_.decode('utf-8')}) -> "
              f"{output.decode('utf-8')}")


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

    @count_calls
    @call_history
    def store(self,
              data: Union[str, bytes, int, float]) -> str:
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

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves the data stored at the specified key in the Redis instance
        and returns it. If a callable is provided as the fn argument, it is
        used to convert the data back to the desired format.

        Args:
            key (str): The key of the data to be retrieved.
            fn (Optional[Callable]): A callable used to convert the data back
                to the desired format.

        Returns:
            Union[str, bytes, int, float]: The data stored at the specified key
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self,
                key: str) -> str:
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

    def get_int(self,
                key: str) -> int:
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
