from umlfri2.application.addon.local.addon import AddOn
from umlfri2.application.addon.local.state import AddOnState


class AddOnStateChangedEvent:
    def __init__(
        self,
        addon: AddOn,
        state: AddOnState
    ) -> None: ...
    @property
    def addon(self) -> AddOn: ...
    @property
    def addon_state(self) -> AddOnState: ...
