class PythonExpression:
    """
    Expression type supposed to be used to debugging purposes only.
    """
    
    def __init__(self, expr):
        self.__expr = expr
    
    def __call__(self, context):
        return self.__expr(**context.as_dict())
