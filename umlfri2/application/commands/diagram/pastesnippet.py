from umlfri2.application.events.diagram import ElementShownEvent, ConnectionShownEvent
from umlfri2.model.element import ElementVisual
from ..base import Command


class PasteSnippetCommand(Command):
    def __init__(self, diagram, snippet):
        self.__diagram_name = diagram.get_display_name()
        self.__diagram = diagram
        self.__snippet = snippet
        self.__pasted_visuals = None
    
    @property
    def description(self):
        return "Elements pasted to diagram {0}".format(self.__diagram_name)
    
    def _do(self, ruler):
        self.__pasted_visuals = list(self.__snippet.paste_to(ruler, self.__diagram))
        
    def _redo(self, ruler):
        for visual in self.__pasted_visuals:
            self.__diagram.add(visual)
    
    def _undo(self, ruler):
        for visual in self.__pasted_visuals:
            self.__diagram.remove(visual)
    
    def get_updates(self):
        for visual in self.__pasted_visuals:
            if isinstance(visual, ElementVisual):
                yield ElementShownEvent(visual)
            else:
                yield ConnectionShownEvent(visual)
