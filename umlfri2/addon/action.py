class AddOnAction:
    def __init__(self, id, icon, label):
        self.__id = id
        self.__icon = icon
        self.__label = label
        self.__enabled = True
    
    @property
    def id(self):
        return self.__id
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def label(self):
        return self.__label
    
    @property
    def enabled(self):
        return self.__enabled
    
    @enabled.setter
    def enabled(self, value):
        self.__enabled = value
