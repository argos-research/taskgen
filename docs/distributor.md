Distributor
===========

The `Distributor` class glues everything together in place. It scans IP ranges
for available sessions, automatically manages open connections to sessions,
distributes task-sets and task-set variants to connected target systems and pass
on incoming events to event handlers.  

Is is possible to hand over a list of IP ranges. Each IP range is described with
the [CIDR](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing) format.  


Small Example
-------------

```Python
from taskgen.tasksets.hey import Hey1TaskSet
from taskgen.distributor import Distributor


taskset = Hey1TaskSet()

distributor = Distributor('172.25.1.2')
distributor.start(taskset)
```


Extended Example
--------------

```Python
from taskgen.tasksets.hey import Hey1TaskSet
from taskgen.distributor import Distributor
from taskgen.events.csv import CsvHandler


# define admission control data
ADMISSION_CTRL_DATA = {
    "optimize" : {
        "goal" : {
            "fairness" : {
                "apply" : 1
            },
            "utilization" : {
                "apply" : 0
            }
        },
        "query_interval" : 1000
    }
}

# attempt connecting to hosts of two ip ranges.
distributor = Distributor(["172.25.1.0/24", 172.49.1.0/24])

# save all events to `events.csv`
event_handler = CsvHandler("events.csv")
distributor.event_handler = event_handler

# create taskset
taskset = Hey1TaskSet()

# start distributing taskset and do not block until finished.
distributor.start(taskset, wait=False)
print("taskset processing started")

# start stopping all target systems.
distributor.stop(wait=True)
print("taskset processing stopped.")


# start processing tasksets with optimization again.
distributor.start(taskset, ADMISSION_CTRL_DATA, wait=True)

# closing all connections after taskset is finished.
distributor.close(wait=False)
print("closing all connections")
distributor.wait_closed()
```




Behavior
--------

* **IP ranges:** When IP ranges are handed over to the distributor, they are
  placed in a pool of hosts. If the availability check for a host, for example:
  ping, is successful, a connection to the host will be established.

* **No available connection:** The Distributor waits until a connected becomes
  available, connects and starts sending task-sets.
  
* **A connection timed out** The current processed task-set is pushed back to a
  processing queue. The host is placed in the host pool again and an
  availability check is repeated later.
  
* **Distributor is closed by user** The event handler is informed about then
  task-set cancel, all task-sets of the target plattforms are stopped,
  connections are closed and threads are stopped.
  

