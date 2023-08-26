from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    NamedTuple,
    Optional,
    Type,
    TypeVar,
    Union,
)

from .interface import Container
from .scope_enum import ScopeEnum
from .static_container_builder import StaticContainerBuilder


TARGET_T = TypeVar("TARGET_T")
PROVIDER_T = TypeVar("PROVIDER_T")
FACTORY_T = Callable[..., PROVIDER_T]


class ProviderBinding(NamedTuple):
    """Represents a binding for providing instances through dependency injection."""

    implementation: Type[PROVIDER_T]
    annotation: Optional[Type[PROVIDER_T]] = None
    scope: Optional[Union[str, ScopeEnum]] = None
    on_activate: Optional[Callable[[PROVIDER_T], PROVIDER_T]] = None


class ConstantBinding(NamedTuple):
    """Represents a binding for providing constant values through dependency injection."""

    value: PROVIDER_T
    annotation: Type[PROVIDER_T]


class FactoryBinding(NamedTuple):
    """Represents a binding for providing instances created by factory functions."""

    factory: Callable[[Container], FACTORY_T]
    annotation: FACTORY_T


def _add_provider_to_map(binding_map: Dict, binding: ProviderBinding):

    annotation = binding.annotation or binding.implementation
    scope = binding.scope or ScopeEnum.REQUESTED

    if isinstance(scope, str):
        try:
            scope = {
                "TRANSIENT": ScopeEnum.TRANSIENT,
                "REQUESTED": ScopeEnum.REQUESTED,
                "SINGLETON": ScopeEnum.SINGLETON,
                "transient": ScopeEnum.TRANSIENT,
                "requested": ScopeEnum.REQUESTED,
                "singleton": ScopeEnum.SINGLETON,
                "t": ScopeEnum.TRANSIENT,
                "r": ScopeEnum.REQUESTED,
                "s": ScopeEnum.SINGLETON,
                "T": ScopeEnum.TRANSIENT,
                "R": ScopeEnum.REQUESTED,
                "S": ScopeEnum.SINGLETON,
            }[scope]

        except KeyError as ex:
            raise ValueError(f'Unknown scope "{scope}"') from ex

    binding_map[annotation] = ProviderBinding(
        implementation=binding.implementation,
        annotation=annotation,
        scope=scope,
        on_activate=binding.on_activate
    )


def _add_binding_to_map(
    binding_map: Dict,
    binding: Union[ProviderBinding, ConstantBinding, FactoryBinding]
):
    if isinstance(binding, ProviderBinding):
        _add_provider_to_map(binding_map, binding)
    else:
        binding_map[binding.annotation] = binding


class BuilderBase(Generic[TARGET_T]):
    """Base class for building instances with dependency injection.

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
        providers: Optional[List[ProviderBinding]] = None,
        constants: Optional[List[ConstantBinding]] = None,
        factories: Optional[List[FactoryBinding]] = None,
    ):
        """
        Initialize the builder with optional providers, constants, and factories.

        Arguments:
            providers: An optional list of provider bindings.
            constants: An optional list of constant bindings.
            factories: An optional list of factory bindings.
        """
        self._target_t = target_t
        self._providers: Dict[Type, ProviderBinding] = {}
        self._constants: Dict[Type, ConstantBinding] = {}
        self._factories: Dict[Type, FactoryBinding] = {}

        for provider in providers or []:
            _add_binding_to_map(self._providers, provider)

        for constant in constants or []:
            _add_binding_to_map(self._constants, constant)

        for factory in factories or []:
            _add_binding_to_map(self._factories, factory)

    def using_provider(
        self,
        implementation: Type[PROVIDER_T],
        annotation: Optional[Type[PROVIDER_T]] = None,
        scope: Optional[Union[str, ScopeEnum]] = None,
        on_activate: Optional[Callable[[PROVIDER_T], PROVIDER_T]] = None,
    ) -> "BuilderABC(Generic[BUILDER_T])":
        """
        Register a provider for dependency injection.

        Arguments:
            implementation: The implementation class.
            annotation: The optional annotion target.
            scope: The optional scope of the provider. Defaults to Requested.
            on_activate: An optional activation callback.

        Returns:
            BuilderABC: The builder instance.
        """
        _add_provider_to_map(
            self._providers,
            ProviderBinding(
                implementation=implementation,
                annotation=annotation,
                scope=scope,
                on_activate=on_activate,
            )
        )
        return self

    def using_constant(
        self,
        value: PROVIDER_T,
        annotation: Type[PROVIDER_T],
    ) -> "BuilderABC(Generic[BUILDER_T])":
        """
        Register a constant for dependency injection.

        Arguments:
            value: The constant value.
            annotation: The annotion target.

        Returns:
            BuilderABC: The builder instance.
        """
        _add_binding_to_map(
            self._constants,
            ConstantBinding(
                value=value,
                annotation=annotation,
            )
        )
        return self

    def using_factory(
        self,
        factory: Callable[[Container], FACTORY_T],
        annotation: FACTORY_T,
    ) -> "BuilderABC(Generic[BUILDER_T])":
        """
        Register a factory function for dependency injection.

        Arguments:
            factory: The factory function.
            annotation: The annotion target.

        Returns:
            BuilderABC: The builder instance.
        """
        _add_binding_to_map(
            self._factories,
            FactoryBinding(
                factory=factory,
                annotation=annotation,
            )
        )
        return self

    def build(self) -> TARGET_T:
        """
        Build an instance of the specified target type using the registered dependencies.

        Returns:
            TARGET_T: The built instance.
        """

        container_builder = StaticContainerBuilder()

        for provider in self._providers.values():
            container_builder.bind(
                annotation=provider.annotation,
                implementation=provider.implementation,
                scope=provider.scope,
                on_activate=provider.on_activate,
            )

        for constant in self._constants.values():
            container_builder.bind_constant(
                annotation=constant.annotation,
                value=constant.value,
            )

        for factory in self._factories.values():
            container_builder.bind_factory(
                annotation=factory.annotation,
                factory=factory.factory,
            )

        container = container_builder.build()
        return container.get(self._target_t)

