import sys

import ply.lex as lex

indentation_stack = [0]


reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'or': 'OR',
    'not': 'NOT',
    'and': 'AND',
    'def': 'DEF',
    'return': 'RETURN',
    'True': 'T_BOOL',
    'False': 'F_BOOL',
    'print': 'PRINT',
    'input': 'INPUT',
    'len': 'LEN'
}

tokens = [
             'ID',
             'WHITESPACE',
             'COLON',
             'LPAR',
             'RPAR',
             'LSQB',
             'RSQB',
             'COMMA',
             'PLUS',
             'MINUS',
             'LESS',
             'GREATER',
             'EQUAL',
             'NOTEQUAL',
             'GREATEREQUAL',
             'FLOAT',
             'INT',
             'COMMENT',
             'INDENT',
             'DEDENT',
             'EQEQUAL',
             'LESSEQUAL',
             'STRING',
             'TIMES',
             'MODULE'
         ] + list(reserved.values())

t_EQUAL = '='
t_COLON = ':'
t_LPAR = '\('
t_RPAR = '\)'
t_LSQB = '\['
t_RSQB = '\]'
t_COMMA = ','
t_PLUS = '\+'
t_MINUS = '-'
t_TIMES = '\*'
t_LESS = '<'
t_GREATER = '>'
t_NOTEQUAL = '!='
t_GREATEREQUAL = '>='
t_EQEQUAL = '=='
t_LESSEQUAL = '<='
t_MODULE = '%'


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'[-+]?\d*\.?\d+'
    try:
        t.value = int(t.value)
        t.type = 'INT'
    except ValueError:
        t.value = float(t.value)
        t.type = 'FLOAT'
    finally:
        return t


def t_WHITESPACE(t):
    r'\n[ ]*'
    t.lexer.lineno += 1
    t.lexer.level = len(t.value[1:])
    if t.lexer.level > indentation_stack[-1]:
        t.type = 'INDENT'
        indentation_stack.append(t.lexer.level)
        return t
    elif t.lexer.level < indentation_stack[-1]:
        t.type = 'DEDENT'
        indentation_stack.append(indentation_stack[-1] - 4)
        if indentation_stack[-1] > t.lexer.level:
            t.lexer.skip(-len(t.value))
        return t


def t_COMMENT(t):
    r'\#.*'
    pass


t_ignore = ' \t;'


def t_error(t):
    print(f"Lexical error at line {t.lexer.lineno}", file=sys.stderr)
    t.lexer.skip(1)


lexer = lex.lex()


# DE-COMMENT TO TEST ALONE
#
# data = '''a = 1
# if a < 6:
#     c = 1
#     while a < 6:
#         c = 2
#         if a < 6:
#             c = 1
#
#         if a < 24:
#             c = 32
# '''
#
# lexer.input(data)
#
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
