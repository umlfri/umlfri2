from umlfri2.application.addon.local.addon import AddOn


class AddOnUninstalledEvent:
    def __init__(self, addon: AddOn) -> None: ...
    @property
    def addon(self) -> AddOn: ...
