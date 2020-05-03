import unittest

from pyioc3.scope_container import PersistentScope


class PersistentScopeTest(unittest.TestCase):
    def setUp(self):
        self.scope = PersistentScope()

    def test_only_once_instance_exists(self):
        self.scope.add("a", 1)
        self.scope.add("a", 2)
        self.scope.add("a", 3)
        self.assertEqual(3, self.scope.use("a"))
        self.assertEqual(3, self.scope.use("a"))
        self.assertEqual(3, self.scope.use("a"))

    def test_raises_key_error(self):
        self.scope.add("a", 1)
        with self.assertRaises(KeyError):
            self.scope.use("b")

    def test_in_oper_returns_true(self):
        self.scope.add("a", 1)
        self.assertIn("a", self.scope)

    def test_in_oper_returns_false(self):
        self.scope.add("a", 1)
        self.assertNotIn("b", self.scope)

    def test_item_is_not_removed_once_used(self):
        self.scope.add("a", 1)
        self.scope.use("a")
        self.scope.use("a")
