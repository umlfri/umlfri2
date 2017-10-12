from .controlcomponent import ControlComponent
from ..base.helpercomponent import HelperComponent
from umlfri2.ufl.types import UflAnyType


class SwitchCaseComponent(HelperComponent):
    ATTRIBUTES = {
        'value': UflAnyType(),
    }
    
    CHILDREN_TYPE = 'return' # return back to type from the switch parent
    
    def __init__(self, children, value):
        super().__init__(children)
        self.__value = value
    
    def get_value(self, context):
        return self.__value(context)
    
    def retype(self, type):
        if hasattr(self.__value, 'change_type'):
            self.__value = self.__value.change_type(type)
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            value=self.__value,
        )
        
        self._compile_children(type_context)


class SwitchDefaultComponent(HelperComponent):
    CHILDREN_TYPE = 'return' # return back to type from the switch parent
    
    def compile(self, type_context):
        self._compile_children(type_context)


class SwitchComponent(ControlComponent):
    ATTRIBUTES = {
        'value': UflAnyType(),
    }
    
    CHILDREN_TYPE = 'switch'
    
    def __init__(self, children, value):
        super().__init__(())
        self.__value = value
        self.__cases = children
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            value=self.__value,
        )
        
        for case in self.__cases:
            if isinstance(case, SwitchCaseComponent):
                case.retype(self.__value.get_type())
            case.compile(type_context)
    
    def filter_children(self, context):
        for case in self.__cases:
            if isinstance(case, SwitchDefaultComponent):
                yield from case.get_children(context)
                break
            if self.__value(context) == case.get_value(context):
                yield from case.get_children(context)
                break
