import os.path

from PyQt5.QtGui import QPixmap

from umlfri2.constants.paths import GRAPHICS

def get_pinned_icon():
    icon = QPixmap()
    
    return icon

class IconResources:
    __loaded = False
    
    def __load(self):
        self.PINNED = QPixmap()
        self.PINNED.load(os.path.join(GRAPHICS, "state", "pinned.png"))
    
    def __getattr__(self, item):
        if self.__loaded:
            raise AttributeError(item)
        
        self.__loaded = True
        self.__load()
        return getattr(self, item)

ICONS = IconResources()
