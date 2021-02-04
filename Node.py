
class AST:
    pass


class ValueNode(AST):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []

    def __repr__(self):
        return "Value Node: " + str(self.type) + " " + str(self.value)


class ProgramNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "Program Node: " + str(self.children.__repr__())


class StatementsNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "Statements Node: " + str(self.children.__repr__())


class StatementNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "Statement Node: " + str(self.children.__repr__())


class FuncNode(AST):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __repr__(self):
        return "Func Node: " + str(self.value) + " " + str(self.children.__repr__())


class ParamNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "Param Node: " + str(self.children.__repr__())


class AssignsNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "Assigns Node: " + str(self.children.__repr__())


class AssignNode(AST):
    def __init__(self, value, children):
        self.value = value.value
        self.children = children
        self.type = children[0].children[0].type

    def __repr__(self):
        return "Assign Node: " + str(self.value) + " " + str(self.children.__repr__()) + " " + str(self.type)


class CallNode(AST):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __repr__(self):
        return "Call Node: " + str(self.value) + " " + str(self.children.__repr__())


class IfNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "If Node: " + str(self.children.__repr__())


class WhileNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "While Node: " + str(self.children.__repr__())


class ConditionNode(AST):
    def __init__(self, children):
        if len(children) == 3:
            self.type = children[1].value
        else:
            self.type = children[0].children[0].value
        self.children = children

    def __repr__(self):
        return "Condition Node: " + str(self.type) + " " + str(self.children.__repr__())


class RelopNode(AST):
    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self):
        return "Relop Node: " + str(self.value)


class ExprNode(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "Expr Node: " + str(self.children.__repr__())


class ListNode(AST):
    def __init__(self, children):
        self.children = children
        if len(children) > 1:
            self.value = children[0]
            self.type = children[0].type

    def __repr__(self):
        return "List Node: " + str(self.value) + " " + str(self.type) + " " + str(self.children.__repr__())


class TupleNode(AST):
    def __init__(self, children):
        self.children = children
        if len(children) > 1:
            self.value = children[0]
            self.type = children[0].type

    def __repr__(self):
        return "Tuple Node: " + str(self.value) + " " + str(self.type) + " " + str(self.children.__repr__())
