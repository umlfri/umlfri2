class Context:
    def __init__(self):
        self.__locals = {}
    
    def get_variable(self, name):
        return self.__locals[name]
    
    def as_dict(self):
        return self.__locals.copy()
    
    def extend(self, item, name = None):
        # dont call constructor
        ret = object.__new__(Context)
        ret.__locals = self.__locals.copy()
        if name is None:
            ret.__locals.update(item.get_values())
        else:
            ret.__locals[name] = item
        return ret
