from .interface import Interface


class IMetamodel(Interface):
    def __init__(self, executor, metamodel):
        super().__init__(executor)
        self.__metamodel = metamodel

    @property
    def id(self):
        return '{{{0}}}metamodel'.format(self.__metamodel.addon.identifier)

    @property
    def api_name(self):
        return 'Metamodel'

    def get_connection(self, name: str):
        raise NotImplementedError

    def get_connections(self):
        raise NotImplementedError

    def get_diagram(self, name: str):
        raise NotImplementedError

    def get_diagrams(self):
        raise NotImplementedError

    def get_element(self, name: str):
        raise NotImplementedError

    def get_elements(self):
        raise NotImplementedError

    def get_identifier(self):
        raise NotImplementedError

    def get_version(self):
        raise NotImplementedError
