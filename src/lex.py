#!/usr/bin/env python
# -*- coding: utf8 -*-

import ply.lex as lex
import sys
from tokens import tokens

states = (
        ('string', 'exclusive'),
)

reserved = {}

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_ASSIGN = r'='

t_ignore = ' \t'
t_string_ignore = ' \t'

def t_IDENT(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t

def t_DOUBLE(t):
    r'([1-9][0-9]*|0)\.[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print "Line %d: double value %s is too large" % t.lineno, t.value
        t.value = 0
    return t

def t_INT(t):
    r'[1-9][0-9]*|0'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Line %d: integer value %s is too large" % t.lineno, t.value
        t.value = 0
    return t

def t_NEWLINE(t):
    r'\n'
    return t

def t_begin_string(t):
    r'"'
    t.lexer.push_state('string')

def t_string_STRVALUE(t):
    r'[^"]+'
    return t

def t_string_end(t):
    r'"'
    t.lexer.pop_state()

def t_error(t):
    print "Illigal charactor '%s'" % t.value[0]
    t.skip(1)

def t_string_error(t):
    print "Illigal charactor '%s'" % t.value[0]
    t.skip(1)

def t_COMMENT(t):
    r'\#.*'
    pass

# Build the lexer
lexer = lex.lex()

# Tokenize
if __name__ == "__main__":
    data = sys.stdin.read()
    lexer.input(data)
    while 1:
        tok = lexer.token()
        if not tok:
            break
        print tok