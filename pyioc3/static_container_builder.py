from typing import Dict, Union, Type, Callable, Optional, List

from .bound_member_factory import BoundMemberFactory
from .errors import CircularDependencyError, _MemberNotBoundErrorAsKeyError
from .queued_cycle_test import QueuedCycleTest
from .scope_enum import ScopeEnum
from .static_container import StaticContainer
from .interface import (
    ConstantBinding,
    Container,
    ContainerBuilder,
    FACTORY_T,
    FactoryBinding,
    PROVIDER_T,
    ProviderBinding,
    Binding,
)


class StaticContainerBuilder(ContainerBuilder):
    """Bind classes, values, functions, and factories to a container."""

    def __init__(
        self,
        bindings: Optional[List[Binding]] = None,
    ) -> None:
        """Create a StaticContainerBuilder.

        Arguments:
            bindings: Optional: A list of default binidngs.

        Returns:
            StaticContainerBuilder
        """
        self._bindings: Dict[Type[PROVIDER_T], Binding] = {}
        for binding in bindings or []:
            self._bindings[binding.annotation] = binding

    def bind(
        self,
        annotation: Type[PROVIDER_T],
        implementation: Optional[Type[PROVIDER_T]] = None,
        scope: Union[str, ScopeEnum] = ScopeEnum.TRANSIENT,
        on_activate: Callable[[PROVIDER_T], PROVIDER_T] = None,
    ) -> "StaticContainerBuilder":
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

        Returns:
            StaticContainerBuilder
        """
        self._bindings[annotation] = ProviderBinding(
            implementation=implementation,
            annotation=annotation,
            scope=scope,
            on_activate=on_activate,
        )
        return self

    def bind_constant(
        self,
        annotation: Type[PROVIDER_T],
        value: PROVIDER_T,
    ) -> "StaticContainerBuilder":
        """Bind a constant value

        This allows you to bind any object to an annotation in a singleton scope.

        Arguments:
          annotation: The hint used to inject the constant
          value: Any value. Object, function, type, anything.

        Example:

            ioc_builder.bind_constant(
                annotation="my_constant",
                value="Hello, world!")

        Returns:
            StaticContainerBuilder
        """
        self._bindings[annotation] = ConstantBinding(
            value=value,
            annotation=annotation,
        )
        return self

    def bind_factory(
        self, annotation: FACTORY_T, factory: Callable[[Container], FACTORY_T]
    ) -> "StaticContainerBuilder":
        """Bind a higher order function

        This approach allows you to control the creation of objects and gives you access
        to the container. This lets you make runtime decision about how to create an instance.

        Arguments:
          annotation: The hint used to inject the factory
          factory:    A higher order function that accepts the StackContainer as an
                      arugment.

        Example:
            def my_factory_wrapper(ctx: Container)

                def my_factory(foo):
                    bar = ctx.get("bar")
                    bar.baz(foo)
                    return bar

                return my_factory

            ioc_builder.bind_factory(
                annotation="my_factory",
                factory=my_function)

        Returns:
            StaticContainerBuilder
        """
        self._bindings[annotation] = FactoryBinding(
            factory=factory,
            annotation=annotation,
        )
        return self

    def build(self) -> Container:
        """Compute dependency graph and return the container

        This call will roll over all the objects and compute the dependants of each
        member. The container itself is also added to the graph and can thus be
        injected using it's Type as the annotation.

        Example:
            ioc_builder = StaticContainerBuilder()
            ioc = ioc_builder.build()
            container = ioc.get(Container)
            container == ioc ## True
        """

        bound_members = {
            binding.annotation: BoundMemberFactory.build(binding)
            for binding in self._bindings.values()
        }

        container = StaticContainer(bound_members)

        bound_members[Container] = BoundMemberFactory.build(
            ConstantBinding(
                annotation=Container,
                value=container,
            )
        )

        # This is here for backwards compatability
        bound_members[StaticContainer] = BoundMemberFactory.build(
            ConstantBinding(
                annotation=StaticContainer,
                value=container,
            )
        )

        for bound_member in bound_members.values():
            for annotation in bound_member.parameters:
                try:
                    bound_member.bind_dependant(bound_members[annotation])
                except KeyError:
                    raise _MemberNotBoundErrorAsKeyError(
                        f"Binding {bound_member.implementation} depends "
                        f"on {annotation} which is not bound."
                    )

        cycle = QueuedCycleTest.find_cycle(bound_members)

        if cycle:
            raise CircularDependencyError(
                "Circular Dependency Detected: "
                + ", ".join([str(m.implementation) for m in cycle])
            )

        return container
