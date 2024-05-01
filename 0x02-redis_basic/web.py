#!/usr/bin/env python3
"""
This module provides functionality to cache web pages using Redis.
"""

import redis
import requests
from functools import wraps
from typing import Callable

r = redis.Redis()


def counturl(func: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Wrapper function to cache the content of a URL.
        """
        r.incr(f"count:{url}")
        if r.get(f"cached:{url}"):
            return r.get(f"cached:{url}").decode('utf-8')
        text = func(url)
        r.setex(f"cached:{url}", 10, text)
        return text

    return wrapper


@counturl
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of the URL.
    """
    return requests.get(url).text
