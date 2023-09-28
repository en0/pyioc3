from typing import TypeAlias, Callable
from abc import ABC, abstractmethod


class GreeterInterface(ABC):

    @abstractmethod
    def greet(self, name: str = None) -> str:
        ...

    @abstractmethod
    def set_language(self, lang: str) -> None:
        ...


class FormatterInterface(ABC):

    @abstractmethod
    def format(self, name: str) -> str:
        ...


FormatterFactory: TypeAlias = Callable[[str], FormatterInterface]

