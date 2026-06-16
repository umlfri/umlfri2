from .box import BoxComponent as BoxComponent, BoxObject as BoxObject
from umlfri2.types.geometry import Point as Point, Size as Size
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Tuple,
    Union,
)
from umlfri2.types.geometry.point import Point
from umlfri2.types.geometry.size import Size
from umlfri2.types.threestate import MaybeType
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.visual.padding import PaddingComponent
from umlfri2.ufl.components.visual.sizer import SizerComponent

class HBoxObject(BoxObject): ...

class HBoxComponent(BoxComponent):
    def __init__(
        self,
        children: List[Union[SizerComponent, PaddingComponent]],
        expand: Dict[SizerComponent, ConstantValueProvider]
    ) -> None: ...
