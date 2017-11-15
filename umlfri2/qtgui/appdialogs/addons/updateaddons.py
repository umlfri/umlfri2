from umlfri2.application import Application
from umlfri2.application.events.addon import AddOnInstalledEvent, AddOnUninstalledEvent
from .listwidget import AddOnListWidget


class UpdateAddOnList(AddOnListWidget):
    def __init__(self):
        super().__init__(check_boxes=True, show_prev_version=True)

        Application().event_dispatcher.subscribe(AddOnInstalledEvent, self.__addon_list_changed)
        Application().event_dispatcher.subscribe(AddOnUninstalledEvent, self.__addon_list_changed)
        
    @property
    def _addons(self):
        for addon in Application().addons.online:
            if addon.local_addon is not None and addon.local_addon.version < addon.latest_version.version:
                yield addon
    
    def _addon_button_factory(self):
        pass
    
    def _addon_content_menu(self, addon):
        pass

    def __addon_list_changed(self, event):
        self.refresh()
