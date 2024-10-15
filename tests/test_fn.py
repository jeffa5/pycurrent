import unittest

import current
import logging

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

if __name__ == "__main__":
    unittest.main()
