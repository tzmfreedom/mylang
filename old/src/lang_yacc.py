#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import sys
from lang_lex import lexer
from tokens import tokens
from statement import Statement
from lang_enums import StatementType, ResultType
from condition import Condition
from basic_types import BasicType, Method

# precedence = (
#     ('left','ADD','SUB'),
#     ('left','MUL','DIV','LP','RP')
# )

statementlist = []

def p_main(p):
    '''
    main : newline_or_blank translation_units newline_or_blank
    '''

def p_translation_units(p):
    '''
    translation_units : translation_unit
                      | translation_units newline translation_unit
    '''
    if len(p) == 2:
        statementlist.append(p[1])
    else:
        statementlist.append(p[3])


def p_translation_unit(p):
    '''
    translation_unit : statement
                     | define_function
                     | define_class
    '''
    p[0] = p[1]


def p_statement(p):
    '''
    statement : assign_statement
              | if_statement
              | loop_statement
              | call_func
              | continue_statement
              | break_statement
              | return_statement
    '''
    p[0] = p[1]

def p_increment(p):
    '''
    assign_statement : IDENT INCREMENT
    '''
    p[0] = Statement(StatementType.ASSIGN, p.lineno(1), {'variable_name': p[1], 'type': 'increment'})


def p_decrement(p):
    '''
    assign_statement : IDENT DECREMENT
    '''
    p[0] = Statement(StatementType.ASSIGN, p.lineno(1), {'variable_name': p[1], 'type': 'decrement'})


def p_call_func(p):
    '''
    call_func : IDENT LP args RP
              | IDENT LP RP
    '''
    if len(p) == 5:
        p[0] = Statement(StatementType.FUNCTION_CALL, p.lineno(1), {'function_name': p[1], 'args': p[3]})
    else:
        p[0] = Statement(StatementType.FUNCTION_CALL, p.lineno(1), {'function_name': p[1], 'args': []})
    # print('{0}: {1}'.format(p.lineno(1), p[0]))


def p_define_func(p):
    '''
    define_function : FUNCTION IDENT LP RP block
                    | FUNCTION IDENT LP define_function_args RP block
    '''
    if len(p) == 6:
        p[0] = Statement(StatementType.FUNCTION_DEFINE, p.lineno(1), {'function_name': p[2], 'function_args': [], 'statementlist': p[5]})
    else:
        p[0] = Statement(StatementType.FUNCTION_DEFINE, p.lineno(1), {'function_name': p[2], 'function_args': p[4], 'statementlist': p[6]})


def p_define_func_args(p):
    '''
    define_function_args : IDENT
                         | define_function_args COMMA IDENT
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

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
        p[0] = Statement(StatementType.EXPRESSION, p.lineno(2), {'left': p[1], 'right': p[3], 'op': p[2]})
    else:
        p[0] = p[1]


def p_term(p):
    '''
    term : primary_expression
         | term MUL primary_expression
         | term DIV primary_expression
    '''
    if len(p) == 4:
        p[0] = Statement(StatementType.EXPRESSION, p.linno(2), {'left': p[1], 'right': p[3], 'op': p[2]})
    else:
        p[0] = p[1]


def p_statement_list_statement(p):
    '''
    statement_list : statement
                   | statement_list newline statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_empty(p):
    '''
    empty :
    '''

def p_newline_or_blank(p):
    '''
    newline_or_blank : newline
                     | empty
    '''


def p_block(p):
    '''
    block : LC newline_or_blank statement_list newline_or_blank RC
    '''
    p[0] = p[3]

## Todo: Multiple condition
def p_condition_statement(p):
    '''
    condition_statement : condition
    '''
    p[0] = p[1]


def p_condition(p):
    '''
    condition : expression EQUAL expression
              | expression LTHAN expression
              | expression GTHAN expression
              | expression NOT_EQUAL expression
    '''
    p[0] = Condition(p[1], p[2], p[3])


def p_if_statement(p):
    '''
    if_statement : IF LP condition_statement RP block
                 | IF LP condition_statement RP block ELSE statement
    '''
    if len(p) == 6:
        p[0] = Statement(StatementType.IF, p.lineno(1), {'condition': p[3], 'statementlist': p[5]})
    else:
        p[0] = Statement(StatementType.IF, p.lineno(1), {'condition': p[3], 'statementlist': p[5], 'else_statementlist': [p[7]]})

def p_if_statement_else(p):
    '''
    if_statement : IF LP condition_statement RP block ELSE block
    '''
    p[0] = Statement(StatementType.IF, p.lineno(1), {'condition': p[3], 'statementlist': p[5], 'else_statementlist': p[7]})


def p_loop_statement(p):
    '''
    loop_statement : LOOP LP condition_statement RP block
                   | LOOP LP IDENT COLON expression RP block
    '''
    if len(p) == 6:
        p[0] = Statement(StatementType.LOOP, p.lineno(1), {'condition': p[3], 'statementlist': p[5]})
    else:
        p[0] = Statement(StatementType.LOOP, p.lineno(1), {'ident': p[3], 'loop_count': p[5], 'statementlist': p[7]})


def p_number(p):
    '''
    number : INT
           | DOUBLE
    '''
    p[0] = BasicType(p[1])

def p_string(p):
    '''
    string : STRVALUE
    '''
    p[0] = BasicType(p[1])

def p_expression1(p):
    '''
    primary_expression : call_func
                        | string
                        | map
                        | list
                        | number
    '''
    p[0] = p[1]


def p_expression_ident(p):
    '''
    primary_expression : IDENT
    '''
    p[0] = Statement(StatementType.VAR, p.lineno(1), {'variable_name': p[1]})


def p_args(p):
    '''
    args : expression
         | args COMMA expression
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_map(p):
    '''
    map : LC RC
    '''
    p[0] = BasicType({})

def p_list(p):
    '''
    list : LB RB
         | LB args RB
    '''
    if len(p) == 3:
        p[0] = BasicType([])
    else:
        p[0] = BasicType(p[2])

def p_newline(p):
    '''
    newline : NEWLINE
            | newline NEWLINE
    '''

def p_break(p):
    '''
    break_statement : BREAK
    '''
    p[0] = Statement(StatementType.BREAK, p.lineno(1), {})

def p_continue(p):
    '''
    continue_statement : CONTINUE
    '''
    p[0] = Statement(StatementType.CONTINUE, p.lineno(1), {})

def p_return(p):
    '''
    return_statement : RETURN
                     | RETURN expression
    '''
    if len(p) == 2:
        p[0] = Statement(StatementType.RETURN, p.lineno(1), {'return_value': None})
    else:
        p[0] = Statement(StatementType.RETURN, p.lineno(1), {'return_value': p[2]})

def p_class_instanciation(p):
    '''
    expression : NEW IDENT LP RP
               | NEW IDENT LP args RP
    '''
    if len(p) == 5:
        p[0] = Statement(StatementType.NEW_CLASS, p.lineno(1), {'class_name': p[2], 'class_args': {}})
    else:
        p[0] = Statement(StatementType.NEW_CLASS, p.lineno(1), {'class_name': p[2], 'class_args': p[4]})


def p_instance_method(p):
    '''
    call_func : IDENT DOT IDENT LP RP
              | IDENT DOT IDENT LP args RP
    '''
    if len(p) == 6:
        p[0] = Statement(StatementType.CALL_METHOD, p.lineno(1), {'variable_name': p[1], 'method_name': p[3], 'method_args': {}})
    else:
        p[0] = Statement(StatementType.CALL_METHOD, p.lineno(1), {'variable_name': p[1], 'method_name': p[3], 'method_args': p[5]})


def p_define_class(p):
    '''
    define_class : CLASS IDENT LC newline define_class_properties newline define_methods newline RC
                 | CLASS IDENT LC newline define_methods newline RC
    '''
    if len(p) == 8:
        p[0] = Statement(StatementType.CLASS_DEFINE, p.lineno(1), {'class_name': p[2], 'properties': [], 'methods': p[5]})
    else:
        p[0] = Statement(StatementType.CLASS_DEFINE, p.lineno(1), {'class_name': p[2], 'properties': p[5], 'methods': p[7]})

def p_define_class_properties(p):
    '''
    define_class_properties : PROPERTY define_function_args
    '''
    p[0] = p[2]

def p_define_method(p):
    '''
    define_method : METHOD IDENT LP define_function_args RP block
                  | METHOD IDENT LP RP block
    '''
    if len(p) == 5:
        p[0] = Method(p[2], [], p[5])
    else:
        p[0] = Method(p[2], p[4], p[6])

def p_define_methods(p):
    '''
    define_methods : define_method
                   | define_methods newline define_method
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
