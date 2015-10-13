"""
@todo: this module needs a rewrite ASAP to support the new api.
"""
import unittest
import naming as n


class NamingTests(unittest.TestCase):

    def test_tuple_len(self):
        self.assertEqual(len(tuple()), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
