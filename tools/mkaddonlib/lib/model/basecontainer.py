from .base import Base


class BaseContainer(Base):
    def __init__(self, name, parent, children=(), sorted=True):
        Base.__init__(self, name, parent)
        
        self.__sorted = sorted
        
        self.__children = dict((child.getName(), child) for child in children)
        self.__ordered_children = list(children)
        if self.__sorted:
            self.__ordered_children.sort(key = lambda x: x.name)
    
    @property
    def children(self):
        for child in self.__ordered_children:
            yield child
    
    @property
    def has_children(self):
        for child in self.__ordered_children:
            return True
        return False
    
    def children_of_type(self, *type_names):
        for child in self.__ordered_children:
            if child.type_name in type_names:
                yield child
    
    def has_children_of_type(self, *type_names):
        for child in self.__ordered_children:
            if child.type_name in type_names:
                return True
        return False
    
    def get_child(self, name):
        return self.__children[name]

    def validate(self):
        Base.validate(self)
        
        for child in self.children:
            child.validate()
    
    def _link(self, builder):
        Base._link(self, builder)
        
        for child in self.children:
            child._link(builder)
    
    def add_child(self, child):
        self.__children[child.name] = child
        self.__ordered_children.append(child)
        if self.__sorted:
            self.__ordered_children.sort(key = lambda x: x.name)
