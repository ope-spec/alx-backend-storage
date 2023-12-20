#!/usr/bin/env python3
"""Cache module"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times methods of
    the Cache class are called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap the decorated function and return the wrapper."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs
    and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap the decorated function and return the wrapper."""
        inputs = str(args)
        self._redis.rpush(f"{method.__qualname__}:inputs", inputs)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    func_name = fn.__qualname__
    c = int(r.get(func_name).decode("utf-8")) if r.get(func_name) else 0
    print(f"{func_name} was called {c} times:")
    inputs = r.lrange(f"{func_name}:inputs", 0, -1)
    outputs = r.lrange(f"{func_name}:outputs", 0, -1)
    for inp, outp in zip(inputs, outputs):
        inp = inp.decode("utf-8") if inp else ""
        outp = outp.decode("utf-8") if outp else ""
        print(f"{func_name}(*{inp}) -> {outp}")


class Cache:
    """Cache class to interact with Redis"""

    def __init__(self):
        """
        Initializes the Cache object with a Redis client
        and flushes the Redis database.
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key using uuid, stores the input
        data in Redis with the key, and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn:
            Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis based on the key and
        applies an optional conversion function.
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves a string from Redis based on the key.
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves an integer from Redis based on the key.
        """
        return self.get(key, fn=int)

    def get_int(self, key: str) -> int:
        '''parametrize Cache.get with correct conversion function'''
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
