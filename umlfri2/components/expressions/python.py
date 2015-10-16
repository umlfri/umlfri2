from .expression import Expression

class PythonExpression(Expression):
    """
    Expression type supposed to be used for debugging purposes only.
    """
    
    def __init__(self, expr, return_type):
        self.__expr = expr
        self.__return_type = return_type
    
    def compile(self, variables):
        pass
    
    def get_type(self):
        return self.__return_type
    
    def __call__(self, context):
        return self.__expr(**context.as_dict())
