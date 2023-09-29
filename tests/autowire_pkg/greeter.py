from typing import NamedTuple
from pyioc3.autowire import bind
from .interface import GreeterInterface, FormatterFactory, FormatterInterface


class GreeterOpts(NamedTuple):
    default_name: str


@bind(GreeterInterface)
class Greeter(GreeterInterface):
    def __init__(
        self,
        formatter_factory: FormatterFactory,
        opts: GreeterOpts,
    ) -> None:
        self._formatter: FormatterInterface = formatter_factory("en_US")
        self._formatter_factory = formatter_factory
        self._default = opts.default_name

    def set_language(self, lang: str):
        self._formatter = self._formatter_factory(lang)

    def greet(self, name: str = None) -> str:
        message = self._formatter.format(name or self._default)
        return message
