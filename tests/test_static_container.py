import unittest
from unittest.mock import MagicMock

from pyioc3.errors import MemberNotBoundError
from pyioc3.static_container import StaticContainer
from pyioc3.scope_enum import ScopeEnum
from pyioc3.bound_member import BoundMember


class StaticContainerTest(unittest.TestCase):
    def setUp(self):
        foo1 = BoundMember(
            annotation="foo1",
            implementation=object,
            scope=ScopeEnum.TRANSIENT,
            parameters=[],
        )

        foo2 = BoundMember(
            annotation="foo2",
            implementation=MagicMock(),
            scope=ScopeEnum.TRANSIENT,
            parameters=["foo1"],
        )

        foo3 = BoundMember(
            annotation="foo3",
            implementation=MagicMock(),
            scope=ScopeEnum.TRANSIENT,
            parameters=["foo1"],
        )

        foo2.bind_dependant(foo1)
        foo3.bind_dependant(foo1)

        self.members = {f.annotation: f for f in [foo1, foo2, foo3]}
        self.container = StaticContainer(self.members)

    def test_retrieves_instance(self):
        self.members["foo1"].implementation = MagicMock(return_value="bar")
        bar = self.container.get("foo1")
        self.assertEqual("bar", bar)

    def test_retrieves_unique_instance_when_transient(self):
        obj1 = self.container.get("foo1")
        obj2 = self.container.get("foo1")
        self.assertTrue(obj1 is not obj2)

    def test_retrieves_unique_instance_when_requested(self):
        self.members["foo1"].scope = ScopeEnum.REQUESTED
        obj1 = self.container.get("foo1")
        obj2 = self.container.get("foo1")
        self.assertTrue(obj1 is not obj2)

    def test_retrieves_same_instance_when_singleton(self):
        self.members["foo1"].scope = ScopeEnum.SINGLETON
        obj1 = self.container.get("foo1")
        obj2 = self.container.get("foo1")
        self.assertTrue(obj1 is obj2)

    def test_injects_deps(self):
        self.members["foo1"].implementation = MagicMock(return_value="bar")
        self.container.get("foo2")
        self.members["foo2"].implementation.assert_called_with("bar")

    def test_injected_deps_are_unique_when_transient(self):
        self.container.get("foo2")
        self.container.get("foo3")
        self.assertNotEqual(
            self.members["foo2"].implementation.call_args,
            self.members["foo3"].implementation.call_args,
        )

    def test_injected_deps_are_the_same_when_singleton(self):
        self.members["foo1"].scope = ScopeEnum.SINGLETON
        self.container.get("foo2")
        self.container.get("foo3")
        self.assertEqual(
            self.members["foo2"].implementation.call_args,
            self.members["foo3"].implementation.call_args,
        )

    def test_injected_deps_are_unqueue_when_requested(self):
        self.members["foo1"].scope = ScopeEnum.REQUESTED
        self.container.get("foo2")
        self.container.get("foo3")
        self.assertNotEqual(
            self.members["foo2"].implementation.call_args,
            self.members["foo3"].implementation.call_args,
        )

    def test_injected_deps_are_the_same_when_requested_in_same_tree(self):
        self.members["foo1"].scope = ScopeEnum.REQUESTED
        self.members["foo3"].parameters = ["foo1", "foo2"]
        self.members["foo3"].bind_dependant(self.members["foo2"])
        self.container.get("foo3")
        foo2_args = self.members["foo2"].implementation.call_args
        foo3_args = self.members["foo3"].implementation.call_args
        self.assertEqual(foo2_args[0][0], foo3_args[0][0])

    def test_calls_on_activate(self):
        self.members["foo1"].implementation = MagicMock(return_value="bar")
        self.members["foo1"].on_activate = MagicMock(return_value="bar")
        self.container.get("foo1")
        self.members["foo1"].on_activate.assert_called_with("bar")

    def test_calls_on_activate_for_dep(self):
        self.members["foo1"].scope = ScopeEnum.SINGLETON
        self.members["foo1"].implementation = MagicMock(return_value="bar")
        self.members["foo1"].on_activate = MagicMock(return_value="bar")
        self.container.get("foo2")
        self.members["foo1"].on_activate.assert_called_with("bar")

    def test_calls_on_activate_only_once_when_singleton(self):
        self.members["foo1"].scope = ScopeEnum.SINGLETON
        self.members["foo1"].implementation = MagicMock(return_value="bar")
        self.members["foo1"].on_activate = MagicMock(return_value="bar")
        self.container.get("foo2")
        self.container.get("foo3")
        self.members["foo1"].on_activate.assert_called_once_with("bar")

    def test_calls_on_activate_only_once_when_requested_in_same_tree(self):
        self.members["foo1"].scope = ScopeEnum.REQUESTED
        self.members["foo1"].implementation = MagicMock(return_value="bar")
        self.members["foo1"].on_activate = MagicMock(return_value="bar")
        self.members["foo3"].bind_dependant(self.members["foo2"])
        self.container.get("foo3")
        self.members["foo1"].on_activate.assert_called_once_with("bar")

    def test_calls_on_activate_each_time_it_is_needed_when_transient(self):
        self.members["foo1"].scope = ScopeEnum.TRANSIENT
        self.members["foo1"].implementation = MagicMock(return_value="bar")
        self.members["foo1"].on_activate = MagicMock(return_value="bar")
        self.members["foo3"].bind_dependant(self.members["foo2"])
        self.container.get("foo3")
        self.assertEqual(2, self.members["foo1"].on_activate.call_count)

    def test_unbound_member_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.container.get("NoExist")

    def test_unbound_member_raises_member_not_bound_error(self):
        with self.assertRaises(MemberNotBoundError):
            self.container.get("NoExist")
