from typing import Type
from .bound_member import BoundMember
from .interface import Scope, PROVIDER_T
from .scope_enum import ScopeEnum


class PersistentScope(Scope):
    """
    PersistentScope is an implementation of the Scope interface for managing
    persistent instances.

    Attributes:
        _cache (Dict[Type[PROVIDER_T], PROVIDER_T]): A dictionary storing persistent
            instances mapped to their associated annotations.

    Methods:
        __contains__(self, annotation: Type[PROVIDER_T]) -> bool:
            Checks if a persistent instance with the specified annotation exists in the
            scope.

        add(self, annotation: Type[PROVIDER_T], instance: PROVIDER_T) -> None:
            Adds a persistent instance to the scope.

        use(self, annotation: Type[PROVIDER_T]) -> object:
            Retrieves a persistent instance from the scope.

    Example:
        To use `PersistentScope` to manage persistent instances:

        ```python
        from pyioc3.scope_container import PersistentScope

        # Create a PersistentScope.
        scope = PersistentScope()

        # Add a persistent instance to the scope.
        scope.add(MyAnnotation, my_instance)

        # Retrieve a persistent instance from the scope.
        instance = scope.use(MyAnnotation)
        ```

    See Also:
        - `Scope`: The base interface for managing dependency scopes.

    """

    def __init__(self):
        self._cache = {}

    def __contains__(self, annotation: Type[PROVIDER_T]) -> bool:
        """
        Checks if a persistent instance with the specified annotation exists in
        the scope.

        Args:
            annotation (Type[PROVIDER_T]): The annotation of the persistent instance.

        Returns:
            bool: True if a persistent instance with the specified annotation exists;
            otherwise, False.

        """
        return annotation in self._cache.keys()

    def add(self, annotation: Type[PROVIDER_T], instance: PROVIDER_T) -> None:
        """
        Adds a persistent instance to the scope.

        Args:
            annotation (Type[PROVIDER_T]): The annotation of the persistent instance.
            instance (PROVIDER_T): The persistent instance to add to the scope.

        """
        self._cache[annotation] = instance

    def use(self, annotation: Type[PROVIDER_T]) -> object:
        """
        Retrieves a persistent instance from the scope.

        Args:
            annotation (Type[PROVIDER_T]): The annotation of the persistent instance.

        Returns:
            object: The persistent instance associated with the specified annotation.

        """
        return self._cache[annotation]


class TransientScope(Scope):
    """
    TransientScope is an implementation of the Scope interface for managing transient
    instances.

    Attributes:
        _cache (Dict[Type[PROVIDER_T], List[PROVIDER_T]]): A dictionary storing lists
            of transient instances mapped to their associated annotations.

    Methods:
        __contains__(self, annotation: Type[PROVIDER_T]) -> bool:
            Checks if any transient instances with the specified annotation exist in
            the scope.

        add(self, annotation: Type[PROVIDER_T], instance: PROVIDER_T) -> None:
            Adds a transient instance to the scope.

        use(self, annotation) -> object:
            Retrieves a transient instance from the scope.

    Example:
        To use `TransientScope` to manage transient instances:

        ```python
        from pyioc3.scope_container import TransientScope

        # Create a TransientScope.
        scope = TransientScope()

        # Add a transient instance to the scope.
        scope.add(MyAnnotation, my_instance)

        # Retrieve a transient instance from the scope.
        instance = scope.use(MyAnnotation)
        ```

    See Also:
        - `Scope`: The base interface for managing dependency scopes.
    """

    def __init__(self):
        self._cache = {}

    def __contains__(self, annotation: Type[PROVIDER_T]) -> bool:
        """
        Checks if any transient instances with the specified annotation exist in the scope.

        Args:
            annotation (Type[PROVIDER_T]): The annotation of the transient instance.

        Returns:
            bool: True if any transient instances with the specified annotation exist;
            otherwise, False.
        """
        return annotation in self._cache.keys()

    def add(self, annotation: Type[PROVIDER_T], instance: PROVIDER_T) -> None:
        """
        Adds a transient instance to the scope.

        Args:
            annotation (Type[PROVIDER_T]): The annotation of the transient instance.
            instance (PROVIDER_T): The transient instance to add to the scope.
        """
        if annotation in self:
            self._cache[annotation].append(instance)
        else:
            self._cache[annotation] = [instance]

    def use(self, annotation) -> object:
        """
        Retrieves a transient instance from the scope.

        Args:
            annotation: The annotation of the transient instance.

        Returns:
            object: The transient instance associated with the specified annotation.
        """
        inst = self._cache[annotation].pop()
        if len(self._cache[annotation]) == 0:
            del self._cache[annotation]
        return inst


class ScopeContainer:
    """
    ScopeContainer is a class for managing dependency scopes and resolving
    dependencies.

    Args:
        singleton (Scope): The scope for managing singleton instances.

    Methods:
        has(self, member: BoundMember) -> bool:
            Checks if a bound member is present in the associated scope.

        add(self, member: BoundMember) -> None:
            Adds a bound member to the associated scope.

        get_instance_of(self, member: BoundMember) -> PROVIDER_T:
            Retrieves an instance of a bound member from the associated scope.

    Example:
        To use `ScopeContainer` for managing dependency scopes:

        ```python
        from pyioce3.scope_container import ScopeContainer

        # Create a ScopeContainer with a PersistentScope for singletons.
        container = ScopeContainer(singleton=PersistentScope())

        # Add a bound member to the container.
        container.add(my_bound_member)

        # Retrieve an instance of the bound member from the container.
        instance = container.get_instance_of(my_bound_member)
        ```

    See Also:
        - `Scope`: The base interface for managing dependency scopes.
        - `ScopeEnum`: Enumeration of different dependency scopes.
        - `BoundMember`: Metadata associated with a bound member.
    """

    def __init__(self, singleton: Scope):
        self._scopes = {
            ScopeEnum.SINGLETON: singleton,
            ScopeEnum.REQUESTED: PersistentScope(),
            ScopeEnum.TRANSIENT: TransientScope(),
        }

    def _create_instance(self, member: BoundMember) -> PROVIDER_T:
        args = list()
        for dep in member:
            args.append(self.get_instance_of(dep))
        return member.on_activate(member.implementation(*args))

    def _get_scope(self, member: BoundMember) -> Scope:
        return self._scopes[member.scope]

    def has(self, member: BoundMember) -> bool:
        """
        Checks if a bound member is present in the associated scope.

        Args:
            member (BoundMember): The bound member to check.

        Returns:
            bool: True if the member is present in the scope, False otherwise.
        """
        return member.annotation in self._get_scope(member)

    def add(self, member: BoundMember) -> None:
        """
        Adds a bound member to the associated scope.

        Args:
            member (BoundMember): The bound member to add to the scope.
        """
        self._get_scope(member).add(member.annotation, self._create_instance(member))

    def get_instance_of(self, member: BoundMember) -> PROVIDER_T:
        """
        Retrieves an instance of a bound member from the associated scope.

        Args:
            member (BoundMember): The bound member for which to retrieve an instance.

        Returns:
            PROVIDER_T: An instance of the bound member.
        """
        return self._get_scope(member).use(member.annotation)
