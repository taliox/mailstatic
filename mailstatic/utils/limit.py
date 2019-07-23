#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, Alle Rechte vorbehalten
# taliox UG - https://taliox.io
# Robert Kamuda, robert@taliox.io

from redis import StrictRedis

redis = StrictRedis(host="redis")


class LimitExceeded(Exception):
    def __init__(self, key, limit, ttl_left, ttl):
        self.key = key
        self.limit = limit
        self.ttl_left = ttl_left
        self.ttl = ttl


def limit_by_key(key, limit, ttl=60*60):
    r = redis.get(key) or 0
    if int(r) >= limit:
        raise LimitExceeded(key, limit, redis.ttl(key), ttl)
    else:
        r = redis.incr(key, 1)
        redis.expire(key, ttl)
