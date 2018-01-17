from .moveto import MoveTo
from .lineto import LineTo
from .cubicto import CubicTo
from .close import Close

PATH_COMPONENTS = {
    'MoveTo': MoveTo,
    'LineTo': LineTo,
    'CubicTo': CubicTo,
    'Close': Close
}
