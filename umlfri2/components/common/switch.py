from .controlcomponent import ControlComponent
from ..base.helpercomponent import HelperComponent
from umlfri2.ufl.types import UflAnyType


class CaseComponent(HelperComponent):
    CHILDREN_TYPE = 'return' # return back to type from the switch parent
    
    def __init__(self, children, value):
        super().__init__(children)
        self.__value = value
    
    def get_value(self, context):
        return self.__value(context)
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            value=self.__value,
        )
        
        self._compile_children(variables)


class SwitchComponent(ControlComponent):
    ATTRIBUTES = {
        'value': UflAnyType(),
    }
    
    CHILDREN_TYPE = 'switch'
    
    def __init__(self, children, value):
        super().__init__(())
        self.__value = value
        self.__cases = children
        
        if any(not isinstance(case, CaseComponent) for case in self.__cases):
            raise Exception("Switch can contain only case elements")
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            value=self.__value,
        )
        
        self._compile_children(variables)
    
    def filter_children(self, context):
        for case in self.__cases:
            if self.__value(context) == case.get_value(context):
                yield from case.get_children(context)
