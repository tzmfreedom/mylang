class Condition:
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def eval(self, context={}):
        if self.op == '==':
            return self.left.eval(context) == self.right.eval(context)
        elif self.op == '<':
            return self.left.eval(context) < self.right.eval(context)
        elif self.op == '>':
            return self.left.eval(context) > self.right.eval(context)
        return False