from typing import Optional
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.types.structured.object import UflObjectType


class UflTechnicalVariableNode:
    def __init__(self, name: str, type: Optional[UflObjectType] = ...) -> None: ...
    def accept(self, visitor: UflCompilingVisitor) -> str: ...
    @property
    def name(self) -> str: ...
