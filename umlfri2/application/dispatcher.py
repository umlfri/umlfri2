class EventDispatcher:
    def __init__(self):
        self.__events = {}
    
    def register(self, event_type, function):
        self.__events.setdefault(event_type, []).append(function)
    
    def deregister(self, event_type, function):
        self.__events[event_type].remove(function)
    
    def dispatch(self, event):
        for function in self.__events.get(event.__class__, ()):
            function(event)
    
    def dispatch_all(self, events):
        for event in events:
            self.dispatch(event)
