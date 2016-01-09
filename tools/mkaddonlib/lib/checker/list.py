from lib.checker.interface import UmlFriInterface


class UmlFriInterfaceList:
    def __init__(self, interfaces):
        self.__interfaces = tuple(interfaces)
    
    def fix_from(self, interfaces):
        new_interfaces = []
        old_interfaces = {interface.name: interface for interface in self.__interfaces}
        
        for obj in interfaces:
            if obj.api_name in old_interfaces:
                new_interfaces.append(old_interfaces[obj.api_name].fix_from(obj))
                del old_interfaces[obj.api_name]
            else:
                new_interfaces.append(UmlFriInterface.create_from(obj))
        
        return UmlFriInterfaceList(new_interfaces)
    
    def __iter__(self):
        yield from self.__interfaces
