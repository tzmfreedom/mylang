from statement import eval_var


class Condition:
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def eval(self):
        if self.op == '==':
            return eval_var(self.left) == eval_var(self.right)
        elif self.op == '<':
            return eval_var(self.left) < eval_var(self.right)
        elif self.op == '>':
            return eval_var(self.left) > eval_var(self.right)
        return False