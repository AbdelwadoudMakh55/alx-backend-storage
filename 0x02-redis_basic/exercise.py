#!/usr/bin/env python3
"""
Thle provides a Cache class for storing data using Redis.
"""

import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of a method.
    """
    inputs = f"{method.__qualname__}:inputs"
    outputs = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def replay(fn: Callable):
    """
    Function to display the history of calls of a function.
    """
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    n_calls = n_calls.decode('utf-8') if n_calls else 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        i = i.decode('utf-8') if i else ""
        o = o.decode('utf-8') if o else ""
        print(f'{f_name}(*{i}) -> {o}')


class Cache:
    """
    Class to create a cache using Redis.
    """

    def __init__(self):
        """
        Initialize the Redis client.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data and return its key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Get the data associated with the given key.
        If a function is provided, apply it to the data.
        """
        if fn and self._redis.exists(key):
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_int(self, key: str) -> int:
        """
        Get the data associated with the given
        key and convert it to an integer.
        """
        value = self._redis.get(key)
        return int(value.decode("utf-8")) if value else 0

    def get_str(self, key: str) -> str:
        """
        Get the data associated with the given key and convert it to a string.
        """
        return self._redis.get(key).decode("utf-8")
