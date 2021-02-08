from AST import *
from Lexer import reserved
import os

useful = None


class CodeGenerator:
    def __init__(self, symTable):
        self.symTable = symTable
        self.current_scope = None

    def generate(self, node, output):
        self.generate_code(node, output)

    def generate_code(self, node, output, isParam=True):
        global useful
        if isinstance(node, ProgramNode):
            output.write("public Class main{\n")
            self.generate_code(node.children[0], output)
            output.write("\n}")

        if isinstance(node, StatementsNode):
            self.generate_code(node.children[0], output)

            if len(node.children) == 2:
                self.generate_code(node.children[1], output)

        if isinstance(node, StatementNode):
            if node.value != "return":
                self.generate_code(node.children[0], output)
            else:
                output.write("return ")
                for i in range(len(node.children)):
                    self.generate_code(node.children[i], output)
            output.write("\n")

        if isinstance(node, FuncNode):
            self.current_scope = str(node.value)
            if isinstance(node.children[0], ParamNode):
                if self.verify_return(node.children[1]):
                    output.write("public static Object " + str(node.value) + "(")
                else:
                    output.write("public static void " + str(node.value) + "(")
                self.generate_code(node.children[0], output, True)
                output.write("){\n")
                self.generate_code(node.children[1], output)
            else:
                if self.verify_return(node.children[0]):
                    output.write("public static Object " + str(node.value) + "(")
                else:
                    output.write("public static void " + str(node.value) + "(")
                output.write("){\n")
                self.generate_code(node.children[0], output)
            output.write("}\n")

        if isinstance(node, ParamNode):
            for i in range(len(node.children)):
                if not isinstance(node.children[i], ParamNode) and isParam:
                    output.write("Object ")
                self.generate_code(node.children[i], output, isParam)
                if not isinstance(node.children[i], ParamNode):
                    output.write(", ")

        if isinstance(node, AssignsNode):
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)

        if isinstance(node, AssignNode):
            i = self.lookup(node.value, self.current_scope)
            node_type = str(self.symTable[i][1])
            if node_type == "str":
                node_type = "String"
            elif node_type == "list_str":
                node_type = "list_String"
            if node_type != "generic":
                if node_type[0:5] == "list_":
                    node_type = node_type[5:] + "[]"
                elif node_type[0:6] == "tuple_":
                    node_type = node_type[6:] + "[]"
                output.write(node_type)
            elif node.children[0].children[0].value == 'input':
                output.write("Scanner")
                useful = node.value
            else:
                output.write("Object")
            output.write(" " + str(node.value) + " = ")
            if str(self.symTable[i][1])[0:5] == "list_" or str(self.symTable[i][1])[0:6] == "tuple_":
                output.write("{")
            self.generate_code(node.children[0], output)
            if str(self.symTable[i][1])[0:5] == "list_" or str(self.symTable[i][1])[0:6] == "tuple_":
                output.write("}")

        if isinstance(node, CallNode):
            if node.value not in reserved:
                output.write(node.value)
                output.write("(")
            elif node.value == "input":
                output.write("new Scanner")
                output.write("(System.in)\n")
                if len(node.children) == 1:
                    output.write("System.out.println(")
                    self.generate_code(node.children[0], output, False)
                    output.write(")\n")
                output.write("String input = " + str(useful) + ".nextLine()")
                useful = None
            elif node.value == "print":
                output.write("System.out.println")
                output.write("(")
            if len(node.children) == 1 and node.value != "input":
                self.generate_code(node.children[0], output, False)
                output.write(")")

        if isinstance(node, IfNode):
            output.write("if (")
            self.generate_code(node.children[0], output)
            output.write("){\n")
            self.generate_code(node.children[1], output)
            output.write("}\n")
            if len(node.children) == 3:
                output.write("else{\n")
                self.generate_code(node.children[1], output)
                output.write("\n}")

        if isinstance(node, WhileNode):
            output.write("while (")
            self.generate_code(node.children[0], output)
            output.write("){\n")
            self.generate_code(node.children[1], output)
            output.write("}\n")

        if isinstance(node, ConditionNode):
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)

        if isinstance(node, RelopNode):
            output.write(" " + str(node.value) + " ")

        if isinstance(node, ExprNode):
            self.generate_code(node.children[0], output)
            if len(node.children) == 2:
                output.write(" " + str(node.value) + " ")
                self.generate_code(node.children[1], output)

        if isinstance(node, ListNode) or isinstance(node, TupleNode):
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)
                if isinstance(node.children[i], ValueNode):
                    output.write(", ")

        if isinstance(node, ValueNode):
            output.write(str(node.value))

    # The function returns the index.
    def lookup(self, value, scope, parameters=0, length=0):
        for i in range(len(self.symTable)):
            if value == self.symTable[i][0] and scope in (self.symTable[i][2], "global"):
                return i

    # verify if the function has a return
    def verify_return(self, node):
        a = False
        if node.children[0].value == 'return':
            return True
        if len(node.children) == 2:
            a = self.verify_return(node.children[1])
        return a

    def post(self):
        file = open("output/main.java")
        lines = file.readlines()
        file.close()
        os.remove("output/main.java")
        file = open("output/main.java", "w")
        array_type = ("String[]", "int[]", "float[]", "bool[]")
        for line in lines:
            if line[0] == "\n":
                line = line[1:-1]
            if len(line) > 3 and line[-2] not in ("{", "}"):
                line = line[0:-1] + ";" + line[-1]
            if line.endswith(", ){\n") or line.endswith(", );\n"):
                line = line[0:-5] + line[-3:]
            if line.startswith(array_type):
                line = line[0:-1] + ";\n"
            file.write(line)


