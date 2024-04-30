#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        if not self._redis.exists(key) or fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))

    def get_int(self, key: str) -> int:
        return self.get(key, int)

    def get_str(self, key: str) -> str:
        return self.get(key, lambda d: d.decode("utf-8"))


def replay(fn: Callable) -> None:
    """ Display infos """
    cache = fn.__self__
    inputs = cache._redis.lrange("{}:inputs".format(fn.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(fn.__qualname__), 0, -1)
    num_calls = cache.get_int(fn.__qualname__)
    print(f'{fn.__qualname__} was called {num_calls} times:')
    for pair in tuple(zip(inputs, outputs)):
        print(f'{fn.__qualname__}(*{pair[0].decode("utf-8")}) -> \
        {pair[1].decode("utf-8")}')
