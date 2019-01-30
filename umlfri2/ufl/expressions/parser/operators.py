from collections import namedtuple
from enum import Enum, unique
from itertools import zip_longest, islice


@unique
class PriorityGroup(Enum):
    Unary = 1
    Power = 2
    Multiplicative = 3
    Additive = 4
    Relational = 5
    LogicalAdditive = 6
    LogicalMultiplicative = 7


BINARY_PRIORITIES = {
    '*': PriorityGroup.Multiplicative,
    '/': PriorityGroup.Multiplicative,
    '//': PriorityGroup.Multiplicative,
    '%': PriorityGroup.Multiplicative,
    '+': PriorityGroup.Additive,
    '-': PriorityGroup.Additive,
    '>': PriorityGroup.Relational,
    '>=': PriorityGroup.Relational,
    '<': PriorityGroup.Relational,
    '<=': PriorityGroup.Relational,
    '==': PriorityGroup.Relational,
    '!=': PriorityGroup.Relational,
    '||': PriorityGroup.LogicalAdditive,
    '&&': PriorityGroup.LogicalMultiplicative,
}

BINARY_OPERATOR_SYNONYMS = {
    'gt': '>',
    'lt': '<',
    'ge': '>=',
    'le': '<=',
    'eq': '==',
    'ne': '!=',
    'and': '&&',
    'or': '||',
}

BINARY_OPERATORS = tuple(BINARY_PRIORITIES.keys()) + tuple(BINARY_OPERATOR_SYNONYMS.keys())

UNARY_OPERATOR_LIST = ('!', '-', '+')

UNARY_OPERATOR_SYNONYMS = {
    'not': '!',
}

UNARY_OPERATORS = tuple(UNARY_OPERATOR_LIST) + tuple(UNARY_OPERATOR_SYNONYMS.keys())

OPERATOR_KEYWORDS = tuple(BINARY_OPERATOR_SYNONYMS.keys()) + tuple(UNARY_OPERATOR_SYNONYMS.keys())


def get_priority(operator):
    return BINARY_PRIORITIES[operator].value


def get_binary_operator(operator):
    return BINARY_OPERATOR_SYNONYMS.get(operator, operator)


def get_unary_operator(operator):
    return UNARY_OPERATOR_SYNONYMS.get(operator, operator)


operator_tree_stack_node = namedtuple('operator_tree_stack_node', ['value', 'operator'])


def make_binary_operator_tree(linear, mk_node=lambda a, op, b: (a, op, b)):
    stack = []
    
    for value, operator in zip_longest(islice(linear, 0, None, 2), islice(linear, 1, None, 2)):
        operator = get_binary_operator(operator)
        while stack and (operator is None or get_priority(stack[-1].operator) <= get_priority(operator)):
            top_value, top_operator = stack.pop(-1)
            value = mk_node(top_value, top_operator, value)
        stack.append(operator_tree_stack_node(value, operator))
    
    if len(stack) > 1 or stack[0].operator is not None:
        raise Exception("Weird expression")
    
    return stack[0].value


def make_unary_operator_tree(linear, mk_node=lambda op, a: (op, a)):
    value = linear[-1]
    for operator in islice(reversed(linear), 1, None):
        operator = get_unary_operator(operator)
        value = mk_node(operator, value)
    return value
