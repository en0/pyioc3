from pyioc3.adapters import FactoryAsImplAdapter, ValueAsImplAdapter
from pyioc3.bound_member import BoundMember
from pyioc3.scope_enum import ScopeEnum
from pyioc3.static_container import StaticContainer


class StaticContainerBuilder:
    """Bind classes, values, functions, and factories to a static container."""

    _bound_members: dict = {}

    def bind(self, annotation, implementation, scope: ScopeEnum = ScopeEnum.TRANSIENT):
        """Bind a class

        This allows you to bind any callable type to an annotation. Dependencies will be
        injected into this object as needed when created.

        Scoping can be set to control reuse.

        Arguments:
            annotation:
                The hint used to inject an instance of implementation

            implementation:
                A callable type who's result will be stored return and stored according to the scope

            scope:
                Identifies how the object should be cached. Options are Transient, Requested, Singleton
                Default: Transient.

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
        self._bound_members[annotation] = BoundMember(annotation, implementation, scope)

    def bind_constant(self, annotation, value):
        """Bind a constant value

        This allows you to bind any object to an annotation in a singleton scope.

        Arguments:
            annotation:
                The hint used to inject the constant

            value:
                Any value. Object, function, type, anything.

        Example:

            ioc_builder.bind_constant(
                annotation="my_constant",
                value="Hello, world!")

        """
        self.bind(
            annotation,
            ValueAsImplAdapter(value),
            scope=ScopeEnum.SINGLETON)

    def bind_factory(self, annotation, factory):
        """Bind a higher order function

        This approach allows you to control the creation of objects and gives you access
        to the container. This lets you make runtime decision about how to create an instance.

        Arguments:
            annotation:
                The hint used to inject the factory

            factory:
                A higher order function that accepts the StackContainer as an arugment.

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
        self.bind(
            annotation,
            FactoryAsImplAdapter(factory),
            scope=ScopeEnum.SINGLETON)

    def build(self) -> StaticContainer:
        """Compute dependency graph and return the container

        This call will roll over all the objects and compute the dependants of each member. The container
        itself is also added to the graph and can thus be injected using it's Type as the annotation.

        Example:
            ioc_builder = StaticContainerBuilder()
            ioc = ioc_builder.build()
            container = ioc.get(StaticContainer)
            container == ioc ## True
        """

        container = StaticContainer(self._bound_members)
        self.bind_constant(StaticContainer, container)

        for bound_member in self._bound_members.values():
            for annotation in bound_member.parameters:
                bound_member.depends_on.append(self._bound_members[annotation])

        return container
