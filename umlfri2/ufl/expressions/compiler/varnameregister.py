from itertools import count

from umlfri2.types.enums import ALL_ENUMS


class VariableNameRegister:
    def __init__(self, user_variable_prefix):
        self.__variable_count = 0
        self.__registered_functions = {}
        self.__registered_function_names = set()
        self.__user_variable_prefix = user_variable_prefix
    
    def register_temp_variable(self):
        self.__variable_count += 1
        return "_{0}".format(self.__variable_count)
    
    def register_function(self, function):
        if function in self.__registered_functions:
            return self.__registered_functions[function]
        
        name = function.__name__.strip('_')
        
        if name.startswith(self.__user_variable_prefix) or name in ALL_ENUMS or name in self.__registered_function_names:
            name_fmt = name + '{0}'
            for i in count(start=1):
                name = name_fmt.format(i)
                if name not in self.__registered_function_names:
                    break
        
        self.__registered_functions[name] = function
        self.__registered_function_names.add(name)
        
        return name
    
    def build_globals(self):
        return {i[1]: i[0] for i in self.__registered_functions.items()}
