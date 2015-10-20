class Context:
    def __init__(self, object, config = None):
        self.__locals = {'self': object}
        if config is not None:
            self.__locals['cfg'] = config
    
    def set_config(self, config):
        if config is None:
            if 'cfg' in self.__locals:
                del self.__locals['cfg']
        else:
            self.__locals['cfg'] = config
    
    def get_variable(self, name):
        return self.__locals[name]
    
    def as_dict(self):
        return self.__locals.copy()
    
    def extend(self, item, name = None):
        ret = object.__new__(Context)
        ret.__locals = self.__locals.copy()
        if name is None:
            # dont call constructor
            ret.__locals.update(item.get_values())
        else:
            ret[name] = item
        return ret
