from weakref import ref
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from umlfri2.plugin.executor import PluginExecutor


class Interface:
    def __init__(self, executor: 'PluginExecutor') -> None:
        self.__executor = executor
    
    @property
    def id(self) -> str:
        raise NotImplementedError
    
    @property
    def type(self) -> str:
        return self.__class__.__name__[1:]
    
    @property
    def _application(self):
        from umlfri2.application import Application
        return Application()
    
    @property
    def _executor(self) -> 'PluginExecutor':
        return self.__executor
    
    def _ref(self, object: Any) -> ref:
        return ref(object, self.__removed)
    
    def __removed(self, object):
        self.__executor.object_removed(self)
