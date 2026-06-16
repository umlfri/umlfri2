from .installedaddons import InstalledAddOnList as InstalledAddOnList
from .onlineaddons import OnlineAddOnList as OnlineAddOnList
from .process import AddOnProcessManager as AddOnProcessManager
from .updateaddons import UpdateAddOnTab as UpdateAddOnTab
from PyQt5.QtWidgets import QDialog
from umlfri2.application import Application as Application
from umlfri2.application.events.addon import AddOnInstalledEvent as AddOnInstalledEvent, AddOnUninstalledEvent as AddOnUninstalledEvent, AddOnUpdatedEvent as AddOnUpdatedEvent

class AddOnsDialog(QDialog):
    def __init__(self, main_window) -> None: ...
    def sizeHint(self): ...
    def closeEvent(self, event) -> None: ...
