from umlfri2.datalayer import AddOnLoader


class AddOnManager:
    def __init__(self):
        self.__addons = []
    
    def load_addons(self, storage):
        for dir in storage.list():
            with storage.create_substorage(dir) as addon_storage:
                loader = AddOnLoader(addon_storage)
                if loader.is_addon():
                    self.__addons.append(loader.load())
    
    def get_addon(self, identifier):
        for addon in self.__addons:
            if addon.identifier == identifier:
                return addon
    
    def start_all(self):
        def recursion(addon):
            if addon.is_started:
                return
            
            for dependency in addon.dependencies:
                recursion(self.get_addon(dependency))
            
            addon.start()
        
        for addon in self.__addons:
            recursion(addon)
    
    def stop_all(self):
        reverse_dependencies = {}
        
        for addon in self.__addons:
            for dependency in addon.dependencies:
                reverse_dependencies.setdefault(dependency, []).append(addon.identifier)
        
        def recursion(addon):
            if not addon.is_started:
                return
            
            for dependency in reverse_dependencies.get(addon.identifier, ()):
                recursion(self.get_addon(dependency))
            
            addon.stop()
        
        for addon in self.__addons:
            recursion(addon)
    
    def __iter__(self):
        yield from self.__addons
