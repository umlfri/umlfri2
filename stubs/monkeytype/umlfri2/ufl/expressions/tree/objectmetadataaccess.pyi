from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.image import UflImageType
from umlfri2.ufl.types.structured.iterable import UflIterableType


class UflObjectMetadataAccessNode:
    def __init__(
        self,
        obj: UflVariableNode,
        metadata_name: str,
        type: Optional[Union[UflStringType, UflImageType, UflIterableType]] = ...
    ) -> None: ...
    def _get_params(self) -> Tuple[UflVariableNode]: ...
    def accept(
        self,
        visitor: Union[UflCompilingVisitor, UflTypingVisitor]
    ) -> Union[UflObjectMetadataAccessNode, str]: ...
    @property
    def metadata_name(self) -> str: ...
    @property
    def object(self) -> UflVariableNode: ...
