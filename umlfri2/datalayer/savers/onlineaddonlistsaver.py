from ..constants import ONLINE_ADDON_LAST_VERSION_FILE


class OnlineAddOnListSaver:
    def __init__(self, storage):
        self.__storage = storage
    
    def save(self, zipball_storage, version):
        self.__storage.copy_from(zipball_storage)
        self.__storage.store_string(ONLINE_ADDON_LAST_VERSION_FILE, version)
