from umlfri2.model import ElementObject


class Project:
    def __init__(self, metamodel, name=None):
        if name is None:
            self.__name = "Project"
        else:
            self.__name = name
        self.__metamodel = metamodel
        self.__children = []
    
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
    
    def create_child_element(self, type, save_id=None):
        obj = ElementObject(self, type, save_id)
        self.__children.append(obj)
        return obj
