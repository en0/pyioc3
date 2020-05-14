from inspect import signature, isclass
from types import FunctionType, MethodType
from typing import get_type_hints, Callable, Any

from .bound_member import BoundMember
from .scope_enum import ScopeEnum
from .interface import BoundMemberFactory


class DefaultBoundMemberFactory(BoundMemberFactory):

    def build(
        self,
        annotation: any,
        implementation: Callable,
        scope: ScopeEnum,
        on_activate: Callable[[Any], Any] = None,
    ) -> BoundMember:

        if isclass(implementation):
            params = get_type_hints(implementation.__init__)
        elif type(implementation) == FunctionType:
            params = get_type_hints(implementation)
        elif type(implementation) == MethodType:
            params = get_type_hints(implementation)
        elif hasattr(implementation, '__call__'):
            params = get_type_hints(implementation.__call__)
        else:
            params = get_type_hints(implementation)

        return BoundMember(
            annotation=annotation,
            implementation=implementation,
            scope=scope,
            parameters=[p for k, p in params.items() if k != 'return'],
            on_activate=on_activate
        )
