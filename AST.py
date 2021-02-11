def print_tree(d, indent=0):
    print("\t" * indent + "{")
    for key, value in d.items():
        print('\t' * indent + str(key) + ":")
        if isinstance(value, dict):
            print_tree(value, indent + 1)
        else:
            print('\t' * (indent+1) + str(value))
    print('\n' + '\t' * indent + "}")


class AST:
    pass


class ProgramNode(AST):
    def __init__(self, children):
        self.children = children
        self.tree = {
            "node": "Root Node",
            "value": None,
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return "ProgramNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class StatementsNode(AST):
    def __init__(self, children):
        self.children = children
        self.tree = {
            "node": "Statements Node",
            "value": None,
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " StatementsNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class StatementNode(AST):
    def __init__(self, children, value=None):
        self.children = children
        self.value = value
        self.tree = {
            "node": "Statement Node",
            "value": str(self.value),
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " StatementNode{ Value: " + str(self.value) + ", Children:{" \
               + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class FuncNode(AST):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.tree = {
            "node": "Function Node",
            "value": str(self.value),
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " FuncNode{ Value: " + str(self.value) + ", Children:{"\
               + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ParamNode(AST):
    def __init__(self, children):
        self.children = children
        self.tree = {
            "node": "Parameter Node",
            "value": None,
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " ParamNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class AssignsNode(AST):
    def __init__(self, children):
        self.children = children
        self.tree = {
            "node": "Assignements Node",
            "value": None,
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " AssignsNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class AssignNode(AST):
    def __init__(self, value, children):
        self.value = value.value
        self.children = children
        if not isinstance(children[0].children[0], CallNode):
            self.type = children[0].children[0].type
        else:
            self.type = "call"
        self.tree = {
            "node": "Assignment Node",
            "value": str(self.value),
            "type": str(self.type),
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " AssignNode{ Value: " + str(self.value) + ", Type: " + str(self.type) + ", Children:{" \
               + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class CallNode(AST):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.tree = {
            "node": "Call Node",
            "value": str(self.value),
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " CallNode{ Value: " + str(self.value) + ", Children:{"\
               + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class IfNode(AST):
    def __init__(self, children):
        self.children = children
        self.tree = {
            "node": "If Node",
            "value": None,
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " IfNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class WhileNode(AST):
    def __init__(self, children):
        self.children = children
        self.tree = {
            "node": "While Node",
            "value": None,
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " WhileNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ConditionNode(AST):
    def __init__(self, children):
        if len(children) == 3:
            self.type = children[1].value
        else:
            self.type = None
        self.children = children
        self.tree = {
            "node": "Condition Node",
            "value": None,
            "type": str(self.type),
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " ConditionNode{ Type: " + str(self.type) + ", Children:{" \
               + str(self.children.__repr__()).split("[")[1].split("]")[0] \
               + "}"


class RelopNode(AST):
    def __init__(self, value):
        self.value = value
        self.children = []
        self.tree = {
            "node": "Relational Operator Node",
            "value": str(self.value),
            "type": None,
            "index": None,
            "children": None
        }

    def __repr__(self):
        return " RelopNode{ Value: " + str(self.value) + "}"


class ExprNode(AST):
    def __init__(self, children, value=None):
        self.children = children
        self.value = value
        self.tree = {
            "node": "Expression Node",
            "value": str(self.value),
            "type": None,
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " ExprNode{ Value: " + str(self.value) + " Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ListNode(AST):
    def __init__(self, children):
        self.children = children
        if len(children) > 0:
            self.value = children[0]
            self.type = children[0].type
        else:
            self.type = None
            self.value = None
        self.tree = {
            "node": "List Node",
            "value": None,
            "type": str(self.type),
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " List Node{ Value: " + str(self.value) + ", Type: " + str(self.type) \
               + ", Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class TupleNode(AST):
    def __init__(self, children):
        self.children = children
        if len(children) > 0:
            self.value = children[0]
            self.type = children[0].type
        else:
            self.type = None
            self.value = None
        self.tree = {
            "node": "Tuple Node",
            "value": None,
            "type": str(self.type),
            "index": None,
            "children": {key: value for i in range(len(self.children)) for key, value in self.children[i].tree.items()}
        }

    def __repr__(self):
        return " TupleNode{ Value: " + str(self.value) + ", Type: " + str(self.type) \
               + ", Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ValueNode(AST):
    def __init__(self, type, value, index=0):
        self.type = type
        self.value = value
        self.children = []
        self.index = index
        self.tree = {
            "node": "Value Node",
            "value": str(self.value),
            "type": str(self.type),
            "index": str(self.index),
            "children": None
        }

    def __repr__(self):
        return " ValueNode{ Type: " + str(self.type) + ", Value: " + str(self.value) + ", Index: " + str(self.index) + "}"
