from PyQt5.QtGui import (
    QIcon,
    QPixmap,
)
from typing import (
    Callable,
    Union,
)
from umlfri2.types.image import Image
from weakref import WeakKeyDictionary


def load(image: Image) -> QPixmap: ...


def load_from_cache(
    cache: WeakKeyDictionary,
    image: Image,
    factory: Callable
) -> Union[QPixmap, QIcon]: ...


def load_icon(image: Image) -> QIcon: ...
