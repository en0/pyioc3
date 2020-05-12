from inspect import signature
from typing import Callable

from .bound_member import BoundMember
from .scope_enum import ScopeEnum


class DefaultBoundMemberFactory:

    def build(
        self,
        annotation: any,
        implementation: Callable,
        scope: ScopeEnum
    ) -> BoundMember:
        params = signature(implementation).parameters
        return BoundMember(
            annotation=annotation,
            implementation=implementation,
            scope=scope,
            parameters=[p.annotation for p in params.values()],
        )
