from .default import DefaultMacro, DefaultWithValueMacro
from .iterate import IterateMacro

STANDARD_NULLABLE_MACROS = (
    # DefaultMacro(), TODO
    DefaultWithValueMacro(),
    IterateMacro(),
)
