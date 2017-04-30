#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ply.yacc as yacc
from lex import lexer
import sys
from tokens import tokens
from statement import *
from basic_type import BasicType

statement_list = []

def p_main(p):
    '''
    main : newline_or_empty translation_units newline_or_empty
    '''
    global statement_list
    statement_list = p[2]

def p_translation_units(p):
    '''
    translation_units : translation_unit
                      | translation_units newline translation_unit
    '''
    print len(p)
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_translation_unit(p):
    '''
    translation_unit : statement
    '''
    p[0] = p[1]

def p_statement(p):
    '''
    statement : assign_statement
              | expression
    '''
    p[0] = p[1]

def p_assign_statement(p):
    '''
    assign_statement : IDENT ASSIGN expression
    '''
    p[0] = AssignStatement(p.lineno(0), p[1], p[3])

def p_expression(p):
    '''
    expression : number_expression
               | string_expression
    '''
    p[0] = p[1]

def p_number_expression(p):
    '''
    number_expression : term
                      | number_expression ADD term
                      | number_expression SUB term
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = CalculateStatement(p.lineno(0), p[2], p[1], p[3])

def p_term(p):
    '''
    term : number
         | term MUL number
         | term DIV number
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = CalculateStatement(p.lineno(0), p[2], p[1], p[3])

def p_number(p):
    '''
    number : INT
           | DOUBLE
    '''
    p[0] = BasicType(p[1])

def p_string_expression(p):
    '''
    string_expression : string
                      | string_expression ADD string
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = CalculateStatement(p.lineno(0), p[2], p[1], p[3])

def p_string(p):
    '''
    string : STRVALUE
    '''
    p[0] = BasicType(p[1])

def p_newline(p):
    '''
    newline : NEWLINE
            | newline NEWLINE
    '''

def p_newline_or_empty(p):
    '''
    newline_or_empty : newline
                     | empty
    '''

def p_empty(p):
    '''
    empty :
    '''

def p_error(p):
    print("Syntax error at '%s'" % p)


data = sys.stdin.read()
yacc.yacc()
yacc.parse(data, lexer=lexer)

for statement in statement_list:
    statement.eval()

from storage import storage
print storage.variables
print storage.variables['c'].eval().value
