from uuid import uuid4
from weakref import ref
from umlfri2.components.base.context import Context
from umlfri2.ufl.dialog import UflDialog
from ..cache import ModelTemporaryDataCache
from ..connection.connectionobject import ConnectionObject
from umlfri2.ufl.types.uniquevaluegenerator import UniqueValueGenerator


class ElementValueGenerator(UniqueValueGenerator):
    def __init__(self, parent, type):
        self.__parent = parent
        self.__type = type
        self.__name = None
    
    def get_parent_name(self):
        return self.__parent.get_display_name()
    
    def for_name(self, name):
        ret = ElementValueGenerator(self.__parent, self.__type)
        ret.__name = name
        return ret
    
    def has_value(self, value):
        if self.__name is None:
            return None
        
        for child in self.__parent.children:
            if child.type == self.__type and child.data.get_value(self.__name) == value:
                return True
        
        return False


class ElementObject:
    def __init__(self, parent, type, save_id=None):
        self.__parent = ref(parent)
        self.__type = type
        self.__data = type.ufl_type.build_default(ElementValueGenerator(parent, type))
        self.__connections = []
        self.__children = []
        self.__diagrams = []
        self.__cache = ModelTemporaryDataCache(None)
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    @property
    def cache(self):
        return self.__cache
    
    @property
    def parent(self):
        return self.__parent()
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    @property
    def connections(self):
        yield from self.__connections
    
    def get_display_name(self):
        context = Context().extend(self.__data, 'self')
        return self.__type.get_display_name(context)
    
    def create_appearance_object(self, ruler):
        context = Context().extend(self.__data, 'self')
        return self.__type.create_appearance_object(context, ruler)
    
    def connect_with(self, connection_type, second_element, save_id=None):
        connection = ConnectionObject(connection_type, self, second_element, save_id)
        self.__connections.append(connection)
        second_element.__connections.append(connection)
        return connection
    
    @property
    def project(self):
        if isinstance(self.__parent(), ElementObject):
            return self.__parent().project
        else:
            return self.__parent()
    
    @property
    def children(self):
        yield from self.__children
    
    @property
    def diagrams(self):
        yield from self.__diagrams
    
    @property
    def save_id(self):
        return self.__save_id
    
    def create_child_element(self, type, save_id=None):
        obj = ElementObject(self, type, save_id)
        self.__children.append(obj)
        return obj
    
    def create_child_diagram(self, type, save_id=None):
        from ..diagram import Diagram # circular imports
        
        diagram = Diagram(self, type, save_id)
        self.__diagrams.append(diagram)
        return diagram
    
    def apply_ufl_patch(self, patch):
        self.__data.apply_patch(patch)
        self.__cache.refresh()
    
    def create_ufl_dialog(self):
        dialog = UflDialog(self.type.ufl_type)
        dialog.associate(self.data)
        return dialog
