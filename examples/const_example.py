from pyioc import StaticContainerBuilder

ioc_builder = StaticContainerBuilder()

ioc_builder.bind_constant(
    annotation="my_constant",
    value="hello, world")

ioc = ioc_builder.build()

value = ioc.get("my_constant")
print(value)
