from .interface import Interface


class IAction(Interface):
    def __init__(self, executor, action):
        super().__init__(executor)
        self.__action = self._ref(action)

    @property
    def id(self):
        return '{{{0}}}action:{1}'.format(self.__action().addon.identifier, self.__action().id)

    @property
    def api_name(self):
        return 'Action'

    def get_enabled(self):
        return self.__action().enabled

    def set_enabled(self, value: bool):
        self.__action().enabled = value

    def get_id(self):
        return self.__action().id
