from weakref import WeakSet


class ModelTemporaryDataCache:
    def __init__(self, callback):
        self.__reverse_dependencies = WeakSet()
        self.__invalidated = True
        self.__callback = callback
        self.__is_refreshing = False
    
    def depend_on(self, cache):
        cache.__reverse_dependencies.add(self)
    
    def invalidate(self):
        self.__invalidated = True
    
    def refresh(self, **kwargs):
        self.__is_refreshing = True
        if self.__callback is not None:
            self.__callback(**kwargs)
        
        for dependant in self.__reverse_dependencies:
            dependant.invalidate()
        self.__invalidated = False
    
    def ensure_valid(self, **kwargs):
        if self.__invalidated:
            self.refresh(**kwargs)
