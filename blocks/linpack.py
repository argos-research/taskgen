"""
Drives the single precision LINPACK benchmark program. Parameter N is the
problem size. Default value is `N = 1000`.
"""
import random

def Value(arg1):
    return {
        "pkg" : "linpack",
        "quota" : "1M", # not sure, if enough...
        "config" : {
            "arg1" : arg1
        }
    }


"""
Random argument `arg1`, `n` is the maximum value for `arg1`.
"""
def Random(n):
    return Value(random.randint(1, n))



def Variants(variants):
    return Value(range(variants))


