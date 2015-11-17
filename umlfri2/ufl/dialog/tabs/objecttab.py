from .tab import UflDialogTab


class UflDialogObjectTab(UflDialogTab):
    def associate(self, ufl_object):
        self._set_current_object(ufl_object)
