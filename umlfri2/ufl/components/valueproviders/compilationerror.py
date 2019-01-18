class ValueCompilationError(Exception):
    def __init__(self, source):
        self.__source = source
    
    def __str__(self):
        if self.__source is not None:
            return "Compilation error for value in file {0} at position {1} ({2})".format(
                self.__source.file_name, self.__source.line_number, self.__cause__
            )
        else:
            return "Compilation error ({0})".format(self.__cause__)
