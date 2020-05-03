import unittest
from unittest.mock import MagicMock, patch

from pyioc3.scope_container import ScopeContainer
from pyioc3.scope_enum import ScopeEnum


class ScopeContainerTests(unittest.TestCase):

    @patch("pyioc3.scope_container.PersistentScope")
    @patch("pyioc3.scope_container.TransientScope")
    def setUp(self, transient, persistent):

        self.transient = transient()
        self.persistent = persistent()
        self.singleton = MagicMock()
        self.container = ScopeContainer(self.singleton)

        self.scope_cases = [
            (ScopeEnum.TRANSIENT, self.transient),
            (ScopeEnum.REQUESTED, self.persistent),
            (ScopeEnum.SINGLETON, self.singleton),
        ]

    def test_add_uses_correct_scope(self):
        for scope_id, scope in self.scope_cases:
            with self.subTest(msg=scope_id):
                member = MagicMock()
                member.scope = scope_id
                member.annotation = "foo"
                member.implementation = MagicMock(return_value="bar")
                self.container.add(member)
                scope.add.assert_called_with("foo", "bar")

    def test_has_uses_correct_scope(self):
        for scope_id, scope in self.scope_cases:
            with self.subTest(msg=scope_id):
                member = MagicMock()
                member.scope = scope_id
                member.annotation = "foo"
                member.implementation = MagicMock(return_value="bar")
                self.container.has(member)
                scope.__contains__.assert_called_with("foo")

    def test_get_instance_of_uses_correct_scope(self):
        for scope_id, scope in self.scope_cases:
            with self.subTest(msg=scope_id):
                member = MagicMock()
                member.scope = scope_id
                member.annotation = "foo"
                member.implementation = MagicMock(return_value="bar")
                self.container.get_instance_of(member)
                scope.use.assert_called_with("foo")

    def test_creates_inst_with_deps(self):

        a1 = MagicMock()
        a1.scope = ScopeEnum.SINGLETON
        a1.annotation="a1"
        a1.implementation = MagicMock(return_value="a1_impl")
        self.container.add(a1)

        a2 = MagicMock()
        a2.scope = ScopeEnum.SINGLETON
        a2.annotation="a2"
        a2.implementation = MagicMock(return_value="a2_impl")
        self.container.add(a2)

        member = MagicMock()
        member.scope = ScopeEnum.SINGLETON
        member.annotation = "foo"
        member.depends_on = [a1, a2]
        member.implementation = MagicMock(return_value="bar")
        self.container.add(member)

        member.implementation.called_with("a1_impl", "a2_impl")
