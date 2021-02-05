import sys

from Node import *


class SemanticAnalyzer:
    def __init__(self):
        self.symTable = []
        self.current_scope = None
        self.error = []

    def pre_analysis(self, node):

        # Save a variable
        if isinstance(node, AssignNode):

            if node.type != 'id':
                for i in range(len(node.children[0].children)):
                    # Verify if an id inside the assign exist before.
                    self.invalid_operation(node.children[0].children[i], node.type)

                # If the type of the node is not an id we can insert that directly in the symTab
                inserted = self.insert(node, self.current_scope)
                if not inserted:
                    self.error.append(node.value + " redeclared.")
            else:

                # If the type of the node is id, maybe it has been declared previously. We check it.
                _, index = self.lookup(node.children[0].children[0], self.current_scope)
                if _:
                    inserted = self.insert(node, self.current_scope, self.symTable[index][1])
                    if not inserted:
                        self.error.append(node.value + " redeclared.")
        else:

            # We change the current_scope based on the function we are in
            if isinstance(node, FuncNode):
                self.current_scope = str(node.value)
                self.insert(node=node, type="func", scope="Global", parameters=self.control_parameters(node))

            # Recursion
            for i in range(len(node.children)):
                self.pre_analysis(node.children[i])

        # Check variables in condition
        if isinstance(node, ConditionNode):
            for i in range(len(node.children[0].children)):
                self.check_condition(node.children[0].children[i])

        # Check errors in the AST
        if isinstance(node, ProgramNode):
            self.post_analysis(node)

    def post_analysis(self, node):

        # We change the current_scope based on the function we are in
        if isinstance(node, FuncNode):
            self.current_scope = str(node.value)

        # We check the validity of an operation, based on the assumption that the correct type
        # is the type of the first variable.
        if isinstance(node, AssignNode):
            _, index = self.lookup(node, self.current_scope)
            type = self.symTable[index][1]

            for i in range(len(node.children[0].children)):
                # We created this function in order to check the children of the node without losing the type.
                self.invalid_operation(node.children[0].children[i], type)

        # Check if called function exists
        if isinstance(node, CallNode):
            found, _ = self.lookup(node, "Global")
            if not found:
                self.error.append("function " + node.value + " not defined.")
            correct, _ = self.lookup(node, "Global", self.control_parameters(node))
            if not correct:
                self.error.append("Wrong number of parameters in " + node.value + " call.")

        # Recursion
        for i in range(len(node.children)):
            self.post_analysis(node.children[i])

    # Check if a variable exists in the symTab
    def lookup(self, node, scope, parameters=None):
        if not isinstance(node, ValueNode):
            if not isinstance(node, CallNode):
                found, index = self.lookup(node.children[0], self.current_scope)
                return found, index

        # The function returns True if the object is in the symTab, False if not, with the index.
        for i in range(len(self.symTable)):
            if node.value in self.symTable[i] and (scope in self.symTable[i] or scope == "Global") \
                    and parameters == self.symTable[i][3]:
                found, index = True, i
                return found, index
        found, index = False, -1
        return found, index

    # Add a variable in the symTab
    def insert(self, node, scope, type=None, parameters=None):
        # The function returns True if the object has been added. Type is used if the node.type is 'id'.
        found, _ = self.lookup(node, scope)
        if not found and type is None:
            # Save a value in symTab if type not declared
            self.symTable.append((node.value, str(node.type), scope, parameters))
            return True

        elif not (found and type is None):
            # Save a value/func in symTab if type declared
            self.symTable.append((node.value, type, scope, parameters))
            return True
        else:
            return False

    # Check the validity of an operation by checking if id inside it exists and have the same type
    def invalid_operation(self, node, type=None):

        if isinstance(node, ValueNode):
            # Verify the type of the symbol in the symTab
            if node.type == 'id':
                _, index = self.lookup(node, self.current_scope)
                if not _:
                    # Verify variable exist in analyze() function
                    # print(node.value + " not declared.", file=sys.stderr)
                    self.error.append(node.value + " not declared.")
                    return
                node_type = self.symTable[index][1]
            else:
                node_type = node.type
            if node_type != type:
                self.error.append("Invalid operation between " + str(type) + " and " + str(node_type))

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

    def check_condition(self, node):
        # Recursive function for all the variables in condition
        if isinstance(node, ValueNode) and node.type == 'id':
            _, index = self.lookup(node, self.current_scope)
            if not _:
                self.error.append(node.value + " not declared.")
            else:
                type = self.symTable[index][1]
                self.invalid_operation(node, type)
        elif isinstance(node, ExprNode):
            for i in range(len(node.children)):
                self.check_condition(node.children[i])

    def print_error(self):
        print('\n'.join(self.error), file=sys.stderr)
