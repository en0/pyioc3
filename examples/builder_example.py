from abc import ABC, abstractmethod

from pyioc3 import StaticContainerBuilder
from pyioc3.builder import BuilderBase, ProviderBinding


class QuackBehavior(ABC):
    @abstractmethod
    def do_quack(self):
        raise NotImplementedError()


class Duck:

    def __init__(self, quacker: QuackBehavior):
        self._quacker = quacker

    def quack(self):
        self._quacker.do_quack()


class Squeak(QuackBehavior):

    def do_quack(self):
        print("SQUEAK")


class Quack(QuackBehavior):

    def do_quack(self):
        print("QUACK")


class DuckBuilder(BuilderBase[Duck]):

    def __init__(self):
        super().__init__(
            target_t=Duck,
            providers=[
                ProviderBinding(Duck),
                ProviderBinding(Quack, QuackBehavior),
            ]
        )

duck = (
    DuckBuilder()
    # Override the default QuackBehavior
    .using_provider(Squeak, QuackBehavior)
    .build()
)


duck.quack() # SQUEAK
