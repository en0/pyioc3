class PyIOC3Error(RuntimeError):
    ...

class CircularDependencyError(PyIOC3Error):
    pass

class ScopeError(PyIOC3Error):
    pass

class AutoWireError(PyIOC3Error):
    pass
