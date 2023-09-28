# pyioc3

Python Inversion of Control (IoC) Container

# About

pyioc3 is a lightweight and versatile Inversion of Control (IoC) container for
Python. It simplifies the management of dependencies and enables cleaner, more
modular code by promoting the use of Dependency Injection (DI) patterns. With
pyioc3, you can effortlessly wire up your application's components, specify
their lifecycles, and inject dependencies without the hassle of manual
instantiation.

# Key Features

## Multiple APIs

pyioc3 offers multiple configuration interfaces including two manual
configuration APIs and a decorator-based autowiring API. These APIs are
flexible, yet simple to use.

## Fluent Interface

pyioc3 manual APIs support method chaining to minimize boiler-plate code and
intermediate variables.

## Scoped Lifecycles

pyioc3 supports various scopes, including Singleton, Transient, and Requested.
This provides fine-grained control of the lifecycle of your objects.

## Predictability

pyioc3 is an immutable ioc container that guarentees predictability of the
dependency tree.

## Constuctor Based DI

pyioc3 implements constructor based dependency injection making it easy to drop
into existing applications.

## Performance

pyioc3 pre-computes the dependency tree, resulting in fast instantiations to
keep your code fast.

## OOP Principles

pyioc3 is designed to improve the maintainability, testability, and flexibility
of your Python applications.

# Quick Start

Install the package

```bash
pip install --user pyioc3
```

## StaticContainerBuilder API

```python
from pyioc3 import StaticContainerBuilder

container = (
    StaticContainerBuilder()
    .bind(Duck)
    .bind(QuackProvider, Squeak)
    .build()
)

duck = container.get(Duck)
duck.quack()
```

## BuilderBase API

```python
from pyioc3.builder import BuilderBase, ProviderBinding

class DuckBuilder(Duck):
    def __init__(self):
        super().__init__(target_t=Duck)

    def with_quack_noise(self, noise: str) -> "DuckBuilder":
        self.using_provider(
            annotation=QuackProvider,
            implementation=DynamicQuackProvider,
            on_activate=lambda x: x.set_quack_noise(noise)
        )
        return self

rubber_duck = (
    DuckBuilder()
    .with_quack_noise("Squeak")
    .build()
)

rubber_duck.quack()
```

## BuilderBase API

```python
from pyioc3.autowire import bind, AutoWireContainerBuilder


class QuackProvider:
    def quack(self):
        raise NotImplementedError()


@bind()
class Duck:
    def __init__(self, quack: QuackProvider):
        self._quack = quack

    def quack(self):
        self._quack.quack()


@bind(QuackProvider)
class Squeak(QuackProvider):

    def quack(self):
        print("Squeak")


duck = AutoWireContainerBuilder("my_package").build().get(Duck)
duck.quack()
```
