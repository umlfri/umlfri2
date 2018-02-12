class ArgumentTypeChecker:
    @property
    def argument_count(self):
        raise NotImplementedError
    
    def check_argument(self, no, expected_type):
        raise NotImplementedError
