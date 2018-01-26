from .macro import Macro


class InlinedMacro(Macro):
    def compile(self, visitor, registrar, node):
        raise NotImplementedError
