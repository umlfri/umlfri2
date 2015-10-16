from umlfri2.components.base.context import Context


class ElementType:
    def __init__(self, id, ufl_type, display_name, appearance):
        self.__id = id
        self.__ufl_type = ufl_type
        self.__display_name = display_name
        self.__appearance = appearance
    
    @property
    def id(self):
        return self.__id
    
    @property
    def ufl_type(self):
        return self.__ufl_type
    
    @property
    def display_name(self):
        return self.__display_name
    
    @property
    def appearance(self):
        return self.__appearance
    
    def compile(self):
        self.__appearance.compile({'self': self.__ufl_type})
        self.__display_name.compile({'self': self.__ufl_type})
    
    def draw(self, data, canvas, pos, size=None):
        ctx = Context(data)
        
        if size is None:
            bounds = pos + (None, None)
        else:
            bounds = pos + size
        
        self.appearance.draw(ctx, canvas, bounds)
