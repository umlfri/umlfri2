class ApiEventBound:
    def __init__(self, name, documentation, instance, connector, disconnector):
        self.__name__ = name
        self.__doc__ = documentation
        self.__instance = instance
        self.__connector = connector
        self.__disconnector = disconnector
    
    def connect(self, handler):
        """
        Connects handler to the event. 
        """
        self.__connector(self.__instance, handler)
    
    def disconnect(self, handler):
        """
        Disconnects handler from the event 
        """
        self.__disconnector(self.__instance, handler)


class ApiEvent:
    def __init__(self, name, documentation):
        self.__name__ = name
        self.__doc__ = documentation
        self.__connector = None
        self.__disconnector = None
    
    def connector(self, function):
        self.__connector = function
        return self
    
    def disconnector(self, function):
        self.__disconnector = function
        return self
    
    def __get__(self, instance, owner):
        return ApiEventBound(self.__name__, self.__doc__, instance, self.__connector, self.__disconnector)
