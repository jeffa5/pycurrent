import logging
from pathlib import Path
import time
import current


def cat(path: str):
    with open(path) as f:
        return f.read()


logging.basicConfig(level=logging.INFO)
print("Running cat")

foo = current.Fn(cat, Path("foo"), name="foo")
bar = current.Fn(cat, Path("bar"), name="bar")

def dbg(x):
    print(x)
    return x

foop = current.Fn(dbg, foo, name="foop")
barp = current.Fn(dbg, bar, name="barp")

while True:
    print("loop")
    current.propagate(foo, bar)
    time.sleep(1)
