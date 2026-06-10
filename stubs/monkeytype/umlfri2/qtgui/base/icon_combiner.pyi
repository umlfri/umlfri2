from PyQt5.QtCore import QSize
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
)
from typing import (
    List,
    Optional,
)


def combine_icons(
    icon: QIcon,
    overlay: QPixmap,
    sizes: Optional[List[QSize]] = ...
) -> QIcon: ...
