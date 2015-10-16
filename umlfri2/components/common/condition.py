from .controlcomponent import ControlComponent
from umlfri2.ufl.types import UflBoolType


class Condition(ControlComponent):
    ATTRIBUTES = {
        'condition': UflBoolType,
    }
    
    def __init__(self, children, condition):
        super().__init__(children)
        self.__condition = condition
    
    def filter_children(self, context):
        if self.__condition(context):
            yield from self._get_children(context)
