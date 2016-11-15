from basic_types import BasicType


context = {}

class Function:
    def __init__(self, arg_names, statementlist):
        self.arg_names = arg_names
        self.arg_length = len(arg_names)
        self.statementlist = statementlist

    def eval(self, args, context={}):
        if len(args) != self.arg_length:
            print('ArgumentError!!')
        else:
            new_context = context.copy()
            new_context.update({self.arg_names[i]: BasicType(args[i]) for i in xrange(len(self.arg_names))})
            for statement in self.statementlist:
                statement.eval(new_context)
