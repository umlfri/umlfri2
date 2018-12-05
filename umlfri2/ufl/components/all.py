from .base.componenttype import ComponentType
from .common import COMMON_COMPONENTS
from .connectionvisual import CONNECTION_VISUAL_COMPONENTS
from .graphic import GRAPHIC_COMPONENTS
from .pathpart import PATH_COMPONENTS
from .text import TEXT_COMPONENTS
from .visual import VISUAL_COMPONENTS, TABLE_COMPONENTS

ALL_COMPONENTS = {
    ComponentType.visual: VISUAL_COMPONENTS.copy(),
    ComponentType.table: TABLE_COMPONENTS.copy(),
    ComponentType.graphic: GRAPHIC_COMPONENTS.copy(),
    ComponentType.path_part: PATH_COMPONENTS.copy(),
    ComponentType.text: TEXT_COMPONENTS.copy(),
    ComponentType.connection_visual: CONNECTION_VISUAL_COMPONENTS.copy()
}

for components in ALL_COMPONENTS.values():
    components.update(COMMON_COMPONENTS)
