from .controlcomponent import ControlComponent
from umlfri2.ufl.types import UflIterableType, UflObjectType, UflAnyType, UflIntegerType


class ForEachComponent(ControlComponent):
    ATTRIBUTES = {
        'src': UflIterableType(UflAnyType()),
        'index': str,
        'item': str,
    }
    
    def __init__(self, children, src, item, index=None):
        super().__init__(children)
        self.__src = src
        self.__item = item
        self.__index = index
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            src=self.__src,
        )

        item_type = self.__src.get_type().item_type
        
        type_context = type_context.set_variable_type(self.__item, item_type)
        
        if self.__index is not None:
            type_context = type_context.set_variable_type(self.__index, UflIntegerType())
        
        self._compile_children(type_context)
    
    def filter_children(self, context):
        for line, item in enumerate(self.__src(context)):
            local = context.set_variable(self.__item, item)
            
            if self.__index is not None:
                local = local.set_variable(self.__index, line)
            
            yield from self._get_children(local)
