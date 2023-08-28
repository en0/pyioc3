from inspect import isclass
from types import FunctionType, MethodType
from typing import get_type_hints, Callable, Type, Union

from .bound_member import BoundMember
from .scope_enum import ScopeEnum
from .adapters import ValueAsImplAdapter, FactoryAsImplAdapter
from .interface import PROVIDER_T, Binding, FactoryBinding, ConstantBinding, ProviderBinding
from .errors import PyIOC3Error


class BoundMemberFactory:

    @staticmethod
    def build(binding: Binding) -> BoundMember:
        if isinstance(binding, ProviderBinding):
            return BoundMemberFactory._build(
                annotation=binding.annotation,
                implementation=binding.implementation or binding.annotation,
                scope=binding.scope or ScopeEnum.TRANSIENT,
                on_activate=binding.on_activate
            )

        elif isinstance(binding, ConstantBinding):
            return BoundMemberFactory._build(
                annotation=binding.annotation,
                implementation=ValueAsImplAdapter(binding.value),
                scope=ScopeEnum.SINGLETON,
                on_activate=None
            )

        elif isinstance(binding, FactoryBinding):
            return BoundMemberFactory._build(
                annotation=binding.annotation,
                implementation=FactoryAsImplAdapter(binding.factory),
                scope=ScopeEnum.SINGLETON,
                on_activate=None
            )
        else:
            raise PyIOC3Error("Unable to create bound member.")

    @staticmethod
    def _build(
        annotation: Type[PROVIDER_T],
        implementation: Type[PROVIDER_T],
        scope: Union[str, ScopeEnum],
        on_activate: Callable[[PROVIDER_T], PROVIDER_T] = None,
    ) -> BoundMember:
        if isclass(implementation):
            params = get_type_hints(implementation.__init__)
        elif type(implementation) == FunctionType:
            params = get_type_hints(implementation)
        elif type(implementation) == MethodType:
            params = get_type_hints(implementation)
        elif hasattr(implementation, '__call__'):
            params = get_type_hints(implementation.__call__)
        else:
            params = get_type_hints(implementation)

        return BoundMember(
            annotation=annotation,
            implementation=implementation,
            scope=ScopeEnum.from_string(scope) if isinstance(scope, str) else scope,
            parameters=[p for k, p in params.items() if k != 'return'],
            on_activate=on_activate
        )
