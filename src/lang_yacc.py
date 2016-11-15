#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import sys
from lang_lex import lexer
from tokens import tokens
from statement import Statement
from lang_enums import StatementType
from condition import Condition


# precedence = (
#     ('left','ADD','SUB'),
#     ('left','MUL','DIV','LP','RP')
# )

statementlist = []

def p_translation_units(p):
    '''
    translation_units : translation_unit NEWLINE
                    | translation_units translation_unit NEWLINE
    '''
    if len(p) == 3:
        statementlist.append(p[1])
    else:
        statementlist.append(p[2])


def p_translation_unit(p):
    '''
    translation_unit : statement
    '''
    p[0] = p[1]


def p_statement(p):
    '''
    statement : assign_statement
              | if_statement
              | call_func
    '''
    p[0] = p[1]


def p_call_func(p):
    '''
    call_func : IDENT LP args RP
    '''
    p[0] = Statement(StatementType.FUNCTION_CALL, p.lineno(1), {'function_name': p[1], 'args': p[3]})
    # print('{0}: {1}'.format(p.lineno(1), p[0]))


def p_assign_statement(p):
    '''
    assign_statement : IDENT ASSIGN expression
    '''
    # variables[p[1]] = p[3]
    p[0] = Statement(StatementType.ASSIGN, p.lineno(1), {'variable_name': p[1], 'expression': p[3]})


def p_expression(p):
    '''
    expression : term
               | expression ADD term
               | expression SUB term
    '''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
    else:
        p[0] = p[1]


def p_term(p):
    '''
    term : number
         | term MUL number
         | term DIV number
    '''
    if len(p) == 4:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
    else:
        p[0] = p[1]


def p_statement_list(p):
    '''
    statement_list : statement NEWLINE
                   | statement_list statement NEWLINE
    '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
    

def p_block(p):
    '''
    block : LC statement_list RC
          | LC NEWLINE statement_list RC
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[3]

## Todo: Multiple condition
def p_condition_statement(p):
    '''
    condition_statement : condition
    '''
    p[0] = p[1]


def p_condition(p):
    '''
    condition : arg EQUAL arg
              | arg LTHAN arg
              | arg GTHAN arg
              | arg NOT_EQUAL arg
    '''
    p[0] = Condition(p[1], p[2], p[3])


def p_if(p):
    '''
    if_statement : IF LP condition_statement RP block
    '''
    p[0] = Statement(StatementType.IF, p.lineno(1), {'condition': p[3], 'statementlist': p[5]})


def p_number(p):
    '''
    number : INT
           | DOUBLE
    '''
    p[0] = p[1]


def p_arg(p):
    '''
    arg : call_func
        | number
        | STRVALUE
    '''
    p[0] = p[1]


def p_arg_ident(p):
    '''
    arg : IDENT
    '''
    p[0] = Statement(StatementType.VAR, p.lineno(1), {'variable_name': p[1]})


def p_args(p):
    '''
    args : arg
         | args COMMA arg
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_error(p):
    print("Syntax error at '%s'" % p)


data = sys.stdin.read()
yacc.yacc()
yacc.parse(data, lexer=lexer)

for statement in statementlist:
    statement.eval()
