from ..base import Event


class ChangeStatusChangedEvent(Event):
    def __init__(self, change_status):
        self.__change_status = change_status
    
    @property
    def change_status(self):
        return self.__change_status
