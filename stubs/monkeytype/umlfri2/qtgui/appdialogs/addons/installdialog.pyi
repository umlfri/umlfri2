from umlfri2.application.addon.online.addon import OnlineAddOn
from umlfri2.qtgui.appdialogs.addons.onlineaddons import OnlineAddOnList


class InstallAddOnDialog:
    def __init__(
        self,
        addon_window: OnlineAddOnList,
        online_addon: OnlineAddOn
    ) -> None: ...
