class MoveConnectionLabelAction:
    def __init__(self, connection, id):
        self.__connection = connection
        self.__id = id
    
    @property
    def connection(self):
        return self.__connection
    
    @property
    def id(self):
        return self.__id
