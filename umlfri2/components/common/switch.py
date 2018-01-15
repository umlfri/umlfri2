from .controlcomponent import ControlComponent
from ..base.helpercomponent import HelperComponent
from umlfri2.ufl.types import UflAnyType


class SwitchCaseComponent(HelperComponent):
    ATTRIBUTES = {
        'value': UflAnyType(),
    }
    
    def __init__(self, children, value):
        super().__init__(children)
        self.__value = value
    
    def get_value(self, context):
        return self.__value(context)
    
    def retype(self, type):
        self._change_attribute_type('value', type)
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            value=self.__value,
        )
        
        self._compile_children(type_context)


class SwitchDefaultComponent(HelperComponent):
    def compile(self, type_context):
        self._compile_children(type_context)


class SwitchComponent(ControlComponent):
    ATTRIBUTES = {
        'value': UflAnyType(),
    }

    SPECIAL_CHILDREN = {
        'Case': SwitchCaseComponent,
        'Default': SwitchDefaultComponent,
    }
    
    ONLY_SPECIAL_CHILDREN = True
    
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
    
    def _get_semantic_children(self):
        for case in self.__cases:
            yield from case._get_semantic_children()
    
    def filter_children(self, context):
        for case in self.__cases:
            if isinstance(case, SwitchDefaultComponent):
                yield from case.get_children(context)
                break
            if self.__value(context) == case.get_value(context):
                yield from case.get_children(context)
                break
