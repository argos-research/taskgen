from taskgen.task import Task
from taskgen.taskset import TaskSet

class BenchmarkTask(Task):
    def __init__(self, variants):
        super().__init__()
        self.update({
            "id" : range(0, variants),
            "executiontime" : 99999999,
            "criticaltime" : 0,
            "deadline" : 0,
            "priority" : 128,
            "period" : 0,
            "offset" : 0,
            "numberofjobs" : 0,
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {
                "arg1" : 1
            }
        })

class BenchmarkTaskSet(TaskSet):
    def __init__(self, variants, tasks):
        super().__init__()

        self.append(BenchmarkTask(int(variants)))
        for v in range(int(tasks-1)):
            self.append(BenchmarkTask(1))
        
