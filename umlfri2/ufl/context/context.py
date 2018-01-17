class Context:
    def __init__(self):
        self.__locals = {}
    
    def get_variable(self, name):
        return self.__locals[name]
    
    def get_variables(self, names):
        return (self.__locals[name] for name in names)
    
    def set_variable(self, name, item):
        ret = Context()
        ret.__locals = self.__locals.copy()
        ret.__locals[name] = item
        return ret
