from collections import deque
from typing import Set, Dict

from .bound_member import BoundMember
from .interface import CycleTest


class QueuedCycleTest(CycleTest):
    def has_cycle(self, bound_members: Dict[any, BoundMember]) -> bool:
        """Check if a graph of bound members contains a cycle.

        Arguments:
        bound_members: A dict of BoundMembers.
        """
        for r in bound_members.values():
            cycle = _find_cycle(r)
            if cycle is not None:
                return True
        return False

    def _find_cycle(self, root: BoundMember) -> Set[BoundMember]:
        """Find a set of bound members that contain circular dependencies.

        Arguments:
        root: The bound member to begin the cycle test.
        """
        visited = set()
        stack = deque()
        stack.append((root, 0))
        while len(stack):
            v, s = stack.pop()
            if s == 0 and v in visited:
                return visited
            elif s == 0:
                visited.add(v)
                stack.append((v, 1))
                [stack.append((v, 0)) for v in v.depends_on]
            elif s == 1:
                visited.remove(v)
        return None
