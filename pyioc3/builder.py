from __future__ import annotations

from typing import (
    Callable,
    Generic,
    List,
    Optional,
    Type,
    Union,
)

from .scope_enum import ScopeEnum
from .static_container_builder import StaticContainerBuilder
from .interface import (
    Binding,
    Container,
    FACTORY_T,
    PROVIDER_T,
    ProviderBinding,
    TARGET_T,
)


class BuilderBase(Generic[TARGET_T]):
    """Base class for building instances with dependency injection.

    This class creates a new dependency tree each time build() it is run. This means
    that there is no distinction between SINGLETON and REQUESTED scope as the the
    underlaying container will only be activated once.

    Example Usage:

        class DuckInterface(ABC):
            ...

        class DuckBuilder(Builder[DuckInterface]):
            def __init__(self) -> None:
                super().__init__(DuckInterface)

        class Mallard(DuckInterface):
            ...

        duck = (
            DuckBuilder()
            .using_provider(Mallard, DuckInterface)
            .build()
        )

        assert isinstance(duck, Mallard)
    """

    def __init__(
        self,
        target_t: Type[TARGET_T],
        bindings: Optional[List[Binding]] = None,
    ):
        """Initialize the builder with optional bindings.

        The provided target_t will be automatically bound as a default. If included
        in bindings, the bindings entry will be used.

        Arguments:
            target_t: Type type produced by this builder.
            bindings: An optional list of bindings.
        """
        self._target_t = target_t
        # Bind target_t FIRST. Allow 'bindings' to override
        bindings = [ProviderBinding(target_t)] + (bindings or [])
        self._container_builder = StaticContainerBuilder(bindings)

    def using_provider(
        self,
        annotation: Type[PROVIDER_T],
        implementation: Optional[Type[PROVIDER_T]] = None,
        scope: Optional[Union[str, ScopeEnum]] = None,
        on_activate: Optional[Callable[[PROVIDER_T], PROVIDER_T]] = None,
    ) -> BuilderBase(Generic[PROVIDER_T]):
        """
        Register a provider for dependency injection.

        Arguments:
            annotation: The annotion target.
            implementation: The optional implementation class. If not provided,
                            The annotation is used as the implementation.
            scope: The optional scope of the provider. Defaults to Requested.
            on_activate: An optional activation callback.

        Returns:
            BuilderBase: The builder instance.
        """
        self._container_builder.bind(
            annotation=annotation,
            implementation=implementation,
            scope=scope,
            on_activate=on_activate,
        )
        return self

    def using_constant(
        self,
        annotation: Type[PROVIDER_T],
        value: PROVIDER_T,
    ) -> BuilderBase(Generic[PROVIDER_T]):
        """
        Register a constant for dependency injection.

        Arguments:
            annotation: The annotion target.
            value: The constant value.

        Returns:
            BuilderBase: The builder instance.
        """
        self._container_builder.bind_constant(annotation=annotation, value=value)
        return self

    def using_factory(
        self,
        annotation: FACTORY_T,
        factory: Callable[[Container], FACTORY_T],
    ) -> BuilderBase(Generic[PROVIDER_T]):
        """
        Register a factory function for dependency injection.

        Arguments:
            annotation: The annotion target.
            factory: The factory function.

        Returns:
            BuilderBase: The builder instance.
        """
        self._container_builder.bind_factory(annotation=annotation, factory=factory)
        return self

    def build(self) -> TARGET_T:
        """
        Build an instance of the specified target type using the registered dependencies.

        Returns:
            TARGET_T: The built instance.
        """
        return self._container_builder.build().get(self._target_t)
