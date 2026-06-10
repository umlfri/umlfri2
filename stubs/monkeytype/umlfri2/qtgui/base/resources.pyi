from PyQt5.QtGui import QPixmap


class IconResources:
    def __getattr__(self, item: str) -> QPixmap: ...
