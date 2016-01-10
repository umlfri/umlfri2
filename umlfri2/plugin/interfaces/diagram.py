from umlfri2.model.element import ElementVisual
from .helpers.uflobject import UflObjectApiHelper
from .interface import Interface


class IDiagram(Interface):
    def __init__(self, executor, diagram):
        super().__init__(executor)
        self.__diagram = self._ref(diagram)

    @property
    def id(self):
        return str(self.__diagram().save_id)

    @property
    def api_name(self):
        return 'Diagram'
    
    @property
    def diagram(self):
        return self.__diagram()

    def get_connections(self):
        from .connectionvisual import IConnectionVisual
        
        for connection in self.__diagram().connections:
            yield IConnectionVisual(self._executor, connection)

    def get_elements(self):
        from .elementvisual import IElementVisual
        
        for element in self.__diagram().elements:
            yield IElementVisual(self._executor, element)

    def get_connection(self, obj: object):
        from .connectionvisual import IConnectionVisual
        
        visual = self.__diagram().get_visual_for(obj.connection_object)
        
        if visual is None:
            return None
        else:
            return IConnectionVisual(self._executor, visual)

    def get_element(self, obj: object):
        from .elementvisual import IElementVisual
        
        visual = self.__diagram().get_visual_for(obj.element_object)
        
        if visual is None:
            return None
        else:
            return IElementVisual(self._executor, visual)

    def get_name(self):
        return self.__diagram().get_display_name()

    def get_parent(self):
        from .elementobject import IElementObject
        
        return IElementObject(self._executor, self.__diagram().parent)

    def get_project(self):
        from .project import IProject
        
        return IProject(self._executor, self.__diagram().project)

    def get_selection(self) -> object:
        from .elementvisual import IElementVisual
        from .connectionvisual import IConnectionVisual
        
        tab = self._application.tabs.get_tab_for(self.__diagram())
        
        if tab is None:
            return
        
        for visual in tab.drawing_area.selection.selected_visuals:
            if isinstance(visual, ElementVisual):
                yield IElementVisual(self._executor, visual)
            else:
                yield IConnectionVisual(self._executor, visual)

    def get_type(self):
        from .diagramtype import IDiagramType
        
        return IDiagramType(self._executor, self.__diagram().type)

    def get_value(self, path: str):
        return UflObjectApiHelper(self.__diagram().data)[path]

    def get_values(self):
        yield from UflObjectApiHelper(self.__diagram().data)
