#!/usr/bin/env python3
""" Writing strings to Redis, Reading from Redis and recovering original type,
    Incrementing values, Storing lists, Retrieving lists """
from typing import Union, Callable, Optional, Any
import redis
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a particular
    function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


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
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in the Redis instance using a randomly generated
        key and returns the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
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
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves the data stored at the specified key in the Redis instance,
        converts it to a string using decode("utf-8"), and returns it.

        Args:
            key (str): The key of the data to be retrieved.

        Returns:
            str: The data stored at the specified key as a string.
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

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
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data


def replay(method: Callable):
    """
    Displays the history of calls of a particular function.

    Args:
        method (Callable): The method whose call history is to be displayed.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inputList = redis.lrange(inputs, 0, -1)
    outputList = redis.lrange(outputs, 0, -1)
    redis_zipped = list(zip(inputList, outputList))
    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))
