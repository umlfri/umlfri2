from weakref import WeakKeyDictionary

from PyQt5.QtGui import QPixmap, QIcon


pixmap_cache = WeakKeyDictionary()
icon_cache = WeakKeyDictionary()


def load_from_cache(cache, image, factory):
    storage_cache = cache.setdefault(image.storage, {})
    if image.path in storage_cache:
        return storage_cache[image.path]
    
    ret = factory(image)
    
    storage_cache[image.path] = ret
    return ret


def load(image):
    def factory(image):
        pix = QPixmap()
        pix.loadFromData(image.load().read())
        return pix
    return load_from_cache(pixmap_cache, image, factory)


def load_icon(image):
    return load_from_cache(icon_cache, image, lambda image: QIcon(load(image)))
