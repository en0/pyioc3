import unittest
from typing import Callable

from pyioc3.builder import BuilderBase
from pyioc3.interface import ProviderBinding, ConstantBinding, FactoryBinding


GreeterFactory = Callable[[str], str]


class Foo: ...


class FooBuilder(BuilderBase[Foo]):
    def __init__(self, *args, **kwargs):
        super().__init__(Foo, *args, **kwargs)


def eng_greeter_factory(ctx) -> GreeterFactory:
    def greeter_factory(name: str) -> str:
        return f"Hello, {name}!"

    return greeter_factory


class BuilderTest(unittest.TestCase):
    def test_builder(self):
        foo = FooBuilder().build()
        assert isinstance(foo, Foo)

    def test_builder_with_provider_and_constant_defaults(self):
        class Foo_Test(Foo):
            def __init__(self, c: str):
                self.c = c

        foo = FooBuilder(
            [
                ProviderBinding(Foo, Foo_Test),
                ConstantBinding("bar", str),
            ]
        ).build()
        assert foo.c == "bar"

    def test_builder_with_provider_and_constant_and_factory_defaults(self):
        class Foo_Test(Foo):
            def __init__(self, name: str, greet: GreeterFactory):
                self.greeting = greet(name)

        foo = FooBuilder(
            [
                ProviderBinding(Foo, Foo_Test),
                ConstantBinding("world", str),
                FactoryBinding(eng_greeter_factory, GreeterFactory),
            ]
        ).build()

        assert foo.greeting == "Hello, world!"

    def test_builder_with_provider_override(self):
        foo = FooBuilder().using_provider(Foo).build()
        assert isinstance(foo, Foo)

    def test_builder_with_provider_and_constant(self):
        class Foo_Test(Foo):
            def __init__(self, name: str):
                self.name = name

        foo = (
            FooBuilder()
            .using_provider(Foo, Foo_Test)
            .using_constant(str, "World")
            .build()
        )

        assert foo.name == "World"

    def test_builder_with_provider_and_constant_and_factory_override(self):
        class Foo_Test(Foo):
            def __init__(self, name: str, greet: GreeterFactory):
                self.greeting = greet(name)

        foo = (
            FooBuilder()
            .using_provider(Foo, Foo_Test)
            .using_constant(str, "World")
            .using_factory(GreeterFactory, eng_greeter_factory)
            .build()
        )

        assert foo.greeting == "Hello, World!"

    def test_mixed(self):
        class Bar(Foo):
            def __init__(self, name: str, greet: GreeterFactory):
                self.greeting = greet(name)

        class FooTestBuilder(BuilderBase[Bar]):
            def __init__(self):
                super().__init__(Bar)

        bar = (
            FooTestBuilder()
            .using_constant(str, "World")
            .using_factory(GreeterFactory, eng_greeter_factory)
            .build()
        )

        assert isinstance(bar, Bar)
        assert bar.greeting == "Hello, World!"
