import sys

from AST import *
from Lexer import reserved


class SemanticAnalyzer:
    def __init__(self):
        self.symTable = []
        self.current_scope = None
        self.error = []

    def analysis(self, node):
        # Update the symTab.
        if isinstance(node, AssignNode):
            inserted = False
            node_type = ""
            # Specify if we are in a list.
            if isinstance(node.children[0].children[0], ListNode):
                node_type = "list"
                node_type += "_"
            if isinstance(node.children[0].children[0], TupleNode):
                node_type = "tuple"
                node_type += "_"
            if node.type != 'id':
                node_type += str(node.type)
                inserted = self.insert(node=node, scope=self.current_scope, type=node_type, length=self.length(node.children[0].children[0], (ListNode, TupleNode)))
            else:
                _, index = self.lookup(node.children[0].children[0], self.current_scope)
                if _:
                    if isinstance(node.children[0].children[0], ListNode) \
                            or isinstance(node.children[0].children[0], TupleNode):
                        node_type += "_" + self.symTable[index][1]
                        inserted = self.insert(node=node, scope=self.current_scope, type=node_type, length=self.length(node.children[0].children[0], (ListNode, TupleNode)))
                    else:
                        node_type += self.symTable[index][1]
                        inserted = self.insert(node=node, scope=self.current_scope, type=node_type, length=self.length(node.children[0].children[0], (ListNode, TupleNode)))
                if not inserted:
                    self.error.append("Cannot resolve the type of " + node.value + ".")
            for i in range(len(node.children[0].children)):
                self.invalid_operation(node.children[0].children[i], node_type)
        # Update the symTab with the formal parameters of the function to avoid conflicts.
        if isinstance(node, ParamNode) and self.current_scope != 'main':
            for i in range(len(node.children)):
                if isinstance(node.children[i], ValueNode):
                    inserted = self.insert(node=node.children[i], scope=self.current_scope, type="generic")
        # Update the symTab with functions names.
        if isinstance(node, FuncNode):
            self.current_scope = str(node.value)
            inserted = self.insert(node=node, type="func", scope="global", parameters=self.length(node, ParamNode))
            if not inserted:
                self.error.append("Function " + node.value + " already exists.")
        # Check if a value exist in the symTab.
        if isinstance(node, ValueNode) and node.type == 'id':
            found, _ = self.lookup(node=node, scope=self.current_scope)
            if not found and node.value != "__name__":
                self.error.append(node.value + " not declared.")
            else:
                found, _ = self.lookup(node=node, scope=self.current_scope, length=node.index)
                if not found and node.value != "__name__":
                    self.error.append("Error with " + node.value + ": index out of range")
        # Recursion.
        for i in range(len(node.children)):
            self.analysis(node.children[i])
        # These type of control are done after the symTab is completed. We are controlling if the function
        # exists and has the right number of parameters.
        if isinstance(node, CallNode):
            found, _ = self.lookup(node=node, scope="global", parameters=self.length(node, ParamNode))
            if not found and node.value not in reserved:
                self.error.append("Function " + node.value + " not defined.")

    # The function returns True if the object is in the symTab, False if not, with the index.
    def lookup(self, node, scope, parameters=0, length=0):
        if not (isinstance(node, ValueNode) or isinstance(node, CallNode) or isinstance(node, FuncNode)):
            found, index = self.lookup(node.children[0], scope)
            return found, index

        if isinstance(node, ValueNode):
            for i in range(len(self.symTable)):
                if node.value == self.symTable[i][0] and (scope == self.symTable[i][2]
                                                          or self.symTable[i][2] == "global") and\
                                                            ((self.symTable[i][4] * -1 <= length < self.symTable[i][4])
                                                             or length == 0):
                    return True, i
            return False, -1
        elif isinstance(node, CallNode) or isinstance(node, FuncNode):
            for i in range(len(self.symTable)):
                if node.value == self.symTable[i][0] and scope == "global" \
                        and parameters == self.symTable[i][3] and self.symTable[i][1] == "func":
                    return True, i
            return False, -1

    # Add a variable in the symTab. The function returns True if the object has been added.
    # Type is used if the node.type is 'id'.
    def insert(self, node, scope, type=None, parameters=0, length=0):
        if type is None:
            # Save a value in symTab if type not declared.
            self.symTable.append((node.value, str(node.type), scope, parameters, length))
            return True
        else:
            if type == "call":
                type = "generic"
            # Save a value/func in symTab if type declared.
            self.symTable.append((node.value, type, scope, parameters, length))
            return True

    # Check the validity of an operation by checking if id inside it exists and have the same type.
    def invalid_operation(self, node, type=None):
        if isinstance(node, ValueNode):
            # Verify the type of the symbol in the symTab.
            if node.type == 'id':
                _, index = self.lookup(node, self.current_scope)
                node_type = self.symTable[index][1]
            else:
                node_type = node.type
            if node_type != type:
                self.error.append("Invalid operation between " + str(type) + " and " + str(node_type) + ".")
        if isinstance(node, ExprNode):
            # Recursion.
            for i in range(len(node.children)):
                self.invalid_operation(node.children[i], type)

    # Counter.
    def length(self, node, type, counter=0):
        for i in range(len(node.children)):
            if isinstance(node.children[i], type):
                counter += 1
                counter = self.length(node.children[i], type, counter)
        return counter

    def print_error(self):
        print('\n'.join(self.error), file=sys.stderr)

    def print_symtab(self):
        for i in range(len(self.symTable)):
            print(str(self.symTable[i]) + "\n", end="")

    def get_symtab(self):
        return self.symTable
