from collections import namedtuple

from umlfri2.application.events.model import ConnectionDeletedEvent, ElementDeletedEvent, DiagramDeletedEvent
from ..diagram import HideElementsCommand, HideConnectionCommand
from ..base import Command


DeletedElementDescription = namedtuple('DeletedElementDescription', ('index', 'element'))
DeletedDiagramDescription = namedtuple('DeletedDiagramDescription', ('index', 'diagram'))


class DeleteElementsCommand(Command):
    def __init__(self, elements):
        self.__all_elements = elements
        self.__elements = []
        self.__connections = set()
        self.__diagrams = []
        self.__hide_commands = []
    
    @property
    def description(self):
        return "Deleting elements from the project"
    
    def _do(self, ruler):
        for element in self.__all_elements:
            if not self.__is_chain_in_elements(element.parent):
                index = element.parent.get_child_index(element)
                self.__elements.append(DeletedElementDescription(index, element))
                self.__connections.update(element.connections)
                for index, diagram in enumerate(element.diagrams):
                    self.__diagrams.append(DeletedDiagramDescription(index, diagram))
                self.__add_hide_recursion(element)
        
        for index, element in self.__elements:
            element.parent.remove_child(element)
        
        for connection in self.__connections:
            connection.source.remove_connection(connection)
            connection.destination.remove_connection(connection)
        
        for command in self.__hide_commands:
            command.do(ruler)

    def __is_chain_in_elements(self, element):
        if element in self.__all_elements:
            return True
        
        if element.parent is not None:
            return self.__is_chain_in_elements(element.parent)
        
        return False

    def __add_hide_recursion(self, element):
        for visual in element.visuals:
            self.__hide_commands.append(HideElementsCommand(visual.diagram, [visual]))
        
        for child in element.children:
            self.__add_hide_recursion(child)
    
    def _undo(self, ruler):
        for index, element in self.__elements:
            element.parent.add_child(element, index=index)
        
        for connection in self.__connections:
            connection.source.add_connection(connection)
            connection.destination.add_connection(connection)
        
        for command in self.__hide_commands:
            command.undo(ruler)
    
    def _redo(self, ruler):
        for index, element in self.__elements:
            element.parent.remove_child(element)
        
        for connection in self.__connections:
            connection.source.remove_connection(connection)
            connection.destination.remove_connection(connection)
        
        for command in self.__hide_commands:
            command.redo(ruler)
    
    def get_updates(self):
        for index, element in self.__elements:
            yield ElementDeletedEvent(element, index)
        
        for connection in self.__connections:
            yield ConnectionDeletedEvent(connection, indirect=True)
        
        for index, diagram in self.__diagrams:
            yield DiagramDeletedEvent(diagram, index, indirect=True)
        
        for hide_command in self.__hide_commands:
            yield from hide_command.get_updates()
