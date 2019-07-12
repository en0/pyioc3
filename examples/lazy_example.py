from pyioc import StaticContainerBuilder


class Squeak:
    def do_quack(self):
        print("SQUEAK")


class RubberDucky:
    def __init__(self, quack_behavior: "squeak"):
        self._quack_behavior = quack_behavior

    def quack(self):
        self._quack_behavior.do_quack()


ioc_builder = StaticContainerBuilder()
ioc_builder.bind(
    annotation="duck",
    implementation=RubberDucky)

ioc_builder.bind(
    annotation="squeak",
    implementation=Squeak)

ioc = ioc_builder.build()
duck: RubberDucky = ioc.get("duck")

duck.quack()
