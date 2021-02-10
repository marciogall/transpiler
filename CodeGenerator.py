from AST import *
from Lexer import reserved
import os

useful = None
concatenation = False
already_declared = []


class CodeGenerator:
    def __init__(self, symTable):
        self.symTable = symTable
        self.current_scope = None

    def generate(self, node, output):
        self.generate_code(node, output)

    def generate_code(self, node, output, isParam=True, node_type=None):
        global useful
        global concatenation

        if isinstance(node, ProgramNode):
            output.write("import java.util.Scanner\nimport java.util.Arrays\npublic class Example{\n")
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
                    if self.current_scope == "main":
                        output.write("String[] args")
                self.generate_code(node.children[0], output, True)
                output.write("){\n")
                output.write("Scanner input = new Scanner(System.in)\n")
                self.generate_code(node.children[1], output)
            else:
                if self.verify_return(node.children[0]):
                    output.write("public static Object " + str(node.value) + "(")
                else:
                    output.write("public static void " + str(node.value) + "(")
                    if self.current_scope == "main":
                        output.write("String[] args")
                output.write("){\n")
                output.write("Scanner input = new Scanner(System.in)\n")
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
            if node.value not in already_declared:
                if node_type == "str":
                    node_type = "String"
                if node_type == "bool":
                    node_type = "boolean"
                elif node_type == "list_str":
                    node_type = "list_String"
                elif node_type == "tuple_str":
                    node_type = "tuple_String"
                if node_type != "generic":
                    if node_type[0:5] == "list_":
                        if node_type[5:] == "float":
                            node_type = "Double[]"
                        elif node_type[5:] == "int":
                            node_type = "Integer[]"
                        elif node_type[5:] == "bool":
                            node_type = "Boolean[]"
                        elif node_type[5:] == "str":
                            node_type = "String[]"
                        elif node_type[6:] == "generic":
                            node_type = "String[]"
                    elif node_type[0:6] == "tuple_":
                        if node_type[6:] == "float":
                            node_type = "Double[]"
                        elif node_type[6:] == "int":
                            node_type = "Integer[]"
                        elif node_type[6:] == "bool":
                            node_type = "Boolean[]"
                        elif node_type[6:] == "str":
                            node_type = "String[]"
                        elif node_type[7:] == "generic":
                            node_type = "String[]"
                    if node_type == "float":
                        output.write("double")
                    output.write(node_type)
                elif node.children[0].children[0].value == 'input':
                    useful = node.value
                else:
                    output.write("Object")
            already_declared.append(str(node.value))
            if not node.children[0].children[0].value == 'input':
                output.write(" " + str(node.value) + " = ")
            if node.children[0].value == "+" and (str(self.symTable[i][1])[0:5] == "list_" or str(self.symTable[i][1])[0:6] == "tuple_"):
                concatenation = True
                output.write("concatAll(")
                self.generate_code(node.children[0], output, False, node_type)
                output.write(")")
            else:
                self.generate_code(node.children[0], output)

        if isinstance(node, CallNode):
            temp = False
            if node.value not in reserved:
                output.write(node.value)
                output.write("(")
            elif node.value == "input":
                if len(node.children) == 1:
                    output.write("System.out.println(")
                    self.generate_code(node.children[0], output, False)
                    output.write(")\n")
                output.write("String " + str(useful) + " = input.nextLine()")
                useful = None
            elif node.value == "print":
                output.write("System.out.println")
                output.write("(")
                i = self.lookup(node.children[0].value, self.current_scope)
                if i is not None:
                    temp = str(self.symTable[i][1]).split("_")[0] in ("tuple", "list")
                if temp:
                    output.write("Arrays.toString(")
            elif node.value == "len":
                output.write(str(node.children[0].children[0].value) + ".length")
            if len(node.children) == 1 and node.value not in ("input", "len"):
                self.generate_code(node.children[0], output, False)
                output.write(")")
            if temp and node.value != "len":
                output.write(")")

        if isinstance(node, IfNode):
            output.write("if (")
            self.generate_code(node.children[0], output)
            output.write("){\n")
            self.generate_code(node.children[1], output)
            output.write("}\n")
            if len(node.children) == 3:
                output.write("else{\n")
                self.generate_code(node.children[2], output)
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
            if not isParam and node.children[0].type != "id":
                output.write(" new " + node_type)
            self.generate_code(node.children[0], output)
            if len(node.children) == 2:
                if isParam:
                    output.write(" " + str(node.value) + " ")
                else:
                    output.write(" , ")
                self.generate_code(node.children[1], output, isParam, node_type)

        if isinstance(node, ListNode) or isinstance(node, TupleNode):
            if isParam:
                output.write("{")
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output, False)
                if isinstance(node.children[i], ValueNode):
                    output.write(", ")
            if isParam:
                output.write("}")

        if isinstance(node, ValueNode):
            if node.value not in ("True", "False"):
                output.write(str(node.value))
            else:
                output.write(str(node.value).lower())

    # The function returns the index.
    def lookup(self, value, scope, parameters=0, length=0):
        for i in range(len(self.symTable)):
            if value == self.symTable[i][0] and scope in (self.symTable[i][2], "global", None):
                return i

    # verify if the function has a return
    def verify_return(self, node):
        a = False
        for i in range(len(node.children)):
            if isinstance(node.children[i], StatementNode) and node.children[i].value == 'return':
                return True
            a = self.verify_return(node.children[i])
        return a

    def post(self):
        file = open("output/main.java")
        lines = file.readlines()
        file.close()
        os.remove("output/main.java")
        file = open("output/main.java", "w")
        array_type = ("String[]", "Integer[]", "Double[]", "Boolean[]")
        for line in lines:
            if line[0] == "\n":
                line = line[1:-1]
            if len(line) > 3 and line[-2] not in ("{", "}"):
                line = line[0:-1] + ";" + line[-1]
            if line.endswith(", ){\n") or line.endswith(", );\n"):
                line = line[0:-5] + line[-3:]
            if line.startswith(array_type) and not line.endswith(";\n"):
                line = line[0:-1] + ";\n"
            if line.startswith("Object"):
                temp = line.split(" ")
                temp[0] = "Double"
                _ = [temp[-1].split(";")[0]]
                temp = temp[0:-1] + _
                a = False
                for i in range(3, len(temp), 2):
                    a = self.lookup(temp[i], None)
                    if a:
                        temp[i] = "Double.parseDouble(" + temp[i] + ".toString())"
                if not a:
                    temp = temp[0:3] + ["(Double)"] + temp[3:]
                line = " ".join(temp)
                line += ";\n"
            if line.startswith("public class") and concatenation:
                line += "\n@SafeVarargs\npublic static <T> T[] concatAll(T[] first, T[]... rest) {\nint totalLength = " \
                        "first.length;\nfor (T[] array : rest) {\ntotalLength += array.length;\n}\nT[] result =" \
                        " Arrays.copyOf(first, totalLength);" \
                        "\nint offset = first.length;\nfor (T[] array : rest) {\nSystem.arraycopy(array, 0, result, " \
                        "offset, array.length);\n" \
                        "offset += array.length;\n}\nreturn result;\n}\n"
            file.write(line)
