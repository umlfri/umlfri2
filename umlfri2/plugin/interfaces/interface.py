from weakref import ref


class Interface:
    def __init__(self, executor):
        self.__executor = executor
    
    @property
    def id(self):
        raise NotImplementedError
    
    @property
    def type(self):
        return self.__class__.__name__[1:]
    
    @property
    def _executor(self):
        return self.__executor
    
    def _ref(self, object):
        return ref(object, self.__removed)
    
    def __removed(self, object):
        self.__executor.object_removed(self)
