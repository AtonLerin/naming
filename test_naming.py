"""
@todo: this module needs a rewrite ASAP to support the new api.
"""
import unittest
import naming as n


class NamingTests(unittest.TestCase):

    def setUp(self):
        n.new_profile("test")

    def tearDown(self):
        n.delete_profile("test")

    def test_list_tokens(self):
        n.clear_tokens()
        self.assertEqual(len(n.list_tokens()), 0)

    def test_add_tokens(self):
        n.clear_tokens()
        self.assertIsNotNone(n.new_token("name", "value1"))
        self.assertFalse(n.new_token("name", "value2"))
        self.assertEqual(len(n.list_tokens()), 1)
        self.assertIsInstance(n.list_tokens()[0], n.Token)

    def test_get_token(self):
        n.clear_tokens()
        t = n.new_token("name", "value")
        self.assertEqual(n.get_token("name"), t)
        self.assertIsNone(n.get_token("foo"))

    def test_delete_token(self):
        n.clear_tokens()
        self.assertFalse(n.delete_token("foo"))
        n.new_token("foo", "bar")
        self.assertTrue(n.delete_token("foo"))

    def test_list_profile(self):
        self.assertIsNotNone(n.list_profiles())

    def test_new_profile(self):
        self.assertIsNotNone(n.new_profile("test1"))
        self.assertIn("test1", n.list_profiles())
        self.assertIsNotNone(n.get_profile("test1"))
        self.assertTrue(n.set_profile("test1"))
        self.assertEqual(n.current_profile().name, "test1")
        l1 = len(n.list_profiles())
        n.delete_profile("test1")
        self.assertEqual(len(n.list_profiles()), l1 - 1)

    def test_profile_fields(self):
        fields = ["category", "name", "enum", "side", "type"]
        p = n.current_profile()
        for f in fields:
            p.add_field(f)
        self.assertEqual(p.list_fields(), fields)
        n.delete_profile("tests")

    def test_solver(self):
        p = n.current_profile()
        for i in range(3):
            n.clear_tokens()

            n.new_token("l", "L")
            n.new_token("r", "R")
            n.new_token("m", "M")

            f = p.add_field("side")
            f.append_token("l")
            f.append_token("r")
            f.append_token("m", True)

            p.add_field("name")
            (
                lambda: self.assertEqual(n.solve("test"), "M_test"),
                lambda: self.assertIsNone(n.solve()),
                lambda: self.assertIsNone(n.solve("l"))
            )[i]()

if __name__ == "__main__":
    unittest.main(verbosity=2)
