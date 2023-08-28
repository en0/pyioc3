from typing import Callable, List, Type, Any
from .scope_enum import ScopeEnum
from .interface import PROVIDER_T


class BoundMember:

    def __init__(self,
        annotation: Type[PROVIDER_T],
        implementation: Type[PROVIDER_T],
        scope: ScopeEnum,
        parameters: List[Any],
        on_activate: Callable[[PROVIDER_T], PROVIDER_T] = None,
    ) -> None:
        self.annotation: Type[PROVIDER_T] = annotation
        self.implementation: Type[PROVIDER_T] = implementation
        self.scope: ScopeEnum = scope
        self.parameters: List[Any] = parameters
        self._depends_on: List["BoundMember"] = []
        self.on_activate: Callable[[PROVIDER_T], PROVIDER_T] = on_activate if on_activate else lambda x: x

    def bind_dependant(self, dependant: "BoundMember") -> None:
        self._depends_on.append(dependant)

    def __iter__(self) -> None:
        return iter(self._depends_on)

    def __repr__(self) -> str:
        return f"<BoundMember annotation={self.annotation}, implementation={self.implementation}, scope={self.scope}>"
