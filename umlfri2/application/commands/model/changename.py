from umlfri2.application.events.model import ProjectChangedEvent
from ..base import Command, CommandNotDone


class ChangeProjectNameCommand(Command):
    def __init__(self, project, name):
        self.__project = project
        self.__name = name
        self.__old_name = None
    
    @property
    def description(self):
        return "Changed project name to '{0}'".format(self.__name)

    def _do(self, ruler):
        if self.__project.name == self.__name:
            raise CommandNotDone
        self.__old_name = self.__project.name
        self._redo(ruler)

    def _redo(self, ruler):
        self.__project.name = self.__name
    
    def _undo(self, ruler):
        self.__project.name = self.__old_name
    
    def get_updates(self):
        yield ProjectChangedEvent(self.__project)
