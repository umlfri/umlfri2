from collections import namedtuple

from umlfri2.application.events.diagram import ElementHiddenEvent, ConnectionHiddenEvent
from umlfri2.model.element import ElementVisual
from ..base import Command


HiddenVisualDescription = namedtuple('HiddenVisualDescription', ('type', 'z_order', 'visual'))


class VisualType:
    element = 1
    connection = 2


class HideElementsCommand(Command):
    def __init__(self, diagram, elements):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__elements = elements
        self.__hidden_visual_descriptions = []
    
    @property
    def description(self):
        return "Hiding selected elements from diagram {0}".format(self.__diagram_name)
    
    def _do(self, ruler):
        visuals = set()
        for element in self.__elements:
            visuals.add(element)
            for connection in element.connections:
                visuals.add(connection)
        
        for visual in visuals:
            if isinstance(visual, ElementVisual):
                type = VisualType.element
            else:
                type = VisualType.connection
            
            z_order = self.__diagram.get_z_order(visual)
            self.__hidden_visual_descriptions.append(HiddenVisualDescription(type, z_order, visual))
        
        self.__hidden_visual_descriptions.sort(reverse=True) # sort by type (elements should be last) and z_order (desc)
        
        self._redo(ruler)
    
    def _redo(self, ruler):
        for type, z_order, visual in self.__hidden_visual_descriptions:
            self.__diagram.remove(visual)
    
    def _undo(self, ruler):
        for type, z_order, visual in reversed(self.__hidden_visual_descriptions):
            self.__diagram.add(visual, z_order=z_order)
    
    def get_updates(self):
        for type, z_order, visual in self.__hidden_visual_descriptions:
            if type == VisualType.element:
                yield ElementHiddenEvent(visual)
            else:
                yield ConnectionHiddenEvent(visual)
