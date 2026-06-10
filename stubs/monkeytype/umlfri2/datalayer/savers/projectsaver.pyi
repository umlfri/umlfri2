from umlfri2.datalayer.storages.zip import ZipStorage
from umlfri2.model.project import Project
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ProjectSaver:
    def __init__(
        self,
        storage: ZipStorage,
        path: str,
        ruler: QTRuler
    ) -> None: ...
    def save(self, project: Project) -> None: ...
