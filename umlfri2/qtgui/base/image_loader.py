from weakref import WeakKeyDictionary

from PySide.QtGui import QPixmap, QIcon


icon_cache = WeakKeyDictionary()


def load(image):
    pix = QPixmap()
    pix.loadFromData(image.load().read())
    return pix


def load_icon(image):
    storage_icon_cache = icon_cache.setdefault(image.storage, {})
    if image.path in storage_icon_cache:
        return storage_icon_cache[image.path]
    icon = QIcon(load(image))
    storage_icon_cache[image.path] = icon
    return icon
