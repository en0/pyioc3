from abc import ABCMeta, abstractmethod

from pyioc3 import StaticContainerBuilder


class QuackBehavior(metaclass=ABCMeta):
    @abstractmethod
    def do_quack(self): raise NotImplementedError()


class Duck(metaclass=ABCMeta):
    @abstractmethod
    def quack(self): raise NotImplementedError()


class Squeak(QuackBehavior):
    def do_quack(self):
        print("SQUEAK")


class RubberDucky(Duck):
    def __init__(self, squeak: QuackBehavior):
        self._quack_behavior = squeak

    def quack(self):
        self._quack_behavior.do_quack()

ioc = (
    StaticContainerBuilder()
    .bind(Duck, RubberDucky)
    .bind(QuackBehavior, Squeak)
    .build()
)

rubber_duck = ioc.get(Duck)
rubber_duck.quack()
