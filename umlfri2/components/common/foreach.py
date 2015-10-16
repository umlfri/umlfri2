from .controlcomponent import ControlComponent
from umlfri2.ufl.types import UflListType


class ForEach(ControlComponent):
    ATTRIBUTES = {
        'src': UflListType,
        'index': str,
        'item': str,
    }
    
    def __init__(self, children, src, index=None, item=None):
        super().__init__(children)
        self.__src = src
        self.__index = index
        self.__item = item
    
    def filter_children(self, context):
        for line, item in enumerate(self.__src(context)):
            if self.__item is None:
                local = context.extend(item)
            else:
                local = context.extend(item, self.__item)
            
            if self.__index is not None:
                local = local.extend(line, self.__index)
            
            yield from self._get_children(local)
