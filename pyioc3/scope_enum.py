from enum import Enum


class ScopeEnum(Enum):
    TRANSIENT = 1
    REQUESTED = 2
    SINGLETON = 3
