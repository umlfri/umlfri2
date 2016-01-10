from .interface import Interface


class IConnectionLabel(Interface):
    def __init__(self, executor, label):
        super().__init__(executor)
        self.__label = self._ref(label)

    @property
    def id(self):
        connection = self.__label().connection
        return "{0}/{1}/{2}".format(connection.diagram.save_id, connection.object.save_id, self.__label().id)

    @property
    def api_name(self):
        return 'ConnectionLabel'

    def get_center(self):
        center = self.__label().get_bounds(self._application.ruler).center
        
        return center.x, center.y

    def get_connection(self):
        from .connectionvisual import IConnectionVisual
        
        return IConnectionVisual(self._executor, self.__label().connection)

    def get_diagram(self):
        from .diagram import IDiagram
        
        return IDiagram(self._executor, self.__label().connection.diagram)

    def get_position(self):
        top_left = self.__label().get_bounds(self._application.ruler).top_left
        
        return top_left.x, top_left.y

    def get_size(self):
        size = self.__label().get_bounds(self._application.ruler).size
        
        return size.width, size.height
