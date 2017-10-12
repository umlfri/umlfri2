from .controlcomponent import ControlComponent
from umlfri2.ufl.types import UflIterableType, UflAnyType, UflIntegerType, UflDataWithMetadataType, UflBoolType


class ForEachItemMetadata:
    METADATA = {
        'index': UflIntegerType(),
        'count': UflIntegerType(),
        'is_first': UflBoolType(),
        'is_last': UflBoolType(),
    }
    
    def __init__(self, value, count, index):
        self.__index = index
        self.__count = count
        self.__value = value
    
    @property
    def value(self):
        return self.__value
    
    @property
    def index(self):
        return self.__index
    
    @property
    def count(self):
        return self.__count
    
    @property
    def is_first(self):
        return self.__index == 0
    
    @property
    def is_last(self):
        return self.__index == self.count - 1


class ForEachComponent(ControlComponent):
    ATTRIBUTES = {
        'src': UflIterableType(UflAnyType()),
        'item': str,
    }
    
    def __init__(self, children, src, item):
        super().__init__(children)
        self.__src = src
        self.__item = item
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            src=self.__src,
        )

        item_type = self.__src.get_type().item_type
        
        type_context = type_context.set_variable_type(
            self.__item,
            UflDataWithMetadataType(item_type, **ForEachItemMetadata.METADATA)
        )
        
        self._compile_children(type_context)
    
    def filter_children(self, context):
        items = list(self.__src(context))
        for line, item in enumerate(items):
            local = context.set_variable(self.__item, ForEachItemMetadata(item, len(items), line))
            
            yield from self._get_children(local)
