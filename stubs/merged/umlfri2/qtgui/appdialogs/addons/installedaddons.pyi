from .info import AddOnInfoDialog as AddOnInfoDialog
from .listwidget import AddOnListWidget as AddOnListWidget
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.application import Application as Application
from umlfri2.application.addon.local import AddOnState as AddOnState
from umlfri2.application.events.addon import AddOnInstalledEvent as AddOnInstalledEvent, AddOnStateChangedEvent as AddOnStateChangedEvent, AddOnUninstalledEvent as AddOnUninstalledEvent, AddOnUpdatedEvent as AddOnUpdatedEvent

class InstalledAddOnList(AddOnListWidget):
    class __AddonButtons(NamedTuple):
        start: Incomplete
        stop: Incomplete
    def __init__(self, processes) -> None: ...
    def add_buttons(self, addon, button_box, container) -> None: ...
