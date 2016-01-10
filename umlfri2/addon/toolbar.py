from uuid import uuid4


class ToolBar:
    def __init__(self, label, actions):
        self.__label = label
        self.__actions = tuple(actions)
        self.__id = uuid4() # random ID for now
    
    @property
    def id(self):
        return self.__id
    
    @property
    def label(self):
        return self.__label
    
    @property
    def actions(self):
        yield from self.__actions
