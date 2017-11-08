from _weakref import ref
from types import MethodType


class methodref(ref):
    def __new__(cls, method, callback=None):
        self = ref.__new__(cls, method.__self__, callback)
        self.__fnc = method.__func__
        return self
    
    def __call__(self):
        obj = super().__call__()
        if obj is None:
            return None
        return MethodType(self.__fnc, obj)


class EventDispatcher:
    def __init__(self, application):
        self.__application = application
        self.__events = {}
    
    def subscribe(self, event_type, function, auto_unsubscribe=True):
        if auto_unsubscribe:
            if isinstance(function, MethodType):
                function = methodref(function)
            else:
                function = ref(function)
        self.__events.setdefault(event_type, []).append(function)
    
    def unsubscribe(self, event_type, function):
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
    
    def dispatch(self, event):
        if self.__application.thread_manager is None:
            self.__dispatch_internal(event)
        else:
            self.__application.thread_manager.execute_in_main_thread(self.__dispatch_internal, event)
    
    def __dispatch_internal(self, event):
        self.__dispatch_recursive(event)
        for function in self.__events.get(None, ()):
            self.__call_event_function(function, event)
    
    def __dispatch_recursive(self, event):
        for function in self.__events.get(event.__class__, ()):
            self.__call_event_function(function, event)
        
        for other_event in event.get_chained():
            self.__dispatch_recursive(other_event)
    
    def __call_event_function(self, function, event):
        if isinstance(function, ref):
            reference = function()
            if reference is not None:
                reference(event)
        else:
            function(event)
    
    def dispatch_all(self, events):
        if self.__application.thread_manager is None:
            self.__dispatch_all_internal(events)
        else:
            self.__application.thread_manager.execute_in_main_thread(self.__dispatch_all_internal, events)
    
    def __dispatch_all_internal(self, events):
        for event in events:
            self.__dispatch_internal(event)
    
    def clear(self):
        self.__events.clear()
