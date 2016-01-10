from .interface import Interface


class IElementVisual(Interface):
    def __init__(self, executor, element):
        super().__init__(executor)
        self.__element = self._ref(element)

    @property
    def id(self):
        return "{0}/{1}".format(self.__element().diagram.save_id, self.__element().object.save_id)

    @property
    def api_name(self):
        return 'ElementVisual'

    def get_center(self):
        center = self.__element().get_bounds(self._application.ruler).center
        
        return center.x, center.y

    def get_connections(self):
        from .connectionvisual import IConnectionVisual
        
        for connection in self.__element().connections:
            yield IConnectionVisual(self._executor, connection)

    def get_diagram(self):
        from .diagram import IDiagram
        
        return IDiagram(self._executor, self.__element().diagram)

    def get_minimal_size(self):
        size = self.__element().get_minimal_size(self._application.ruler)
        
        return size.width, size.height

    def get_object(self):
        from .elementobject import IElementObject
        
        return IElementObject(self._executor, self.__element().object)

    def get_position(self):
        top_left = self.__element().get_bounds(self._application.ruler).top_left
        
        return top_left.x, top_left.y

    def get_size(self):
        size = self.__element().get_bounds(self._application.ruler).size
        
        return size.width, size.height
