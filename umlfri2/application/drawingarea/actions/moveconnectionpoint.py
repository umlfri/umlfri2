class MoveConnectionPointAction:
    def __init__(self, connection, index):
        self.__connection = connection
        self.__index = index
    
    @property
    def connection(self):
        return self.__connection
    
    @property
    def index(self):
        return self.__index
