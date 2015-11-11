class Solution:
    def __init__(self, project):
        self.__project = project
    
    @property
    def projects(self):
        yield self.__project
