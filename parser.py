import ply.yacc as yacc
from lexer import lexer, tokens
import argparse
from Node import *
from SemanticAnalyzer import *


def p_program(p):
    '''program : statements'''
    p[0] = ProgramNode(children=[p[1]])
    if args["verbose"]:
        print(p[0])
    visitor = SemanticAnalyzer()
    visitor.analyze(p[0])
    print(visitor.symTable)
    if len(visitor.error) > 0:
        print("TranslationError: your code contains error", file=sys.stderr)
    p[0] = None


def p_statements(p):
    '''statements : statement
    | statement statements'''

    if len(p) == 2:
        p[0] = StatementsNode(children=[p[1]])
    if len(p) == 3:
        p[0] = StatementsNode(children=[p[1], p[2]])

def p_statement(p):
    '''statement : if_statement
	| while_statement
	| assignment_statement
	| funcdef
	| call
	| COMMENT
	| RETURN
	| RETURN value'''

    if len(p) == 2 and p[1] != "return":
        p[0] = StatementNode(children=[p[1]])
    if len(p) == 2 and p[1] == "return":
        p[0] = StatementNode(children=[])
    if len(p) == 3:
        p[0] = StatementNode(children=[p[2]])


def p_funcdef(p):
    '''funcdef : DEF ID LPAR parameters RPAR COLON INDENT statements DEDENT
	| DEF ID LPAR RPAR COLON INDENT statements DEDENT'''

    if len(p) == 10:
        p[0] = FuncNode(children=[p[4], p[8]], value=p[2])
    if len(p) == 9:
        p[0] = FuncNode(children=[p[7]], value=p[2])


def p_parameters(p):
    '''parameters : value
	| value COMMA parameters
	| assignment_statements '''

    if len(p) == 2:
        p[0] = ParamNode(children=[p[1]])
    if len(p) == 4:
        p[0] = ParamNode(children=[p[1], p[3]])


def p_assignment_statements(p):
    '''assignment_statements : assignment_statement
    | assignment_statement COMMA assignment_statements'''

    if len(p) == 2:
        p[0] = AssignsNode(children=[p[1]])
    if len(p) == 4:
        p[0] = AssignsNode(children=[p[1], p[3]])


def p_assignment_statement(p):
    '''assignment_statement : value EQUAL expression'''

    p[0] = AssignNode(value=p[1], children=[p[3]])


def p_call(p):
    '''call	: ID LPAR parameters RPAR
	| ID LPAR RPAR
	| ID FULLSTOP EXTEND LPAR value RPAR
	| ID FULLSTOP EXTEND LPAR list RPAR'''

    if len(p) == 4:
        p[0] = CallNode(value=p[1], children=[])
    if len(p) == 5:
        p[0] = CallNode(value=p[1], children=[p[3]])
    if len(p) == 7:
        p[0] = CallNode(value=p[1], children=[p[5]])

def p_if_statement(p):
    '''if_statement : IF condition COLON INDENT statements DEDENT
	| IF condition COLON INDENT statements DEDENT ELSE COLON INDENT statements DEDENT'''

    if len(p) == 7:
        p[0] = IfNode(children=[p[2], p[5]])
    if len(p) == 12:
        p[0] = IfNode(children=[p[2], p[5], p[10]])


def p_while_statement(p):
    '''while_statement : WHILE condition COLON INDENT statements DEDENT'''

    p[0] = WhileNode(children=[p[2], p[5]])


def p_condition(p):
    '''condition : expression relop condition
	| LPAR expression RPAR relop condition
	| expression
	| LPAR condition RPAR'''

    if len(p) == 2:
        p[0] = ConditionNode(children=[p[1]])
    if len(p) == 4 and p[1]=="(":
        p[0] = ConditionNode(children=[p[2]])
    if len(p) == 4 and p[1] != "(":
        p[0] = ConditionNode(children=[p[1], p[2], p[3]])
    if len(p) == 6:
        p[0] = ConditionNode(children=[p[2], p[4], p[5]])


def p_relop(p):
    '''relop : AND
	| OR
	| LESS
	| GREATER
	| EQEQUAL
	| LESSEQUAL
	| GREATEREQUAL
	| NOT
	| NOTEQUAL'''

    p[0] = RelopNode(value=p[1])


def p_expression(p):
    '''expression : value PLUS expression
	| value MINUS expression
	| value
	| call
	| list
	| list PLUS expression
	| tuple
	| tuple PLUS expression'''

    if len(p) == 4:
        p[0] = ExprNode(children=[p[1], p[3]])
    if len(p) == 2:
        p[0] = ExprNode(children=[p[1]])



def p_list(p):
    '''list : LSQB list RSQB
    | value COMMA list
    | value
    | LSQB RSQB'''

    if len(p) == 2:
        p[0] = ListNode(children=[p[1]])
    if len(p) == 3:
        p[0] = ListNode(children=[])
    if len(p) == 4 and p[1] != "[":
        p[0] = ListNode(children=[p[1], p[3]])
    if len(p) == 4 and p[1] == "[":
        p[0] = ListNode(children=[p[2]])


def p_tuple(p):
    '''tuple : LPAR tuple RPAR
    | value COMMA tuple
    | value
    | LPAR RPAR'''

    if len(p) == 2:
        p[0] = TupleNode(children=[p[1]])
    if len(p) == 3:
        p[0] = TupleNode(children=[])
    if len(p) == 4 and p[1] != "[":
        p[0] = TupleNode(children=[p[1], p[3]])
    if len(p) == 4 and p[1] == "[":
        p[0] = TupleNode(children=[p[2]])

def p_value(p):
    '''value : FLOAT
	| INT
	| ID
	| T_BOOL
	| F_BOOL
	| STRING'''


    if type(p[1]) == str and p[1][0] == "\"":
        p[0] = ValueNode(value=p[1], type="str")
    elif type(p[1]) == str and not p[1][0] == "\"":
        p[0] = ValueNode(value=p[1], type="id")
    else:
        p[0] = ValueNode(value=p[1], type=type(p[1]).__name__)


# Error rule for syntax errors

def p_error(p):
    print("Syntax Error at line {}".format(lexer.linenumber))


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="input code")
ap.add_argument("-v", "--verbose", action="store_true")
args = vars(ap.parse_args())
data = args['input']
data = open(data).read() + "\n"

# Build the parser
parser = yacc.yacc(debug=False, write_tables=False)

while True:
    pars = parser.parse(data, lexer)
    if not pars:
        break
