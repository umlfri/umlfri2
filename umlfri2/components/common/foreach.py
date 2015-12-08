from .controlcomponent import ControlComponent
from umlfri2.ufl.types import UflListType, UflObjectType, UflAnyType, UflIntegerType


class ForEachComponent(ControlComponent):
    ATTRIBUTES = {
        'src': UflListType(UflAnyType()),
        'index': str,
        'item': str,
    }
    
    def __init__(self, children, src, index=None, item=None):
        super().__init__(children)
        self.__src = src
        self.__index = index
        self.__item = item
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            src=self.__src,
        )
        
        item_type = self.__src.get_type().item_type
        
        variables = variables.copy()
        if self.__item is not None:
            variables[self.__item] = item_type
        elif isinstance(item_type, UflObjectType):
            variables.update({attr.name: attr.type for attr in item_type.attributes})
        else:
            raise Exception("You have to specify item name or use list of objects")
        
        if self.__index is not None:
            variables[self.__index] = UflIntegerType()
        
        self._compile_children(variables)
    
    def filter_children(self, context):
        for line, item in enumerate(self.__src(context)):
            if self.__item is None:
                local = context.extend(item)
            else:
                local = context.extend(item, self.__item)
            
            if self.__index is not None:
                local = local.extend(line, self.__index)
            
            yield from self._get_children(local)
