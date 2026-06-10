from typing import Optional
from umlfri2.ufl.expressions.compiler.macroargumenttypeprovider import MacroArgumentTypeProvider
from umlfri2.ufl.macro.signature import FoundSignature


class InlinedMacro:
    def compare_signature(
        self,
        selector: str,
        argument_types: MacroArgumentTypeProvider
    ) -> Optional[FoundSignature]: ...
