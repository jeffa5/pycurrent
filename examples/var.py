import logging

from current import Fn, Var, CachedVar, graph, propagate

logging.basicConfig(level=logging.INFO)

x = Var(1, name="x")
y = CachedVar(1, name="y")
z = Fn(lambda v: v, y, name="yz")
a = CachedVar(2, name="a")
b = Fn(lambda a: a + 1, a, name="b")
mul = Fn(lambda x, z, b: print(x, z, b, x * z * b), x, z, b, name="mul")
add = Fn(lambda x: x + 1, x, name="add")
# mul.with_args(z, b, 2)

print(graph(x, y, a, debug=True))

# for i in range(10):
#     print("loop")
#     x.update(i)
#     y.update(i)
#     propagate(x, y)
#     a.update(i * 2)
#     propagate(a)

propagate(a, x, y)
print(graph(x, y, a, debug=True))
a.update(a.get())
# should have no effect
print(graph(x, y, a, debug=True))
propagate(a)
print(graph(x, y, a, debug=True))
