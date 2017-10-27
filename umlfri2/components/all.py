from .common import COMMON_COMPONENTS
from .connectionline import CONNECTION_LINE_COMPONENTS
from .graphic import GRAPHIC_COMPONENTS
from .pathpart import PATH_COMPONENTS
from .text import TEXT_COMPONENTS
from .visual import VISUAL_COMPONENTS, TABLE_COMPONENTS

ALL_COMPONENTS = {
    'visual': VISUAL_COMPONENTS.copy(),
    'table': TABLE_COMPONENTS.copy(),
    'graphic': GRAPHIC_COMPONENTS.copy(),
    'pathpart': PATH_COMPONENTS.copy(),
    'text': TEXT_COMPONENTS.copy(),
    'connection': CONNECTION_LINE_COMPONENTS.copy()
}

for components in ALL_COMPONENTS.values():
    components.update(COMMON_COMPONENTS)
