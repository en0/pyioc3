import unittest
from random import randint, choice
from pyioc3.interface import Container, ProviderBinding
from pyioc3.bound_member_factory import BoundMemberFactory
from pyioc3.adapters import (
    ValueAsImplAdapter,
    FunctionAsImplAdapter,
    FactoryAsImplAdapter,
)

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
        cases = [
            (ProviderBinding(DuckInterface, DuckA), [QuackBehavior]),
            (ProviderBinding(DuckInterface, DuckB), [QuackBehavior]),
            (ProviderBinding(DuckInterface, DuckC), []),
            (ProviderBinding("foo", duck_d), [QuackBehavior]),
            (
                ProviderBinding(FlockInterface[DuckInterface], FlockOfDucks),
                [DuckA, DuckB],
            ),
            (ProviderBinding("lambda", lambda: "x"), []),
            (ProviderBinding("value", ValueAsImplAdapter(1)), []),
            (ProviderBinding("function", FunctionAsImplAdapter(lambda: "x")), []),
            (
                ProviderBinding("factory", FactoryAsImplAdapter(lambda: "x")),
                [Container],
            ),
            (ProviderBinding(DuckInterface, MasterDuck), [QuackBehavior]),
            (ProviderBinding(DuckInterface, MetaMasterDuck), [QuackBehavior]),
        ]
        for binding, result in cases:
            with self.subTest(binding):
                b = BoundMemberFactory.build(binding)
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
        b = BoundMemberFactory.build(ProviderBinding("foo", g["func"]))
        self.assertListEqual(expected, b.parameters)
