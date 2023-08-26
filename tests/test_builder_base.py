import unittest
from typing import Callable

from pyioc3.builder import BuilderBase, ProviderBinding, ConstantBinding, FactoryBinding


GreeterFactory = Callable[[str], str]


class Foo:
    ...

class FooBuilder(BuilderBase[Foo]):
    def __init__(self, *args, **kwargs):
        super().__init__(Foo, *args, **kwargs)

def eng_greeter_factory(ctx) -> GreeterFactory:
    def greeter_factory(name: str) -> str:
        return f"Hello, {name}!"
    return greeter_factory


class BuilderTest(unittest.TestCase):

    def test_builder_with_provider_defaults(self):
        foo = FooBuilder(providers=[ProviderBinding(Foo)]).build()
        assert isinstance(foo, Foo)

    def test_builder_with_constant_defaults(self):

        class Foo_Test(Foo):
            def __init__(self, c: str):
                self.c = c

        foo = FooBuilder(
            providers=[ProviderBinding(Foo_Test, Foo)],
            constants=[ConstantBinding("bar", str)]
        ).build()
        assert foo.c == "bar"

    def test_builder_with_constant_factory(self):

        class Foo_Test(Foo):
            def __init__(self, name: str, greet: GreeterFactory):
                self.greeting = greet(name)

        foo = FooBuilder(
            providers=[ProviderBinding(Foo_Test, Foo)],
            constants=[ConstantBinding("world", str)],
            factories=[FactoryBinding(eng_greeter_factory, GreeterFactory)]
        ).build()

        assert foo.greeting == "Hello, world!"

    def test_builder_with_provider(self):
        foo = (
            FooBuilder()
            .using_provider(Foo)
            .build()
        )
        assert isinstance(foo, Foo)

    def test_builder_with_constant(self):

        class Foo_Test(Foo):
            def __init__(self, name: str):
                self.name = name

        foo = (
            FooBuilder()
            .using_provider(Foo_Test, Foo)
            .using_constant("World", str)
            .build()
        )

        assert foo.name == "World"

    def test_builder_with_factory(self):

        class Foo_Test(Foo):
            def __init__(self, name: str, greet: GreeterFactory):
                self.greeting = greet(name)

        foo = (
            FooBuilder()
            .using_provider(Foo_Test, Foo)
            .using_constant("World", str)
            .using_factory(eng_greeter_factory, GreeterFactory)
            .build()
        )

        assert foo.greeting == "Hello, World!"

    def test_mixed(self):

        class Bar(Foo):
            def __init__(self, name: str, greet: GreeterFactory):
                self.greeting = greet(name)

        class FooTestBuilder(BuilderBase[Bar]):
            def __init__(self):
                super().__init__(
                    target_t=Bar,
                    providers=[ProviderBinding(Bar)],
                )

        bar = (
            FooTestBuilder()
            .using_constant("World", str)
            .using_factory(eng_greeter_factory, GreeterFactory)
            .build()
        )

        assert isinstance(bar, Bar)
        assert bar.greeting == "Hello, World!"

