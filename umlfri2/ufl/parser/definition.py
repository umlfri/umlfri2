import pyparsing as pp

EXPRESSION = pp.Forward()

METADATA_ACCESS = '@(' + EXPRESSION + ')'

VARIABLE = pp.pyparsing_common.identifier

TARGET = VARIABLE ^ ('(' + EXPRESSION + ')') ^ METADATA_ACCESS

METHODORATTRORENUM = TARGET + (
    pp.OneOrMore(
        '.' + pp.Word(pp.alphanums)
        + pp.Optional('(' + pp.Optional(
            pp.Optional(EXPRESSION) + pp.ZeroOrMore("," + pp.Optional(EXPRESSION))
        ) + ')')
    ) |
    pp.Optional('::' + pp.Word(pp.alphanums))
)

STRING = pp.QuotedString(quoteChar="'", escChar="\\")
NUMBER = pp.pyparsing_common.real

VALUE = METHODORATTRORENUM ^ STRING ^ NUMBER

RELATIONAL = VALUE + pp.Optional(pp.oneOf(["<=", "<", "==", "!=", ">=", ">"]) + VALUE)

EXPRESSION << RELATIONAL

WHOLE_EXPRESSION = pp.StringStart() + EXPRESSION + pp.StringEnd()
