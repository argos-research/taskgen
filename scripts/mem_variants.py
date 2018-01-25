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

sys.path.append('../../')

def _call(session_count, task_count, variant_count):
    cmd = 'python3 -m taskgen run'.split(' ')
    ts = '-t benchmark.BenchmarkTaskSet {} {}'.format(
        variant_count,task_count).split(' ')
    s = '-s benchmark.Session'.split(' ')
    ip = ['172.25.1.2' for x in range(session_count)]
    
    taskgen = subprocess.Popen(cmd + ts + s+ ip, cwd='../../',
                               stdout = subprocess.DEVNULL,
                               stderr = subprocess.DEVNULL)
        
    process = psutil.Process(taskgen.pid)
    max_mem = None
    max_rss = 0
    while taskgen.poll() == None:
        mem = process.memory_info()
        if max_rss < mem.rss:
            max_rss = mem.rss
            max_mem = mem
        time.sleep(0.1)
    return max_rss

def _call_all(session_range, task_range, variant_range):
    print('{: <20} {: <20} {: <20} {: <20} {: <20}'.format(
        "Sessions", "Tasks", "Variants", "Memory(MB)", "Time(sec))"))
    for session in session_range:
        for task in task_range:
            for variant in variant_range:
                start_time = time.clock()
                rss = _call(session, task, variant)

                print('{: <20} {: <20} {: <20} {: <20} {: <20}'.format(session,
                        task, variant, rss/1024/1024, time.clock()-start_time))
                sys.stdout.flush()


_call_all(range(1,2), range(1,2), range(1,2))
#_call_all(range(1,2), range(1,5), range(1,5))
_call_all(range(1,3), range(5,11), range(1,5))
#_call_all(range(1,40), range(10,100, 10), range(10,100, 10))
