from collections import namedtuple

from umlfri2.application.events.diagram import ElementHiddenEvent, ConnectionHiddenEvent
from ..base import Command


HiddenVisualDescription = namedtuple('HiddenVisualDescription', ('z_order', 'visual'))


class HideElementsCommand(Command):
    def __init__(self, diagram, elements):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__elements = elements
        self.__element_visual_descriptions = []
        self.__connection_visual_descriptions = []
    
    @property
    def description(self):
        return "Hiding selected elements from diagram {0}".format(self.__diagram_name)
    
    def _do(self, ruler):
        elements = set()
        connections = set()
        for element in self.__elements:
            elements.add(element)
            for connection in element.connections:
                connections.add(connection)
        
        for visual in elements:
            z_order = self.__diagram.get_z_order(visual)
            self.__element_visual_descriptions.append(HiddenVisualDescription(z_order, visual))
        
        for visual in connections:
            z_order = self.__diagram.get_z_order(visual)
            self.__connection_visual_descriptions.append(HiddenVisualDescription(z_order, visual))
        
        self.__element_visual_descriptions.sort(reverse=True) # sort by z_order (desc)
        self.__connection_visual_descriptions.sort(reverse=True) # sort by z_order (desc)
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        for z_order, visual in self.__connection_visual_descriptions:
            self.__diagram.remove(visual)
        
        for z_order, visual in self.__element_visual_descriptions:
            self.__diagram.remove(visual)
    
    def _undo(self, ruler):
        for z_order, visual in reversed(self.__element_visual_descriptions):
            self.__diagram.add(visual, z_order=z_order)
        
        for z_order, visual in reversed(self.__connection_visual_descriptions):
            self.__diagram.add(visual, z_order=z_order)
    
    def get_updates(self):
        for z_order, visual in self.__element_visual_descriptions:
            yield ElementHiddenEvent(visual)
        
        for z_order, visual in self.__connection_visual_descriptions:
            yield ConnectionHiddenEvent(visual)
