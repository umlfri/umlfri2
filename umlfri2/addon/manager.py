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
        for addon in self.__addons:
            self.__start_recursive_if_needed(addon)
    
    def __start_recursive_if_needed(self, addon):
        if addon.is_started:
            return
        
        for dependency in addon.dependencies:
            self.__start_recursive_if_needed(self.get_addon(dependency))
        
        addon.start()
    
    def __iter__(self):
        yield from self.__addons
