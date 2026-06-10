from umlfri2.plugin.communication.executor import PluginExecutor


class Interface:
    def __init__(self, executor: PluginExecutor) -> None: ...
    @property
    def _executor(self) -> PluginExecutor: ...
