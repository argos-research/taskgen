# Basics

Task-sets are located in the [tasksets](../tasksets/) directory. Each task-set
is a subclass of `taskset.TaskSet` and a container for `tasks.Task` classes.
Task-sets do not behave like a list or dictionary. Only an append method and
the concatenation operator are supported. This has some performance reasons.

```python3
from taskgen.tasksets.example import Hey0TaskSet
from taskgen.distributors.multi_distributor import MultiDistributor

ts = Hey0TaskSet()

md = MultiDistributor("172.25.0.1", 1234)
md.start(ts)
```

# Customization

The usage of task-sets is not limited to predefined implementations. It is
possible to build custom task-set with the base class `taskset.TaskSet` and
`Task` classes.

```python3
from taskgen.taskset import TaskSet

task = Task({
    ...
})

taskset = TaskSet()
taskset.append(task)

```

# Variants

Tasks can store multiple values for one attribute. These leads to multiple
variants of a Task and finally multiple variants of a TaskSet. There is no way
to determine the actual number of variants. It also can have infinite variants,
which will keep the distributor running.

# Examples

[`tasksets/example.py`](../tasksets/example.py) contains many simple implementations for task-sets. 
