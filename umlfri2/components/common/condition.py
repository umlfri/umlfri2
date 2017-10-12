from .controlcomponent import ControlComponent
from umlfri2.ufl.types import UflBoolType


class ConditionComponent(ControlComponent):
    ATTRIBUTES = {
        'condition': UflBoolType(),
    }
    
    def __init__(self, children, condition):
        super().__init__(children)
        self.__condition = condition
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            condition=self.__condition,
        )
        
        self._compile_children(type_context)
    
    def filter_children(self, context):
        if self.__condition(context):
            yield from self._get_children(context)
