class UflNode:
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
    
    def accept(self, visitor):
        raise NotImplementedError
