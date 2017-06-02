import datetime
import sys
import time

import pyparsing

from monasca_common.monasca_query_language.query_structures import (Dimension,
                                                                    MetricSelector,
                                                                    LogicalExpression,
                                                                    SourceExpression,
                                                                    TargetsExpression,
                                                                    ExcludesExpression,
                                                                    GroupByExpression,
                                                                    Rule)

COMMA = pyparsing.Suppress(pyparsing.Literal(","))
LPAREN = pyparsing.Suppress(pyparsing.Literal("("))
RPAREN = pyparsing.Suppress(pyparsing.Literal(")"))
LBRACE = pyparsing.Suppress(pyparsing.Literal("{"))
RBRACE = pyparsing.Suppress(pyparsing.Literal("}"))
LBRACKET = pyparsing.Suppress(pyparsing.Literal("["))
RBRACKET = pyparsing.Suppress(pyparsing.Literal("]"))

MINUS = pyparsing.Literal("-")

integer_number = pyparsing.Word(pyparsing.nums)
decimal_number = (pyparsing.Optional(MINUS) + integer_number +
                  pyparsing.Optional("." + integer_number))
decimal_number.setParseAction(lambda tokens: float("".join(tokens)))

# Initialize non-ascii unicode code points in the Basic Multilingual Plane.
unicode_printables = u''.join(
    unichr(c) for c in range(128, 65536) if not unichr(c).isspace())

# Does not like comma. No Literals from above allowed.
valid_identifier_chars = (
    (unicode_printables + pyparsing.alphanums + ".-_#$%&'*+/:;?@[\\]^`|"))

metric_name = (
    pyparsing.Word(pyparsing.alphas, valid_identifier_chars, min=1, max=255)("metric_name"))
dimension_name = pyparsing.Word(valid_identifier_chars + ' ', min=1, max=255)
dimension_value = pyparsing.Word(valid_identifier_chars + ' ', min=1, max=255)

dim_comparison_op = pyparsing.oneOf("=")

dimension = dimension_name + dim_comparison_op + dimension_value
dimension.setParseAction(Dimension)

dimension_list = pyparsing.Group((LBRACE + pyparsing.Optional(
    pyparsing.delimitedList(dimension)) +
                                  RBRACE))

metric = (metric_name + pyparsing.Optional(dimension_list) |
          pyparsing.Optional(metric_name) + dimension_list)
metric.addParseAction(MetricSelector)

source = pyparsing.Keyword("source")
source_expression = source + metric
source_expression.addParseAction(SourceExpression)

targets = pyparsing.Keyword("targets")
targets_expression = targets + metric
targets_expression.addParseAction(TargetsExpression)

excludes = pyparsing.Keyword("excluding")
excludes_expression = excludes + metric
excludes_expression.addParseAction(ExcludesExpression)

group_by = pyparsing.Keyword("group by")
group_by_expr = group_by + pyparsing.delimitedList(dimension_name)
group_by_expr.addParseAction(GroupByExpression)

grammar = pyparsing.Optional(source_expression) + pyparsing.Optional(targets_expression) + pyparsing.Optional(excludes_expression) + pyparsing.Optional(group_by_expr)
grammar.addParseAction(Rule)


class RuleExpressionParser(object):

    def __init__(self, expr):
        self._expr = expr

    def parse(self):
        parse_result = grammar.parseString(self._expr, parseAll=True)
        return parse_result
