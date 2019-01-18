from collections import namedtuple

ArgumentTypeCheckerResult = namedtuple('ArgumentTypeCheckerResult', ('argument_types', 'result_type'))


class ArgumentTypeChecker:
    def check_arguments(self, self_type, expected_types, return_type):
        raise NotImplementedError
