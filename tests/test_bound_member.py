import unittest
from pyioc3.bound_member import BoundMember
from pyioc3.bound_member_factory import DefaultBoundMemberFactory
from pyioc3.scope_enum import ScopeEnum

from .fixtures import DuckA, DuckB, DuckC, duck_d, DuckInterface, QuackBehavior

class BoundMemberTest(unittest.TestCase):


    def test_expands_parameter_annotations_for_classes(self):
        factory = DefaultBoundMemberFactory()
        cases = [
            (DuckA, [QuackBehavior]),
            (DuckB, ["QuackBehavior"]),
            (DuckC, []),
            (duck_d, [QuackBehavior]),
        ]
        for impl, result in cases:
            with self.subTest(impl):
                b = factory.build(DuckInterface, impl, ScopeEnum.TRANSIENT)
                self.assertListEqual(b.parameters, result)

