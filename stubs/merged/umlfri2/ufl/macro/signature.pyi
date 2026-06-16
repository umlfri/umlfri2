from _typeshed import Incomplete
from typing import NamedTuple

class FoundSignature(NamedTuple):
    self_type: Incomplete
    parameter_types: Incomplete
    return_type: Incomplete
    true_argument_types: Incomplete
    true_result_type: Incomplete

class MacroSignature:
    def __init__(self, identifier, self_type, parameter_types, return_type) -> None: ...
    def compare(self, selector, argument_type_checker): ...
