from ..base import Event


class NodeMovedEvent(Event):
    def __init__(self, node, old_parent, old_index, new_parent, new_index):
        self.__node = node
        self.__old_parent = old_parent
        self.__old_index = old_index
        self.__new_parent = new_parent
        self.__new_index = new_index
    
    @property
    def node(self):
        return self.__node
    
    @property
    def old_parent(self):
        return self.__old_parent
    
    @property
    def old_index(self):
        return self.__old_index
    
    @property
    def new_parent(self):
        return self.__new_parent
    
    @property
    def new_index(self):
        return self.__new_index
    
    def get_opposite(self):
        return NodeMovedEvent(self.__node, self.__new_parent, self.__new_index, self.__old_parent, self.__old_index)
