import sys

from Node import *


class SemanticAnalyzer:
    def __init__(self):
        self.symTable = []
        self.current_scope = None
        self.error = []

    def analysis(self, node):
        # Update the symTab.
        if isinstance(node, AssignNode):
            inserted = False
            node_type = node.type
            if node.type != 'id':
                inserted = self.insert(node, self.current_scope, node.type)
            else:
                _, index = self.lookup(node, self.current_scope)
                if _:
                    node_type = self.symTable[index][1]
                    inserted = self.insert(node, self.current_scope, node_type)
                if not inserted:
                    self.error.append("Cannot resolve the type of " + node.value + ".")
            for i in range(len(node.children[0].children)):
                self.invalid_operation(node.children[0].children[i], node_type)
        # Update the symTab with the formal parameters of the function to avoid conflicts.
        if isinstance(node, ParamNode) and self.current_scope != 'main':
            for i in range(len(node.children)):
                if isinstance(node.children[i], ValueNode):
                    inserted = self.insert(node.children[i], self.current_scope, type="parameter")
        # Update the symTab with functions names.
        if isinstance(node, FuncNode):
            self.current_scope = str(node.value)
            inserted = self.insert(node=node, type="func", scope="global", parameters=self.control_parameters(node))
        # Check if a value exist in the symTab.
        if isinstance(node, ValueNode) and node.type == 'id':
            found, _ = self.lookup(node, self.current_scope)
            if not found and node.value != "__name__":
                self.error.append(node.value + " not declared.")
        # Recursion.
        for i in range(len(node.children)):
            self.analysis(node.children[i])
        # These type of control are done after the symTab is completed. We are controlling if the function
        # exists and has the right number of parameters.
        if isinstance(node, CallNode):
            found, _ = self.lookup(node, "global", self.control_parameters(node))
            if not found:
                self.error.append("Function " + node.value + " not defined.")

    # The function returns True if the object is in the symTab, False if not, with the index.
    def lookup(self, node, scope, parameters=None):
        if not (isinstance(node, ValueNode) or isinstance(node, CallNode) or isinstance(node, FuncNode)):
            found, index = self.lookup(node.children[0], scope)
            return found, index

        if isinstance(node, ValueNode):
            for i in range(len(self.symTable)):
                if node.value == self.symTable[i][0] and (scope == self.symTable[i][2] or scope == "global"):
                    found, index = True, i
                    return True, i
            return False, -1
        elif isinstance(node, CallNode) or isinstance(node, FuncNode):
            for i in range(len(self.symTable)):
                if node.value == self.symTable[i][0] and scope == "global" \
                        and parameters == self.symTable[i][3] and self.symTable[i][1] == "func":
                    return True, i
            return False, -1

    # Add a variable in the symTab.
    def insert(self, node, scope, type=None, parameters=None):
        # The function returns True if the object has been added. Type is used if the node.type is 'id'.
        found, _ = self.lookup(node, scope, parameters)
        if not found and type is None:
            # Save a value in symTab if type not declared.
            self.symTable.append((node.value, str(node.type), scope, parameters))
            return True
        elif not (found and type is None):
            # Save a value/func in symTab if type declared.
            self.symTable.append((node.value, type, scope, parameters))
            return True
        else:
            return False

    # Check the validity of an operation by checking if id inside it exists and have the same type.
    def invalid_operation(self, node, type=None):
        if isinstance(node, ValueNode):
            # Verify the type of the symbol in the symTab
            if node.type == 'id':
                _, index = self.lookup(node, self.current_scope)
                node_type = self.symTable[index][1]
            else:
                node_type = node.type
            if node_type != type:
                self.error.append("Invalid operation between " + str(type) + " and " + str(node_type) + ".")
        if isinstance(node, ExprNode):
            # Recursion
            for i in range(len(node.children)):
                self.invalid_operation(node.children[i], type)

    def control_parameters(self, node, counter=0):
        for i in range(len(node.children)):
            if isinstance(node.children[i], ParamNode):
                counter += 1
                counter = self.control_parameters(node.children[i], counter)
        return counter

    def print_error(self):
        print('\n'.join(self.error), file=sys.stderr)

    def print_symTab(self):
        for i in range(len(self.symTable)):
            print(str(self.symTable[i]) + "\n", end="")
