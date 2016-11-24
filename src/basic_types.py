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
    def __init__(self, method_name, arg_names, statementlist):
        self.name = method_name
        self.arg_names = arg_names
        self.statementlist = statementlist

    def eval(self, args, context=None):
        if len(args) != len(args):
            print("Method Argument Mismatch!!")
        else:
            if context is None:
                new_context = {}
            else:
                new_context = context.copy()
            new_context.update({self.arg_names[i]: BasicType(args[i]) for i in xrange(len(args))})
            for statement in self.statementlist:
                statement.eval(new_context)

class Class:
    def __init__(self, class_type, args):
        self.type = class_type
        self.properties = {property: None for property in self.type.properties}

        if 'init' in self.type.methods:
            self.type.methods['init'].eval(args)


    def eval(self):
        return self.type.class_name