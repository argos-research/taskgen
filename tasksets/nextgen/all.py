from taskgen.taskset import BlockTaskSet
from taskgen.blocks import *
import random


class Random1(BlockTaskSet):
    """One task with random priority, period and binary. No variants, not repeatable"""
    def __init__(self, _seed=None, size=1):
        random.seed(seed) # use same seed like AttributeTaskSet
        super().__init__(
            binaries.RandomList(size, 1),
            priority.Custom,
            period.Random,
            jobs.Random,
            seed = _seed
        )

class Random10(Random1):
    """10 tasks with random priorities, periods and binaries. No variants, not repeatble"""
    def __init__(self, seed=None):
        super().__init__(seed, 10)

class Random100(Random1):
    """100 tasks with random priorities, periods and binaries. No variants, not repeatable."""
    def __init__(self, seed=None):
        super().__init__(seed, 100)

class Random1k(Random1):
    """1000 tasks with random priorities, periods and binaries. No variants, not repeatable."""
    def __init__(self, seed=None):
        super().__init__(seed, 1000)

class Random10k(Random1):
    """10.000 tasks with random priorities, periods and binaries. No variants, not repeatable."""
    def __init__(self, seed=None):
        super().__init__(seed, 10000)

class Repeatable1(Random1):
    """One task without variants."""
    def __init__(self):
        super().__init__(0)  # seed: 0

class Repeatable10(Random10):
    """10 tasks without variants."""
    def __init__(self):
        super().__init__(0)  # seed: 0

class Repeatable100(Random100):
    """100 tasks without variants."""
    def __init__(self):
        super().__init__(0)  # seed: 0

class Repeatable1k(Random1k):
    """1000 tasks without variants."""
    def __init__(self):
        super().__init__(0)  # seed: 0

class Repeatable10k(Random10k):
    """10000 tasks without variants."""
    def __init__(self):
        super().__init__(0)  # seed: 0

        
class RandomSize(BlockTaskSet):
    """Random taskset size with random priorities, periods, tasks and task arguments"""
    def __init__(self, _seed=None, size=1):
        random.seed(_seed)  # use the same seed like AttributeTaskSet...
        task_count = random.randint(1, 100)
        task_par1_max = 100

        super().__init__(
            binaries.RandomList(task_count, task_par1_max),
            priority.Random,
            period.Random,
            seed=_seed
        )
