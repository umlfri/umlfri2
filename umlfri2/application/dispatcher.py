class EventDispatcher:
    def __init__(self):
        self.__events = {}
    
    def subscribe(self, event_type, function):
        self.__events.setdefault(event_type, []).append(function)
    
    def unsubscribe(self, event_type, function):
        if event_type not in self.__events or function not in self.__events[event_type]:
            raise Exception
        self.__events[event_type].remove(function)
        if not self.__events[event_type]:
            del self.__events[event_type]
    
    def dispatch(self, event):
        self.__dispatch_recursive(event)
        for function in self.__events.get(None, ()):
            function(event)
    
    def __dispatch_recursive(self, event):
        for function in self.__events.get(event.__class__, ()):
            function(event)
        
        for other_event in event.get_chained():
            self.__dispatch_recursive(other_event)
    
    def dispatch_all(self, events):
        for event in events:
            self.dispatch(event)
