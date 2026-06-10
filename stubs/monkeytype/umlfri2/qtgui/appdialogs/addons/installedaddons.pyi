from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QWidget,
)
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.local.manager import AddOnManager
from umlfri2.qtgui.appdialogs.addons.process import AddOnProcessManager


class InstalledAddOnList:
    def __init__(self, processes: AddOnProcessManager) -> None: ...
    def _addon_button_factory(self) -> InstalledAddOnList: ...
    def _addon_content_menu(self, addon: AddOn) -> QMenu: ...
    @property
    def _addons(self) -> AddOnManager: ...
    def add_buttons(
        self,
        addon: AddOn,
        button_box: QHBoxLayout,
        container: QWidget
    ) -> None: ...
