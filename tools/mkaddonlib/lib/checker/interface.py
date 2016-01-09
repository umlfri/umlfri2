from lib.checker.method import UmlFriInterfaceMethod


class UmlFriInterface:
    def __init__(self, name, methods, removed=(), change=None):
        self.__name = name
        self.__methods = tuple(methods)
        self.__removed_methods = tuple(removed)
        self.__change = change
    
    @property
    def name(self):
        return self.__name
    
    @property
    def methods(self):
        yield from self.__methods
    
    @property
    def has_removed_methods(self):
        return len(self.__removed_methods) > 0
    
    @property
    def removed_methods(self):
        yield from self.__removed_methods
    
    @property
    def has_change(self):
        return self.__change is not None
    
    @property
    def change(self):
        return self.__change

    @staticmethod
    def create_from(interface):
        methods = []
        for child in interface.children:
            if child.type_name == 'InterfaceMethod':
                methods.append(UmlFriInterfaceMethod.create_from(child))
            elif child.type_name == 'InterfaceProperty':
                for member in child.children:
                    if member.type_name in ('InterfacePropertyGetter', 'InterfacePropertySetter',
                                            'InterfacePropertyIterator'):
                        methods.append(UmlFriInterfaceMethod.create_from(member.create_method()))
        
        return UmlFriInterface(interface.name, methods, change='added')
    
    def fix_from(self, interface):
        if self.__name != interface.api_name:
            raise Exception
        
        old_methods = {method.name: method for method in self.__methods}
        new_methods = []
        
        for child in interface.children:
            if child.type_name == 'InterfaceMethod':
                method = self.__fix_method_from(child, old_methods.get(child.api_name))
                new_methods.append(method)
                if method.name in old_methods:
                    del old_methods[method.name]
            elif child.type_name == 'InterfaceProperty':
                for member in child.children:
                    if member.type_name in ('InterfacePropertyGetter', 'InterfacePropertySetter',
                                            'InterfacePropertyIterator'):
                        method = self.__fix_method_from(member.create_method(member.api_name),
                                                        old_methods.get(member.api_name))
                        new_methods.append(method)
                        if method.name in old_methods:
                            del old_methods[method.name]
        
        return UmlFriInterface(self.__name, new_methods, old_methods.values())

    def __fix_method_from(self, new_method, old_method):
        if old_method is None:
            return UmlFriInterfaceMethod.create_from(new_method, change='added')
        else:
            return old_method.fix_from(new_method)
