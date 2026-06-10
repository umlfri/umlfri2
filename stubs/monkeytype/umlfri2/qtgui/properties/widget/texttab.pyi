from umlfri2.qtgui.properties.widget.widget import PropertiesWidget
from umlfri2.ufl.dialog.tabs.valuetab import UflDialogValueTab


class TextTab:
    def __init__(
        self,
        widget: PropertiesWidget,
        tab: UflDialogValueTab
    ) -> None: ...
    @property
    def label(self) -> str: ...
    def reload_data(self) -> None: ...
    def reload_texts(self) -> None: ...
