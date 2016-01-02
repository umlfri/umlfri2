from uuid import uuid4
from weakref import ref, WeakSet
from umlfri2.ufl.dialog import UflDialog, UflDialogOptions
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
        self.__visuals = WeakSet()
        self.__cache = ModelTemporaryDataCache(None)
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    def add_visual(self, visual):
        if visual.object is not self:
            raise Exception
        self.__visuals.add(visual)
    
    def remove_visual(self, visual):
        self.__visuals.remove(visual)
    
    @property
    def visuals(self):
        yield from self.__visuals
    
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
        return self.__type.get_display_name(self)
    
    def create_appearance_object(self, ruler):
        return self.__type.create_appearance_object(self, ruler)
    
    def connect_with(self, connection_type, second_element, save_id=None):
        connection = ConnectionObject(connection_type, self, second_element, save_id)
        self.__connections.append(connection)
        second_element.__connections.append(connection)
        return connection
    
    def add_connection(self, connection):
        if not connection.is_connected_with(self):
            raise Exception
        
        if connection in self.__connections:
            raise Exception
        
        self.__connections.append(connection)
    
    def remove_connection(self, connection):
        if not connection.is_connected_with(self):
            raise Exception
        
        if connection not in self.__connections:
            raise Exception
        
        self.__connections.remove(connection)
    
    def reconnect(self, connection):
        if connection in self.__connections:
            raise Exception
        if not connection.is_connected_with(self):
            raise Exception
        self.__connections.append(connection)
        connection.get_other_end(self).__connections.append(connection)
    
    def disconnect(self, connection):
        if connection not in self.__connections:
            raise Exception
        self.__connections.remove(connection)
        connection.get_other_end(self).__connections.remove(connection)
    
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
    
    def get_child_index(self, obj):
        if isinstance(obj, ElementObject):
            return self.__children.index(obj)
        else:
            return self.__diagrams.index(obj)
    
    def add_child(self, obj, index=None):
        if obj.parent is not self:
            raise Exception
        if isinstance(obj, ElementObject):
            if obj in self.__children:
                raise Exception
            if index is None:
                self.__children.append(obj)
            else:
                self.__children.insert(index, obj)
        else:
            if obj in self.__diagrams:
                raise Exception
            if index is None:
                self.__diagrams.append(obj)
            else:
                self.__diagrams.insert(index, obj)
    
    def remove_child(self, obj):
        if obj.parent is not self:
            raise Exception
        if isinstance(obj, ElementObject):
            if obj not in self.__children:
                raise Exception
            self.__children.remove(obj)
        else:
            if obj not in self.__diagrams:
                raise Exception
            self.__diagrams.remove(obj)
    
    def apply_ufl_patch(self, patch):
        self.__data.apply_patch(patch)
        self.__cache.refresh()
    
    @property
    def has_ufl_dialog(self):
        return self.__type.ufl_type.has_attributes
    
    def create_ufl_dialog(self, language, options=UflDialogOptions.standard):
        if not self.__type.ufl_type.has_attributes:
            raise Exception
        translation = self.__type.metamodel.addon.get_translation(language)
        dialog = UflDialog(self.__type.ufl_type, translation, options)
        dialog.associate(self.__data)
        return dialog
