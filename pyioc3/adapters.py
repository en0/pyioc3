from pyioc3.static_container import StaticContainer


class ValueAsImplAdapter:

    def __init__(self, value):
        self._value = value

    def __call__(self):
        return self._value


class FunctionAsImplAdapter:

    def __init__(self, fn, *args):
        self._args = args
        self._fn = fn

    def __call__(self):
        args = self._args
        return self._fn(*args)


class FactoryAsImplAdapter:

    def __init__(self, fn):
        self._fn = fn

    def __call__(self, ctx: StaticContainer):
        return self._fn(ctx)

