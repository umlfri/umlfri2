from .controlcomponent import ControlComponent
from umlfri2.ufl.types import UflBoolType


class Condition(ControlComponent):
    ATTRIBUTES = {
        'condition': UflBoolType,
    }
    
    def __init__(self, children, condition):
        super().__init__(children)
        self.__condition = condition
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            condition=self.__condition,
        )
        
        self._compile_children(variables)
    
    def filter_children(self, context):
        if self.__condition(context):
            yield from self._get_children(context)
