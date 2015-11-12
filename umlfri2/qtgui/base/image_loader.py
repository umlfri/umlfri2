from PySide.QtGui import QPixmap, QIcon


def load(image):
    pix = QPixmap()
    pix.loadFromData(image.load().read())
    return pix


def load_icon(image):
    return QIcon(load(image))
