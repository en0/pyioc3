from typing import Callable, NewType, TypeAlias
from pyioc3 import StaticContainerBuilder, Container


GreetingFactory: TypeAlias = Callable[[str], str]
Greeting = NewType("Greeting", str)


def my_factory_wrapper(ctx: Container) -> GreetingFactory:

    def greeting_factory(name: str) -> str:
        greeting = ctx.get(Greeting)
        return "{}, {}!".format(greeting, name)

    return greeting_factory


ioc = (
    StaticContainerBuilder()
    .bind_factory(GreetingFactory, my_factory_wrapper)
    .bind_constant(Greeting, "Hello")
    .build()
)

greeting_factory = ioc.get(GreetingFactory)
value = greeting_factory("Factory")

print(value)
