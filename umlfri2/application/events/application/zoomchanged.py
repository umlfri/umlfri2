from ..base import Event


class ZoomChangedEvent(Event):
    def __init__(self, drawing_area):
        self.__drawing_area = drawing_area
    
    @property
    def drawing_area(self):
        return self.__drawing_area
