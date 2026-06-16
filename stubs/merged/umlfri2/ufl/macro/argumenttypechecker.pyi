from _typeshed import Incomplete
from typing import NamedTuple

class ArgumentTypeCheckerResult(NamedTuple):
    argument_types: Incomplete
    result_type: Incomplete

class ArgumentTypeChecker:
    def check_arguments(self, self_type, expected_types, return_type) -> None: ...
