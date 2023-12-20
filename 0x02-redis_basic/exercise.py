#!/usr/bin/env python3
"""
Exercise file
"""

import redis
import uuid
from typing import Union


class Cache:
    """ This class Writes strings to Redis"""
    def __init__(self):
        """ this function Initialize Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """This function Generate a random key using uuid"""
        key = str(uuid.uuid4())

        # Store data in Redis with the generated key
        if isinstance(data, (int, float)):
            # Convert int or float to string for storage
            data = str(data)
        self._redis.set(key, data)

        # Return the generated key
        return key
