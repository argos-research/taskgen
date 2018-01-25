#!/usr/local/bin/python3
"""This is the first attempt to measure the memory consumption in dependent on
number of variants.
"""


import sys
import time
import psutil
import subprocess
import time
import os
import sys

sys.path.append('../../')
from taskgen.tasksets.benchmark import BenchmarkTaskSet

def _call( task_count, variant_count):

    ts = BenchmarkTaskSet(variant_count, task_count)
    ts_iter = ts.variants()
    process = psutil.Process(os.getpid())

    max_rss = 0
    max_size = 0

    iter_time = 0
    description_time = 0
    try:
        while True:
            start_time = time.clock()
            ts_variant = ts_iter.__next__()
            iter_time += time.clock() - start_time

            start_time = time.clock()
            description = ts_variant.description()  # just hold it
            description_time += time.clock() - start_time

            size = len(description.encode("utf8"))
            if max_size < size:
                max_size = size
            
            mem = process.memory_info() # measure memory usage
            if max_rss < mem.rss:
                max_rss = mem.rss
    except StopIteration:
        pass
    return (max_rss, max_size, iter_time, description_time)

def _call_all(task_range, variant_range):
    print('{: <20} {: <20} {: <20} {: <20} {: <30} {: <30} {: <30}'.format(
         "Tasks", "Variants", "Memory (MB)", "XML (KB)",  "Total (sec)", "Generator (%)",
        "Description (%)"))
    for task in task_range:
        for variant in variant_range:
            start_time = time.clock()
            data = _call(task, variant)
            total = time.clock()-start_time
            print('{: <20} {: <20} {: <20} {: <20} {: <30} {: <30} {: <30}'.format(
                task, variant, data[0]/1024/1024, data[1]/1024,
                total,  data[2]/total, data[3]/total))
            sys.stdout.flush()


_call_all(range(10,10000, 1000), range(10,11))
#_call_all(range(1,2), range(1,5), range(1,5))
#_call_all(range(1,3), range(5,11), range(1,5))
#_call_all(range(1,40), range(10,100, 10), range(10,100, 10))
