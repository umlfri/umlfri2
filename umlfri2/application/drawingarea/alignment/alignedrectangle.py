class AlignedRectangle:
    def __init__(self, rectangle, horizontal_indicators=(), vertical_indicators=()):
        self.__rectangle = rectangle
        self.__horizontal_indicators = sorted(horizontal_indicators, key=lambda item: item.x)
        self.__vertical_indicators = sorted(vertical_indicators, key=lambda item: item.y)
    
    @property
    def rectangle(self):
        return self.__rectangle
    
    @property
    def aligned_horizontally(self):
        return bool(self.__horizontal_indicators)
    
    @property
    def aligned_vertically(self):
        return bool(self.__vertical_indicators)
    
    @property
    def horizontal_indicators(self):
        yield from self.__horizontal_indicators
    
    @property
    def vertical_indicators(self):
        yield from self.__vertical_indicators
