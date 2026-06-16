from ..base import Event as Event
from umlfri2.model.project import Project
from umlfri2.ufl.objects.patch.object import UflObjectPatch


class MetamodelConfigChangedEvent(Event):
    def __init__(
        self,
        metamodel: Project,
        patch: UflObjectPatch
    ) -> None: ...
    @property
    def metamodel(self): ...
    @property
    def patch(self): ...
    def get_opposite(self): ...
