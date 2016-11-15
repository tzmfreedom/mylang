from basic_types import BasicType


class Storage:
    def __init__(self, native_functions={}):
        self.variables = {}
        self.native_functions = native_functions
        self.user_functions = {}


def echo(args):
    print("echo {0}".format(args[0]))
    return BasicType(None)


def fib_main(args):
    return BasicType(fib(args[0]))


def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

storage = Storage({
    'echo': echo,
    'fib': fib_main,
})