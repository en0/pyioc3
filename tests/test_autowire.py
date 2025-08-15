from unittest import TestCase
from pyioc3 import ScopeEnum
from pyioc3.errors import AutoWireError
from pyioc3.autowire import bind, bind_factory, AutoWireContainerBuilder
from pyioc3.interface import ProviderBinding, FactoryBinding


class AutoWireDecoratorTests(TestCase):
    def setUp(self):
        AutoWireContainerBuilder._staged_bindings = []

    def test_binding_decorator_stages_binding_with_defaults(self):
        @bind()
        class MyClass: ...

        self.assertListEqual(
            AutoWireContainerBuilder._staged_bindings,
            [
                (
                    "tests.test_autowire",
                    ProviderBinding(MyClass, MyClass, ScopeEnum.TRANSIENT, None),
                ),
            ],
        )

    def test_binding_decorator_sets_scope(self):
        @bind(scope="SINGLETON")
        class MyClass: ...

        self.assertListEqual(
            AutoWireContainerBuilder._staged_bindings,
            [
                (
                    "tests.test_autowire",
                    ProviderBinding(MyClass, MyClass, "SINGLETON", None),
                )
            ],
        )

    def test_binding_decorator_sets_annotation(self):
        class MyClassInterface: ...

        @bind(MyClassInterface)
        class MyClass: ...

        self.assertListEqual(
            AutoWireContainerBuilder._staged_bindings,
            [
                (
                    "tests.test_autowire",
                    ProviderBinding(
                        MyClassInterface, MyClass, ScopeEnum.TRANSIENT, None
                    ),
                )
            ],
        )

    def test_binding_decorator_stages_binding_with_on_activate(self):
        def my_activator(x):
            return x

        @bind(on_activate=my_activator)
        class MyClass: ...

        self.assertListEqual(
            AutoWireContainerBuilder._staged_bindings,
            [
                (
                    "tests.test_autowire",
                    ProviderBinding(
                        MyClass, MyClass, ScopeEnum.TRANSIENT, my_activator
                    ),
                )
            ],
        )

    def test_binding_factory_decorator_stages_binding_with_defaults(self):
        @bind_factory("MyFactory")
        def my_factory(ctx):
            def wrapped(foo): ...

            return wrapped

        self.assertListEqual(
            AutoWireContainerBuilder._staged_bindings,
            [
                (
                    "tests.test_autowire",
                    FactoryBinding(my_factory, "MyFactory"),
                )
            ],
        )

    def test_binding_factory_requires_annotation(self):
        with self.assertRaises(TypeError):

            @bind_factory()
            def my_factory(ctx):
                def wrapped(foo): ...

                return wrapped


class AutoWireDiscoveryTests(TestCase):
    def setUp(self):
        AutoWireContainerBuilder._staged_bindings = []

    def test_autowire_can_build_simple_module(self):
        output = []

        class QuackInterface:
            def quack(self) -> None:
                raise NotImplementedError()

        @bind(QuackInterface)
        class Squeak(QuackInterface):
            def quack(self) -> None:
                output.append("Squeak")

        @bind()
        class Duck:
            def __init__(self, quack: QuackInterface) -> None:
                self._quack = quack

            def quack(self) -> None:
                self._quack.quack()

        container = AutoWireContainerBuilder("tests.test_autowire").build()
        duck = container.get(Duck)
        self.assertIsInstance(duck, Duck)
        duck.quack()
        self.assertListEqual(output, ["Squeak"])

    def test_autowire_can_build_from_submodules(self):
        from tests.autowire_pkg.greeter import GreeterOpts
        from tests.autowire_pkg.interface import GreeterInterface

        container = (
            AutoWireContainerBuilder("tests.autowire_pkg", "tests.autowire_pkg.script")
            .bind_constant(GreeterOpts, GreeterOpts(default_name="World"))
            .build()
        )
        greeter = container.get(GreeterInterface)
        self.assertEqual(greeter.greet("Unittest"), "Hello, Unittest!")
        self.assertEqual(greeter.greet(), "Hello, World!")
        greeter.set_language("es_MX")
        self.assertEqual(greeter.greet("Ian"), "Hola, Ian!")
        self.assertEqual(greeter.greet(), "Hola, Mundo!")

    def test_autowire_raises_on_duplicates(self):
        class QuackInterface:
            def quack(self) -> None: ...

        @bind(QuackInterface)
        class Squeak(QuackInterface):
            def quack(self) -> None: ...

        @bind(QuackInterface)
        class Honk(QuackInterface):
            def quack(self) -> None: ...

        @bind()
        class Duck:
            def __init__(self, quack: QuackInterface) -> None: ...

        with self.assertRaises(AutoWireError):
            AutoWireContainerBuilder("tests.test_autowire").build()
