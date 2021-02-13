import ply.yacc as yacc
from Lexer import lexer, tokens
import argparse
from SemanticAnalyzer import *
from CodeGenerator import *
import shutil


def p_program(p):
    '''program : statements'''
    p[0] = ProgramNode(children=[p[1]])
    ast_string = "AST TREE"
    sym_string = "SYMTABLE"
    if args["verbose"]:
        print("\n\n" + ast_string.center(shutil.get_terminal_size().columns) + "\n\n")
        print_tree(p[0].tree)
    semantic_checker = SemanticAnalyzer()
    semantic_checker.analysis(p[0])
    if args["verbose"]:
        print("\n\n" + sym_string.center(shutil.get_terminal_size().columns) + "\n\n")
        semantic_checker.print_symtab()
    semantic_checker.invalid_redeclaration()
    if len(semantic_checker.error) > 0:
        semantic_checker.print_error()
        print("Translation failed: your code contains error.", file=sys.stderr)
    else:
        try:
            f = open("output/Output.java", "w")
        except FileNotFoundError:
            os.mkdir("output")
        finally:
            f = open("output/Output.java", "w")
        code_generator = CodeGenerator(semantic_checker.get_symtab())
        code_generator.generate(p[0], f)
        f.close()
        code_generator.post()
        print("Translation completed correctly.")
    if not args["verbose"]:
        print("You can print the symtable and the Abstract Syntax Tree by running the same command with --verbose.")
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
	| RETURN expression'''

    if len(p) == 2 and p[1] != "return":
        p[0] = StatementNode(children=[p[1]])
    if len(p) == 2 and p[1] == "return":
        p[0] = StatementNode(children=[], value="return")
    if len(p) == 3:
        p[0] = StatementNode(children=[p[2]], value="return")


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
	| PRINT LPAR value RPAR
	| INPUT LPAR value RPAR
	| INPUT LPAR RPAR
	| PRINT LPAR RPAR
	| LEN LPAR expression RPAR'''

    if len(p) == 4:
        p[0] = CallNode(value=p[1], children=[])
    if len(p) == 5:
        p[0] = CallNode(value=p[1], children=[p[3]])
    if len(p) == 7:
        p[0] = CallNode(value=p[3], children=[p[5]])

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
    if len(p) == 4 and p[1] == "(":
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
	| value TIMES expression
	| value MODULE expression
	| value
	| call
	| list
	| list PLUS expression
	| tuple
	| tuple PLUS expression'''

    if len(p) == 4:
        p[0] = ExprNode(children=[p[1], p[3]], value=p[2])
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
    if len(p) == 4 and p[1] != "(":
        p[0] = TupleNode(children=[p[1], p[3]])
    if len(p) == 4 and p[1] == "(":
        p[0] = TupleNode(children=[p[2]])

def p_value(p):
    '''value : FLOAT
	| INT
	| ID
	| T_BOOL
	| F_BOOL
	| STRING
	| ID LSQB value RSQB'''


    if type(p[1]) == str and p[1][0] == "\"":
        p[0] = ValueNode(value=p[1], type="str")
    elif type(p[1]) == str and not p[1][0] == "\"":
        p[0] = ValueNode(value=p[1], type="id")
    else:
        p[0] = ValueNode(value=p[1], type=type(p[1]).__name__)
    if len(p) == 5:
        p[0] = ValueNode(value=p[1], type="id", index=p[3])
    if p[0].value in ("True", "False"):
        p[0] = ValueNode(value=p[1], type="bool")


# Error rule for syntax errors

def p_error(p):
    print("Syntax Error at line {}".format(lexer.linenumber))


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="input code")
ap.add_argument("-v", "--verbose", action="store_true")
args = vars(ap.parse_args())
data = args['input']
data = open(data).read() + "\n"
if data[-39:] == "if __name__ == '__main__':\n    main()\n\n":
    data = data[:-39]
else:
    print("WARNING: Missing \"if __name__ == '__main__': main()\" at the end of file.", file=sys.stderr)

# Build the parser
parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())

while True:
    pars = parser.parse(data, lexer)
    if not pars:
        break
