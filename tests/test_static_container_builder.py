from pyioc3.errors import CircularDependencyError
from pyioc3.interface import Container
from pyioc3.static_container_builder import StaticContainerBuilder
from unittest.mock import Mock, patch
import unittest

from .fixtures import (
    DuckA,
    DuckInterface,
    HalfCircle1,
    HalfCircle2,
    QuackBehavior,
    Sqeak,
    DuckFactory,
    rubber_duck_factory,
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
        container = self.builder.build()
        container_mock.assert_called()

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_container_with_initialized_dep_graph(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        dep, = list(members[DuckInterface])
        self.assertEqual(QuackBehavior, dep.annotation)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_container_with_members(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(DuckInterface, members)
        self.assertIn(QuackBehavior, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_with_static_container(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(container_mock, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_builds_with_static_container_as_container_interface(self, container_mock):
        self.builder.bind(DuckInterface, DuckA)
        self.builder.bind(QuackBehavior, Sqeak)
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(Container, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_basic_bindings_from_dict(self, container_mock):
        self.builder.load([
            {"annotation": DuckInterface, "implementation": DuckA},
            {"annotation": QuackBehavior, "implementation": Sqeak},
        ])
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(DuckInterface, members)
        self.assertIn(QuackBehavior, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_basic_bindings_from_dict_with_strings(self, container_mock):
        self.builder.load([
            {
                "annotation": "tests.fixtures.DuckInterface",
                "implementation": "tests.fixtures.DuckA"
            },{
                "annotation": "tests.fixtures.QuackBehavior",
                "implementation": "tests.fixtures.Sqeak"
            },
        ])
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(DuckInterface, members)
        self.assertIn(QuackBehavior, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_factory_bindings_from_dict(self, container_mock):
        self.builder.load([
            {"annotation": DuckFactory, "factory": rubber_duck_factory},
        ])
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(DuckFactory, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_factory_bindings_from_dict_as_strings(self, container_mock):
        self.builder.load([{
            "annotation": "tests.fixtures.DuckFactory",
            "factory": "tests.fixtures.rubber_duck_factory"
        }])
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn(DuckFactory, members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_factory_bindings_from_dict_with_string_annotation(self, container_mock):
        self.builder.load([{
            "annotation": "str(MyDuckFactory)",
            "factory": "tests.fixtures.rubber_duck_factory"
        }])
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn("MyDuckFactory", members)

    @patch("pyioc3.static_container_builder.StaticContainer")
    def test_const_bindings_from_dict(self, container_mock):
        self.builder.load([{
            "annotation": "str(my_const)",
            "value": 1
        }])
        container = self.builder.build()
        members, *_ = container_mock.call_args[0]
        self.assertIn("my_const", members)
