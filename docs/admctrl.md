# Admission Control

When a task-set processing starts, you are able to handle over data for the
admission control component. Due to the fact, that this data is represented as
xml during sending, the data are represented as python dict. The translation
from dict to xml is done by the actual session.

```Python

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

distributor.send(taskset, ADMISSION_CTRL_DATA)
        
```

Keep in mind, that the support for the admission control is optional for
the session. Not every session implements this parameter.

## Example 1

`genode.GenodeSession` supports it.

```Python
class GenodeSession(AbstractSession):
    
    def start(self, taskset, admctrl=None):
        self._optimize(admctrl)
        # ...
```

## Example 2

`stdio.StdIOSession` does not support it.

```Python
class StdIOSession(AbstractSession):
    
    def start(self, taskset):
        # ...
```
