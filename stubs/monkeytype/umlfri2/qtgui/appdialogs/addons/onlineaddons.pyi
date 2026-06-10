from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QWidget,
)
from umlfri2.application.addon.online.addon import OnlineAddOn
from umlfri2.application.addon.online.manager import OnlineAddOnManager
from umlfri2.qtgui.appdialogs.addons.process import AddOnProcessManager


class OnlineAddOnList:
    def __init__(self, processes: AddOnProcessManager) -> None: ...
    def _addon_button_factory(self) -> OnlineAddOnList: ...
    def _addon_content_menu(self, addon: OnlineAddOn) -> QMenu: ...
    @property
    def _addons(self) -> OnlineAddOnManager: ...
    def add_buttons(
        self,
        addon: OnlineAddOn,
        button_box: QHBoxLayout,
        container: QWidget
    ) -> None: ...
