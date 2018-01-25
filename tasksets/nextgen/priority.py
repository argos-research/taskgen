from taskgen.taskset import BlockTaskSet
from taskgen.blocks import *
import random


class Low1(BlockTaskSet):
    """1 tasks with random periods, binaries and only low priorities"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            binaries.RandomList(size, 1),
            priority.LowRandom,  # only uuse low prioties
            period.Random
        )

class Low10(Low1):
    """10 tasks with random periods, binaries and only low priorities"""
    def __init__(self, seed=None):
        super().__init__(seed, 10)

class Low100(Low1):
    """100 tasks with random periods, binaries and only low priorities"""
    def __init__(self, seed=None):
        super().__init__(seed, 100)

class Low1k(Low1):
    """1000 tasks with random periods, binaries and only low priorities"""
    def __init__(self, seed=None):
        super().__init__(seed, 1000)

class High1(BlockTaskSet):
    """1 tasks with random periods, binaries and only high priorities"""
    def __init__(self, seed=None, size=1):
        random.seed(seed)
        super().__init__(
            binaries.RandomList(size, 1),
            priority.HighRandom,  # only uuse high prioties
            period.Random
        )

class High10(High1):
    """10 tasks with random periods, binaries and only high priorities"""
    def __init__(self, seed=None):
        super().__init__(seed, 10)

class High100(High1):
    """100 tasks with random periods, binaries and only high priorities"""
    def __init__(self, seed=None):
        super().__init__(seed, 100)

class High1k(High1):
    """1000 tasks with random periods, binaries and only high priorities"""
    def __init__(self, seed=None):
        super().__init__(seed, 1000)
