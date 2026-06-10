from umlfri2.model.project import Project


class OpenProjectEvent:
    def __init__(self, project: Project) -> None: ...
    @property
    def project(self) -> Project: ...
