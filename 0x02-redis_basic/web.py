#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable


def count_calls(method: Callable) -> Callable:
    """ Counting calls of function """
    @wraps(method)
    def wrapper(url):
        r = redis.Redis()
        r.expire(f'count:{url}', 10)
        r.incr(f'count:{url}')
        return method(url)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """ Get HTML content of url and return it """
    r = requests.get(url)
    return r.text
