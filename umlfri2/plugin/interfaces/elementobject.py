from umlfri2.model import ElementObject
from .helpers.uflobject import UflObjectApiHelper
from .interface import Interface


class IElementObject(Interface):
    def __init__(self, executor, element):
        super().__init__(executor)
        self.__element = self._ref(element)

    @property
    def id(self):
        return str(self.__element().save_id)

    @property
    def api_name(self):
        return 'ElementObject'
    
    @property
    def element_object(self):
        return self.__element()

    def get_children(self):
        for child in self.__element().children:
            yield IElementObject(self._executor, child)

    def get_connections(self):
        from .connectionobject import IConnectionObject
        
        for connection in self.__element().connections:
            yield IConnectionObject(self._executor, connection)

    def get_diagrams(self):
        from .diagram import IDiagram
        
        for diagram in self.__element().diagrams:
            yield IDiagram(self._executor, diagram)

    def get_name(self):
        return self.__element().get_display_name()

    def get_parent(self):
        parent = self.__element().parent
        if isinstance(parent, ElementObject):
            return IElementObject(self._executor, parent)
        else:
            return None

    def get_project(self):
        from .project import IProject
        
        return IProject(self._executor, self.__element().project)

    def get_type(self):
        from .elementtype import IElementType
        
        return IElementType(self._executor, self.__element().type)

    def get_value(self, path: str):
        return UflObjectApiHelper(self.__element().data)[path]

    def get_values(self):
        yield from UflObjectApiHelper(self.__element().data)

    def get_visuals(self):
        from .elementvisual import IElementVisual
        
        for visual in self.__element().visuals:
            yield IElementVisual(self._executor, visual)
