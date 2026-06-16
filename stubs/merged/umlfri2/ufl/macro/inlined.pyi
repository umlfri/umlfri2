from .macro import Macro as Macro

from typing import Optional
from umlfri2.ufl.expressions.compiler.macroargumenttypeprovider import MacroArgumentTypeProvider
from umlfri2.ufl.macro.signature import FoundSignature

class InlinedMacro(Macro):
    @property
    def signature(self) -> None: ...
    def compare_signature(
        self,
        selector: str,
        argument_types: MacroArgumentTypeProvider
    ) -> Optional[FoundSignature]: ...
    def compile(self, visitor, registrar, node) -> None: ...
