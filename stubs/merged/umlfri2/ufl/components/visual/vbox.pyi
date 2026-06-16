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
from umlfri2.ufl.components.base.component import Component
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.visual.rectangle import RectangleComponent
from umlfri2.ufl.components.visual.sizer import SizerComponent

class VBoxObject(BoxObject): ...

class VBoxComponent(BoxComponent):
    def __init__(
        self,
        children: List[Component],
        expand: Union[Dict[RectangleComponent, ConstantValueProvider], Dict[SizerComponent, ConstantValueProvider]]
    ) -> None: ...
