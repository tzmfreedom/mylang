from lang_enums import StatementType
from storage import storage
from basic_type import BasicType

class Statement(object):
    def __init__(self, lineno):
        self.lineno = lineno

class AssignStatement(Statement):
    def __init__(self, lineno, ident, expression):
        super(AssignStatement, self).__init__(lineno)
        self.type = StatementType.ASSIGN
        self.ident = ident
        self.expression = expression

    def eval(self):
        storage.variables[self.ident] = self.expression

class CalculateStatement(Statement):
    def __init__(self, lineno, operator, left, right):
        super(CalculateStatement, self).__init__(lineno)
        self.type = StatementType.EXPRESSION
        self.left = left
        self.right = right
        self.operator = operator

    def eval(self):
        if self.operator == '+':
            return BasicType(self.left.eval().value + self.right.eval().value)
        elif self.operator == '-':
            return BasicType(self.left.eval().value - self.right.eval().value)
        elif self.operator == '*':
            return BasicType(self.left.eval().value * self.right.eval().value)
        elif self.operator == '/':
            return BasicType(self.left.eval().value / self.right.eval().value)
        elif self.operator == '%':
            return BasicType(self.left.eval().value % self.right.eval().value)
