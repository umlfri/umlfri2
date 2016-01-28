class SnappedPoint:
    def __init__(self, point, horizontal_indicators=(), vertical_indicators=()):
        self.__point = point
        self.__horizontal_indicators = sorted(horizontal_indicators, key=lambda item: item.x)
        self.__vertical_indicators = sorted(vertical_indicators, key=lambda item: item.y)
    
    @property
    def point(self):
        return self.__point
    
    @property
    def snapped_horizontally(self):
        return bool(self.__horizontal_indicators)
    
    @property
    def snapped_vertically(self):
        return bool(self.__vertical_indicators)
    
    @property
    def horizontal_indicators(self):
        yield from self.__horizontal_indicators
    
    @property
    def vertical_indicators(self):
        yield from self.__vertical_indicators
