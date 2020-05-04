from collections import deque

from .scope_enum import ScopeEnum
from .bound_member import BoundMember
from .scope_container import PersistentScope, ScopeContainer
from .interface import Container


class StaticContainer(Container):

    def __init__(self, bound_members):
        self._singletons = PersistentScope()
        self._bound_members = bound_members

    def _build_scope(self, requested_member: BoundMember):

        # Build a scope using a post-order traversal of the
        # dependency tree.  This will guarantee the scope has
        # all dependencies for each object it is given to build.

        scope = ScopeContainer(self._singletons)
        stack = deque()
        stack.append((requested_member, 0))
        while len(stack) > 0:
            m, s = stack.pop()
            if m.scope != ScopeEnum.TRANSIENT and scope.has(m):
                continue
            elif s == 0:
                stack.append((m, 1))
                [stack.append((v, 0)) for v in m]
            else:
                scope.add(m)
        return scope

    def get(self, annotation):
        member = self._bound_members[annotation]
        scope = self._build_scope(member)
        return scope.get_instance_of(member)
