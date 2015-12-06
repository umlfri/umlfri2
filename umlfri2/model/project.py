from uuid import uuid4

from umlfri2.model import ElementObject


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
    def children(self):
        yield from self.__children
    
    @property
    def save_id(self):
        return self.__save_id
    
    def create_child_element(self, type, save_id=None):
        obj = ElementObject(self, type, save_id)
        self.__children.append(obj)
        return obj
    
    def add(self, obj):
        if obj.parent is not self:
            raise Exception
        if obj in self.__children:
            raise Exception
        self.__children.append(obj)
    
    def remove(self, obj):
        if obj.parent is not self:
            raise Exception
        if obj not in self.__children:
            raise Exception
        self.__children.remove(obj)
