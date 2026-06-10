from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow
from umlfri2.qtgui.properties.widget.widget import PropertiesWidget
from umlfri2.ufl.dialog.tabs.objecttab import UflDialogObjectTab


class ObjectTab:
    def __init__(
        self,
        main_window: UmlFriMainWindow,
        widget: PropertiesWidget,
        tab: UflDialogObjectTab
    ) -> None: ...
    @property
    def label(self) -> str: ...
    def reload_data(self) -> None: ...
    def reload_texts(self) -> None: ...
