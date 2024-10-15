from current import graph
from current import Var
from current import Fn
from current import propagate

x = Var(1, name="x")
y = Var(1, name="y")
z = Fn(lambda v: v, y, name="yz")
a = Var(2, name="a")
b = Fn(lambda a: a + 1, a, name="b")
mul = Fn(lambda x, z, b: print(x, z, b, x * z * b), x, z, b, name="mul")
mul.with_args(z, b, 2)

graph(x, y, a)

for i in range(10):
    print("loop")
    x.update(i)
    y.update(i)
    propagate(x, y)
    a.update(i*2)
    propagate(a)
