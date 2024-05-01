#!/usr/bin/env python3
import redis
import time

r = redis.Redis()

r.set("a", 123)
r.expire("a", 5)
time.sleep(1)
t = r.ttl("a")
print(t)
