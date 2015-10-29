from weakref import ref
from umlfri2.components.base.context import Context


class ConnectionObject:
    def __init__(self, type, source, destination):
        self.__type = type
        self.__data = type.ufl_type.build_default()
        self.__source = ref(source)
        self.__destination = ref(destination)
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    @property
    def source(self):
        return self.__source()
    
    @property
    def destination(self):
        return self.__destination()
    
    def create_appearance_object(self, ruler):
        context = Context(self.__data)
        return self.__type.create_appearance_object(context, ruler)
    
    def create_label_objects(self, ruler):
        context = Context(self.__data)
        for label in self.__type.labels:
            yield label.id, label.create_visual_object(context, ruler)
