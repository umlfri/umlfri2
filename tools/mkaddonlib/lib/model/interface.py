from .basecontainer import BaseContainer
from . import helper


class Interface(BaseContainer):
    def __init__(self, name, namespace, api_name=None, base=None, abstract=False, generate=True, documentation=None):
        BaseContainer.__init__(self, name, namespace)
        
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_interface_api_name(self.identifier)
        
        self.__base = base
        self.__abstract = abstract
        self.__generate = generate
        self.__documentation = documentation
        self.__descendants = []
    
    @property
    def namespace(self):
        return self.parent
    
    @property
    def api_name(self):
        return self.__api_name
    
    @property
    def base(self):
        return self.__base
    
    @property
    def is_abstract(self):
        return self.__abstract
    
    @property
    def generate(self):
        return self.__generate
    
    @property
    def documentation(self):
        return self.__documentation
    
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
    
    @property
    def referenced(self):
        ret = set()
        if self.__base is not None:
            ret.add(self.__base)
        
        for child in self.children:
            for type in child.referenced:
                ret.add(type)
        
        for obj in ret:
            yield obj
    
    def validate(self):
        BaseContainer.validate(self)
        
        if self.__base is not None and not self.__base.is_abstract:
            raise Exception("Base interface of %s is not marked as abstract" % self.fqn)
    
    def _link(self, builder):
        BaseContainer._link(self, builder)
        
        if self.__base is not None:
            self.__base = builder.get_type_by_name(self.__base)
            
            if not isinstance(self, Interface):
                raise Exception
            
            self.__base.__descendants.append(self)
