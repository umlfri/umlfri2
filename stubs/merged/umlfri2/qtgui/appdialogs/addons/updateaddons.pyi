from .listwidget import AddOnListWidget as AddOnListWidget
from PyQt5.QtWidgets import QWidget
from umlfri2.application import Application as Application
from umlfri2.application.events.addon import AddOnInstalledEvent as AddOnInstalledEvent, AddOnUninstalledEvent as AddOnUninstalledEvent, AddOnUpdatedEvent as AddOnUpdatedEvent
from umlfri2.qtgui.appdialogs.addons.info import AddOnInfoDialog as AddOnInfoDialog

class UpdateAddOnList(AddOnListWidget):
    def __init__(self, processes) -> None: ...

class UpdateAddOnTab(QWidget):
    def __init__(self, processes) -> None: ...
