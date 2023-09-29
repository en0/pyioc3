from pyioc3.autowire import bind, AutoWireContainerBuilder


class QuackProvider:
    def quack(self):
        raise NotImplementedError()


@bind(scope="SINGLETON")
class Duck:
    def __init__(self, quack: QuackProvider):
        self._quack = quack

    def quack(self):
        self._quack.quack()


@bind(QuackProvider)
class Squeak(QuackProvider):
    def quack(self):
        print("Squeak")


if __name__ == "__main__":
    duck = AutoWireContainerBuilder("__main__").build().get(Duck)
    duck.quack()
