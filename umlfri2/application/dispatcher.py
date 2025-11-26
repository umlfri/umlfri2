from __future__ import annotations

from _weakref import ref
from types import MethodType
from typing import Any, Callable, Dict, List, Optional, Type, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from umlfri2.application import Application
    from umlfri2.application.events.base import Event


class methodref(ref):
    def __new__(cls, method, callback = None):
        self = ref.__new__(cls, method.__self__, callback)
        self.__fnc = method.__func__
        return self
    
    def __call__(self):
        obj = super().__call__()
        if obj is None:
            return None
        return MethodType(self.__fnc, obj)


class EventDispatcher:
    def __init__(self, application: Application) -> None:
        self.__application = application
        self.__events = {}
    
    def subscribe(self, event_type: Optional[Type[Event]], function: Callable[[Event], None],
                  auto_unsubscribe: bool = True) -> None:
        if auto_unsubscribe:
            if isinstance(function, MethodType):
                function = methodref(function)
            else:
                function = ref(function)
        self.__events.setdefault(event_type, []).append(function)
    
    def unsubscribe(self, event_type: Type[Event], function: Callable[[Event], None]) -> None:
        if event_type not in self.__events:
            raise Exception
        
        for event_func in self.__events[event_type]:
            if isinstance(event_func, ref):
                event_func_ref = event_func()
            else:
                event_func_ref = event_func
            if event_func_ref == function:
                self.__events[event_type].remove(event_func)
                break
        else:
            raise Exception
        
        if not self.__events[event_type]:
            del self.__events[event_type]
    
    def dispatch(self, event: Event) -> None:
        if self.__application.thread_manager is None:
            self.__dispatch_internal(event)
        else:
            self.__application.thread_manager.execute_in_main_thread(self.__dispatch_internal, event)
    
    def __dispatch_internal(self, event: Event) -> None:
        self.__dispatch_recursive(event)
        for function in self.__events.get(None, ()):
            self.__call_event_function(function, event)
    
    def __dispatch_recursive(self, event: Event) -> None:
        for function in self.__events.get(event.__class__, ()):
            self.__call_event_function(function, event)
        
        for other_event in event.get_chained():
            self.__dispatch_recursive(other_event)
    
    def __call_event_function(self, function, event: Event) -> None:
        if isinstance(function, ref):
            reference = function()
            if reference is not None:
                reference(event)
        else:
            function(event)
    
    def dispatch_all(self, events: List[Event]) -> None:
        if self.__application.thread_manager is None:
            self.__dispatch_all_internal(events)
        else:
            self.__application.thread_manager.execute_in_main_thread(self.__dispatch_all_internal, events)
    
    def __dispatch_all_internal(self, events: List[Event]) -> None:
        for event in events:
            self.__dispatch_internal(event)
    
    def clear(self) -> None:
        self.__events.clear()
