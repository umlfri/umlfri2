from typing import Iterator
from umlfri2.application.events.solution.metamodelconfigchanged import MetamodelConfigChangedEvent
from umlfri2.model.project import Project
from umlfri2.model.solution import Solution
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.ufl.objects.patch.object import UflObjectPatch


class ApplyMetamodelConfigPatchCommand:
    def __init__(
        self,
        solution: Solution,
        project: Project,
        patch: UflObjectPatch
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    def get_updates(
        self
    ) -> Iterator[MetamodelConfigChangedEvent]: ...
