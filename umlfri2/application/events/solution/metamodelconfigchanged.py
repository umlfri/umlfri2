from ..base import Event


class MetamodelConfigChangedEvent(Event):
    def __init__(self, metamodel, patch):
        self.__metamodel = metamodel
        self.__patch = patch

    @property
    def metamodel(self):
        return self.__metamodel

    @property
    def patch(self):
        return self.__patch

    def get_opposite(self):
        return MetamodelConfigChangedEvent(self.__metamodel, self.__patch.make_reverse())
