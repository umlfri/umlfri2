from .interface import Interface


class IConnectionVisual(Interface):
    def __init__(self, executor, connection):
        super().__init__(executor)
        self.__connection = connection

    @property
    def id(self):
        return "{0}/{1}".format(self.__connection.diagram.save_id, self.__connection.object.save_id)

    @property
    def api_name(self):
        return 'ConnectionVisual'

    def get_destination(self):
        raise NotImplementedError

    def get_diagram(self):
        raise NotImplementedError

    def get_labels(self):
        raise NotImplementedError

    def get_object(self):
        raise NotImplementedError

    def get_points(self):
        raise NotImplementedError

    def get_source(self):
        raise NotImplementedError
