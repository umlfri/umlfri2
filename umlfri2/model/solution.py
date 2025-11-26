from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from umlfri2.model import Project, ElementObject, Diagram


class Solution:
    def __init__(self, project: Optional[Project] = None, save_id: Optional[UUID] = None) -> None:
        if project is None:
            self.__projects = []
        else:
            self.__projects = [project]
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    def add_project(self, project: Project) -> None:
        self.__projects.append(project)
    
    def remove_project(self, project: Project) -> None:
        self.__projects.remove(project)
    
    @property
    def children(self) -> Iterator[Project]:
        yield from self.__projects
    
    @property
    def save_id(self) -> UUID:
        return self.__save_id
    
    def get_all_diagrams(self) -> Iterator[Diagram]:
        for element in self.get_all_elements():
            yield from element.diagrams
    
    def get_all_elements(self) -> Iterator[ElementObject]:
        def recursion(obj):
            for child in obj.children:
                yield child
                yield from recursion(child)
        
        for project in self.__projects:
            yield from recursion(project)
    
    def invalidate_all_caches(self) -> None:
        for project in self.__projects:
            project.invalidate_all_caches()
