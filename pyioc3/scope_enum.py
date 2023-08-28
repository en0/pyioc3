from enum import Enum
from .errors import ScopeError


class ScopeEnum(Enum):
    TRANSIENT = 1
    REQUESTED = 2
    SINGLETON = 3

    @staticmethod
    def from_string(val: str) -> "ScopeEnum":
        try:
            return {
                "TRANSIENT": ScopeEnum.TRANSIENT,
                "REQUESTED": ScopeEnum.REQUESTED,
                "SINGLETON": ScopeEnum.SINGLETON,
                "transient": ScopeEnum.TRANSIENT,
                "requested": ScopeEnum.REQUESTED,
                "singleton": ScopeEnum.SINGLETON,
                "t": ScopeEnum.TRANSIENT,
                "r": ScopeEnum.REQUESTED,
                "s": ScopeEnum.SINGLETON,
                "T": ScopeEnum.TRANSIENT,
                "R": ScopeEnum.REQUESTED,
                "S": ScopeEnum.SINGLETON,
            }[val]

        except KeyError as ex:
            raise ScopeError(f'Unknown scope "{val}"') from ex
