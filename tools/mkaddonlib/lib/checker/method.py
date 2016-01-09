from lib.checker.parameter import UmlFriInterfaceMethodParameter
from lib.model.primitivetype import PrimitiveType


class UmlFriInterfaceMethod:
    def __init__(self, name, parameters, polymorfic, change=None):
        self.__name = name
        self.__parameters = tuple(parameters)
        self.__polymorfic = polymorfic
        self.__change = change
    
    @property
    def name(self):
        return self.__name
    
    @property
    def has_parameters(self):
        return len(self.__parameters) > 0
    
    @property
    def parameters(self):
        yield from self.__parameters
    
    @property
    def polymorfic(self):
        return self.__polymorfic
    
    @property
    def has_change(self):
        return self.__change is not None
    
    @property
    def change(self):
        return self.__change

    @staticmethod
    def create_from(new_method, change=None):
        parameters = []
        
        for name, type in UmlFriInterfaceMethod.__build_new_parameters(new_method):
            parameters.append(UmlFriInterfaceMethodParameter(name, type))
        
        if new_method.return_type is None or isinstance(new_method.return_type.type, PrimitiveType):
            polymorfic = False
        else:
            polymorfic = new_method.return_type.type.is_abstract
        
        return UmlFriInterfaceMethod(new_method.api_name, parameters, polymorfic, change=change)
    
    def fix_from(self, new_method):
        if self.name != new_method.api_name:
            raise Exception

        new_parameters = tuple(self.__build_new_parameters(new_method))
        
        changed = False
        if len(new_parameters) != len(self.__parameters):
            changed = True
        else:
            for new, old in zip(new_parameters, self.__parameters):
                if new[0] != old.name:
                    changed = True
                    break
                if new[1] != old.type:
                    changed = True
                    break
        
        if new_method.return_type is None or isinstance(new_method.return_type.type, PrimitiveType):
            polymorfic = False
        else:
            polymorfic = new_method.return_type.type.is_abstract
        
        if self.__polymorfic != polymorfic:
            changed = True
        
        if changed:
            return UmlFriInterfaceMethod.create_from(new_method, change='changed')
        else:
            return self
    
    @staticmethod
    def __build_new_parameters(new_method):
        for parameter in new_method.parameters:
            if isinstance(parameter.type, PrimitiveType):
                if parameter.type.name == 'boolean':
                    type = bool
                elif parameter.type.name == 'int32':
                    type = int
                elif parameter.type.name == 'float':
                    type = float
                elif parameter.type.name == 'variant':
                    type = None
                elif parameter.type.name == 'string':
                    type = str
                elif parameter.type.name == 'xy':
                    type = (int, int)
                elif parameter.type.name == 'wh':
                    type = (int, int)
                elif parameter.type.name == 'xywh':
                    type = (int, int, int, int)
                else:
                    raise Exception
            else:
                type = object

            yield parameter.api_name, type
            
