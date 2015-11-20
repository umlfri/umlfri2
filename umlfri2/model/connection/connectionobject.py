from weakref import ref
from umlfri2.components.base.context import Context
from umlfri2.model.cache import ModelTemporaryDataCache
from umlfri2.ufl.dialog import UflDialog


class ConnectionObject:
    def __init__(self, type, source, destination):
        self.__type = type
        self.__data = type.ufl_type.build_default(None)
        self.__source = ref(source)
        self.__destination = ref(destination)
        self.__cache = ModelTemporaryDataCache(None)
    
    @property
    def cache(self):
        return self.__cache
    
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
        context = Context().extend(self.__data, 'self')
        return self.__type.create_appearance_object(context, ruler)
    
    def create_label_object(self, id, ruler):
        context = Context().extend(self.__data, 'self')
        return self.__type.get_label(id).create_appearance_object(context, ruler)
    
    def apply_ufl_patch(self, patch):
        self.__data.apply_patch(patch)
        self.__cache.refresh()
    
    def create_ufl_dialog(self):
        dialog = UflDialog(self.type.ufl_type)
        dialog.associate(self.data)
        return dialog
