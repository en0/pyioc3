"""
How to deal with types that provide the same interface.

This gets very close to the service lookup pattern so it should be
avoided, However, the following is a decent workaround.
"""
from abc import ABC, abstractmethod
from typing import Callable, TypeAlias

from pyioc3 import StaticContainerBuilder, Container


class Base(ABC):
    """Common base class used to find all subclasses"""

    name: str

    @abstractmethod
    def foo(self):
        raise NotImplementedError()


class Provider1(Base):
    """A concrete provider of type base"""

    name: str = "p1"

    def foo(self):
        print("Foo from provider 1")


class Provider2(Base):
    """Another concrete provider of type base"""

    name: str = "p2"

    def foo(self):
        print("Foo from provider 2")


CreateProviderFactory: TypeAlias = Callable[[str], Base]


def create_provider_factory(ctx: Container) -> CreateProviderFactory:
    """A factory used to locate the appropriate provider"""

    # This factory will return a single provider, but you could
    # also return all the provider as a list.

    def create_provider(name):
        # Get all subclasses that implement the BASE interface
        for subclass in Base.__subclasses__():
            # Pull each one out of the container and see if it can be used
            inst: Base = ctx.get(subclass)
            if inst.name == name:
                return inst

        # You could also return a default here.
        raise Exception(
            "One of the many issues with the service locator anti-pattern..."
        )

    return create_provider


class Main:
    """The application entry point"""

    def __init__(self, factory: CreateProviderFactory):
        self._create_provider = factory

    def __call__(self, **kwargs):
        kwargs.setdefault("provider", "p1")
        provider: Base = self._create_provider(kwargs["provider"])
        provider.foo()


ioc = (
    StaticContainerBuilder()
    # Application Entry
    .bind(Main)
    # Bind each provider under it's own annotation
    .bind(Provider1)
    .bind(Provider2)
    # Bind the factory
    .bind_factory(CreateProviderFactory, create_provider_factory)
    .build()
)

main = ioc.get(Main)
main(provider="p2")
