from umlfri2.application.addon.local.addon import AddOn
from umlfri2.plugin.communication.pipechannel import PipeChannel
from umlfri2.plugin.interfaces.action import IAction
from umlfri2.plugin.interfaces.diagram import IDiagram
from umlfri2.qtgui.base.qtthreadmanager import QTThreadManager


class PluginExecutor:
    def __init__(
        self,
        addon: AddOn,
        channel: PipeChannel,
        thread_manager: QTThreadManager
    ) -> None: ...
    def fire_event(self, target: IAction, selector: str, **arguments) -> None: ...
    def object_removed(self, object: IDiagram): ...
    @property
    def running(self) -> bool: ...
    def send_stop(self) -> None: ...
    def start(self) -> None: ...
