from AST import *


class CodeGenerator:
    def __init__(self, symTable):
        self.symTable = symTable
        self.current_scope = None

    def generate(self, node, output):
        self.generate_code(node, output)

    def generate_code(self, node, output):
        if isinstance(node, ProgramNode):
            output.write("public Class main{\n")
            self.generate_code(node.children[0], output)
            output.write("\n}")

        if isinstance(node, StatementsNode):
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)

        if isinstance(node, StatementNode):
            if node.value != "return":
                self.generate_code(node.children[0], output)
            else:
                output.write("return ")
                for i in range(len(node.children)):
                    self.generate_code(node.children[i], output)
                output.write(";\n")

        if isinstance(node, FuncNode):
            self.current_scope = str(node.value)
            output.write("public static void " + str(node.value) + "(")
            if isinstance(node.children[0], ParamNode):
                self.generate_code(node.children[0], output)
                output.write("){\n")
                self.generate_code(node.children[1], output)
            else:
                output.write("){\n")
                self.generate_code(node.children[0], output)
            output.write("}\n")

        if isinstance(node, ParamNode):
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)

        if isinstance(node, AssignsNode):
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)

        if isinstance(node, AssignNode):
            i = self.lookup(node.value, self.current_scope)
            node_type = str(self.symTable[i][1])
            if node_type != "generic":
                if node_type[0:5] == "list_":
                    node_type = node_type[5:] + "[]"
                elif node_type[0:6] == "tuple_":
                    node_type = node_type[6:] + "[]"
                output.write(node_type)
            output.write(" " + str(node.value) + " = ")
            if str(self.symTable[i][1])[0:5] == "list_" or str(self.symTable[i][1])[0:6] == "tuple_":
                output.write("[")
            self.generate_code(node.children[0], output)
            if str(self.symTable[i][1])[0:5] == "list_" or str(self.symTable[i][1])[0:6] == "tuple_":
                output.write("]")
            output.write(";\n")

        if isinstance(node, CallNode):
            output.write(node.value)
            output.write("()")

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
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)

        if isinstance(node, ListNode) or isinstance(node, TupleNode):
            for i in range(len(node.children)):
                self.generate_code(node.children[i], output)

        if isinstance(node, ValueNode):
            output.write(str(node.value))

    # The function returns the index.
    def lookup(self, value, scope, parameters=0, length=0):
        for i in range(len(self.symTable)):
            if value == self.symTable[i][0] and scope in (self.symTable[i][2], "global"):
                return i
