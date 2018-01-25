from taskgen.taskset import BlockTaskSet, TaskSet
from taskgen.task import Task
from taskgen.blocks import *
import random


class Hey(BlockTaskSet):
    """One task with random priority, period and binary. No variants, not repeatable"""
    def __init__(self,  size=1):
        super().__init__(
            [hey.HelloWorld] * size,
            priority.Random,
            period.Custom(0),
            jobs.Custom(0),
        )

class Hey10(Hey):
    def __init__(self):
        super().__init__(10)

class Manual(TaskSet):
    """Static task with the `hey` binary. 
    
    It is possible to create a task from a dictionary. All values from the dict
    are mapped directly to a xml represenation.
    """
    def __init__(self):
        super().__init__()
        task = Task({
            "id" : 1,
            "executiontime" : 1000,
            "criticaltime" : 1000,
            "priority" : 52,
            "period" : 0,
            "numberofjobs" : 0,
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {}
        })
        self.append(task)

        task = Task({
            "id" : 2,
            "executiontime" : 1000,
            "criticaltime" : 1000,
            "priority" : 51,
            "period" : 0,
            "numberofjobs" : 0,
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {}
        })
        self.append(task)

