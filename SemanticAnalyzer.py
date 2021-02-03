import sys

from Node import *


class SemanticAnalyzer:
    def __init__(self):
        self.symTable = []
        self.current_scope = None
        self.error = []

    def analyze(self, node):
        if isinstance(node, AssignNode):
            if node.type != '<class \'id\'>':
                inserted = self.insert(node, self.current_scope)
                if not inserted:
                    print("Variable " + node.value + " redeclared.", file=sys.stderr)
                    self.error.append(True)
            else:
                _, index = self.lookup(node.children[0].children[0], self.current_scope)
                if _:
                    inserted = self.insert(node, self.current_scope, self.symTable[index][1])
                    if not inserted:
                        print("Variable " + node.value + " redeclared.", file=sys.stderr)
                        self.error.append(True)
        else:
            if isinstance(node, FuncNode):
                self.current_scope = str(node.name)
            for i in range(len(node.children)):
                self.analyze(node.children[i])
        if isinstance(node, ProgramNode):
            self.find_error(node)

    def find_error(self, node):
        if isinstance(node, FuncNode):
            self.current_scope = str(node.name)
        if isinstance(node, ValueNode) and node.type == "<class 'id'>" and node.value != "__name__":
            found, _ = self.lookup(node, self.current_scope)
            if not found:
                print(node.value + " not declared.", file=sys.stderr)
                self.error.append(True)
        else:
            for i in range(len(node.children)):
                self.find_error(node.children[i])

    def lookup(self, node, scope):
        for i in range(len(self.symTable)):
            if node.value in self.symTable[i] and scope in self.symTable[i]:
                return True, i
        return False, -1

    def insert(self, node, scope, type=None):
        found, _ = self.lookup(node, scope)
        if not found and type is None:
            self.symTable.append((node.value, str(node.type).split("\'")[1], scope))
            return True
        elif not (found and type is None):
            self.symTable.append((node.value, type, scope))
            return True
        else:
            return False
