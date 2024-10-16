"""
Current only updates computations when the values change.
This is useful for only redoing work that needs to be done.
However, it only lasts for the duration of the python session.
We can instead persist things across runs to get this benefit back.
"""

import json
import logging
import os.path

import current

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def cache_single(f, *args, path):
    def write(path, args, result):
        with open(path, "w", encoding="utf-8") as file:
            logger.debug("Writing result to cache file %r", path)
            json.dump(
                {"args": [hash(a) for a in args], "kwargs": {}, "result": result}, file
            )

    if not os.path.exists(path):
        logger.debug("Cache path (%r) did not exist, re-evaluating", path)
        v = f(*args)
        write(path, args, v)
        return v
    with open(path, encoding="utf-8") as file:
        logger.debug("Cache path (%r) did exist, loading", path)
        content = json.load(file)
        cached_args = content["args"]
        cached_kwargs = content["kwargs"]
        cached_result = content["result"]
        mismatch = False
        if len(cached_args) == len(args):
            for c, a in zip(cached_args, args):
                ha = hash(a)
                if c != ha:
                    mismatch = True
        else:
            mismatch = True
        if mismatch:
            logger.debug("Cached arguments didn't match, re-evaluating")
            v = f(*args)
            write(path, args, v)
            return v
        logger.debug("Cached arguments matched, using cached result")
        return cached_result


def fib(i):
    if i < 2:
        return i
    return fib(i - 1) + fib(i - 2)


x = current.Var(37)
y = current.Fn(cache_single, fib, x, path="cached_foo")
current.propagate(x)
print(y.get())
