import logging

from current import CachedFn, CachedVar, Fn, Var, graph, propagate

logging.basicConfig(level=logging.INFO)

x = Var(1, name="x")
y = CachedVar(1, name="y")
z = Fn(lambda v: v, y, name="yz")
a = CachedVar(1, name="a")
b = Fn(lambda a: a + 1, a, name="b")
mul = Fn(lambda x, z, b: print(x, z, b, x * z * b), x, z, b, name="mul")
add = Fn(lambda x: x + 1, x, name="add")
i = CachedFn(lambda x: 2, x, name="const")
j = Fn(lambda x: print("id val", x), i, name="print id")
# mul.with_args(z, b, 2)

# graph(a, x, y)
#
# for i in range(1):
#     print("loop")
#     x.update(i)
#     y.update(i)
#     propagate(x, y)
#     a.update(i * 2)
#     propagate(a)
#
# print("noop update for a")
# a.update(a.get())
# # should have no effect
# propagate(a)

propagate(i, x)
propagate(i, x)
propagate(i, x)
