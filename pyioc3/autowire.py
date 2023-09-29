import pkgutil
import importlib
from typing import Union, List, Callable, Optional, Type, Set
from types import ModuleType
from collections import deque

from .errors import AutoWireError
from .interface import PROVIDER_T, Binding, ProviderBinding, FactoryBinding
from .scope_enum import ScopeEnum
from .static_container_builder import StaticContainerBuilder


ModuleRef = Union[str, ModuleType]
ModuleList = Union[List[ModuleRef], ModuleRef]
ExcludeList = Union[str, List[str]]


def bind(
    annotation: Optional[Type[PROVIDER_T]] = None,
    scope: Union[str, ScopeEnum] = None,
    on_activate: Callable[[PROVIDER_T], PROVIDER_T] = None,
) -> Callable[[Callable], Callable]:
    """
    Decorator for binding a class for use in dependency injection.

    Args:
        annotation (Optional[Type[PROVIDER_T]]): The interface or annotation to which the
            class should be bound as a provider. If not provided, the implementation
            class itself will be used as the annotation.
        scope (Union[str, ScopeEnum]): The scope in which the provider instances should
            be created and managed. It can be one of the values from the `ScopeEnum`
            enumeration, such as "singleton," "transient," or "requested." If not
            specified, the default scope, "transient" will be used.
        on_activate (Callable[[PROVIDER_T], PROVIDER_T]): An optional callback function
            to be executed when instances of the provider class are activated or
            retrieved from the container. This function can perform additional
            initialization or configuration on the provider instance.

    Returns:
        Callable[[Callable], Callable]: A decorator function that can be used to annotate
        a class as a provider for the specified interface.

    Example:
        To bind a class as a provider for the `SomeInterface` interface with a transient
        scope:

        >>> @bind(SomeInterface, scope="transient")
        ... class SomeProvider(SomeInterface):
        ...     def provide(self):
        ...         return SomeImplementation()

    Note:
        - If the `annotation` parameter is not provided, the implementation class itself
          will be used as the annotation.
        - The `scope` parameter determines how instances of the provider class are
          managed within the IoC container.
        - The `on_activate` callback can be used for additional setup or customization
          when instances of the provider class are retrieved.

    See Also:
        - For more information on using decorators to configure providers, refer to the
          library documentation.
        - To understand the different scopes available for providers, refer to the
          `ScopeEnum` enumeration in the library.
    """

    def decorator(implementation: Type[PROVIDER_T]) -> Type[PROVIDER_T]:
        binding = ProviderBinding(
            annotation=annotation or implementation,
            implementation=implementation,
            scope=scope or ScopeEnum.TRANSIENT,
            on_activate=on_activate,
        )
        AutoWireContainerBuilder._staged_bindings.append(
            (implementation.__module__, binding)
        )
        return implementation

    return decorator


def bind_factory(annotation: Type[PROVIDER_T]):
    """
    Decorator for binding a function factory for use in dependency injection.

    This decorator allows you to bind a function factory to an interface or annotation,
    indicating that the factory should be used to create instances of the specified
    type. Function factories are used to construct instances with custom initialization
    or configuration.

    Args:
        annotation (Type[PROVIDER_T]): The interface or annotation to which the
            factory should be bound.

    Returns:
        Callable: A decorator function that can be used to annotate a function as a
        factory for the specified interface or annotation.

    Example:
        To bind a function factory for creating instances of `SomeClass`:

        >>> @bind_factory(SomeClassFactory)
        ... def some_class_factory(ctx: Container) -> SomeClassFactory:
        ...     def wrapped(some_args) -> SomeClass:
        ...         instance = SomeClass()
        ...         # Perform additional initialization here if needed.
        ...         return instance
    """

    def decorator(factory: Callable):
        binding = FactoryBinding(
            annotation=annotation,
            factory=factory,
        )
        AutoWireContainerBuilder._staged_bindings.append((factory.__module__, binding))
        return factory

    return decorator


class AutoWireContainerBuilder(StaticContainerBuilder):
    """
    Container builder for auto-wiring dependencies from specified modules.

    This class facilitates the creation of an IoC container by automatically scanning
    and binding dependencies from the provided modules.

    Arguments:
        modules (Union[List[ModuleRef], ModuleRef]): A list of module references
            (either module names or module objects) to be scanned for dependencies.
            If a single module reference is provided, it will be treated as a list
            with a single element.
        excludes (Optional[ExcludeList]): A list of module names to be excluded
            from scanning. Modules listed here will not be considered for dependency
            binding. If a single module name is provided, it will be treated as a
            list with a single element. If not specified or set to an empty list, no
            modules will be excluded.

    Example:
        To create an `AutoWireContainerBuilder` that scans the 'my_package' module and
        excludes the 'excluded_module' from scanning:

        >>> builder = AutoWireContainerBuilder(
        ...     modules=['my_package'],
        ...     excludes=['excluded_module']
        ... )


    Note:
        Dependencies are auto-wired based on class decorators defined within the
        specified modules. Ensure that the modules follow the appropriate
        conventions for dependency binding.

    See Also:
        For more information on how to use and configure the IoC container, refer to
        the documentation.
    """

    _staged_bindings: List[Binding] = []

    def __init__(
        self,
        modules: ModuleList,
        excludes: Optional[ExcludeList] = None,
    ) -> None:
        """
        Initialize a new AutoWireContainerBuilder.


        Arguments:
            modules (Union[List[ModuleRef], ModuleRef]): A list of module references
                (either module names or module objects) to be scanned for
                dependencies. If a single module reference is provided, it will
                be treated as a list with a single element.
            excludes (Optional[ExcludeList]): A list of module names to be
                excluded from scanning. Modules listed here will not be considered
                for dependency binding. If a single module name is provided, it will
                be treated as a list with a single element. If not specified or set
                to an empty list, no modules will be excluded.

        Returns:
            None
        """
        modules = [modules] if isinstance(modules, str) else modules
        excludes = [excludes] if isinstance(excludes, str) else (excludes or [])
        included_modules = AutoWireContainerBuilder._collect_modules(modules, excludes)
        bindings = [
            binding
            for module_name, binding in set(AutoWireContainerBuilder._staged_bindings)
            if module_name in included_modules
        ]
        AutoWireContainerBuilder._check_for_duplicates(bindings)
        super().__init__(bindings)

    @staticmethod
    def _check_for_duplicates(bindings: List[Binding]):
        seen = set()
        for binding in bindings:
            if binding.annotation in seen:
                impls = ", ".join(
                    [
                        str(
                            b.implementation
                            if hasattr(b, "implementation")
                            else b.factory
                        )
                        for b in bindings
                        if b.annotation == binding.annotation
                    ]
                )
                raise AutoWireError(
                    f"AutoWire found multiple providers for annotation '{binding.annotation}'. "
                    f"[{impls}]"
                )
            seen.add(binding.annotation)

    @staticmethod
    def _collect_modules(modules: List[ModuleRef], excludes: List[str]) -> Set[str]:
        excludes = set(excludes)
        queue = deque(set(modules) - excludes)
        ret = set()
        while queue:
            mod = queue.pop()
            if isinstance(mod, str):
                mod = importlib.import_module(mod)
            ret.add(mod.__name__)
            if hasattr(mod, "__path__"):
                for submod_info in pkgutil.iter_modules(mod.__path__):
                    submod_name = f"{mod.__name__}.{submod_info.name}"
                    if submod_name not in excludes:
                        queue.append(submod_name)
        return ret
