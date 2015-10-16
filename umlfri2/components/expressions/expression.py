class Expression:
    def compile(self, variables, expected_type):
        raise NotImplementedError
    
    def get_type(self):
        raise NotImplementedError
    
    def __call__(self, context):
        raise NotImplementedError
