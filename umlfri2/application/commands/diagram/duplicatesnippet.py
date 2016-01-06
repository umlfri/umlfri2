from umlfri2.application.events.diagram import ElementShownEvent, ConnectionShownEvent
from umlfri2.application.events.model import ElementCreatedEvent, ConnectionCreatedEvent
from umlfri2.model.element import ElementVisual
from ..base import Command


class DuplicateSnippetCommand(Command):
    def __init__(self, diagram, snippet):
        self.__diagram_name = diagram.get_display_name()
        self.__parent = diagram.parent
        self.__diagram = diagram
        self.__snippet = snippet
        self.__pasted_visuals = None
    
    @property
    def description(self):
        return "Elements pasted to diagram {0} as duplicate".format(self.__diagram_name)
    
    def _do(self, ruler):
        self.__pasted_visuals = list(self.__snippet.duplicate_to(ruler, self.__diagram))
        
    def _redo(self, ruler):
        for visual in self.__pasted_visuals:
            self.__parent.add_child(visual.object)
            self.__diagram.add(visual)
    
    def _undo(self, ruler):
        for visual in self.__pasted_visuals:
            self.__parent.remove_child(visual.object)
            self.__diagram.remove(visual)
    
    @property
    def element_visuals(self):
        for visual in self.__pasted_visuals:
            if isinstance(visual, ElementVisual):
                yield visual
    
    def get_updates(self):
        for visual in self.__pasted_visuals:
            if isinstance(visual, ElementVisual):
                yield ElementCreatedEvent(visual.object)
                yield ElementShownEvent(visual)
            else:
                yield ConnectionCreatedEvent(visual.object)
                yield ConnectionShownEvent(visual)
