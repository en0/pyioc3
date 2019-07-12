from pyioc3 import StaticContainerBuilder, StaticContainer

ioc_builder = StaticContainerBuilder()


def my_factory_wrapper(ctx: StaticContainer):

    def my_factory(name: str):
        greeting = ctx.get("greeting")
        return "{}, {}!".format(greeting, name)

    return my_factory


ioc_builder.bind_factory(
    annotation="my_factory",
    factory=my_factory_wrapper)
ioc_builder.bind_constant(
    annotation="greeting",
    value="Hello")

ioc = ioc_builder.build()

fact = ioc.get("my_factory")
value: str = fact("Factory")
print(value)
