from umlfri2.application.events.model import ObjectChangedEvent
from umlfri2.model import ElementObject
from umlfri2.ufl.objects.patch import UflObjectPatch
from ..base import Command, CommandNotDone


class ApplyPatchCommand(Command):
    def __init__(self, object, patch):
        self.__object = object
        self.__patch = patch
    
    @property
    def description(self):
        if isinstance(self.__object, ElementObject):
            name = "element {0}".format(self.__object.get_display_name())
        else:
            name = "connection"
        
        change = self.__patch.get_lonely_change()
        is_object_patch = isinstance(self.__patch, UflObjectPatch)
        if change is not None and is_object_patch:
            change_desc = "property {0}".format(change.name)
        else:
            change_desc = "properties"
        
        return "Changed {0} of {1}".format(change_desc, name)

    def _do(self, ruler):
        if not self.__patch.has_changes():
            raise CommandNotDone
        
        self._redo(ruler)

    def _redo(self, ruler):
        self.__object.apply_ufl_patch(self.__patch)
    
    def _undo(self, ruler):
        self.__object.apply_ufl_patch(self.__patch.make_reverse())
    
    def get_updates(self):
        yield ObjectChangedEvent(self.__object, self.__patch)
