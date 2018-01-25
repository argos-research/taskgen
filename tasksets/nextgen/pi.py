from taskgen.taskset import BlockTaskSet
from taskgen.blocks import *
import random


class Variants10(BlockTaskSet):
    """1 tasks with random priority, medium period and 10 variants of `pi` binary"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            pi.Variants(10),
            priority.Random,
            period.MediumRandom
        )

class Variants100(BlockTaskSet):
    """1 tasks with random priority, medium period and 100 variants of `pi` binary"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            pi.Variants(100),
            priority.Random,
            period.MediumRandom
        )

class Variants1m(BlockTaskSet):
    """1 tasks with random priority, medium period and 1 million variants of `pi` binary"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            pi.Variants(1000000),
            priority.Random,
            period.MediumRandom
        )

class ThreeVariants100(BlockTaskSet):
    """3 tasks with random priority, medium period and 100 variants of `pi` binary. (100^3 variants)"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            [pi.Variants(100), pi.Variants(100), pi.Variants(100)],
            priority.Random,
            period.MediumRandom
        )
