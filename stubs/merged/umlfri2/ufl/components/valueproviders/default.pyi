from .compilationerror import ValueCompilationError as ValueCompilationError
from .valueprovider import ValueProvider as ValueProvider
from umlfri2.types.color import Color as Color
from umlfri2.types.enums import ALL_ENUMS as ALL_ENUMS
from umlfri2.types.font import Font as Font
from umlfri2.types.proportion import Proportion as Proportion
from umlfri2.ufl.types.basic import UflIntegerType as UflIntegerType, UflStringType as UflStringType
from umlfri2.ufl.types.complex import UflColorType as UflColorType, UflFontType as UflFontType, UflProportionType as UflProportionType
from umlfri2.ufl.types.enum import UflTypedEnumType as UflTypedEnumType
from umlfri2.ufl.types.structured import UflNullableType as UflNullableType

class DefaultValueProvider(ValueProvider):
    def __init__(self, value) -> None: ...
    def compile(self, type_context, expected_type) -> None: ...
    def get_source(self) -> None: ...
    def get_type(self): ...
    def __call__(self, context): ...
