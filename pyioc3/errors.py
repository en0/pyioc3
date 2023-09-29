class PyIOC3Error(RuntimeError):
    """Base class for all custom PyIOC3 exceptions."""

    pass


class CircularDependencyError(PyIOC3Error):
    """Raised if the dependency tree contains cycles."""

    pass


class ScopeError(PyIOC3Error):
    """Raised if a string-based scope is not valid."""

    pass


class AutoWireError(PyIOC3Error):
    """Raised if the autowire api detects duplicate annotations."""

    pass


class MemberNotBoundError(PyIOC3Error):
    """Raised if a member is requested but not bound."""

    pass


class _MemberNotBoundErrorAsKeyError(KeyError, MemberNotBoundError):
    """Raised if a member is requested by not bound.

    DO NOT CATCH THIS EXCEPTION!
    Please use pyioc3.errors.MemberNotBoundError.

    This exception exists to support backwards compatability with 1.5 and prior.
    """

    pass
