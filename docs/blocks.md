# Task Blocks

Task blocks are building blocks for a task and located in [blocks](../blocks). An
block is a dictionary object or a function which dynamically returns a
dictionary object. 

```Python
HelloWorld = {
    "criticaltime" : 1000,
    "executiontime" : 1000,
    "pkg" : "hey",
    "quota" : "1M",
}
```

Randomly chosen values are implemented with a function:

```Python
def HelloWorld():
    return {
        "criticaltime" : 1000,
        "executiontime" : random.randint(10, 100),
        "pkg" : "hey",
        "quota" : "1M",
    }
```

Furthermore, it is possible to provide multiple variants of a value:

```Python
def HelloWorld():
    return {
        "criticaltime" : 1000,
        "executiontime" : [400, 800, 1000],
        "pkg" : "hey",
        "quota" : "1M",
    }
```

Variants are constructed from `Iterable` objects. Beside `list`, `range(min,
max)`, custom `Iterable` objects or Generator functions are possible, too. Only
`str`, which is also an `Iterable`, is not handled as `Iterable`. For more
information about variants, read [task documentation](tasks.md).

## Import Blocks

Importing all blocks at once is suggested:

```Python
from taskgen.blocks import *
```

## Task Creation with Blocks

You can pass all blocks as parameters to a `Task` constructor or update a
`Task` object with a block.

```Python
from taskgen.blocks import *

task = Task (
    hey.HelloWorld,
    period.Random,
    priority.High,
)
```

or


```Python
from taskgen.blocks import *

task = Task()
task.update( hey.HelloWorld)
task.update( period.Random)
task.update( priority.High)
```

## TaskSet Creation with Blocks

Instead of creating all tasks manually and appending them to a task-set, it is
possible to create a task-set from multiple blocks.

The next example shows the previous task with such a task-set:
```Python
from taskset import BlockTaskSet

taskset = BlockTaskSet(
    hey.HelloWorld,
    period.Random,
    priority.High
)
```

Creating a task-set with two `hey.HelloWorld` tasks is just as easy:

```Python
from taskset import BlockTaskSet

taskset = BlockTaskSet(
    [hey.HelloWorld, hey.HelloWorld],
    period.Random,
    priority.High
)
```

The next example creates a task-set with four tasks with `hey.HellowWOrld`
binaries and specific priorities:

```Python
from taskset import BlockTaskSet

taskset = BlockTaskSet(
    hey.HelloWorld,
    period.Random,
    [priority.Custom(10), priority.Custom(24), priority.Custom(44), priority.Custom(100)]
)
```





