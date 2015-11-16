from umlfri2.model import ElementObject
from umlfri2.ufl.objects.patch import UflObjectPatch
from ..base import Command


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
        is_object_patch = isinstance(change, UflObjectPatch)
        if change is not None and is_object_patch and isinstance(change, UflObjectPatch.AttributeChanged):
            change_desc = "property {0}".format(change.name)
        else:
            change_desc = "properties"
        
        return "Changed {0} of {1}".format(name, change_desc)

    def _do(self, ruler):
        self._redo(ruler)

    def _redo(self, ruler):
        self.__object.data.apply_patch(self.__patch)
    
    def _undo(self, ruler):
        self.__object.data.apply_patch(self.__patch.make_reverse())
