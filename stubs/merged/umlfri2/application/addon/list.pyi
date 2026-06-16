from .local import AddOnManager as AddOnManager
from .online import OnlineAddOnManager as OnlineAddOnManager
from umlfri2.application.addon.local.manager import AddOnManager
from umlfri2.application.addon.online.manager import OnlineAddOnManager
from umlfri2.application.application import Application


class AddOnList:
    def __init__(self, application: Application) -> None: ...
    def init(self) -> None: ...
    @property
    def local(self) -> AddOnManager: ...
    @property
    def online(self) -> OnlineAddOnManager: ...
