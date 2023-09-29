from abc import ABC, abstractmethod
from pyioc3 import StaticContainerBuilder, ScopeEnum
import unittest


class Interface(ABC):
    @abstractmethod
    def method(self) -> None:
        raise NotImplementedError()


class DependentInterface(ABC):
    @abstractmethod
    def x(self) -> None:
        raise NotImplementedError()


class CacheInterface(ABC):
    @abstractmethod
    def inc(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_count(self) -> int:
        raise NotImplementedError()


class Cache(CacheInterface):
    def __init__(self):
        self._count = 0

    def inc(self) -> None:
        self._count += 1

    def get_count(self) -> None:
        return self._count


class Cache2(CacheInterface):
    def __init__(self):
        self._count = 0

    def inc(self) -> None:
        self._count += 1

    def get_count(self) -> None:
        return self._count


class Parent(Interface):
    def __init__(self, dep: DependentInterface):
        self._dep = dep

    def method(self):
        self._dep.x()


class Child(DependentInterface):
    def __init__(self, cache: CacheInterface):
        self.cache = cache

    def x(self):
        self.cache.inc()


class SystemTest(unittest.TestCase):
    def test_simple(self):
        builder = StaticContainerBuilder()
        builder.bind(Interface, Parent)
        builder.bind(DependentInterface, Child)
        builder.bind(CacheInterface, Cache, ScopeEnum.SINGLETON)
        ioc = builder.build()
        parent = ioc.get(Interface)
        cache = ioc.get(CacheInterface)
        parent.method()
        self.assertEqual(cache.get_count(), 1)

    def test_simple_with_str_scope(self):
        builder = StaticContainerBuilder()
        builder.bind(Interface, Parent)
        builder.bind(DependentInterface, Child)
        builder.bind(CacheInterface, Cache, "SINGLETON")
        ioc = builder.build()
        parent = ioc.get(Interface)
        cache = ioc.get(CacheInterface)
        parent.method()
        self.assertEqual(cache.get_count(), 1)
