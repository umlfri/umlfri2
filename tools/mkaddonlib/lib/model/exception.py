from .basecontainer import BaseContainer
from . import helper


class ExceptionDefinition(BaseContainer):
    def __init__(self, name, namespace, api_name=None, base=None, documentation=None):
        BaseContainer.__init__(self, name, namespace)
        
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_exception_api_name(self.identifier)
        
        self.__documentation = documentation
        self.__base = base
        self.__descendants = []
    
    @property
    def namespace(self):
        return self.parent
    
    @property
    def api_name(self):
        return self.__api_name
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def base(self):
        return self.__base
    
    @property
    def descendants(self):
        return tuple(self.__descendants)
    
    @property
    def all_bases(self):
        ret = []
        if self.__base is not None:
            base = self.base
            while base is not None:
                ret.insert(0, base)
                base = base.base
        return tuple(ret)
    
    def _link(self, builder):
        BaseContainer._link(self, builder)
        
        if self.__base is not None:
            self.__base = builder.get_type_by_name(self.__base)
            
            if not isinstance(self, ExceptionDefinition):
                raise Exception
            
            self.__base.__descendants.append(self)
