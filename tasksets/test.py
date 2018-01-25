from taskgen.task import Task
from taskgen.taskset import TaskSet, BlockTaskSet
from taskgen.blocks import *

"""This module implements current problems

Settings
========
 
1. Current `argos-research/operating-system` 
2. Target: QEMU (PBXA9)
3. No other settings are changed. So DHCP is in use.


Listing all problems
====================

> ./taskgen-cli list -t | grep "test\|OPEN"

"""


class Problem0(TaskSet):
    """`numberofjobs` ignored by taskgen (CLOSED)
    
    COMMAND
    =======
    
    > ./taskgen-cli run -d -t test.Problem0 172.25.1.0/24


    LOG
    ===

    [init -> taskloader -> 00.hey] hey: Hello!
    [init -> taskloader] virtual void Task::Child_policy::exit(int): child 00.hey exited with exit value 0
    [init -> dom0-HW] Sending profile data of size 154
    [init -> taskloader] virtual void Task::Child_destructor_thread::entry(): Destroying task 00.hey
    [init -> dom0-HW] void Dom0_server::Dom0_server::Child_starter_thread::do_stop(int): Stopping tasks.
    [init -> taskloader] Stopping all tasks.
    [init -> taskloader] Stopping task 00.hey


    PROBLEM
    =======

    [Github Issue](https://github.com/pecheur/toolchain-host/issues/7)
    taskgen stops the task-set if all tasks run once. taskgen ignores the `numberofjobs`.
    
    SOLUTION
    ========

    `genode-Taskloader` does not support `numberofjobs` anymore. Due to that fact, this attribute
    will not be supported in future.


    """
    def __init__(self):
        super().__init__()

        self.append( Task( {
            # general
            "id" : 0, # ignored and set by TaskSet
            "criticaltime" : 0,
            "executiontime" : 99999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 0,
            "period" : 3,

            # scheduler
            "priority" : 10,
        }))



class Problem1(TaskSet):
    """`numberofjobs` ignored by genode-Taskloader (CLOSED)

    COMMAND
    =======

    > ./taskgen-cli run -d -t test.Problem1 172.25.1.0/24

    
    LOG
    ===

    [init -> taskloader -> 00.hey] Initializing LOG session
    [init -> taskloader -> 00.hey] Warning: no VFS configured
    [init -> taskloader -> 00.hey] hey: Hello!
    [init -> taskloader] virtual void Task::Child_policy::exit(int): child 00.hey exited with exit value 0
    [init -> dom0-HW] Sending profile data of size 156
    [init -> taskloader] virtual void Task::Child_destructor_thread::entry(): Destroying task 00.hey
    [init -> taskloader] Starting task 00.hey with quota 1048576 and priority 50 in iteration 2
    [init] Warning: priority band too small, losing least-significant priority bits
    [init -> taskloader -> 00.hey] Initializing LOG session
    [init -> taskloader -> 00.hey] Warning: no VFS configured
    [init -> taskloader -> 00.hey] hey: Hello!
    [init -> taskloader] virtual void Task::Child_policy::exit(int): child 00.hey exited with exit value 0
    [init -> dom0-HW] Sending profile data of size 156
    [init -> taskloader] virtual void Task::Child_destructor_thread::entry(): Destroying task 00.hey
    [init -> taskloader] Starting task 00.hey with quota 1048576 and priority 50 in iteration 3
    [init] Warning: priority band too small, losing least-significant priority bits
    [init -> taskloader -> 00.hey] Initializing LOG session
    [init -> taskloader -> 00.hey] Warning: no VFS configured
    [init -> taskloader -> 00.hey] hey: Hello!
    [init -> taskloader] virtual void Task::Child_policy::exit(int): child 00.hey exited with exit value 0
    [init -> dom0-HW] Sending profile data of size 156
    [init -> taskloader] virtual void Task::Child_destructor_thread::entry(): Destroying task 00.hey
    [init -> taskloader] Starting task 00.hey with quota 1048576 and priority 50 in iteration 4


    PROBLEM
    =======

    To prevent the short-term stop by taskgen (Task0), another task is
    added. This test shows, that genode-Taskloader ignores `numberofjobs`, too.
    `hey: Hello!` from task 0 occures 3 times!

    SOLUTION
    ========

    `genode-Taskloader` does not support `numberofjobs` anymore. The task runs endless.

    """
    def __init__(self):
        super().__init__()

        self.append( Task( {
            # general
            "id" : 0,
            "criticaltime" : 0,
            "executiontime" : 99999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 2, # <- tested attribute
            "period" : 3,

            # scheduler
            "priority" : 50,

        }))

        self.append( Task( {
            # general
            "id" : 1,
            "criticaltime" : 0,
            "executiontime" : 99999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 2,
            "period" : 3,

            # scheduler
            "priority" : 100,
        }))


class Problem2(TaskSet):
    """What means `Deadline hit for task 1` if there is no deadline? (OPEN)

    COMMAND
    =======

    > ./taskgen-cli run -d -t test.Problem2 172.25.1.0/24

    
    LOG
    ===

    [init -> taskloader] Task with id 0 was accepted by the controller
    [init -> taskloader] id: 1, name: 01.hey, prio: 100, deadline: 0, wcet: 99999999, period: 3
    [init -> sched_controller] Task with name 01.hey, is now enqueued to run queue 1
    [init -> sched_controller] R_ub: 99999999.2147483647 at new_task possition 0, deadline: 0 
    [init -> sched_controller] Deadline hit for task 1, Task set might be not schedulable! Maybe try an exact test.
    [init -> sched_controller] New task has higher or the same prio then lowest existing task, prio_new = 100, prio_last = 50
    [init -> sched_controller] response_time = 3333333366666666, response_time_old = 99999999, deadline = 0
    [init -> sched_controller] Task-Set is NOT schedulable!
    [init -> sched_controller] Task set is not schedulable!


    PROBLEM
    =======

    Why is task 1 not added to the run queue? What means `Deadline hit for task 1` if there is no deadline?
    Which values for `priority` will make both tasks runnable?


    
    """
    def __init__(self):
        super().__init__()

        self.append( Task( {
            # general
            "id" : 0,
            "criticaltime" : 0,
            "executiontime" : 99999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 2,
            "period" : 3,

            # scheduler
            "priority" : 50,

        }))

        self.append( Task( {
            # general
            "id" : 1,
            "criticaltime" : 0,
            "executiontime" : 99999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 2,
            "period" : 3,

            # scheduler
            "priority" : 100,     # <- tested attribute
        }))







class Problem3(TaskSet):
    """Genode freezes. (CLOSED)
    
    COMMAND
    =======

    > ./taskgen-cli run -d -t test.Problem3 172.25.1.0/24

    
    LOG
    ===
    
    [init -> taskloader] id: 0, name: 00.hey, prio: 4, deadline: 0, wcet: 2990538751, period: 0
    [init -> sched_controller] Task with name 00.hey, is now enqueued to run queue 1
    [init -> sched_controller] Rq is empty, Task set is schedulable!
    [init -> sched_controller] Sched_controller (enq): Task 00.hey was rta analyzed
    [init -> sched_controller] New element inserted to buffer at position 0 with pointer e010
    [init -> taskloader] Task with id 0 was accepted by the controller
    [init -> taskloader] id: 1, name: 01.cond_42, prio: 20, deadline: 0, wcet: 2701131775, period: 0
    [init -> sched_controller] Task with name 01.cond_42, is now enqueued to run queue 1
    [init -> sched_controller] R_ub: 2147483647.2147483647 at new_task possition 0, deadline: 0 
    [init -> sched_controller] Deadline hit for task 1, Task set might be not schedulable! Maybe try an exact test.
    [init -> sched_controller] New task has higher or the same prio then lowest existing task, prio_new = 20, prio_last = 4
    [init -> sched_controller] response_time = 18446744073709551615, response_time_old = 2990538751, deadline = 0
    [init -> sched_controller] Task-Set is NOT schedulable!
    [init -> sched_controller] Task set is not schedulable!
    [init -> taskloader] Task with id 1 was not accepted by the controller
    [init -> dom0-HW] void Dom0_server::Dom0_server::serve(): Done SEND_DESCS. Took: 429
    [init -> dom0-HW] void Dom0_server::Dom0_server::Child_starter_thread::do_send_binaries(int): Ready to receive binaries.
    [init -> dom0-HW] 2 binaries to be sent.
    [init -> taskloader] virtual Genode::Ram_dataspace_capability Taskloader_session_component::binary_ds(Genode::Ram_dataspace_capability, size_t): Reserving 233948 bytes for binary cond_42
    Hang up.
 

    PROBLEM
    =======

    This task-set forces genode to hang up.


    SOLUTION
    ========
    
    This might happen sometimes...

    """
    def __init__(self):
        super().__init__()

        self.append( Task( {
            # general
            "id" : 0,
            "criticaltime" : 0,
            "executiontime" : 9999999999999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 0,
            "period" : 0,

            # scheduler
            "priority" : 4,

        }))


        self.append( Task( {
            # general
            "id" : 1,
            "criticaltime" : 0,
            "executiontime" : 9999999999999999,

            # binary
            "quota" : "1M",
            "pkg" : "cond_42",
            "config" : {
                "arg1" : 30
            },

            # frequency
            "numberofjobs" : 0,
            "period" : 0,

            # scheduler
            "priority" : 20,

        }))





class Problem4(TaskSet):
    """EDF does not execute the task. (CLOSED)
    
    COMMAND
    =======

    > ./taskgen-cli run -d -t test.Problem4 172.25.1.0/24

    
    LOG
    ===
 
    [init -> taskloader] id: 0, name: 00.hey, prio: 0, deadline: 10000, wcet: 1874919423, period: 0
    [init -> sched_controller] Task with name 00.hey, is now enqueued to run queue 1
    [init -> sched_controller] New element inserted to buffer at position 0 with pointer e010
    [init -> taskloader] Task with id 0 was accepted by the controller
    [init -> dom0-HW] void Dom0_server::Dom0_server::serve(): Done SEND_DESCS. Took: 307
    [init -> dom0-HW] void Dom0_server::Dom0_server::Child_starter_thread::do_send_binaries(int): Ready to receive binaries.
    [init -> dom0-HW] 1 binary to be sent.
    [init -> taskloader] virtual Genode::Ram_dataspace_capability Taskloader_session_component::binary_ds(Genode::Ram_dataspace_capability, size_t): Reserving 44372 bytes for binary hey
    [init -> dom0-HW] Got binary 'hey' of size 44372.
    [init -> dom0-HW] void Dom0_server::Dom0_server::serve(): Done SEND_BINARIES. Took: 676
    [init -> dom0-HW] void Dom0_server::Dom0_server::Child_starter_thread::do_start(int): Starting tasks.
    [init -> taskloader] Starting 1 task.
    [init -> taskloader] 00.hey ALLOWED!
    [init -> taskloader] Starting task 00.hey with quota 1048576 and priority 0 in iteration 1
    [init -> dom0-HW] void Dom0_server::Dom0_server::serve(): Done START. Took: 403


    PROBLEM
    =======
 
    There is no `hey: Hello`. Why is the task not executed?
 

    SOLUTION
    ========

    Deadline parameter requires microseconds. This is fixed in neat future to milliseconds.

    """
    def __init__(self):
        super().__init__()

        self.append( Task( {
            # general
            "id" : 0,
            "criticaltime" : 0,
            "executiontime" : 9999999999999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 0,
            "period" : 0,

            # scheduler
            "deadline" : 10000, # 10 seconds.

        }))


class Problem5(TaskSet):
    """EDF does not execute a periodic task.
    
    COMMAND
    =======

    > ./taskgen-cli run -d -t test.Problem5 172.25.1.0/24

    
    LOG
    ===

    [init -> taskloader] Starting 1 task.
    [init -> dom0-HW] void Dom0_server::Dom0_server::serve(): Done START. Took: 5
    [init -> taskloader] 00.hey ALLOWED!
    [init -> taskloader] Starting task 00.hey with quota 1048576 and priority 0 in iteration 1
    [init -> taskloader] 00.hey ALLOWED!
    [init -> taskloader] Trying to start 00.hey but previous instance still running or undestroyed. Abort.
    [init -> taskloader] 00.hey ALLOWED!
    [init -> taskloader] Trying to start 00.hey but previous instance still running or undestroyed. Abort.
    ...

    PROBLEM
    =======
 
    There is no `hey: Hello`. Why are the jobs not executed? Due to this fact,
    taskgen does not know, when a task-set is done.


    SOLUTION
    ========

    unknown

    """
    def __init__(self):
        super().__init__()

        self.append( Task( {
            # general
            "id" : 0,
            "criticaltime" : 0,
            "executiontime" : 9999999999999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 0,
            "period" : 3, # 3 seconds & endless

            # scheduler
            "deadline" : 10000000, # 10 seconds.
        }))


class Problem6(TaskSet):
    """Multiple EDF tasks are not executed (OPEN)
    
    COMMAND
    =======

    > ./taskgen-cli run -d -t test.Problem6 172.25.1.0/24

    
    LOG
    ===
 
    [init -> taskloader] Starting 2 tasks.
    [init -> taskloader] 00.hey ALLOWED!
    [init -> taskloader] Starting task 00.hey with quota 1048576 and priority 0 in iteration 1
    [init -> taskloader] 01.hey ALLOWED!
    [init -> taskloader] Starting task 01.hey with quota 1048576 and priority 0 in iteration 1
    [init -> taskloader -> 00.hey] Initializing LOG session
    Warning: Quota exceeded! amount=65536, size=4096, consumed=65536
    [init -> taskloader -> 00.hey] Warning: no VFS configured
    [init -> dom0-HW] void Dom0_server::Dom0_server::serve(): Done START. Took: 962
    [init -> taskloader -> 00.hey] hey: Hello!
    [init -> taskloader] virtual void Task::Child_policy::exit(int): child 00.hey exited with exit value 0
    [init -> sched_controller] Optimizer (_query_monitor): Search in _threads for jobs of task 00.hey
    [init -> sched_controller] Optimizer (_query_monitor): thread 1239: task 00.hey, arrival 62101000 (curr: 64270000), start 63466000, c: 0
    [init -> sched_controller] Optimizer (_query_monitor): Task 00.hey has a new job: foc_id = 1239, arrival = 62101000 (current: 64270000).
    [init -> sched_controller] Optimizer: Task 01.hey has a new job with foc_id 1261, (arrival: 62340000, core: 0).
    [init -> sched_controller] Optimizer (_query_monitor): Task 00.hey - job 1239 has time left (2882231816).
    [init -> sched_controller] Optimizer: Task 00.hey has a new job with foc_id 1239, (arrival: 62101000, core: 0).
    [init -> dom0-HW] Sending profile data of size 153
    [init -> taskloader] virtual void Task::Child_destructor_thread::entry(): Destroying task 00.hey

    PROBLEM
    =======

    Only single `hey: Hello!` is printed. Task 2 is not executed.
  
    """
    def __init__(self):
        super().__init__()


        self.append( Task( {
            # general
            "id" : 0,
            "criticaltime" : 0,
            "executiontime" : 9999999999999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 0,
            "period" : 0, # 3 seconds & endless

            # scheduler
            "deadline" : 20000000, # 10 seconds.
        }))

        self.append( Task( {
            # general
            "id" : 1,
            "criticaltime" : 0,
            "executiontime" : 9999999999999999,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {},

            # frequency
            "numberofjobs" : 0,
            "period" : 0, # 3 seconds & endless

            # scheduler
            "deadline" : 10000000, # 10 seconds.
        }))
