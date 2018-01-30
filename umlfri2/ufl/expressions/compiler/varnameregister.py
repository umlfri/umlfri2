from itertools import count


class VariableNameRegister:
    def __init__(self, user_variable_prefix):
        self.__variable_count = 0
        self.__registered_values = {}
        self.__registered_value_names = set()
        self.__user_variable_prefix = user_variable_prefix
    
    def register_temp_variable(self):
        self.__variable_count += 1
        return "_{0}".format(self.__variable_count)
    
    def register_function(self, function):
        return self.__register_value(function.__name__, function)
    
    def register_class(self, class_):
        return self.__register_value(class_.__name__, class_)
    
    def __register_value(self, name, value):
        if value in self.__registered_values:
            return self.__registered_values[value]
        
        name = name.strip('_')
        
        if name.startswith(self.__user_variable_prefix) or name in self.__registered_value_names:
            name_fmt = name + '{0}'
            for i in count(start=1):
                name = name_fmt.format(i)
                if name not in self.__registered_value_names:
                    break
        
        self.__registered_values[value] = name
        self.__registered_value_names.add(name)
        
        return name
    
    def build_globals(self):
        return {i[1]: i[0] for i in self.__registered_values.items()}
