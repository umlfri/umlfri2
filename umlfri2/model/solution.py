class Solution:
    def __init__(self, project):
        self.__projects = [project]
    
    def add_project(self, project):
        self.__projects.append(project)
    
    @property
    def children(self):
        yield from self.__projects
