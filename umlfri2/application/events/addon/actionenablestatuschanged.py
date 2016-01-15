from ..base import Event


class ActionEnableStatusChangedEvent(Event):
    def __init__(self, action):
        self.__action = action
    
    @property
    def action(self):
        return self.__action
