import logging
import unittest

import naming as n


class DriverTests(unittest.TestCase):

    def tearDown(self):
        n.DB_DRIVER = None  # reset

    def test_explicit_setter(self):
        d = n.MemoDriver()
        n.set_driver(d)
        self.assertEqual(d, n.driver())

    def test_default_driver(self):
        self.assertIsNone(n.driver())

    def test_default_setter(self):
        n.set_driver()
        d = n.driver()
        self.assertIsInstance(d, n.JSONDriver)

    def test_singleton(self):
        self.test_default_setter()
        d = n.driver()
        n.set_driver()
        self.assertEqual(d, n.driver())


class TokenTests(unittest.TestCase):

    def setUp(self):
        n.set_driver(n.MemoDriver())  # in memory driver
        n.save()  # save empty state

    def tearDown(self):
        n.load()  # restore empty

    def test_add_dict(self):
        f = n.add_field("side", {"l": "L", "r": "R", "m": "M"}, default="m")
        self.assertIs(f._type, n.DICT_TYPE)
        self.assertEqual(f.name, "side")
        self.assertIsInstance(f.value, dict)
        self.assertEqual(f.default, "m")
        self.assertTrue(f.required)

    def test_add_str(self):
        f = n.add_field("description", "")
        self.assertIs(f._type, n.STR_TYPE)
        self.assertEqual(f.name, "description")
        self.assertIsInstance(f.value, basestring)
        self.assertIsNone(f.default)
        self.assertTrue(f.required)

    def test_add_int(self):
        f = n.add_field("enumerator", 0, padding=3, required=False)
        self.assertIs(f._type, n.INT_TYPE)
        self.assertEqual(f.name, "enumerator")
        self.assertIsInstance(f.value, int)
        self.assertEqual(f.default, "000")
        self.assertFalse(f.required)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # enable logging
    unittest.main(verbosity=2)
