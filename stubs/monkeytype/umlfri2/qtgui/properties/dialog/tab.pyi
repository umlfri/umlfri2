from PyQt5.QtWidgets import QFormLayout
from typing import Union
from umlfri2.qtgui.properties.dialog.dialog import PropertiesDialog
from umlfri2.ufl.dialog.tabs.listtab import UflDialogListTab
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab


class PropertyTab:
    def __init__(
        self,
        window: PropertiesDialog,
        tab: Union[UflDialogListTab, UflDialogObjectTab]
    ) -> None: ...
    def _create_layout(self) -> QFormLayout: ...
    def _focus_first(self) -> None: ...
    @property
    def _tab(self) -> UflDialogListTab: ...
    def _update_values(self) -> None: ...
