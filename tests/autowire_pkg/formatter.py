from pyioc3.autowire import bind, bind_factory
from .interface import FormatterFactory, FormatterInterface


@bind()
class Formatter_EN_US(FormatterInterface):
    def format(self, name):
        return f"Hello, {name}!"


@bind()
class Formatter_ES_MX(FormatterInterface):
    def format(self, name):
        if name == "World":
            name = "Mundo"
        return f"Hola, {name}!"


@bind_factory(FormatterFactory)
def fomatter_factory(ctx) -> Formatter_EN_US:
    formatters = {
        "en_US": Formatter_EN_US,
        "es_MX": Formatter_ES_MX,
    }

    def factory(lang: str) -> FormatterInterface:
        t = formatters.get(lang, Formatter_EN_US)
        return ctx.get(t)

    return factory
