from collections import deque
from typing import Set, Dict, List

from .bound_member import BoundMember


class QueuedCycleTest:
    @staticmethod
    def find_cycle(bound_members: Dict[any, BoundMember]) -> List[BoundMember]:
        """Check if a graph of bound members contains a cycle.

        Arguments:
        bound_members: A dict of BoundMembers.
        """
        for r in bound_members.values():
            cycle = QueuedCycleTest._find_cycle(r)
            if cycle is not None:
                return cycle
        return []

    @staticmethod
    def _find_cycle(root: BoundMember) -> Set[BoundMember]:
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
                [stack.append((d, 0)) for d in v]
            elif s == 1:
                visited.remove(v)
        return None
