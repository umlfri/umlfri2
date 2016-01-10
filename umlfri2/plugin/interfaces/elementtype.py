from .interface import Interface


class IElementType(Interface):
    def __init__(self, executor, element):
        super().__init__(executor)
        self.__element = element

    @property
    def id(self):
        return '{{{0}}}element:{1}'.format(self.__element.metamodel.addon.identifier, self.__element.id)

    @property
    def api_name(self):
        return 'ElementType'

    def get_name(self):
        return self.__element.id
