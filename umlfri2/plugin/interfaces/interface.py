class params:
    def __init__(self, *types):
        self.__types = types
    
    def __call__(self, fnc):
        fnc.method_param_types = self.__types
        return fnc


def polymorphic(fnc):
    fnc.method_polymorfic = True
    return fnc


class Interface:
    @property
    def id(self):
        raise NotImplementedError
    
    @property
    def type(self):
        return self.__class__.__name__[1:]
