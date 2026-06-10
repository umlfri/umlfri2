from .listtab import ListPropertyTab as ListPropertyTab
from .objecttab import ObjectPropertyTab as ObjectPropertyTab
from PyQt5.QtWidgets import QDialog, QTabWidget as QTabWidget
from umlfri2.application import Application as Application
from umlfri2.application.commands.model import ApplyPatchCommand as ApplyPatchCommand
from umlfri2.application.commands.solution import ApplyMetamodelConfigPatchCommand as ApplyMetamodelConfigPatchCommand
from umlfri2.qtgui.base.validatingtabwidget import ValidatingTabWidget as ValidatingTabWidget
from umlfri2.ufl.dialog import UflDialogListTab as UflDialogListTab, UflDialogNullableValueTab as UflDialogNullableValueTab, UflDialogObjectTab as UflDialogObjectTab, UflDialogValueTab as UflDialogValueTab

class PropertiesDialog(QDialog):
    def __init__(self, main_window, dialog, mk_apply_patch_command) -> None: ...
    def closeEvent(self, event) -> None: ...
    def sizeHint(self): ...
    @staticmethod
    def open_for(main_window, object): ...
    @staticmethod
    def open_config(main_window, project): ...
