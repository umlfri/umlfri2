from umlfri2.plugin.communication.executor import PluginExecutor


class IApplication:
    def __init__(self, executor: PluginExecutor) -> None: ...
    @property
    def id(self) -> str: ...
