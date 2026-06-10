from ...macro.argumenttypechecker import ArgumentTypeChecker as ArgumentTypeChecker, ArgumentTypeCheckerResult as ArgumentTypeCheckerResult
from ...types.executable import UflLambdaType as UflLambdaType
from ...types.structured import UflVariableWithMetadataType as UflVariableWithMetadataType
from ..tree import UflLambdaExpressionNode as UflLambdaExpressionNode, UflUnpackNode as UflUnpackNode
from _typeshed import Incomplete
from collections.abc import Generator

class MacroArgumentTypeProvider(ArgumentTypeChecker):
    def __init__(self, target_type, expressions, typing_visitor) -> None: ...
    def check_arguments(self, self_type, expected_types, return_type): ...
    def resolve_for(self, found_signature) -> Generator[Incomplete, Incomplete]: ...
