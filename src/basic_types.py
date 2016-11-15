class BasicType:
    def __init__(self, value):
        self.type = BasicType
        self.value = value

    def eval(self, context={}):
        return self.value