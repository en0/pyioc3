import unittest

from pyioc3 import ScopeEnum
from pyioc3.errors import ScopeError


class SystemTest(unittest.TestCase):
    def test_transient_from_string(self):
        assert ScopeEnum.TRANSIENT == ScopeEnum.from_string("transient")
        assert ScopeEnum.TRANSIENT == ScopeEnum.from_string("t")
        assert ScopeEnum.TRANSIENT == ScopeEnum.from_string("TRANSIENT")
        assert ScopeEnum.TRANSIENT == ScopeEnum.from_string("T")

    def test_requested_from_string(self):
        assert ScopeEnum.REQUESTED == ScopeEnum.from_string("requested")
        assert ScopeEnum.REQUESTED == ScopeEnum.from_string("r")
        assert ScopeEnum.REQUESTED == ScopeEnum.from_string("REQUESTED")
        assert ScopeEnum.REQUESTED == ScopeEnum.from_string("R")

    def test_singleton_from_string(self):
        assert ScopeEnum.SINGLETON == ScopeEnum.from_string("singleton")
        assert ScopeEnum.SINGLETON == ScopeEnum.from_string("s")
        assert ScopeEnum.SINGLETON == ScopeEnum.from_string("SINGLETON")
        assert ScopeEnum.SINGLETON == ScopeEnum.from_string("S")

    def test_invalid_scope_raises(self):
        with self.assertRaises(ScopeError):
            ScopeEnum.from_string("foo")
