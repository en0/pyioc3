from pyioc3 import StaticContainerBuilder

ioc_builder = StaticContainerBuilder()


def sorta_like_a_factory(name: "name"):

    def but_can_inject_anything():
        print("hello", name(13375))

    return but_can_inject_anything


ioc_builder.bind(
    annotation=5*5*5,
    implementation=sorta_like_a_factory)
ioc_builder.bind_constant(
    annotation="name",
    value=lambda x: "".join([chr(ord(_[0]) ^ ord(_[1])) for _ in zip("Y\x07K\x07G", str(x))]))

ioc = ioc_builder.build()

foo = ioc.get(5**3)
foo()
