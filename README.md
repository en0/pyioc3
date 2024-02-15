# pyioc3

Python Inversion of Control (IoC) Container

# About

pyioc3 is a lightweight and versatile Inversion of Control (IoC) container for
Python. It simplifies the management of dependencies and enables cleaner, more
modular code by promoting the use of Dependency Injection (DI) patterns. With
pyioc3, you can effortlessly wire up your application's components, specify
their lifecycles, and inject dependencies without the hassle of manual
instantiation.

# Key Features

## Multiple APIs

pyioc3 offers multiple configuration interfaces including two manual
configuration APIs and a decorator-based autowiring API. These APIs are
flexible, yet simple to use.

## Fluent Interface

pyioc3 manual APIs support method chaining to minimize boiler-plate code and
intermediate variables.

## Scoped Lifecycles

pyioc3 supports various scopes, including Singleton, Transient, and Requested.
This provides fine-grained control of the lifecycle of your objects.

## Predictability

pyioc3 is an immutable ioc container that guarentees predictability of the
dependency tree.

## Constuctor Based DI

pyioc3 implements constructor based dependency injection making it easy to drop
into existing applications.

## Performance

pyioc3 pre-computes the dependency tree, resulting in fast instantiations to
keep your code fast.

## OOP Principles

pyioc3 is designed to improve the maintainability, testability, and flexibility
of your Python applications.

# Quick Start

Install the package

```bash
pip install --user pyioc3
```

## StaticContainerBuilder API

```python
from pyioc3 import StaticContainerBuilder

container = (
    StaticContainerBuilder()
    .bind(Duck)
    .bind(QuackProvider, Squeak)
    .build()
)

duck = container.get(Duck)
duck.quack()
```

## BuilderBase API

```python
from pyioc3.builder import BuilderBase, ProviderBinding

class DuckBuilder(Duck):
    def __init__(self):
        super().__init__(target_t=Duck)

    def with_quack_noise(self, noise: str) -> "DuckBuilder":
        self.using_provider(
            annotation=QuackProvider,
            implementation=DynamicQuackProvider,
            on_activate=lambda x: x.set_quack_noise(noise)
        )
        return self

rubber_duck = (
    DuckBuilder()
    .with_quack_noise("Squeak")
    .build()
)

rubber_duck.quack()
```

## Annotation API

```python
from pyioc3.autowire import bind, AutoWireContainerBuilder


class QuackProvider:
    def quack(self):
        raise NotImplementedError()


@bind()
class Duck:
    def __init__(self, quack: QuackProvider):
        self._quack = quack

    def quack(self):
        self._quack.quack()


@bind(QuackProvider)
class Squeak(QuackProvider):

    def quack(self):
        print("Squeak")


duck = AutoWireContainerBuilder("my_package").build().get(Duck)
duck.quack()
```

# API Documentation

## Terms

### Provider

A class that provides an implementation of some contract.

### Scope

A rule that defines when a provider is instanciated.

__Transient__: A instanciation rule that causes a new instance of a provider to be created for each dependent reference.
__Requested__: A instanciation rule that causes a new instance of a provider to be created once for each request recieved by the IOC container.
__Singleton__: A instanciation rule that causes a new instance of a provider to be created only once.

Scope Examples:

Consider the given dependency tree.

- Class A depends on Class B and Class C.
- Class B depends on Class C.
- Class C has no dependents.

#### Transient Scope

If class C is bound with transient scope, class A and B will have a unique
instance of C each time they are constructed.

```
a = ioc.get(A)
assert a.c is not a.b.c

a_again = ioc.get(A)
assert a_again.c is not a.c
assert a_again.b.c is not a.b.c
```

#### Requested Scope

If class C is bound with requested scope, class A and B will share an
instance of C each time they are constructed.

```
a = ioc.get(A)
assert a.c is a.b.c

a_again = ioc.get(A)
assert a_again.c is not a.c
assert a_again.b.c is not a.b.c
```

#### Singleton Scope

If class C is bound with singleton scope, class A and B will always recieve the
same instance of C.

```
a = ioc.get(A)
assert a.c is a.b.c

a_again = ioc.get(A)
assert a_again.c is a.c
assert a_again.b.c is a.b.c
```

## References

### pyioc3.interface

#### PROVIDER_T

A Generic TypeVar used to identify the type, concrete or abstract, of an injectable.

#### FACTORY_T

A Generic TypeVar used to identify a factory method.

#### FactoryBinding

Represents a binding for providing instances created by factory functions.

__FactoryBinding.factory:__

Any callable that accepts a `Container` and returns another callable.

__FactoryBinding.annotion:__

Any Type or forward reference used to uniquely identify this injectable.

#### ProviderBinding

Represents a binding for providing instances through dependency injection.

__ProviderBinding.annotation:__

Any Type or forward reference used to uniquely identify this injectable.

__ProviderBinding.implementation:__

Any `Class` or Class-Like reference used as the injectable.

__ProviderBinding.scope:__

Any `ScopeEnum` or str (one of "singleton", "transient", "requested") that
identifies the instantiation strategy.

__ProviderBinding.on_activate:__

Any callable that accepts an instance of `ProviderBinding.implementation` and
returns the same instance.

#### ConstantBinding

__ConstantBinding.annotation:__

Any Type or forward reference used to uniquely identify this injectable.

__ConstantBinding.value:__

Any value used as the injectable.

#### Binding

A type union of FactoryBinding, ProviderBinding, and ConstantBinding.

#### Container

An IOC Container

__Container.get:__

Retrieve an instance of the specified annotation from the container.

Args:

- annotation: The annotation (provider) for which an instance is requested.

Returns:

- PROVIDER_T: An instance of the specified annotation.

Raises:
- MemberNotBoundError: If the requested annotation is not bound in the container.

#### ContainerBuilder

Bind classes, values, functions, and factories to a container.

__ContainerBuilder.bind:__

Bind a class.

Bind any callable type to an annotation. Dependencies will be
injected into this object as needed when created.

Scoping can be set to control reuse.

Arguments:

- annotation: The hint used to inject an instance of implementation
- implementation: (Optional) A callable type who's result will be stored return and stored according to the scope. If implementation is not inlcuded Annotation will be used in it's place.
- scope: (Optional) Identifies how the object should be cached. Options are Transient, Requested, Singleton Default: Transient.
- on_activate: (Optional) A function that will be called with the constructed implementation before it is used as a dep or given as the return in container.get() Default: None.

Scopes:

- Transient scopes and not cached.
- Requested scopes are cached during the current execution of a container.get call.
- Singleton scopes are only instanced once and cached for the lifetime of the container.

Returns:

- An instance of the `ContainerBuilder`

__ContainerBuilder.bind_constant:__

Bind a constant value

This allows you to bind any object to an annotation in a singleton scope.

Arguments:

- annotation: The hint used to inject the constant
- value: Any value. Object, function, type, anything.

Returns: 

- An instance of the `ContainerBuilder`

__ContainerBuilder.bind_factory:__

Bind a higher order function

This approach allows you to control the creation of objects and gives you access
to the container. This lets you make runtime decision about how to create an instance.

Arguments:

- annotation: The hint used to inject the factory
- factory: A higher order function that accepts the StackContainer as an arugment.

Returns: 

- An instance of the `ContainerBuilder`

__ContainerBuidler.build:__

Compute dependency graph and return the container

This call will roll over all the objects and compute the dependants of each
member. The container itself is also added to the graph and can thus be
injected using it's Type as the annotation.

Returns: 

- A `Container`

### pyioc3.scope_enums

#### ScopeEnum

ScopeEnum is an enumeration class representing different dependency scopes.

__ScopeEnum.TRANSIENT:__

Indicates a transient scope where a new instance is created for each request.

__ScopeEnum.REQUESTED:__

Indicates a requested scope where a single instance is created for the duration of a request (a single call to `Container.get`), typically used in web applications.

__ScopeEnum.SINGLETON:__

Indicates a singleton scope where a single instance is created and shared across the entire application.

### pyioc3.static_container_builder

#### StaticContainerBuilder

Implements `ContainerBuilder` to allows the caller to staticly bind classes, values, functions, and factories to a container.

__StaticContainerBuilder.\_\_init\_\_:__

Create a StaticContainerBuilder.

Arguments:

- bindings: (Optional) A list of default binidngs.

Returns: 

- A new `ContainerBuilder`

### pyioc3.builder

#### BuilderBase

Base class for building instances with dependency injection.

This class creates a new dependency tree each time build() it is run. This means
that there is no distinction between SINGLETON and REQUESTED scope as the the
underlaying container will only be activated once.

__BuilderBase.\_\_init\_\_:__

Initialize the builder with optional bindings.

The provided target_t will be automatically bound as a default. If included
in bindings, the bindings entry will be used.

Arguments:

- target_t: Type produced by this builder.
- bindings: (Optional) A list of bindings.

__BuilderBase.using_provider:__

Register a provider for dependency injection.

Arguments:

- annotation: The annotion target.
- implementation: The optional implementation class. If not provided, The annotation is used as the implementation.
- scope: The optional scope of the provider. Defaults to Requested.
- on_activate: An optional activation callback.

Returns:

- BuilderBase: The builder instance.

__BuilderBase.using_constant:__

Register a constant for dependency injection.

Arguments:

- annotation: The annotion target.
- value: The constant value.

Returns:

- BuilderBase: The builder instance.

__BuilderBase.using_factory:__

Register a factory function for dependency injection.

Arguments:

- annotation: The annotion target.
- factory: The factory function.

Returns:

- BuilderBase: The builder instance.

__BuilderBase.build:__

Build an instance of the specified target type using the registered dependencies.

Returns:

- TARGET_T: The built instance.

...


### pyioc3.autowire

#### AutoWireContainerBuilder

Implements `ContainerBuilder` to allows the caller to automatically and staticaly bind classes, values, functions, and factories to a container.

This class facilitates the creation of an IoC container by automatically scanning
and binding dependencies from the provided modules.

__AutoWireContainerBuilder.\_\_init\_\_:__

Initialize a new AutoWireContainerBuilder.

Arguments:

- modules: A list of module references (either module names or module objects) to be scanned for dependencies. If a single module reference is provided, it will be treated as a list with a single element.
- excludes: A list of module names to be excluded from scanning. Modules listed here will not be considered for dependency binding. If a single module name is provided, it will be treated as a list with a single element. If not specified or set to an empty list, no modules will be excluded.


__bind:__

Decorator for binding a class for use in dependency injection.

Arguments:

- annotation: The interface or annotation to which the class should be bound as a provider. If not provided, the implementation class itself will be used as the annotation.
- scope: The scope in which the provider instances should be created and managed. It can be one of the values from the `ScopeEnum` enumeration, such as "singleton," "transient," or "requested." If not specified, the default scope, "transient" will be used.
- on_activate: An optional callback function to be executed when instances of the provider class are activated or retrieved from the container. This function can perform additional initialization or configuration on the provider instance.

Returns:

- A decorator function that can be used to annotate a class as a provider for the specified interface.

__bind_factory:__

Decorator for binding a function factory for use in dependency injection.

This decorator allows you to bind a function factory to an interface or annotation,
indicating that the factory should be used to create instances of the specified
type. Function factories are used to construct instances with custom initialization
or configuration.

Arguments:

- annotation: The interface or annotation to which the factory should be bound.

Returns:

- A decorator function that can be used to annotate a function as a factory for the specified interface or annotation.

### pyioc3.errors

#### PyIOC3Error

Base class for all custom PyIOC3 exceptions.

#### CircularDependencyError

Raised if the dependency tree contains cycles.

#### ScopeError

Raised if a string-based scope is not valid.

#### AutoWireError

Raised if the autowire api detects duplicate annotations.

#### MemberNotBoundError

Raised if a member is requested but not bound.

