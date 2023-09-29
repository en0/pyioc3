from .interface import Container


class ValueAsImplAdapter:
    """
    ValueAsImplAdapter is an adapter class for value-based bindings.

    Args:
        value: The value to be provided when the adapter is called.

    Methods:
        __call__(self) -> Any:
            Returns the stored value when the adapter is called.

    Example:
        To create a ValueAsImplAdapter instance:

        ```python
        from pyioc3.adapters import ValueAsImplAdapter

        # Create a ValueAsImplAdapter with a value.
        value_adapter = ValueAsImplAdapter(42)

        # Call the adapter to retrieve the stored value.
        result = value_adapter()  # result will be 42
        ```
    """

    def __init__(self, value):
        self._value = value

    def __call__(self):
        return self._value


class FunctionAsImplAdapter:
    """
    FunctionAsImplAdapter is an adapter class for function-based bindings.

    Args:
        fn: The function to be executed when the adapter is called.
        *args: Optional arguments to be passed to the function.

    Methods:
        __call__(self) -> Any:
            Calls the stored function with optional arguments and returns the result.

    Example:
        To create a FunctionAsImplAdapter instance:

        ```python
        from pyioce3.adapters import FunctionAsImplAdapter

        # Create a function that takes two arguments.
        def add(a, b):
            return a + b

        # Create a FunctionAsImplAdapter with the function and arguments.
        function_adapter = FunctionAsImplAdapter(add, 2, 3)

        # Call the adapter to execute the function and retrieve the result.
        result = function_adapter()  # result will be 5
        ```
    """

    def __init__(self, fn, *args):
        self._args = args
        self._fn = fn

    def __call__(self):
        args = self._args
        return self._fn(*args)


class FactoryAsImplAdapter:
    """
    FactoryAsImplAdapter is an adapter class for factory-based bindings.

    Args:
        fn: The factory function to be executed when the adapter is called.

    Methods:
        __call__(self, ctx: Container) -> Any:
            Calls the stored factory function with a container and returns the result.

    Example:
        To create a FactoryAsImplAdapter instance:

        ```python
        from pyioc3.adapters import FactoryAsImplAdapter

        # Create a factory function that takes a container.
        def create_instance(ctx):
            def factory(config):
                impl = ctx.get(MyImplementation)
                impl.configure(config)
                return impl
            return factory

        # Create a FactoryAsImplAdapter with the factory function.
        factory_adapter = FactoryAsImplAdapter(create_instance)

        # Call the adapter to get the factory function.
        factory = factory_adapter(container)
        impl = factory({...}) # result will be an instance of MyImplementation
        ```
    """

    def __init__(self, fn):
        self._fn = fn

    def __call__(self, ctx: Container):
        return self._fn(ctx)
