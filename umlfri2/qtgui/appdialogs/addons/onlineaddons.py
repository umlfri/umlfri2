from umlfri2.application import Application
from .listwidget import AddOnListWidget


class OnlineAddOnList(AddOnListWidget):
    def _addon_button_factory(self):
        return None

    def _addon_content_menu(self, addon):
        return None

    @property
    def _addons(self):
        return Application().addons.online
    
    def _get_version(self, addon):
        return addon.latest_version.version
