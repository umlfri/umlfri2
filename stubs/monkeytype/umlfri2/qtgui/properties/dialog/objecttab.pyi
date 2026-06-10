from umlfri2.qtgui.properties.dialog.dialog import PropertiesDialog
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab


class ObjectPropertyTab:
    def __init__(
        self,
        window: PropertiesDialog,
        tab: UflDialogObjectTab,
        lonely: bool = ...
    ) -> None: ...
    def refresh(self) -> None: ...
