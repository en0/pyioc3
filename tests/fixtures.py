from abc import ABC


class DuckInterface(ABC):
    def quack(self):
        raise NotImplementedError()


class QuackBehavior(ABC):
    def quack(self):
        raise NotImplementedError()


class DuckA(DuckInterface):
    def __init__(self, squeak: QuackBehavior):
        self._quack_behavior = squeak

    def quack(self):
        self._quack_behavior.quack()


class DuckB(DuckInterface):
    def __init__(self, squeak: "QuackBehavior"):
        self._quack_behavior = squeak

    def quack(self):
        self._quack_behavior.quack()


class DuckC(DuckInterface):
    def quack(self):
        pass

def duck_d(squeak: QuackBehavior):
    return DuckA(squeak)
