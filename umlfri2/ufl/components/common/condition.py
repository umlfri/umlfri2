from .controlcomponent import ControlComponent
from ..base.helpercomponent import HelperComponent
from umlfri2.ufl.types import UflBoolType


class ThenComponent(HelperComponent):
    def compile(self, type_context):
        self._compile_children(type_context)


class ElseComponent(HelperComponent):
    def compile(self, type_context):
        self._compile_children(type_context)


class ConditionComponent(ControlComponent):
    ATTRIBUTES = {
        'condition': UflBoolType(),
    }
    
    SPECIAL_CHILDREN = {
        'Then': ThenComponent,
        'Else': ElseComponent,
    }
    
    def __init__(self, children, condition):
        self.__condition = condition
        
        self.__then_component = None
        self.__else_component = None
        has_other_components = False
        
        for child in children:
            if isinstance(child, ThenComponent):
                if self.__then_component is not None:
                    raise Exception("Invalid If - more then one Then child")
                self.__then_component = child
            elif isinstance(child, ElseComponent):
                if self.__else_component is not None:
                    raise Exception("Invalid If - more then one Then child")
                self.__else_component = child
            else:
                has_other_components = True
        
        if has_other_components:
            if self.__then_component is not None or self.__else_component is not None:
                raise Exception("Invalid If children combination")
            self.__then_component = ThenComponent(children)
        
        if self.__then_component is None:
            self.__then_component = ThenComponent(())
        if self.__else_component is None:
            self.__else_component = ElseComponent(())
        
        super().__init__((self.__then_component, self.__else_component))
    
    def _get_semantic_children(self):
        if self.__then_component:
            yield from self.__then_component._get_semantic_children()
        if self.__else_component:
            yield from self.__then_component._get_semantic_children()
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            condition=self.__condition,
        )
        
        self.__then_component.compile(type_context)
        self.__else_component.compile(type_context)
    
    def filter_children(self, context):
        if self.__condition(context):
            yield from self.__then_component.get_children(context)
        else:
            yield from self.__else_component.get_children(context)
