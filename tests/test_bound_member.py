import unittest
from types import FunctionType
from random import randint, choice
from pyioc3.interface import Container
from pyioc3.bound_member import BoundMember
from pyioc3.bound_member_factory import DefaultBoundMemberFactory
from pyioc3.scope_enum import ScopeEnum
from pyioc3.adapters import ValueAsImplAdapter, FunctionAsImplAdapter, FactoryAsImplAdapter

from .fixtures import (
    DuckA,
    DuckB,
    DuckC,
    duck_d,
    DuckInterface,
    QuackBehavior,
    FlockOfDucks,
    FlockInterface,
    MasterDuck,
    MetaMasterDuck,
)


class BoundMemberTest(unittest.TestCase):

    def test_expands_parameter_annotations_for_classes(self):
        factory = DefaultBoundMemberFactory()
        cases = [
            (DuckInterface, DuckA, [QuackBehavior]),
            (DuckInterface, DuckB, [QuackBehavior]),
            (DuckInterface, DuckC, []),
            ("foo", duck_d, [QuackBehavior]),
            (FlockInterface[DuckInterface], FlockOfDucks, [DuckA, DuckB]),
            ("lambda", lambda : 'x', []),
            ("value", ValueAsImplAdapter(1), []),
            ("function", FunctionAsImplAdapter(lambda : 'x'), []),
            ("factory", FactoryAsImplAdapter(lambda: 'x'), [Container]),
            (DuckInterface, MasterDuck, [QuackBehavior]),
            (DuckInterface, MetaMasterDuck, [QuackBehavior])
        ]
        for anno, impl, result in cases:
            with self.subTest(impl):
                b = factory.build(anno, impl, ScopeEnum.TRANSIENT)
                self.assertListEqual(b.parameters, result)

    def test_ordering_of_parameter_annotations(self):
        types = {
            "int": int,
            "str": str,
            "bool": bool,
        }
        params = []
        for i in range(255):
            val = f"p{randint(1, 1000)}_{i}"
            anno = choice(list(types.keys()))
            params.append((val, anno))
        args = ",".join([f"{p}: {a}" for p, a in params])
        expected = [types[a] for _, a in params]
        g = {}
        exec(f"def func({args}):...", g)
        factory = DefaultBoundMemberFactory()
        b = factory.build("foo", g['func'], ScopeEnum.TRANSIENT)
        self.assertListEqual(expected, b.parameters)

