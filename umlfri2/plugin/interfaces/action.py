from .interface import Interface


class IAction(Interface):
    def __init__(self, executor):
        super().__init__(executor)

    @property
    def id(self):
        raise NotImplementedError

    @property
    def api_name(self):
        return 'Action'

    def get_enabled(self):
        raise NotImplementedError

    def set_enabled(self, value: bool):
        raise NotImplementedError

    def get_label(self):
        raise NotImplementedError
