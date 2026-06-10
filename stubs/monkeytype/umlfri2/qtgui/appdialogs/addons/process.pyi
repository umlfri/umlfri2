from typing import Union
from umlfri2.application.addon.local.actions.uninstaller import AddOnUninstaller
from umlfri2.application.addon.online.actions.installer import OnlineAddOnInstaller
from umlfri2.qtgui.appdialogs.addons.dialog import AddOnsDialog


class AddOnProcessManager:
    def __init__(self, dialog: AddOnsDialog) -> None: ...
    def run_process(
        self,
        process: Union[AddOnUninstaller, OnlineAddOnInstaller]
    ) -> None: ...
