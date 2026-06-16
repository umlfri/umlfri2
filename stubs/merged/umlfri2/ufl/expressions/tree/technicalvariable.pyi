from .node import UflNode as UflNode

from typing import Optional
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.types.structured.object import UflObjectType

class UflTechnicalVariableNode(UflNode):
    def __init__(self, name: str, type: Optional[UflObjectType] = ...) -> None: ...
    @property
    def name(self) -> str: ...
    def accept(self, visitor: UflCompilingVisitor) -> str: ...
