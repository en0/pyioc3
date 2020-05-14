from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterator


class DuckInterface(ABC):
    @abstractmethod
    def quack(self):
        raise NotImplementedError()


class QuackBehavior(ABC):
    @abstractmethod
    def quack(self):
        raise NotImplementedError()


class Sqeak(QuackBehavior):
    def quack(self):
        pass


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


class HalfCircle1:
    def __init__(self, c: "HalfCircle2"):
        pass


class HalfCircle2:
    def __init__(self, c: HalfCircle1):
        pass


DuckType = TypeVar("DuckType", bound="DuckInterface")


class FlockInterface(Generic[DuckType]):
    @abstractmethod
    def __iter__(self) -> Iterator[DuckType]:
        raise NotImplementedError()


class FlockOfDucks(FlockInterface[DuckInterface]):
    def __init__(self, ducka: DuckA, duckb: DuckB):
        self._ducks = [ducka, duckb]
    def __iter__(self) -> DuckInterface:
        return iter(self._ducks)

class Singleton(type):
    _instances = None
    def __call__(self, *args, **kwargs):
        if not self._instances:
            self._instances = super().__call__(*args, **kwargs)
        return self._instances

class MasterDuck(Singleton):
    def __init__(self, quack: QuackBehavior):
        pass

class MetaMasterDuck(metaclass=Singleton):
    def __init__(self, quack: QuackBehavior):
        pass
