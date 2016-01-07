from .basecontainer import BaseContainer
from . import helper


class Exception(BaseContainer):
    def __init__(self, name, namespace, api_name=None, base=None, throws_from=None, documentation=None):
        BaseContainer.__init__(self, name, namespace)
        
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_event_api_name(self.identifier)
        
        self.__documentation = documentation
        self.__base = base
        if throws_from is None:
            self.__throwsFrom = []
        else:
            self.__throwsFrom = throws_from.split(',')
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
    def throws_from(self):
        return set(self.__throwsFrom)
    
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
            
            if not isinstance(self, Exception):
                raise Exception
            
            self.__base.__descendants.append(self)
