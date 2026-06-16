from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.ufl.components.all import ALL_COMPONENTS as ALL_COMPONENTS
from umlfri2.ufl.components.valueproviders import ConstantValueProvider as ConstantValueProvider, DynamicValueProvider as DynamicValueProvider, ValueSourcePosition as ValueSourcePosition

class ChildAttribute(NamedTuple):
    name: Incomplete
    type: Incomplete
    values: Incomplete

class ComponentLoader:
    def __init__(self, xmlroot, type, file_name) -> None: ...
    def load(self): ...
