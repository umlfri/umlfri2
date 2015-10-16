import pyparsing as pp

EXPRESSION = pp.Forward()

VARIABLE = pp.Word(pp.alphanums)

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

EXPRESSION << METHODORATTRORENUM

WHOLE_EXPRESSION = pp.StringStart() + EXPRESSION + pp.StringEnd()
