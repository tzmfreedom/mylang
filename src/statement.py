from lang_enums import StatementType, ResultType
from storage import storage
from basic_types import BasicType, Class, ClassType
from function import Function
from result import Result

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
            if 'type' in params:
                self.assign_type = params['type']
            else:
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
        elif self.type == StatementType.NEW_CLASS:
            self.class_name = params['class_name']
            self.class_args = params['class_args']
        elif self.type == StatementType.CALL_METHOD:
            self.variable_name = params['variable_name']
            self.method_name = params['method_name']
            self.method_args = params['method_args']
        elif self.type == StatementType.CLASS_DEFINE:
            self.class_name = params['class_name']
            self.methods = params['methods']
            self.properties = params['properties']

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
            result = Result(ResultType.NORMAL, None)
            if self.condition.eval(context):
                for statement in self.statementlist:
                    result = statement.eval(context)
            return result

        elif self.type == StatementType.LOOP:
            if hasattr(self, 'condition'):
                while self.condition.eval(context):
                    for statement in self.statementlist:
                        result = statement.eval(context)
                        if result.type == ResultType.BREAK:
                            return None
                        elif result.type == ResultType.CONTINUE:
                            break
            else:
                context[self.ident] = BasicType(None)
                for idx in xrange(self.loop_count):
                    context[self.ident].set(idx+1)
                    for statement in self.statementlist:
                        result = statement.eval(context)
                        if result.type == ResultType.BREAK:
                            return None
                        elif result.type == ResultType.CONTINUE:
                            break
            return None

        elif self.type == StatementType.ASSIGN:
            if hasattr(self, 'assign_type'):
                if self.assign_type == 'increment':
                    value = Statement(StatementType.VAR, self.lineno, {'variable_name': self.variable_name}).eval() + 1
                else:
                    value = Statement(StatementType.VAR, self.lineno, {'variable_name': self.variable_name}).eval() - 1

                Statement(StatementType.ASSIGN,
                          self.lineno,
                          {
                              'variable_name': self.variable_name,
                              'expression': BasicType(value)
                          }).eval()
                return Result(ResultType.NORMAL, value)
            else:
                # ToDo: refactoring
                if self.expression.type == StatementType.EXPRESSION or self.expression.type == StatementType.NEW_CLASS:
                    expression = self.expression.eval()
                else:
                    expression = self.expression

                if self.variable_name in context:
                    context[self.variable_name] = expression
                else:
                    storage.variables[self.variable_name] = expression

                return Result(ResultType.NORMAL, expression)
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
                return BasicType(storage.user_functions[self.function_name].eval(args, context))
            return Result(ResultType.NORMAL, None)
        elif self.type == StatementType.FUNCTION_DEFINE:
            storage.user_functions[self.function_name] = Function(self.function_args, self.statementlist)
            return Result(ResultType.NORMAL, None)
        elif self.type == StatementType.EXPRESSION:
            if self.op == '+':
                return BasicType(self.left.eval() + self.right.eval())
            elif self.op == '-':
                return BasicType(self.left.eval() - self.right.eval())
            elif self.op == '*':
                return BasicType(self.left.eval() * self.right.eval())
            elif self.op == '/':
                return BasicType(self.left.eval() / self.right.eval())
        elif self.type == StatementType.BREAK:
            return Result(ResultType.BREAK, None)
        elif self.type == StatementType.CONTINUE:
            return Result(ResultType.CONTINUE, None)
        elif self.type == StatementType.RETURN:
            return Result(ResultType.RETURN, None)
        elif self.type == StatementType.NEW_CLASS:
            klass = storage.classes[self.class_name]
            return Class(klass, self.class_args)
        elif self.type == StatementType.CLASS_DEFINE:
            klass = ClassType(self.class_name, self.properties, self.methods)
            storage.classes[self.class_name] = klass
        elif self.type == StatementType.CALL_METHOD:
            klass = storage.variables[self.variable_name]
            if self.method_name in klass.type.methods:
                klass.type.methods[self.method_name].eval(self.method_args)
            else:
                print('Method Missing')
        else:
            return Result(ResultType.NORMAL, None)

