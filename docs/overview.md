Goals
=====

- **Easy extensibility** New modules are simple to add as new classes. The
  primary classes `TaskSet` and `Task` are represented as dictionaries, which
  allows a direct mapping from `Task` attributes to the final xml
  representation.
  
- **Work with Python** No separate models configuration files in a declarative
  format. Models are described in Python code, which is compact, easier to
  debug, and allows for ease of extensibility
  
- **Large-Scale** TaskSet variants up to 1 billion or even infinite taskset
  generators are no problems. Lazy evaluation only generate as much tasksets as
  needed at runtime.
  
- **User friendly** Threading keeps waiting time low and work, like ping,
  connect, processing tasksets, is done in background. A fast-responsive
  framework is the result.


Components of taskgen
=====================
  
* [**Task**](tasks.md) A Task consists of key-value pairs, which describes
  the behavior of a real-time capable process. One key could be `priority` and
  its associated value might be `25`. Tasks are implemented as python
  dictionaries.  
  
* [**Task Blocks**](blocks.md) are building blocks for a task and are
  represented with key-value pairs, too.  A (task) block is a dictionary object or
  a function which returns a dictionary object.  
  
* [**Task-Sets**](taskset.md) are containers for tasks.  

* [**Admission Control**](admctrl.md) objects contains optimization goals
  for a task-set. Optimizations are represented by python dictionaries.  
  
* [**Monitors**](monitor.md) handle occuring events. An event is fired,
  whenever a task processing starts or ends.  
  
* [**Distributor**](distributor.md) sends a task-set and its optimization
  goal to a platform, which is able to execute task-sets. The low level
  connection to such a platform is realized with a **Session**.  
  
* [**Sessions**](session.md) contain the low level implementations for
  sending task-sets, optimization classes and for receiving events.  
  

General Workflow
================

1. Choose a task-set class
3. Optionally choose an event handler
4. Optionally choose a session for a target platform.
5. Start sending and processing task-set.

These steps can be done by using the [command line tool](commandline.md) or
by writing a python script and using the module's classes:

```Python
from taskgen.tasksets.hey import Hey1TaskSet
from taskgen.distributor import Distributor
from taskgen.optimizations.fairness import Fairness

taskset = Hey1TaskSet()

distributor = Distributor("172.25.1.2")
distributor.start(taskset)
```

For more comprehensive examples read the [documentation](.) and look at the
[scripts](../scripts/) folder, please.

