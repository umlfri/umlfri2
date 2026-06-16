from ..base import Event as Event
from umlfri2.application.addon.local.gui.action import AddOnAction


class ActionTriggeredEvent(Event):
    def __init__(self, action: AddOnAction) -> None: ...
    @property
    def action(self) -> AddOnAction: ...
