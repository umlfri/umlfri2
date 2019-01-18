from .changefontstyle import ChangeFontStyleMacro
from .invertcolor import InvertColorMacro
from .stringempty import StringEmptyMacro
from .stringhastext import StringHasTextMacro

STANDARD_OTHER_MACROS = (
    StringEmptyMacro(),
    StringHasTextMacro(),
    ChangeFontStyleMacro(),
    InvertColorMacro(),
)
