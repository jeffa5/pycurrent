import logging
import unittest

import current

logging.basicConfig(level=logging.INFO)


class TestFn(unittest.TestCase):
    def test_fn_get(self):
        x = current.Var(1)
        y = current.Fn(lambda x: x + 1, x)
        self.assertEqual(y.get(), 2)
        current.propagate(x)
        self.assertEqual(y.get(), 2)
        x.update(2)
        current.propagate(x)
        self.assertEqual(y.get(), 3)

    def test_fn_chain(self):
        x = current.Var(1)
        y = current.Fn(lambda x: x + 1, x)
        z = current.Fn(lambda x: x + 1, y)
        self.assertEqual(z.get(), 3)

    def test_file_fn(self):
        f = "test_foo"
        with open(f, "w") as file:
            file.write("0")

        def test_fn(f):
            with open(f) as file:
                return int(file.read())

        x = current.Fn(test_fn, f)
        current.propagate(x)
        self.assertEqual(x.get(), 0)
        with open(f, "w") as file:
            file.write("1")
        x.refresh()
        current.propagate(x)
        self.assertEqual(x.get(), 1)

    def test_fan_out(self):
        count = current.Var(2)
        out = current.Fn(
            lambda count: current.List([current.Var(x) for x in range(1, count + 1)]),
            count,
        )
        m = current.Fn(lambda vs: [current.Fn(lambda x: x * x, v) for v in vs], out)
        resolved = current.flatten(m)
        print(current.graph(count, debug=True))
        current.propagate(count)
        self.assertEqual(resolved.get(), [1, 4])
        count.update(4)
        current.propagate(count)
        print(current.graph(count, debug=True))
        self.assertEqual(resolved.get(), [1, 4, 9, 16])

    def test_fan_in(self):
        count = current.Var(2)
        fanout = current.Fn(
            lambda count: [current.Var(x) for x in range(1, count + 1)], count
        )
        fanin = current.flatten(fanout)
        total = current.Fn(sum, fanin)
        print(current.graph(count, debug=True))
        current.propagate(count)
        self.assertEqual(total.get(), 3)
        count.update(10)
        current.propagate(count)
        self.assertEqual(total.get(), 55)


if __name__ == "__main__":
    unittest.main()
