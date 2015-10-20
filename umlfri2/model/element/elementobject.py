from umlfri2.components.base.context import Context


class ElementObject:
    def __init__(self, type):
        self.__type = type
        self.__data = type.ufl_type.build_default()
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    def get_display_name(self):
        context = Context(self.__data)
        return self.__type.get_display_name(context)
    
    def create_visual_object(self, ruler):
        context = Context(self.__data)
        return self.__type.create_visual_object(context, ruler)
