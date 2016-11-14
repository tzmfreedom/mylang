import ply.yacc as yacc
import sys
from lang_lex import lexer
from lang_tokens import tokens


# precedence = (
#     ('left','ADD','SUB'),
#     ('left','MUL','DIV','LP','RP')
# )

variables = {}


def echo(s):
    print("echo {0}".format(str(s)))
    return str(s)


def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


functions = {
    'echo': echo,
    'fib': fib,
}


def p_lines(p):
    '''
    lines : line NEWLINE
          | lines line NEWLINE
    '''


def p_line(p):
    '''
    line : call_func
         | statement
    '''


def p_call_func(p):
    '''
    call_func : IDENT LP arg RP
    '''
    p[0] = functions[p[1]](p[3])
    # print('{0}: {1}'.format(p.lineno(1), p[0]))


def p_ident(p):
    '''
    ident : IDENT
    '''
    p[0] = variables[p[1]]


def p_assign(p):
    '''
    statement : IDENT ASSIGN expression
    '''
    variables[p[1]] = p[3]
    p[0] = p[3]
    print('{0}: Assign {1} = {2}'.format(p.lineno(1), p[1], p[3]))


def p_statement(p):
    '''
    statement : expression
    '''
    p[0] = p[1]


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
        | ident
    '''
    p[0] = p[1]


# def p_args(p):
#     '''
#     args : arg
#          | args COMMA arg
#     '''
#     p[0] = p[1]


def p_error(p):
    print("Syntax error at '%s'" % p)


data = sys.stdin.read()
yacc.yacc()
# yacc.parse(data)
yacc.parse(data, lexer=lexer)
