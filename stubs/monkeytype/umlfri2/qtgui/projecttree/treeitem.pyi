from typing import Union
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.model.project import Project


class ProjectTreeItem:
    def __init__(
        self,
        model_object: Union[ElementObject, Diagram, Project]
    ) -> None: ...
    @property
    def model_object(
        self
    ) -> Union[ElementObject, Diagram, Project]: ...
    def refresh(self) -> None: ...
    def set_drop_enabled(self, enabled: bool) -> None: ...
