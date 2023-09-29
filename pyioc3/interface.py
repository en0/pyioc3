from abc import ABC, abstractmethod
from typing import (
    Callable,
    NamedTuple,
    Optional,
    Type,
    TypeVar,
    Union,
)

from .scope_enum import ScopeEnum


TARGET_T = TypeVar("TARGET_T")
PROVIDER_T = TypeVar("PROVIDER_T")
FACTORY_T = Callable[..., PROVIDER_T]


class ProviderBinding(NamedTuple):
    """Represents a binding for providing instances through dependency injection."""

    annotation: Type[PROVIDER_T]
    implementation: Optional[Type[PROVIDER_T]] = None
    scope: Optional[Union[str, ScopeEnum]] = None
    on_activate: Optional[Callable[[PROVIDER_T], PROVIDER_T]] = None


class ConstantBinding(NamedTuple):
    """Represents a binding for providing constant values through dependency injection."""

    value: PROVIDER_T
    annotation: Type[PROVIDER_T]


class FactoryBinding(NamedTuple):
    """Represents a binding for providing instances created by factory functions."""

    factory: Callable[["Container"], FACTORY_T]
    annotation: FACTORY_T


Binding = Union[ProviderBinding, ConstantBinding, FactoryBinding]


class Scope(ABC):
    """An IOC Instance Scope"""

    @abstractmethod
    def __contains__(self, annotation: Type[PROVIDER_T]) -> bool:
        """Check if the given annotation exists in this scope.

        Arguments:
         annotation: The str or type var used to identify an instance.

        Returns:
         True, if the annotation exists. Else, False.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, annotation: Type[PROVIDER_T], instance: PROVIDER_T) -> None:
        """Add a instance to this scope under the given annotation

        Arguments:
         annotation: The str or type var used to identify an instance.
         instance: Any value to store as the instance associated with the annotation.
        """
        raise NotImplementedError()

    @abstractmethod
    def use(self, annotation: Type[PROVIDER_T]) -> object:
        """Get the instance associated with the given annotation.

        Arguments:
         annotation: The str or type var used to identify an instance.

        Raises:
         KeyError, if the the given annotation does not exist in this scope.
        """
        raise NotImplementedError()


class Container(ABC):
    """An IOC Container"""

    @abstractmethod
    def get(self, annotation: Type[PROVIDER_T]) -> PROVIDER_T:
        """Retrieve an instance of the specified annotation from the container.

        Args:
            annotation (Type[PROVIDER_T]): The annotation (provider) for which an
                instance is requested.

        Returns:
            PROVIDER_T: An instance of the specified annotation.

        Raises:
            MemberNotBoundError: If the requested annotation is not bound in the
                container.
        """
        raise NotImplementedError()


class ContainerBuilder(ABC):
    """Bind classes, values, functions, and factories to a container."""

    @abstractmethod
    def bind(
        self,
        annotation: Type[PROVIDER_T],
        implementation: Optional[Type[PROVIDER_T]] = None,
        scope: Union[str, ScopeEnum] = ScopeEnum.TRANSIENT,
        on_activate: Callable[[PROVIDER_T], PROVIDER_T] = None,
    ):
        """Bind a class.

        Bind any callable type to an annotation. Dependencies will be
        injected into this object as needed when created.

        Scoping can be set to control reuse.

        Arguments:
          annotation:     The hint used to inject an instance of implementation

          implementation: Optional: A callable type who's result will be stored return
                          and stored according to the scope. If implementation is not
                          inlcuded Annotation will be used in it's place.

          scope:          Optional: Identifies how the object should be cached.
                          Options are Transient, Requested, Singleton
                          Default: Transient.

          on_activate:    Optional: A function that will be called with the
                          constructed implementation before it is used as a dep
                          or given as the return in container.get()
                          Default: None.

        Scopes:
            Transient scopes and not cached.
            Requested scopes are cached during the current execution of a container.get call.
            Singleton scopes are only instanced once and cached for the lifetime of the container.

        Example:

            class Duck:
                def quack(self):
                    print("quack")

            ioc_builder.bind(
                annotation="duck",
                implementation=Duck)
        """
        raise NotImplementedError()

    @abstractmethod
    def bind_constant(self, annotation: Type[PROVIDER_T], value: PROVIDER_T):
        """Bind a constant value

        This allows you to bind any object to an annotation in a singleton scope.

        Arguments:
          annotation: The hint used to inject the constant
          value: Any value. Object, function, type, anything.

        Example:

            ioc_builder.bind_constant(
                annotation="my_constant",
                value="Hello, world!")

        """
        raise NotImplementedError()

    @abstractmethod
    def bind_factory(
        self, annotation: FACTORY_T, factory: Callable[[Container], FACTORY_T]
    ):
        """Bind a higher order function

        This approach allows you to control the creation of objects and gives you access
        to the container. This lets you make runtime decision about how to create an instance.

        Arguments:
          annotation: The hint used to inject the factory
          factory:    A higher order function that accepts the StackContainer as an
                      arugment.

        Example:
            def my_factory_wrapper(ctx: StaticContainer)

                def my_factory(foo):
                    bar = ctx.get("bar")
                    bar.baz(foo)
                    return bar

                return my_factory

            ioc_builder.bind_factory(
                annotation="my_factory",
                factory=my_function)
        """
        raise NotImplementedError()

    @abstractmethod
    def build(self) -> Container:
        """Compute dependency graph and return the container

        This call will roll over all the objects and compute the dependants of each
        member. The container itself is also added to the graph and can thus be
        injected using it's Type as the annotation.

        Example:
            ioc_builder = StaticContainerBuilder()
            ioc = ioc_builder.build()
            container = ioc.get(StaticContainer)
            container == ioc ## True
        """
        raise NotImplementedError()
