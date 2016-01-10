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
        raise NotImplementedError

    def get_connections(self):
        raise NotImplementedError

    def get_diagram(self):
        raise NotImplementedError

    def get_minimal_size(self):
        raise NotImplementedError

    def get_object(self):
        raise NotImplementedError

    def get_position(self):
        raise NotImplementedError

    def get_size(self):
        raise NotImplementedError
