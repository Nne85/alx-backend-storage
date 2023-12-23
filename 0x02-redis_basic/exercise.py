#!/usr/bin/env python3
"""
Exercise file
"""

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ This function reate and return function that increments the
    count for Cache store"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """This method call its self after increment"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ This function stores the history of input and output
    of the Cache class"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        # Store input arguments using lpush
        inputs = '{}:inputs'.format(method.__qualname__)
        outputs = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))

        # Execute the wrapped function and store output
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs, output)

        return output
    return wrapper


def replay(method: Callable) -> None:
    """Displays call history for Cache class"""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    with redis.Redis() as redis_client:
        """Use a context manager for connection """
        inputs = redis_client.lrange(input_key, 0, -1)
        outputs = redis_client.lrange(output_key, 0, -1)

        call_count = len(inputs)
        print(f"{method.__qualname__} was called {call_count} times:")

        for args, output in zip(inputs, outputs):
            args_str = ', '.join(f"'{arg}'" for arg in args)
            print(f"{method.__qualname__}*({args_str}) -> {output}")


class Cache:
    """ This class Writes strings to Redis"""
    def __init__(self):
        """ this function Initialize Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

    def get(self, key: str, fn: Callable =
            None) -> Union[str, bytes, int, float]:
        """ Retrieve data from Redis based on the provided key"""
        data = self._redis.get(key)
        if data is None:
            return None  # Mimic Redis.get behavior if key doesn't exist

        if fn is not None:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> str:
        """
        Retrieves data as a string, decoding bytes if necessary.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: int) -> int:
        """Retrieves data as an integer. """
        return self.get(key, fn=lambda d: int(d))
