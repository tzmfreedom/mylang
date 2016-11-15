from lang_enums import StatementType
from storage import storage


def eval_var(var):
    if isinstance(var, Statement):
        return var.eval()
    return var


class Statement:
    def __init__(self, type, lineno, params):
        self.type = type
        self.lineno = lineno
        if self.type == StatementType.VAR:
            self.variable_name = params['variable_name']
        elif self.type == StatementType.IF or self.type == StatementType.LOOP:
            self.condition = params['condition']
            self.statementlist = params['statementlist']
        elif self.type == StatementType.ASSIGN:
            self.variable_name = params['variable_name']
            self.expression = params['expression']
        elif self.type == StatementType.FUNCTION_CALL:
            self.function_name = params['function_name']
            self.function_args = params['args']
        elif self.type == StatementType.FUNCTION_DEFINE:
            self.function_name = params['function_name']
            self.function_arg_length = params['function_arg_length']
            self.statementlist = params['statementlist']

    def eval(self):
        # print(self.type)
        if self.type == StatementType.VAR:
            return storage.variables[self.variable_name]
        elif self.type == StatementType.IF:
            if self.condition.eval():
                for statement in self.statementlist:
                    statement.eval()
        elif self.type == StatementType.LOOP:
            pass
        elif self.type == StatementType.ASSIGN:
            storage.variables[self.variable_name] = self.expression
        elif self.type == StatementType.FUNCTION_CALL:
            args = []
            for arg in self.function_args:
                args.append(eval_var(arg))
            return storage.native_functions[self.function_name](args)
        elif self.type == StatementType.FUNCTION_DEFINE:
            storage.user_functions[self.function_name] = self.statementlist
