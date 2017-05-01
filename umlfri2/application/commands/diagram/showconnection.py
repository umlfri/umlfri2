from umlfri2.application.events.diagram import ConnectionShownEvent
from ..base import Command, CommandNotDone


class ShowConnectionCommand(Command):
    def __init__(self, diagram, connection_object):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__connection_object = connection_object
        self.__connection_visual = None

    @property
    def description(self):
        return "Showing connection on diagram '{0}'".format(self.__diagram_name)

    def _do(self, ruler):
        if self.__diagram.contains(self.__connection_object):
            raise CommandNotDone

        self.__connection_visual = self.__diagram.show(self.__connection_object)

    def _redo(self, ruler):
        self.__diagram.add(self.__connection_visual)

    def _undo(self, ruler):
        self.__diagram.remove(self.__connection_visual)

    @property
    def connection_visual(self):
        return self.__connection_visual

    @property
    def connection_object(self):
        return self.__connection_object

    def get_updates(self):
        yield ConnectionShownEvent(self.__connection_visual)
