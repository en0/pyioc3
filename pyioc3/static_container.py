from collections import deque

from pyioc3.scope_enum import ScopeEnum
from pyioc3.bound_member import BoundMember
from pyioc3.scope_container import PersistentScope, ScopeContainer


class StaticContainer:
    """A static ioc container"""

    def __init__(self, bound_members):
        self._singletons = PersistentScope()
        self._bound_members = bound_members

    def _build_scope(self, requested_member: BoundMember):
        scope = ScopeContainer(self._singletons)
        stack = deque()
        stack.append((requested_member, 0))
        while len(stack) > 0:
            m, s = stack.pop()
            if m.scope != ScopeEnum.TRANSIENT and scope.has(m):
                continue
            elif s == 0:
                stack.append((m, 1))
                [stack.append((v, 0)) for v in m.depends_on]
            else:
                scope.add(m)
        return scope

    def get(self, annotation):
        """Retrieve an instance from the container

        The instance will be produced according to it's scope. If the instance
        is new, it's dependency chain will also be created according to their scope.

        Arguments:
            annotation:
                The hint used to locate the member

        Returns:
            An object instance, constant, or function
        """
        member = self._bound_members[annotation]
        scope = self._build_scope(member)
        return scope.get_instance_of(member)
