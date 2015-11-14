class AddVisualAction:
    def __init__(self, category, type):
        self.__category = category
        self.__type = type
    
    @property
    def category(self):
        return self.__category
    
    @property
    def type(self):
        return self.__type
