from ..base import Event


class UpdateCheckFinishedEvent(Event):
    def __init__(self, updates):
        self.__updates = updates
    
    @property
    def updates(self):
        return self.__updates
