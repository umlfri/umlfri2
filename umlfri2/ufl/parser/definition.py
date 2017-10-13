import pyparsing as pp

EXPRESSION = pp.Forward()

METADATA_ACCESS = '@(' + EXPRESSION + ')'

VARIABLE = pp.pyparsing_common.identifier.copy()

TARGET = VARIABLE ^ ('(' + EXPRESSION + ')') ^ METADATA_ACCESS

METHODORATTRORENUM = TARGET + (
    pp.OneOrMore(
        '.' + pp.pyparsing_common.identifier.copy()
        + pp.Optional('(' + pp.Optional(
            pp.Optional(EXPRESSION) + pp.ZeroOrMore("," + pp.Optional(EXPRESSION))
        ) + ')')
    ) |
    pp.Optional('::' + pp.pyparsing_common.identifier.copy())
)

STRING = pp.QuotedString(quoteChar="'", escChar="\\")
NUMBER = pp.Regex("[0-9]+(\\.[0-9]+)?")

VALUE = METHODORATTRORENUM ^ STRING ^ NUMBER

UNARY = pp.ZeroOrMore("!") + VALUE

BINARY = UNARY + pp.Optional(pp.oneOf(["<=", "<", "==", "!=", ">=", ">"]) + UNARY)

EXPRESSION << BINARY

WHOLE_EXPRESSION = pp.StringStart() + EXPRESSION + pp.StringEnd()
