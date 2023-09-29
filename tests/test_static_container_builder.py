from pyioc3.errors import CircularDependencyError, MemberNotBoundError
from pyioc3.interface import Container
from pyioc3.static_container_builder import StaticContainerBuilder
from unittest.mock import patch
import unittest

from .fixtures import (
    DuckA,
    DuckInterface,
    HalfCircle1,
    HalfCircle2,
    QuackBehavior,
    Sqeak,
)


class StaticContainerTest(unittest.TestCase):
    def setUp(self):
        self.builder = StaticContainerBuilder()

    def test_raises_if_deep_cycle(self):
        self.builder.bind(HalfCircle1, HalfCircle1)
        self.builder.bind(HalfCircle2, HalfCircle2)
        with self.assertRaises(CircularDependencyError):
            self.builder.build()

    def test_raises_if_any_cycle(self):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        self.builder.bind(HalfCircle1, HalfCircle1)
        self.builder.bind(HalfCircle2, HalfCircle2)
        with self.assertRaises(CircularDependencyError):
            self.builder.build()

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_container(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        self.builder.build()
        container_mock.assert_called()

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_container_with_initialized_dep_graph(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        self.builder.build()
        members, *_ = container_mock.call_args[0]
        (dep,) = list(members[DuckInterface])
        self.assertEqual(QuackBehavior, dep.annotation)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_container_with_members(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(DuckInterface, members)
        self.assertIn(QuackBehavior, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_with_static_container(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(container_mock, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_with_static_container_as_container_interface(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(Container, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_binding_scope_by_string_is_ok(self, container_mock):
        self.builder.bind(DuckInterface, DuckA, "singleton")
        self.builder.bind(QuackBehavior, Sqeak)
        self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(Container, members)

    def test_unbound_dependent_raises_key_error(self):
        self.builder.bind(DuckInterface, DuckA, "singleton")
        with self.assertRaises(KeyError):
            self.builder.build()

    def test_unbound_dependent_raises_member_not_bound_error(self):
        self.builder.bind(DuckInterface, DuckA, "singleton")
        with self.assertRaises(MemberNotBoundError):
            self.builder.build()
