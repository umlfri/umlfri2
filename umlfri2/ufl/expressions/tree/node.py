class UflNode:
    def __init__(self, type):
        self.__type = type
    
    @property
    def type(self):
        return self.__type
    
    def find(self, condition, cut_branch=lambda node: False):
        if condition(self):
            yield self
        
        for param in self._get_params():
            if isinstance(param, UflNode) and not cut_branch(param):
                yield from param.find(condition)
    
    def _get_params(self):
        return ()
    
    def to_string(self):
        ret = self.__class__.__name__ + "("
        first = True
        
        for param in self._get_params():
            if not first:
                ret += ","
            first = False
            if isinstance(param, UflNode):
                ret += param.to_string()
            else:
                ret += repr(param)
        
        ret += ")"
        
        return ret

    def to_string_indented(self, indent=0):
        params = self._get_params()
        name = self.__class__.__name__
        
        if not params:
            return "{0}{1}".format("    " * indent, name)
        elif len(params) == 1 and not isinstance(params[0], UflNode):
            return "{0}{1}({2!r})".format("    " * indent, name, params[0])
        else:
            ret = []
            ret.append("{0}{1}:".format("    " * indent, name))
            
            for param in self._get_params():
                if isinstance(param, UflNode):
                    ret.append(param.to_string_indented(indent+1))
                else:
                    ret.append("{0}{1!r}".format("    " * (indent+1), param))
            
            return "\n".join(ret)
    
    def accept(self, visitor):
        raise NotImplementedError
