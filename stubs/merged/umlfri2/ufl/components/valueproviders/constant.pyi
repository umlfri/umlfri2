from .compilationerror import ValueCompilationError as ValueCompilationError
from .valueprovider import ValueProvider as ValueProvider
from typing import (
    Any,
    Optional,
)
from umlfri2.ufl.components.valueproviders.valuesourceposition import ValueSourcePosition
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.types.base.type import UflType

class ConstantValueProvider(ValueProvider):
    def __init__(
        self,
        value: Any,
        source: Optional[ValueSourcePosition] = ...
    ) -> None: ...
    def compile(
        self,
        type_context: TypeContext,
        expected_type: UflType
    ) -> None: ...
    def get_type(self): ...
    def get_source(self): ...
    def __call__(self, context: Context) -> Any: ...
