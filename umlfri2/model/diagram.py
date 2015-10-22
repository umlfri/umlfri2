from umlfri2.components.base.context import Context
from umlfri2.model.element import ElementObject, ElementVisual


class Diagram:
    def __init__(self, type):
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
    
    def draw(self, canvas):
        context = Context(self.__data)
        canvas.clear(self.__type.get_background_color(context))
        for element in self.__elements:
            element.draw(canvas)
    
    def get_element_at(self, pos):
        for element in reversed(self.__elements):
            x, y = element.position
            w, h = element.size
            
            if x <= pos[0] <= x + w and y <= pos[1] <= y + h:
                return element
        
        return None
