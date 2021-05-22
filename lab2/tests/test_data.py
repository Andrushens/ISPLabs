class SimpleClass:
    def __init__(self):
        self.ruin = True
        self.motivation = None
        self.name = "Te4ka"

    def suicide(self):
        return "D:"

class ComplexClass:
    def __init__(self):
        self.teammate = SimpleClass()
        self.const = int_glob
        self.tuple = tuple([SimpleClass(), self.teammate.suicide])
        self.name = 'Cmplx class'

    def kill(self):
        return "z x ty4ka pauza c" + str_glob

def cmplx_func(a):
    b = int_glob
    return simple_func(2)*b**a

def simple_func(a):
    return a*a

simple_lambda = lambda q: q*q
int_glob = 4
str_glob = 'global'
list_1 = [1, '2', 3.3]
dict_1 = {1: 1, None: None, False: False}