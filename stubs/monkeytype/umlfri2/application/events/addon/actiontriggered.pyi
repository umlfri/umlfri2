from umlfri2.application.addon.local.gui.action import AddOnAction


class ActionTriggeredEvent:
    def __init__(self, action: AddOnAction) -> None: ...
    @property
    def action(self) -> AddOnAction: ...
