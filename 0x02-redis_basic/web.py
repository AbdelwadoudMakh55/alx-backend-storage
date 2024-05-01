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
        if not r.exists(f'count:{url}'):
            r.incr(f'count:{url}')
            r.expire(f'count:{url}', 10)
        elif r.ttl(f'count:{url}') <= 0:
            r.set(f'count:{url}', 0)
            r.incr(f'count:{url}')
            r.expire(f'count:{url}', 10)
        else:
            r.incr(f'count:{url}')
        return method(url)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """ Get HTML content of url and return it """
    r = requests.get(url)
    return r.text
