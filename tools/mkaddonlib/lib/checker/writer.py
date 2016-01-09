import os


class UmlFriInterfaceWriter:
    def __init__(self, interfaces):
        self.__interfaces = tuple(interfaces)
    
    def write_to(self, directory):
        for interface in self.__interfaces:
            file_name = os.path.join(directory, "{0}.py".format(interface.name.lower()))
            with open(file_name, "w") as file:
                self.__write_interface(file, interface)
    
    def __write_interface(self, file, interface):
        file.write('from .interface import Interface\n\n\n')
        if interface.has_change:
            file.write('# change: {0}\n'.format(interface.change))
        file.write('class I{0}(Interface):\n'.format(interface.name))
        file.write('    def __init__(self, executor):\n')
        file.write('        self.__executor = executor\n\n')
        file.write('    @property\n')
        file.write('    def id(self):\n')
        file.write('        raise NotImplementedError\n\n')
        file.write('    @property\n')
        file.write('    def api_name(self):\n')
        file.write('        return \'{0}\'\n'.format(interface.name))
        for method in interface.methods:
            self.__write_method(file, method)
        
        if interface.has_removed_methods:
            file.write('\n')
            for method in interface.removed_methods:
                file.write('    # removed: {0}\n'.format(method.name))
    
    def __write_method(self, file, method):
        file.write('\n')
        if method.has_change:
            file.write('    # change: {0}\n'.format(method.change))
        file.write('    def {0}(self'.format(method.name))
        for parameter in method.parameters:
            self.__write_parameter(file, parameter)
        file.write(')')
        if method.polymorfic:
            file.write(' -> object')
        file.write(':\n')
        file.write('        raise NotImplementedError\n')
    
    def __write_parameter(self, file, parameter):
        if parameter.type is None:
            file.write(', {0}: None'.format(parameter.name))
        else:
            file.write(', {0}: {1}'.format(parameter.name, parameter.type.__name__))
