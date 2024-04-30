#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Callable, Union


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        if not self._redis.exists(key) or fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))