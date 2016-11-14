#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ply.lex as lex
import sys
from lang_tokens import tokens


states = (
        ('string', 'exclusive'),
        )

reserved = {}

# Regular expression rules for simple tokens
t_ADD     = r'\+'
t_SUB     = r'-'
t_MUL     = r'\*'
t_DIV     = r'/'
t_LP      = r'\('
t_RP      = r'\)'
t_ASSIGN  = r'='

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
t_string_ignore = ''


def t_IDENT(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t


# A regular expression rule with some action code
def t_INT(t):
    r'[1-9][0-9]*|0'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t


def t_DOUBLE(t):
    r'[1-9][0-9]*.[0-9]+|0.[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print "Line %d: Number %s is too large!" % (t.lineno,t.value)
        t.value = 0
    return t


# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


# Strings
def t_begin_string(t):
    r'"'
    t.lexer.push_state('string')


def t_string_STRVALUE(t):
    r'[^"]+'
    return t


def t_string_end(t):
    r'"'
    t.lexer.pop_state()


# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.skip(1)


def t_string_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.skip(1)


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
