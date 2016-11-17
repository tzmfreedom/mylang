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

class ClassType:
    def __init__(self, class_name, properties, methods=None):
        self.class_name = class_name
        self.properties = properties
        self.methods = {}
        if methods is not None:
            for method in methods:
                self.methods[method.name] = method

class Method:
    def __init__(self, method_name, args, statementlist):
        self.name = method_name
        self.args = args
        self.statementlist = statementlist

    def eval(self, args, context={}):
        if len(args) != len(args):
            pass
        else:
            for statement in self.statementlist:
                statement.eval()

class Class:
    def __init__(self, class_type, args):
        self.type = class_type
        self.args = args


    def eval(self):
        return self.type.class_name