from .all import AllMacro
from .any import AnyMacro, AnyContainsValueMacro, AnyNotEmptyMacro
from .empty import EmptyMacro
from .join import JoinMacro
from .length import LengthMacro
from .select import SelectMacro
from .oftype import OfTypeMacro
from .orderby import OrderByMacro, OrderByOrderMacro
from .reduce import ReduceMacro, ReduceSimpleMacro
from .reverse import ReverseMacro
from .where import WhereMacro

STANDARD_ITERATOR_MACROS = (
    AllMacro(),
    AnyMacro(),
    AnyContainsValueMacro(),
    AnyNotEmptyMacro(),
    EmptyMacro(),
    JoinMacro(),
    LengthMacro(),
    # OfTypeMacro(), TODO
    OrderByMacro(),
    OrderByOrderMacro(),
    ReduceMacro(),
    ReduceSimpleMacro(),
    ReverseMacro(),
    SelectMacro(),
    WhereMacro(),
)
