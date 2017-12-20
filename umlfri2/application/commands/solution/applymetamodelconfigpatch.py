from umlfri2.application.events.solution import MetamodelConfigChangedEvent
from ..base import Command, CommandNotDone


class ApplyMetamodelConfigPatchCommand(Command):
    def __init__(self, solution, metamodel, patch):
        self.__metamodel = metamodel
        self.__solution = solution
        self.__patch = patch
    
    @property
    def description(self):
        return "Changed config of {0} metamodel".format(self.__metamodel.addon.name)
    
    def _do(self, ruler):
        if not self.__patch.has_changes:
            raise CommandNotDone
        
        self.__metamodel.apply_config_patch(self.__patch)
        self.__solution.invalidate_all_caches()
    
    def _redo(self, ruler):
        self.__metamodel.apply_config_patch(self.__patch)
        self.__solution.invalidate_all_caches()
    
    def _undo(self, ruler):
        self.__metamodel.apply_config_patch(self.__patch.make_reverse())
        self.__solution.invalidate_all_caches()
        
    def get_updates(self):
        yield MetamodelConfigChangedEvent(self.__metamodel, self.__patch)
