from uuid import uuid4

from umlfri2.model import ElementObject
from umlfri2.ufl.dialog import UflDialog


class Project:
    def __init__(self, metamodel, name=None, save_id=None):
        if name is None:
            self.__name = "Project"
        else:
            self.__name = name
        self.__metamodel = metamodel
        self.__children = []
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
        
        self.__config = metamodel.config_structure.build_default(None)

    @property
    def parent(self):
        return None
    
    def get_display_name(self):
        return self.__name
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name
    
    @property
    def metamodel(self):
        return self.__metamodel
    
    @property
    def children_count(self):
        return len(self.__children)
    
    @property
    def children(self):
        yield from self.__children
    
    @property
    def save_id(self):
        return self.__save_id
    
    def create_child_element(self, type, save_id=None):
        obj = ElementObject(self, type, save_id)
        self.__children.append(obj)
        return obj
    
    def get_child_index(self, obj):
        return self.__children.index(obj)
    
    def add_child(self, obj, index=None):
        if obj.parent is not self:
            raise Exception
        if obj in self.__children:
            raise Exception
        
        if index is None:
            self.__children.append(obj)
        else:
            self.__children.insert(index, obj)
    
    def remove_child(self, obj):
        if obj.parent is not self:
            raise Exception
        if obj not in self.__children:
            raise Exception
        self.__children.remove(obj)
    
    def get_all_elements(self):
        def recursion(obj):
            for child in obj.children:
                yield child
                yield from recursion(child)
        
        return recursion(self)
    
    def invalidate_all_caches(self):
        for element in self.__children:
            element.invalidate_all_caches()
    
    @property
    def config(self):
        return self.__config
    
    def apply_config_patch(self, patch):
        if not self.__metamodel.has_config:
            raise Exception
        self.__config.apply_patch(patch)
    
    def create_config_dialog(self):
        if not self.__metamodel.has_config:
            raise Exception
        dialog = UflDialog(self.__metamodel.config_structure)
        dialog.associate(self.__config)
        return dialog
