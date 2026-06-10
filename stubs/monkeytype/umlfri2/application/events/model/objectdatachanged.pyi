from typing import Union
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.ufl.objects.patch.object import UflObjectPatch


class ObjectDataChangedEvent:
    def __init__(
        self,
        object: Union[ElementObject, ConnectionObject],
        patch: UflObjectPatch
    ) -> None: ...
    @property
    def object(
        self
    ) -> Union[ElementObject, ConnectionObject]: ...
