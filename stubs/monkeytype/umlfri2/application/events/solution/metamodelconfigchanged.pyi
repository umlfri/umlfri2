from umlfri2.model.project import Project
from umlfri2.ufl.objects.patch.object import UflObjectPatch


class MetamodelConfigChangedEvent:
    def __init__(
        self,
        metamodel: Project,
        patch: UflObjectPatch
    ) -> None: ...
