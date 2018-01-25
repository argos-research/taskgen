"""This module implements the task"""



from collections.abc import Mapping
from abc import ABCMeta, abstractmethod
import flatdict
import itertools
from collections import Iterable
import flatdict


class Job:
    
    def __init__(self):
        self.start_date = None
        self.end_date = None

    def is_running(self):
        return self.end_date is None


class Task(dict):
    """A Task

    A task is defined by attributes like priority, period, usw. These attributes
    are represented by key-value pairs and stored in a dict.
    
    :param *blocks dict: A number of dicts as parameters, which are merged to
    this task. This concept is called Task-Blocks. Task-Blocks are located in
    the directory `taskgen.blocks`.

    """
    def __init__(self, *blocks):
        super().__init__({
            # default values
            "id" : None,
            "priority" : None,

            # blob values
            "quota" : None,
            "pkg" : None,
            "config" : None,

            # periodic task
            "period" : None,
            
            "numberofjobs" : 1
            # "offset" : None, unused at genode side.
        })

        # stores all job data (added during runtime of this task)
        self.jobs = []
        
        # add inital blocks
        for block in blocks:
            if callable(block):
                block = block()
#            if not isinstance(attr, dict):
#                raise ValueError("An attribute for a task must be dict.")
            super().update(block)

    @property
    def id(self):
        """Getter of the task id attribute
        
        This method is used by monitor implementations for finding the related
        task for an event.

        """
        
        return self['id']
            
    @id.setter
    def id(self, _id):
        """Setter for the task id

        This method is used by `taskgen.taskset.TaskSet`. If a task is added to a
        task-set, an unique id is assigned to the task.

        """
        
        self['id'] = _id

    def variants(self):
        """Generator for task variants
        
        This method generates all variants of a task and is used by
        `taskgen.taskset.TaskSet`.

        """
        
        flat = flatdict.FlatDict(self)

        # make everything to an iterator, except iterators. Pay attention:
        # strings are wrapped with an iterator again.
        iters = map(lambda x: [x] if not isinstance(x, Iterable) or
                    isinstance(x, str) else x, flat.itervalues())
        keys = flat.keys()
        
        for values in itertools.product(*iters):
            # update dictionary with the new combined values. This is done by
            # mapping all keys to their values.
            flat.update(dict(zip(keys, values)))
            
            # create new task
            yield Task(flat.as_dict())

    def binary(self):
        """Binary of the task
        
        Every task has a binary. This method returns it.

        :return: binary of the task
        :rtype: str

        """
        return self['pkg']
