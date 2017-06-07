import os.path
import sys
import traceback
from collections import namedtuple

from umlfri2.constants.paths import ROOT_DIR


ExceptionInfoLine = namedtuple('ExceptionInfoLine', ['filename', 'module', 'lineno', 'function', 'text'])


class ExceptionInfo:
    def __init__(self, type_name, description, traceback, cause=None, context=None):
        self.__type_name = type_name
        self.__description = description
        self.__traceback = traceback
        self.__cause = cause
        self.__context = context

    @staticmethod
    def from_exception(exception):
        if exception.__cause__ is not None:
            cause = ExceptionInfo.from_exception(exception.__cause__)
            context = None
        elif exception.__context__ is not None:
            cause = None
            context = ExceptionInfo.from_exception(exception.__context__)
        else:
            cause = None
            context = None
        
        tb = []
        for filename, lineno, function, text in traceback.extract_tb(exception.__traceback__):
            module = ExceptionInfo.__path_to_module(filename)
            
            if module is None:
                if filename.startswith(ROOT_DIR):
                    filename = filename[len(ROOT_DIR) + 1:]
                tb.append(ExceptionInfoLine(filename, None, lineno, function, text))
            else:
                tb.append(ExceptionInfoLine(None, module, lineno, function, text))
        
        type_name = type(exception).__name__
        desc = str(exception)
        
        return ExceptionInfo(type_name, desc, tb, cause, context)
    
    @staticmethod
    def __path_to_module(path):
        try:
            npath = os.path.normpath(path)
        except:
            return None

        for name, module in sys.modules.items():
            if hasattr(module, '__file__'):
                try:
                    mpath = os.path.normpath(module.__file__)
                except:
                    continue

                if mpath == npath:
                    return name

        return None
    
    @property
    def type_name(self):
        return self.__type_name
    
    @property
    def description(self):
        return self.__description
    
    @property
    def traceback(self):
        yield from self.__traceback
    
    @property
    def cause(self):
        return self.__cause
    
    @property
    def context(self):
        return self.__context
