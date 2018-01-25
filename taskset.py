"""Module for task-set implementation

"""

import xmltodict
from collections.abc import Iterable
from abc import ABCMeta, abstractmethod
import itertools
import random

from taskgen.task import Task



class TaskSet(Iterable):
    """Container for tasks"""
    
    def __init__(self, tasks=[]):
        """Initialize a task-set

        :param tasks [Task]: Initialize a task-set from a list of tasks.
        """
        self._tasks = tasks
        self._task_counter = 0

    def __iter__(self):
        """Iterator for iterating over all tasks"""
        return self._tasks.__iter__()
    
    def __str__(self):
        return self._tasks.__str__()
        
    def append(self, task):
        """Append task to this task-sets

        :param task taskgen.task.Task: Append task to this task-set
        
        """
        task.id = self._task_counter
        self._task_counter += 1
        self._tasks.append(task)

    def variants(self):
        """Generator for generating all variants of this task-set.

        The Generator returns new TaskSet objects. Each TaskSet is a unique
        variant.

        """
        tasks_iters = map(lambda x: x.variants(), self._tasks)
        for tasks_variant in itertools.product(*tasks_iters):
            yield TaskSet(list(tasks_variant))

    def description(self):
        """Description of the task-set

        :return: Description of the task-set
        :rtype: dict
        """
        return {
            "taskset" : {
                "periodictask" : self._tasks
            }
        }

    def binaries(self):
        """List of used binaries
        
        :return: List of used binaries
        :rtype: (str, str,...)
        """
        return set(map(lambda x: x.binary(), self._tasks))

    

class BlockTaskSet(TaskSet):
    """Generates a TaskSet from Task-Blocks. 

    A Task-Block is a python dict and describes a part of a task. Passing a list
    of Task-Blocks results in task-set with variants.  Each Task-Block of the
    list is one variant.

    Example
    =======
    A1 = period.Custom(1)
    A2 = period.Custom(2)
    B1 = priority.Custom(10)

    # TaskSets with one Variant
    BlockTaskSet(A1, B1)
    BlockTaskSet(A1)

    # TaskSet with 2 variants
    BlockTaskSet([A1, A2], B1)

    # TaskSet with 4 variants
    BlockTaskSet([A1, A2], [B1, B1])

    :param *block_combinations: number of Task-Blocks as parameters
    :param task_class: Class of task for generation.
    :param seed int: Seed for the randomness generator.

    """
    def __init__(self, *block_combinations, task_class=Task, seed=None):
        super().__init__()
        random.seed(seed)
        
        # wrap every argument, which is not of type list, with a list-object:
        # example: x->[x]
        block_combinations = map(lambda x: [x] if not isinstance(x, list) else x,
                                 list(block_combinations))
        
        for blocks in itertools.product(*block_combinations):
            # create a task from the block combinations and append it to the
            # taskset
            task = task_class(*blocks)
            self.append(task)


