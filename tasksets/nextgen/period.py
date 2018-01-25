from taskgen.taskset import BlockTaskSet
from taskgen.blocks import *
import random


class Low1(BlockTaskSet):
    """1 tasks with random priority, binaries and only low period"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            binaries.RandomList(size, 1),
            priority.Random,
            period.LowRandom
        )

class Low10(Low1):
    """10 tasks with random priorities, binaries and only low periods"""
    def __init__(self, seed=None):
        super().__init__(seed, 10)

class Low100(Low1):
    """100 tasks with random priorities, binaries and only low periods"""
    def __init__(self, seed=None):
        super().__init__(seed, 100)

class Low1k(Low1):
    """1000 tasks with random priorities, binaries and only low periods"""
    def __init__(self, seed=None):
        super().__init__(seed, 1000)

class High1(BlockTaskSet):
    """1 tasks with random priorities, binaries and only high periods"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            binaries.RandomList(size, 1),
            priority.Random,
            period.HighRandom
        )

class High10(High1):
    """10 tasks with random priorities, binaries and only high periods"""
    def __init__(self, seed=None):
        super().__init__(seed, 10)

class High100(High1):
    """100 tasks with random priorities, binaries and only high periods"""
    def __init__(self, seed=None):
        super().__init__(seed, 100)

class High1k(High1):
    """1000 tasks with random priorities, binaries and only high periods"""
    def __init__(self, seed=None):
        super().__init__(seed, 1000)
