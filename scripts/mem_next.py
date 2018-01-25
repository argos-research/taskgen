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

HEADER = ['tasks', 'variants', 'memory','xml', 'generator', 'description']
FORMAT = '{: <20} {: <20} {: <20} {: <20} {: <30} {: <30}'
CSV_FORMAT = '{},{},{},{},{},{}'


def _output(line, path):
    with open(path,'a') as f:
        f.write(line + '\n')
    


def _variants_call(task_range, variant_range, path):
    """

    """
    print(FORMAT.format(*HEADER))
    _output(CSV_FORMAT.format(*HEADER), path)
    
    process = psutil.Process(os.getpid())
    for task_count in task_range:
        start_time = time.clock()

        ts = BenchmarkTaskSet(max(variant_range), task_count)
        ts_iter = ts.variants()
        
        variant_iter = variant_range.__iter__()
        variant_pos = variant_iter.__next__()

        try:
            variant_counter = 0
            while True:
                # iter
                start_time = time.clock()
                ts_variant = ts_iter.__next__()
                iter_time = int((time.clock() - start_time)*1000*1000)
                variant_counter += 1

                if variant_counter == variant_pos:                   
                    # description
                    start_time = time.clock()
                    description = ts_variant.description()
                    description_time = int((time.clock() - start_time)*1000*1000)

                    xml = len(description.encode("utf8"))
                    mem = process.memory_info() # measure memory usage
                    rss = mem.rss

                    # print
                    _output(CSV_FORMAT.format(
                        task_count,
                        variant_counter,
                        rss,
                        xml,
                        iter_time,
                        description_time), path)

                    print(FORMAT.format(
                        task_count,
                        variant_counter,
                        rss,
                        xml,
                        iter_time,
                        description_time))
                    sys.stdout.flush()
                    variant_pos = variant_iter.__next__()
        except StopIteration:
            pass



_call_all(range(1,2), range(1,1000000,1000), "variants_1m.csv")

#_call_all(range(0,1000000, 1000), range(1,2), "tasks_1m.csv")

#_call_all(range(999,1000), range(1,1000), "variants_1000.csv")
