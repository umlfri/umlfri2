from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Project
    from umlfri2.ufl.objects import UflObjectPatch


class MetamodelConfigChangedEvent(Event):
    def __init__(self, project: Project, patch: UflObjectPatch) -> None:
        self.__project = project
        self.__patch = patch

    @property
    def project(self) -> Project:
        return self.__project

    @property
    def patch(self) -> UflObjectPatch:
        return self.__patch

    def get_opposite(self) -> MetamodelConfigChangedEvent:
        return MetamodelConfigChangedEvent(self.__project, self.__patch.make_reverse())
