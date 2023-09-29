from collections import deque
from typing import Dict, Type

from .errors import _MemberNotBoundErrorAsKeyError
from .scope_enum import ScopeEnum
from .bound_member import BoundMember
from .scope_container import PersistentScope, ScopeContainer
from .interface import (
    Container,
    PROVIDER_T,
)


class StaticContainer(Container):
    """
    StaticContainer is an implementation of the Container interface for managing
    dependencies with static binding information.

    Args:
        bound_members (Dict[Type[PROVIDER_T], BoundMember]): A dictionary containing
            bound members (providers) and their associated metadata.

    Attributes:
        _singletons (PersistentScope): A persistent scope for managing singleton
            instances.
        _bound_members (Dict[Type[PROVIDER_T], BoundMember]): A dictionary containing
            bound members and their associated metadata.

    Methods:
        _build_scope(requested_member: BoundMember) -> ScopeContainer:
            Builds a scope for resolving dependencies for the requested member.

        get(annotation: Type[PROVIDER_T]) -> PROVIDER_T:
            Retrieves an instance of the specified annotation from the container.

    Note:
        The `StaticContainer` class is used to manage dependencies with statically
        defined bindings. It implements the `Container` interface and allows you to
        retrieve instances of bound members (providers) based on their annotations.

    Example:
        To create a `StaticContainer` with bound members and retrieve an instance of a
        specific annotation:

        ```python
        from pyioc3.static_container import StaticContainer

        # Create a StaticContainer with bound members.
        container = StaticContainer(bound_members={
            MyInterface: bound_member_instance,
            AnotherInterface: another_bound_member_instance,
        })

        # Retrieve an instance of MyInterface.
        my_instance = container.get(MyInterface)
        ```

    See Also:
        - `Container`: The base interface for managing dependencies.
        - `ScopeEnum`: Enumeration of different dependency scopes.
        - `BoundMember`: Metadata associated with a bound member.
        - `PersistentScope`: A scope for managing singleton instances.
        - `ScopeContainer`: A container for managing scoped instances.

    """

    def __init__(self, bound_members: Dict[Type[PROVIDER_T], BoundMember]):
        self._singletons = PersistentScope()
        self._bound_members = bound_members

    def _build_scope(self, requested_member: BoundMember):
        # Build a scope using a post-order traversal of the
        # dependency tree.  This will guarantee the scope has
        # all dependencies for each object it is given to build.

        scope = ScopeContainer(self._singletons)
        stack = deque()
        stack.append((requested_member, 0))
        while len(stack) > 0:
            m, s = stack.pop()
            if m.scope != ScopeEnum.TRANSIENT and scope.has(m):
                continue
            elif s == 0:
                stack.append((m, 1))
                [stack.append((v, 0)) for v in m]
            else:
                scope.add(m)
        return scope

    def get(self, annotation: Type[PROVIDER_T]) -> PROVIDER_T:
        """
        Retrieve an instance of the specified annotation from the container.

        Args:
            annotation (Type[PROVIDER_T]): The annotation (provider) for which an
                instance is requested.

        Returns:
            PROVIDER_T: An instance of the specified annotation.

        Raises:
            MemberNotBoundError: If the requested annotation is not bound in the
                container.
        """
        try:
            member = self._bound_members[annotation]
        except KeyError:
            raise _MemberNotBoundErrorAsKeyError(f"{annotation} is not bound.")
        else:
            scope = self._build_scope(member)
            return scope.get_instance_of(member)
