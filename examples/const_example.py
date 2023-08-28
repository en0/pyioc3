from pyioc3 import StaticContainerBuilder
from typing import NewType

HelloWorld = NewType("HelloWorld", str)
GoodByeWorld = NewType("GoodByeWorld", str)

ioc = (
    StaticContainerBuilder()
    .bind_constant(HelloWorld, "Hello, World!")
    .bind_constant(GoodByeWorld, "Good-bye, World!")
    .build()
)

print(ioc.get(HelloWorld))
print(ioc.get(GoodByeWorld))
