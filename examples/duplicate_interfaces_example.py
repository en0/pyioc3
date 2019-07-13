"""
How to deal with types that provide the same interface.

This gets very close to the service lookup pattern so it should be
avoided, However, the following is a decent workaround.
"""
from abc import ABCMeta, abstractmethod

from pyioc3 import StaticContainerBuilder


class Base(metaclass=ABCMeta):
    """Common base class used to find all subclasses"""
    name: str

    @abstractmethod
    def foo(self): raise NotImplementedError()


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


class Main:
    """The application entry point"""

    def __init__(self, factory: "create_provider"):
        self._create_provider = factory

    def __call__(self, **kwargs):
        kwargs.setdefault("provider", "p1")
        provider: Base = self._create_provider(kwargs["provider"])
        provider.foo()


def create_provider_factory(ctx):
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
        raise Exception("One of the many issues with the service locator anti-pattern...")

    return create_provider


ioc_builder = StaticContainerBuilder()

# Bind each provider under it's own annotation
ioc_builder.bind(
    annotation=Provider1,
    implementation=Provider1)
ioc_builder.bind(
    annotation=Provider2,
    implementation=Provider2)

# Bind the factory
ioc_builder.bind_factory(
    annotation="create_provider",
    factory=create_provider_factory)

# Application Entry
ioc_builder.bind(
    annotation=Main,
    implementation=Main)

ioc = ioc_builder.build()

main = ioc.get(Main)
main(provider="p2")
