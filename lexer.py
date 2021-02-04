import ply.lex as lex
from IndentLexer import IndentLexer


# FIRST LEXING STAGE
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
    'extend': 'EXTEND'
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
             'FULLSTOP',
             'STRING'
         ] + list(reserved.values())

t_EQUAL = '='
t_COLON = ':'
t_WHITESPACE = r'\n[ ]*'
t_LPAR = '\('
t_RPAR = '\)'
t_LSQB = '\['
t_RSQB = '\]'
t_COMMA = ','
t_PLUS = '\+'
t_MINUS = '-'
t_LESS = '<'
t_GREATER = '>'
t_NOTEQUAL = '!='
t_GREATEREQUAL = '>='
t_EQEQUAL = '=='
t_LESSEQUAL = '<='
t_FULLSTOP = '\.'


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


def t_COMMENT(t):
    r'\#.*'
    pass


t_ignore = ' \t;'


def t_error(t):
    lexer.error()
    t.lexer.skip(1)


# create our first stage
lexer = lex.lex()


# create our second stage
lexer = IndentLexer(lexer)

# DE-COMMENT TO TEST ALONE
#
# data = '''
# a = 6
# if a < 6:
#     e = 2
#
#
# lexer.input(data)
#
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
