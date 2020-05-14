from typing import Callable, List
from .scope_enum import ScopeEnum


class BoundMember:

    def __init__(self,
        annotation: any,
        implementation: Callable,
        scope: ScopeEnum,
        parameters: List[any],
        on_activate: Callable[[any],any] = None,
    ) -> None:
        self.annotation: any = annotation
        self.implementation: Callable = implementation
        self.scope: ScopeEnum = scope
        self.parameters: List[any] = parameters
        self._depends_on: List["BoundMember"] = []
        self.on_activate: Callable[[any], any] = on_activate if on_activate else lambda x: x

    def bind_dependant(self, dependant: "BoundMember") -> None:
        self._depends_on.append(dependant)

    def __iter__(self):
        return iter(self._depends_on)
