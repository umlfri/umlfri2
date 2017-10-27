import os.path

from PyQt5.QtGui import QPixmap

from umlfri2.constants.paths import GRAPHICS


class IconResources:
    __loaded = False
    
    def __load(self):
        self.PINNED = QPixmap()
        self.PINNED.load(os.path.join(GRAPHICS, "state", "pinned.png"))
        self.LOCKED = QPixmap()
        self.LOCKED.load(os.path.join(GRAPHICS, "state", "locked.png"))
    
    def __getattr__(self, item):
        if self.__loaded:
            raise AttributeError(item)
        
        self.__loaded = True
        self.__load()
        return getattr(self, item)


ICONS = IconResources()
