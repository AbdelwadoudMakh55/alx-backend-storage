#!/usr/bin/env python3
"""
Python module implementing a simple Redis cache
"""


import uuid
import redis
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Counting calls of function """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Keeping call history (inputs and outputs) """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.rpush(f'{key}:inputs', str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f'{key}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """ Display infos """
    cache = fn.__self__
    key = fn.__qualname__
    inputs = cache._redis.lrange(f'{key}:inputs', 0, -1)
    outputs = cache._redis.lrange(f'{key}:outputs', 0, -1)
    num_calls = cache.get_int(key)
    print(f'{key} was called {num_calls} times:')
    for i, o in zip(inputs, outputs):
        print(f'{key}(*{i.decode("utf-8")}) -> {o.decode("utf-8")}')


class Cache:
    def __init__(self) -> None:
        """ Initialize Cache instance """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data inside redis server """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """ Retrieve data from redis server """
        if not self._redis.exists(key) or fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """ Retrieve data as int from redis server """
        return self.get(key, int)

    def get_str(self, key: str) -> str:
        """ Retrieve data as str from redis server """
        return self.get(key, lambda d: d.decode("utf-8"))
