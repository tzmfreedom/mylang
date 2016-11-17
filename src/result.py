class Result:
    def __init__(self, result_type, result_value):
        self.type = result_type
        self.value = result_value

    def eval(self, context={}):
        return self.value