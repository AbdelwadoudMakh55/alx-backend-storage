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
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        if r.get(url):
            return r.get(url).decode("utf-8")
        r.incr(f'count:{url}')
        content = method(url)
        r.setex(url, 10, content)
        return content
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """ Get HTML content of url and return it """
    r = requests.get(url)
    return r.text
