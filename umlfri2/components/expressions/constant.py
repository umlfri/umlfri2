class ConstantExpression:
    def __init__(self, value):
        self.__value = value
    
    def get_type(self, types):
        return type(self.__value)
    
    def __call__(self, context):
        return self.__value

NoneExpression = ConstantExpression(None)
