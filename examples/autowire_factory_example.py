from typing import Callable, NewType, TypeAlias
from pyioc3 import Container
from pyioc3.autowire import bind_factory, AutoWireContainerBuilder


GreetingFactory: TypeAlias = Callable[[str], str]
Greeting = NewType("Greeting", str)


@bind_factory(GreetingFactory)
def my_factory_wrapper(ctx: Container) -> GreetingFactory:
    def greeting_factory(name: str) -> str:
        greeting = ctx.get(Greeting)
        return "{}, {}!".format(greeting, name)

    return greeting_factory


if __name__ == "__main__":
    greeting_factory = (
        AutoWireContainerBuilder("__main__")
        .bind_constant(Greeting, "Hello")
        .build()
        .get(GreetingFactory)
    )

    value = greeting_factory("Factory")
    print(value)
