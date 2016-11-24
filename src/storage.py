from basic_types import BasicType

class Storage:
    def __init__(self, native_functions={}):
        self.variables = {}
        self.native_functions = native_functions
        self.user_functions = {}
        self.classes = {}


class NativeFunction:
    def eval(self, args, context):
        raise Exception('No Action')


class Echo(NativeFunction):
    def eval(self, args, context):
        print("echo {0}".format(args[0]))
        return BasicType(None)


class Fib(NativeFunction):
    def fib_main(args):
        return BasicType(fib(args[0]))


def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

storage = Storage({
    'echo': Echo(),
    'fib': Fib(),
})