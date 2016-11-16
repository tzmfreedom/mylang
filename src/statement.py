from lang_enums import StatementType
from storage import storage
from basic_types import BasicType
from function import Function

class Statement:
    def __init__(self, type, lineno, params):
        self.type = type
        self.lineno = lineno
        if self.type == StatementType.VAR:
            self.variable_name = params['variable_name']
        elif self.type == StatementType.IF or (self.type == StatementType.LOOP and 'condition' in params):
            self.condition = params['condition']
            self.statementlist = params['statementlist']
        elif self.type == StatementType.LOOP and 'ident' in params:
            self.ident = params['ident']
            self.loop_count = int(params['loop_count'].eval())
            self.statementlist = params['statementlist']
        elif self.type == StatementType.ASSIGN:
            self.variable_name = params['variable_name']
            self.expression = params['expression']
        elif self.type == StatementType.FUNCTION_CALL:
            self.function_name = params['function_name']
            self.function_args = params['args']
        elif self.type == StatementType.FUNCTION_DEFINE:
            self.function_name = params['function_name']
            self.function_args = params['function_args']
            self.statementlist = params['statementlist']
        elif self.type == StatementType.EXPRESSION:
            self.left = params['left']
            self.right = params['right']
            self.op = params['op']

    def eval(self, context=None):
        if context is None:
            context = {}

        if self.type == StatementType.VAR:
            if self.variable_name in context:
                return context[self.variable_name].eval()
            elif self.variable_name in storage.variables:
                return storage.variables[self.variable_name].eval()
            else:
                return None

        elif self.type == StatementType.IF:
            if self.condition.eval(context):
                for statement in self.statementlist:
                    statement.eval(context)
        elif self.type == StatementType.LOOP:
            if hasattr(self, 'condition'):
                while self.condition.eval(context):
                    for statement in self.statementlist:
                        statement.eval(context)
            else:
                context[self.ident] = BasicType(None)
                for idx in xrange(self.loop_count):
                    context[self.ident].set(idx+1)
                    for statement in self.statementlist:
                        statement.eval(context)

        elif self.type == StatementType.ASSIGN:
            if self.expression.type == StatementType.EXPRESSION:
                expression = self.expression.eval()
            else:
                expression = self.expression

            if self.variable_name in context:
                context[self.variable_name] = expression
            else:
                storage.variables[self.variable_name] = expression
        elif self.type == StatementType.FUNCTION_CALL:
            args = []
            for arg in self.function_args:
                if arg.type == StatementType.FUNCTION_CALL:
                    args.append(arg.eval(context).eval(context))
                else:
                    args.append(arg.eval(context))
            if self.function_name in storage.native_functions:
                return storage.native_functions[self.function_name](args)
            elif self.function_name in storage.user_functions:
                return storage.user_functions[self.function_name].eval(args, context)
            return BasicType(None)
        elif self.type == StatementType.FUNCTION_DEFINE:
            storage.user_functions[self.function_name] = Function(self.function_args, self.statementlist)
        elif self.type == StatementType.EXPRESSION:
            if self.op == '+':
                return BasicType(self.left.eval() + self.right.eval())
            elif self.op == '-':
                return BasicType(self.left.eval() - self.right.eval())
            elif self.op == '*':
                return BasicType(self.left.eval() * self.right.eval())
            elif self.op == '/':
                return BasicType(self.left.eval() / self.right.eval())
