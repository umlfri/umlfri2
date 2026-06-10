from typing import Union
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementobject import ElementObject


class ProjectMimeData:
    def __init__(
        self,
        model_object: Union[Diagram, ElementObject]
    ) -> None: ...
    @property
    def model_object(self) -> Union[Diagram, ElementObject]: ...
