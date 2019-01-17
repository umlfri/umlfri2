from .macro import Macro


class InlinedMacro(Macro):
    @property
    def signature(self):
        raise NotImplementedError
    
    def compare_signature(self, selector, argument_types):
        return self.signature.compare(selector, argument_types)
    
    def compile(self, visitor, registrar, node):
        raise NotImplementedError
