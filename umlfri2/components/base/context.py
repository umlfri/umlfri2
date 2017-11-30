class Context:
    def __init__(self):
        self.__locals = {}
    
    def get_variable(self, name):
        return self.__locals[name]
    
    def as_dict(self, prefix=None):
        if prefix is None:
            return self.__locals.copy()
        else:
            return {prefix + k: v for k, v in self.__locals.items()}
    
    def set_variable(self, name, item):
        ret = Context()
        ret.__locals = self.__locals.copy()
        ret.__locals[name] = item
        return ret
