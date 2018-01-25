import random
from taskgen.blocks import hey,cond_mod,cond_42,idle,pi,linpack,tumatmul

"""
Returns a list of all binary and randomized values.
"""
def Random(par1_max):
    return [
        hey.HelloWorld,
        cond_mod.Random(par1_max),
        cond_42.Random(par1_max),
        idle.Idle,
        pi.Random(par1_max),
        linpack.Random(par1_max),
        tumatmul.Random(par1_max),
    ]

"""
Returns a list of size `size` with random tasks.
"""
def RandomList(size, par1_max):
    return [random.choice(Random(par1_max)) for x in range(size)]
