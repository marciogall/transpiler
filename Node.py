class AST:
    pass


class ProgramNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "ProgramNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class StatementsNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return " StatementsNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class StatementNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return " StatementNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class FuncNode(AST):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __repr__(self):
        return " FuncNode{ Value: " + str(self.value) + ", Children:{"\
               + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ParamNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return " ParamNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class AssignsNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return " AssignsNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class AssignNode(AST):
    def __init__(self, value, children):
        self.value = value.value
        self.children = children
        self.type = children[0].children[0].type

    def __repr__(self):
        return " AssignNode{ Value: " + str(self.value) + ", Type: " + str(self.type) + ", Children:{" \
               + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class CallNode(AST):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __repr__(self):
        return " CallNode{ Value: " + str(self.value) + ", Children:{"\
               + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class IfNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return " IfNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class WhileNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return " WhileNode{ Children:{" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ConditionNode(AST):
    def __init__(self, children):
        if len(children) == 3:
            self.type = children[1].value
        else:
            self.type = children[0].children[0].value
        self.children = children

    def __repr__(self):
        return " ConditionNode{ Type: " + str(self.type) + ", Children:{" \
               + str(self.children.__repr__()).split("[")[1].split("]")[0] \
               + "}"


class RelopNode(AST):
    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self):
        return " RelopNode{ Value: " + str(self.value) + "}"


class ExprNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return " ExprNode{ Children: {" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ListNode(AST):
    def __init__(self, children):
        self.children = children
        if len(children) > 0:
            self.value = children[0]
            self.type = children[0].type
        else:
            self.type = None

    def __repr__(self):
        return " List Node{ Value: " + str(self.value) + " Type: " + str(self.type) \
               + " Children: {" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class TupleNode(AST):
    def __init__(self, children):
        self.children = children
        if len(children) > 1:
            self.value = children[0]
            self.type = children[0].type

    def __repr__(self):
        return " TupleNode{ Value: " + str(self.value) + " Type: " + str(self.type) \
               + " Children: {" + str(self.children.__repr__()).split("[")[1].split("]")[0] + "}"


class ValueNode(AST):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []

    def __repr__(self):
        return " ValueNode{ Type: " + str(self.type) + " Value: " + str(self.value) + "}"
