from umlfri2.application.events.solution import MetamodelConfigChangedEvent
from ..base import Command, CommandNotDone


class ApplyMetamodelConfigPatchCommand(Command):
    def __init__(self, solution, project, patch):
        self.__project = project
        self.__solution = solution
        self.__patch = patch
    
    @property
    def description(self):
        return "Changed config of the '{0}' project metamodel".format(self.__project.name)
    
    def _do(self, ruler):
        if not self.__patch.has_changes:
            raise CommandNotDone
        
        self.__project.apply_config_patch(self.__patch)
        self.__solution.invalidate_all_caches()
    
    def _redo(self, ruler):
        self.__project.apply_config_patch(self.__patch)
        self.__solution.invalidate_all_caches()
    
    def _undo(self, ruler):
        self.__project.apply_config_patch(self.__patch.make_reverse())
        self.__solution.invalidate_all_caches()
        
    def get_updates(self):
        yield MetamodelConfigChangedEvent(self.__project, self.__patch)
