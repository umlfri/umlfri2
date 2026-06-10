from umlfri2.model.project import Project


class ProjectChangedEvent:
    def __init__(self, project: Project) -> None: ...
    @property
    def project(self) -> Project: ...
