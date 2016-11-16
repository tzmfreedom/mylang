class BasicType:
    def __init__(self, value):
        self.type = BasicType
        self.value = value

    def eval(self, context=None):
        if isinstance(self.value, list):
            return [arg.eval() for arg in self.value]
        else:
            return self.value

    def set(self, value):
        self.value = value