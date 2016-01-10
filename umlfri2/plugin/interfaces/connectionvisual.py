from .interface import Interface


class IConnectionVisual(Interface):
    def __init__(self, executor, connection):
        super().__init__(executor)
        self.__connection = self._ref(connection)

    @property
    def id(self):
        return "{0}/{1}".format(self.__connection().diagram.save_id, self.__connection().object.save_id)

    @property
    def api_name(self):
        return 'ConnectionVisual'

    def get_destination(self):
        from .elementvisual import IElementVisual
        
        return IElementVisual(self._executor, self.__connection().destination)

    def get_diagram(self):
        from .diagram import IDiagram
        
        return IDiagram(self._executor, self.__connection().diagram)

    def get_labels(self):
        from .connectionlabel import IConnectionLabel
        
        for label in self.__connection().get_labels():
            yield IConnectionLabel(self._executor, label)

    def get_object(self):
        from .connectionobject import IConnectionObject
        
        return IConnectionObject(self._executor, self.__connection().object)

    def get_points(self):
        for point in self.__connection().get_points(self._application.ruler, False, False):
            yield point.x, point.y

    def get_source(self):
        from .elementvisual import IElementVisual
        
        return IElementVisual(self._executor, self.__connection().source)
