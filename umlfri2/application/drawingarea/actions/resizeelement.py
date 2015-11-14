class ResizeElementAction:
    def __init__(self, element, horizontal, vertical):
        self.__element = element
        self.__horizontal = horizontal
        self.__vertical = vertical
    
    @property
    def element(self):
        return self.__element
    
    @property
    def horizontal(self):
        return self.__horizontal
    
    @property
    def vertical(self):
        return self.__vertical
