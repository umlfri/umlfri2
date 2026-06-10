from .info import AddOnInfoDialog as AddOnInfoDialog
from .installdialog import InstallAddOnDialog as InstallAddOnDialog
from .listwidget import AddOnListWidget as AddOnListWidget
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.application import Application as Application
from umlfri2.application.events.addon import AddOnInstalledEvent as AddOnInstalledEvent, AddOnUninstalledEvent as AddOnUninstalledEvent

class OnlineAddOnList(AddOnListWidget):
    class __OnlineAddonButtons(NamedTuple):
        install: Incomplete
        installed_info: Incomplete
        container: Incomplete
    def __init__(self, processes) -> None: ...
    def add_buttons(self, addon, button_box, container) -> None: ...
