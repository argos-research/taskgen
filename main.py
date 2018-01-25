#!/usr/bin/env python3
import argparse
import logging, coloredlogs

# inspect
import inspect
import pkgutil
import importlib


from taskgen.distributor import Distributor, AbstractSession
from taskgen.sessions.genode import PingSession
from taskgen.taskset import TaskSet
from taskgen.monitor import AbstractMonitor

if __name__ == '__main__':
    main()


def handle_logging(args):
    _level = 'DEBUG' if args.debug else 'INFO'
    _fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    coloredlogs.install(level=_level, fmt=_fmt)
    
    
def print_classes(class_type, submodule):
    is_class_type = lambda x: inspect.isclass(x) and issubclass(x, class_type)
    # submodules might be: tasksets, optimizations, lives
    submodules = pkgutil.iter_modules(["taskgen/{}".format(submodule)])
    for (module_loader, module_name, ispkg) in submodules:
        if not ispkg:
            module_path = 'taskgen.{}.{}'.format(submodule, module_name)
            module = importlib.import_module(module_path)
            # find all classes with subclass Taskset
            for class_name, obj in inspect.getmembers(module, is_class_type):
                if obj.__module__ == module_path:
                    #class_path = module_path + "." + class_name
                    class_path = module_name + "." + class_name
                    class_doc = "\n" if obj.__doc__ is None else obj.__doc__
                    class_doc = class_doc.splitlines()
                    print('{}{: <30}{} {}'.format('\033[1m', class_path, '\033[0m', class_doc[0]))


def command_list(args):
    if args.taskset:
        print_classes(TaskSet, "tasksets")
    if args.monitor:
        print_classes(AbstractMonitor, "monitors")
    if args.session:
        print_classes(AbstractSession, "sessions")


def load_class(path, submodule):
    # TODO handle constructor parameters
    # TODO handle not found

    if path is None:
        return None
    
    # submodules might be tasksets, optimization, lives
    module_name, class_name = "taskgen.{}.{}".format(submodule, path).rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)

def initialize_class(path, submodule, params=()):
    _class =load_class(path, submodule)
    if _class is not None:
        return _class(*params)
    
def command_run(args):    
    handle_logging(args)
    
    # load tasksets  (right now, no parameters can be passed.)
    tasksets = initialize_class(args.taskset, "tasksets")

    # load monitor
    if args.monitor:
        monitor = initialize_class(args.monitor, "monitors")
    else:
        monitor = None

    # session class
    if args.session:
        session_class = load_class(args.session, "sessions")
    else:
        session_class = PingSession

    try:
        # initialize distributor
        distributor = Distributor(args.IP,
                                  args.port,
                                  session_class)
        distributor.monitor = monitor
        
        # start (and wait until finished)
        distributor.start(tasksets,  wait=True)

        # TODO print current state
    except KeyboardInterrupt:
        # CTRL-C
        pass
    finally:
        distributor.close()
    
    
def main():
    parser = argparse.ArgumentParser(prog="taskgen")
    subparsers = parser.add_subparsers(dest='command')

    # run
    parser_run = subparsers.add_parser('run', help='runs a list of tasksets')
    # run -d
    parser_run.add_argument("-d", "--debug", action='store_true',
                            help="Print debugging information.")
    # run -p
    parser_run.add_argument('-p', '--port', default=3001, type=int,
                            help='Port, default is port number 3001.')
    # run -t
    parser_run.add_argument('-t', '--taskset', required=True, metavar="CLASS",
                            help='Select a taskset class.')
    # run -m
    parser_run.add_argument('-m', '--monitor', metavar="CLASS",
                            help='Select a monitor for incoming events of processed tasksets.')
    # run -s
    parser_run.add_argument('-s', '--session', metavar="CLASS",
                            help='Select a session class. Default: GenodeSession')
    # run [IP]
    parser_run.add_argument('IP', nargs='+',
                            help='IP address or a range of IP addresses (CIDR format)')

    # list
    parser_list = subparsers.add_parser('list', help='lists available tasksets')
    group_list = parser_list.add_mutually_exclusive_group(required=True)

    # list -t
    group_list.add_argument('-t', '--taskset', action='store_true',
                            help="print all available taskset classes.")
    # list -m
    group_list.add_argument('-m', '--monitor', action='store_true',
                            help="print all available monitors.")
    # list -s
    group_list.add_argument('-s', '--session', action='store_true',
                            help="print all available session classes.")

    # parse
    args = parser.parse_args()
    if args.command == 'run':
        command_run(args)
    elif args.command == 'list':
        command_list(args)
        
    
