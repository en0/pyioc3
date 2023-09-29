from typing import Callable, List, Type, Any
from .scope_enum import ScopeEnum
from .interface import PROVIDER_T


class BoundMember:
    """
    BoundMember represents metadata associated with a bound member.

    Args:
        annotation (Type[PROVIDER_T]): The annotation of the bound member.
        implementation (Type[PROVIDER_T]): The implementation of the bound member.
        scope (ScopeEnum): The scope of the bound member.
        parameters (List[Any]): A list of parameters required for the member's
            instantiation.
        on_activate (Callable[[PROVIDER_T], PROVIDER_T], optional): An optional
            callback function to be executed when the bound member is activated.

    Attributes:
        annotation (Type[PROVIDER_T]): The annotation of the bound member.
        implementation (Type[PROVIDER_T]): The implementation of the bound member.
        scope (ScopeEnum): The scope of the bound member.
        parameters (List[Any]): A list of parameters required for the member's
            instantiation.
        on_activate (Callable[[PROVIDER_T], PROVIDER_T]): An optional callback function
            to be executed when the bound member is activated.
        _depends_on (List[BoundMember]): A list of bound members that this member
            depends on.

    Methods:
        bind_dependant(self, dependant: "BoundMember") -> None:
            Binds a dependent member to this member.

    Example:
        To create a `BoundMember` instance:

        ```python
        from pyioc3.bound_member import BoundMember, ScopeEnum

        # Create a BoundMember instance.
        bound_member = BoundMember(
            annotation=MyAnnotation,
            implementation=MyImplementation,
            scope=ScopeEnum.SINGLETON,
            parameters=[param1, param2],
            on_activate=my_callback_function
        )
        ```

    See Also:
        - `ScopeEnum`: Enumeration of different dependency scopes.
        - `interface.PROVIDER_T`: Type variable for provider classes.
    """

    def __init__(
        self,
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
        self.on_activate: Callable[[PROVIDER_T], PROVIDER_T] = (
            on_activate if on_activate else lambda x: x
        )

    def bind_dependant(self, dependant: "BoundMember") -> None:
        """
        Binds a dependent member to this member.

        Args:
            dependant (BoundMember): The dependent member to be bound.
        """
        self._depends_on.append(dependant)

    def __iter__(self) -> None:
        """
        Returns an iterator over the dependent members.

        Returns:
            Iterator: An iterator over the dependent members.
        """
        return iter(self._depends_on)

    def __repr__(self) -> str:
        """
        Returns a string representation of the BoundMember.

        Returns:
            str: A string representation of the BoundMember.
        """
        return (
            f"<BoundMember annotation={self.annotation},"
            f" implementation={self.implementation},"
            f" scope={self.scope}>"
        )
