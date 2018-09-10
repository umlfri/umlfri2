import pyparsing as pp

from .operators import BINARY_OPERATORS, UNARY_OPERATORS

EXPRESSION = pp.Forward()

VARIABLE_METADATA_NAME = pp.pyparsing_common.identifier.copy()
VARIABLE_METADATA_ACCESS = '@' + VARIABLE_METADATA_NAME

VARIABLE = pp.pyparsing_common.identifier.copy()

TARGET = VARIABLE | ('(' + EXPRESSION + ')') | VARIABLE_METADATA_ACCESS

MEMBER_NAME = pp.pyparsing_common.identifier.copy()
ARGUMENTS = '(' + pp.Optional(pp.delimitedList(EXPRESSION, delim=",")) + ')'
METHOD_ATTRIBUTE_OR_ENUM = TARGET + pp.ZeroOrMore(pp.oneOf(('.', '->', '.@' , '::')) + MEMBER_NAME + pp.Optional(ARGUMENTS))

STRING = pp.QuotedString(quoteChar="'", escChar="\\")
NUMBER = pp.Regex("[0-9]+(\\.[0-9]+)?")

VALUE = METHOD_ATTRIBUTE_OR_ENUM | STRING | NUMBER

UNARY = pp.ZeroOrMore(pp.oneOf(UNARY_OPERATORS)) + VALUE

BINARY = UNARY + pp.ZeroOrMore(pp.oneOf(BINARY_OPERATORS) + UNARY)

LAMBDA_EXPRESSION = '[' + pp.OneOrMore(':' + pp.pyparsing_common.identifier.copy()) + '|' + EXPRESSION + ']'

EXPRESSION << (BINARY | LAMBDA_EXPRESSION)

WHOLE_EXPRESSION = pp.StringStart() + EXPRESSION + pp.StringEnd()
