from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from umlfri2.application.events.solution import MetamodelConfigChangedEvent
from ..base import Command, CommandNotDone

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import Solution, Project
    from umlfri2.ufl.objects import UflObjectPatch


class ApplyMetamodelConfigPatchCommand(Command):
    def __init__(self, solution: Solution, project: Project, patch: UflObjectPatch) -> None:
        self.__project = project
        self.__solution = solution
        self.__patch = patch
    
    @property
    def description(self) -> str:
        return "Changed config of the '{0}' project metamodel".format(self.__project.name)
    
    def _do(self, ruler: object) -> None:
        if not self.__patch.has_changes:
            raise CommandNotDone
        
        self.__project.apply_config_patch(self.__patch)
        self.__solution.invalidate_all_caches()
    
    def _redo(self, ruler: object) -> None:
        self.__project.apply_config_patch(self.__patch)
        self.__solution.invalidate_all_caches()
    
    def _undo(self, ruler: object) -> None:
        self.__project.apply_config_patch(self.__patch.make_reverse())
        self.__solution.invalidate_all_caches()
        
    def get_updates(self) -> Iterator[Event]:
        yield MetamodelConfigChangedEvent(self.__project, self.__patch)
