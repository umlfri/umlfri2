from weakref import ref
from umlfri2.components.base.context import Context
from .connection import ConnectionObject, ConnectionVisual
from .element import ElementObject, ElementVisual


class Diagram:
    def __init__(self, parent, type):
        self.__parent = ref(parent)
        self.__type = type
        self.__data = type.ufl_type.build_default()
        self.__elements = []
        self.__connections = []
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    def get_display_name(self):
        context = Context(self.__data)
        return self.__type.get_display_name(context)
    
    def show(self, object):
        if isinstance(object, ElementObject):
            visual = ElementVisual(object)
            self.__elements.append(visual)
            return visual
        elif isinstance(object, ConnectionObject):
            element1 = None
            element2 = None
            for element in self.__elements:
                if element.object is object.source:
                    element1 = element
                elif element.object is object.destination:
                    element2 = element
            
            if element1 is not None and element2 is not None:
                visual = ConnectionVisual(object, element1, element2)
                self.__connections.append(visual)
                return visual
    
    def draw(self, canvas):
        context = Context(self.__data)
        canvas.clear(self.__type.get_background_color(context))
        
        for element in self.__elements:
            element.draw(canvas)
        
        for connection in self.__connections:
            connection.draw(canvas)
    
    def get_object_at(self, ruler, position):
        for connection in reversed(self.__connections):
            if connection.is_at_position(ruler, position):
                return connection
        
        for element in reversed(self.__elements):
            if element.is_at_position(ruler, position):
                return element
        
        return None
