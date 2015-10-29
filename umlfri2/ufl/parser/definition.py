import pyparsing as pp

EXPRESSION = pp.Forward()

VARIABLE = pp.Word(pp.alphas)

TARGET = VARIABLE ^ ('(' + EXPRESSION + ')')

METHODORATTRORENUM = TARGET + (
    pp.OneOrMore(
        '.' + pp.Word(pp.alphanums)
        + pp.Optional('(' + pp.Optional(
            pp.Optional(EXPRESSION) + pp.ZeroOrMore("," + pp.Optional(EXPRESSION))
        ) + ')')
    ) |
    pp.Optional('::' + pp.Word(pp.alphanums))
)

STRING = pp.Regex("'[^']*'")
NUMBER = pp.Regex("[0-9]+(\\.[0-9]+)?")

VALUE = METHODORATTRORENUM ^ STRING ^ NUMBER

RELATIONAL = VALUE + pp.Optional(pp.oneOf(["<=", "<", "==", "!=", ">=", ">"]) + VALUE)

EXPRESSION << RELATIONAL

WHOLE_EXPRESSION = pp.StringStart() + EXPRESSION + pp.StringEnd()
