#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable
import time


def count_calls(method: Callable) -> Callable:
    """ Counting calls of function """
    @wraps(method)
    def wrapper(url):
        r = redis.Redis()
        cache_k = f'cache:{url}'
        r.expire(f'count:{url}', 10)
        r.incr(f'count:{url}')
        if not r.exists(cache_k) or time.time() - float(r.get(cache_k)) > 10:
            r.set(cache_k, time.time())
        return method(url)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """ Get HTML content of url and return it """
    r = requests.get(url)
    return r.text
