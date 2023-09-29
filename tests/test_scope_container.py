import unittest
from unittest.mock import MagicMock, patch

from pyioc3.scope_container import ScopeContainer, PersistentScope
from pyioc3.scope_enum import ScopeEnum
from pyioc3.bound_member import BoundMember


class ContainerScopeTests(unittest.TestCase):
    @patch("pyioc3.scope_container.PersistentScope")
    @patch("pyioc3.scope_container.TransientScope")
    def setUp(self, transient, persistent):
        self.transient = transient()
        self.persistent = persistent()
        self.singleton = persistent()
        self.container = ScopeContainer(self.singleton)

        self.scope_cases = [
            (ScopeEnum.TRANSIENT, self.transient),
            (ScopeEnum.REQUESTED, self.persistent),
            (ScopeEnum.SINGLETON, self.singleton),
        ]

    def test_add_uses_correct_scope(self):
        for scope_id, scope in self.scope_cases:
            with self.subTest(msg=scope_id):
                member = MagicMock(spec=BoundMember)
                member.scope = scope_id
                member.annotation = "foo"
                member.implementation = MagicMock(return_value="bar")
                member.on_activate = lambda x: x
                self.container.add(member)
                scope.add.assert_called_with("foo", "bar")

    def test_has_uses_correct_scope(self):
        for scope_id, scope in self.scope_cases:
            with self.subTest(msg=scope_id):
                member = MagicMock(spec=BoundMember)
                member.scope = scope_id
                member.annotation = "foo"
                member.implementation = MagicMock(return_value="bar")
                member.on_activate = lambda x: x
                self.container.has(member)
                scope.__contains__.assert_called_with("foo")

    def test_get_instance_of_uses_correct_scope(self):
        for scope_id, scope in self.scope_cases:
            with self.subTest(msg=scope_id):
                member = MagicMock(spec=BoundMember)
                member.scope = scope_id
                member.annotation = "foo"
                member.implementation = MagicMock(return_value="bar")
                member.on_activate = lambda x: x
                self.container.get_instance_of(member)
                scope.use.assert_called_with("foo")


class ScopeContainerTests(unittest.TestCase):
    def setUp(self):
        self.container = ScopeContainer(PersistentScope())

    def test_creates_inst_with_deps(self):
        a1 = BoundMember(
            annotation="a1",
            implementation=lambda: "a1_impl",
            scope=ScopeEnum.SINGLETON,
            parameters=[],
        )
        a1._depends_on = []
        self.container.add(a1)

        a2 = BoundMember(
            annotation="a2",
            implementation=lambda: "a2_impl",
            scope=ScopeEnum.SINGLETON,
            parameters=[],
        )
        a2._depends_on = []
        self.container.add(a2)

        impl = MagicMock()
        member = BoundMember(
            annotation="foo",
            implementation=impl,
            scope=ScopeEnum.SINGLETON,
            parameters=["a1", "a2"],
        )
        member._depends_on = [a1, a2]
        self.container.add(member)

        impl.assert_called_with("a1_impl", "a2_impl")

    def test_on_activate_called(self):
        on_activate = MagicMock(return_value="baz")
        member = BoundMember(
            annotation="foo",
            implementation=lambda: "bar",
            scope=ScopeEnum.SINGLETON,
            parameters=["a1", "a2"],
            on_activate=on_activate,
        )
        member._depends_on = []
        self.container.add(member)
        on_activate.assert_called_with("bar")

    def test_on_activate_called_once_if_singleton(self):
        on_activate = MagicMock(return_value="baz")

        a1 = BoundMember(
            annotation="a1",
            implementation=lambda: "a1_impl",
            scope=ScopeEnum.SINGLETON,
            parameters=[],
            on_activate=on_activate,
        )
        a1._depends_on = []

        a2 = BoundMember(
            annotation="a2",
            implementation=lambda a: "a2_impl",
            scope=ScopeEnum.SINGLETON,
            parameters=["a1"],
        )
        a2._depends_on = [a1]

        member = BoundMember(
            annotation="foo",
            implementation=lambda a, b: "bar",
            scope=ScopeEnum.SINGLETON,
            parameters=["a1", "a2"],
        )
        member._depends_on = [a1, a2]

        self.container.add(a1)
        self.container.add(a2)
        self.container.add(member)

        on_activate.assert_called_once_with("a1_impl")

    def test_on_activate_called_for_each_instance_if_transient(self):
        on_activate = MagicMock(return_value="baz")

        a1 = BoundMember(
            annotation="a1",
            implementation=lambda: "a1_impl",
            scope=ScopeEnum.TRANSIENT,
            parameters=[],
            on_activate=on_activate,
        )
        a1._depends_on = []

        a2 = BoundMember(
            annotation="a2",
            implementation=lambda a: "a2_impl",
            scope=ScopeEnum.SINGLETON,
            parameters=["a1"],
        )
        a2._depends_on = [a1]

        member = BoundMember(
            annotation="foo",
            implementation=lambda a, b: "bar",
            scope=ScopeEnum.SINGLETON,
            parameters=["a1", "a2"],
        )
        member._depends_on = [a1, a2]

        self.container.add(a1)
        self.container.add(a1)
        self.container.add(a2)
        self.container.add(member)

        self.assertEqual(2, on_activate.call_count)
