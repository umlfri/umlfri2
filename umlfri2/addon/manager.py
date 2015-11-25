from umlfri2.datalayer import AddOnLoader


class AddOnManager:
    def __init__(self, storage):
        self.__addons = []
        for dir in storage.list():
            with storage.create_substorage(dir) as addon_storage:
                loader = AddOnLoader(addon_storage)
                if loader.is_addon():
                    self.__addons.append(loader.load())
    
    def get_addon(self, identifier):
        for addon in self.__addons:
            if addon.identifier == identifier:
                return addon
    
    def __iter__(self):
        yield from self.__addons
