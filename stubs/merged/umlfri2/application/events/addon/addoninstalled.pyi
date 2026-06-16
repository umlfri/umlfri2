from ..base import Event as Event
from umlfri2.application.addon.local.addon import AddOn


class AddOnInstalledEvent(Event):
    def __init__(self, addon: AddOn) -> None: ...
    @property
    def addon(self) -> AddOn: ...
