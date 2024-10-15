import unittest
import current

class TestVar(unittest.TestCase):
    def test_var_get(self):
        x = current.Var(1)
        self.assertEqual(x.get(), 1)
        x.update(2)
        self.assertEqual(x.get(), 2)

if __name__ == "__main__":
    unittest.main()
