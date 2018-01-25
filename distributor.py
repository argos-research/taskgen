"""Module for asyncron distribution of task-sets

This modules provides a class for the distribution of task-sets to one or
multiple target plattforms. The connection to a target plattform is handled by a
session.

"""


from abc import ABCMeta, abstractmethod
import threading
import time
import logging
import subprocess
import copy
import socket
from queue import Empty, Queue, Full
from collections.abc import Mapping
from ipaddress import ip_network, ip_address
from itertools import chain
from math import ceil

from taskgen.taskset import TaskSet
from taskgen.monitor import AbstractMonitor
from taskgen.session import AbstractSession
from taskgen.sessions.genode import PingSession



class Distributor:
    """Class for asycron distribution of task-sets"""
    
    def __init__(self,
                 destinations,
                 port=3001,
                 session_class=PingSession,
                 starter_threads = 20):
        """Start connecting to target plattforms.

        :param destination str, [str]: IP addresses or ranges of destination/target
        system(s). format: CIDR.  

        :param port int: Port of destination

        :param session_class taskgen.session.AbstractSession: Session class,
        which establishs the connection to the target plattform.

        :param starter_threads int: Number of threads for doing the availablity
        check of a target plattform.
        
        :raises TypeError: wrong parameters types
        :raises ValueError: destination does not appear to be an IPv4 or IPv6 address

        """

        if not isinstance(port, int):
            raise TypeError("port must be int")

        if not issubclass(session_class, AbstractSession):
            raise TypeError("session_class must be a class with subtype AbstractSession")

        self._sessions = []
        self._starter = []
        self._port = port
        self._session_class = session_class
        self.logger = logging.getLogger('Distributor')
        self._close_event = threading.Event()
        self._pool = Queue()
        self._monitor = None
        self._run = False
        self._tasksets = []
        self._session_params = None
        
        # build pool of IP destination addresses
        if isinstance(destinations, str):
            self._append_pool(destinations)
        elif isinstance(destinations, list):
            for destination in destinations:
                self._append_pool(destination)
        else:
            raise TypeError("destinations must be [str] or str.")

        # initialize pinging and connecting of destinations
        for c in range(0, starter_threads):
            starter = threading.Thread(target=Distributor._starter, args=(self,))
            starter.start()
            self._starter.append(starter)

            
    def _append_pool(self, destination):
        """Adds a range of ip addresses to the pool"""
        # try to parse as single ip address
        try:
            ip = ip_address(destination)
            self._pool.put(str(ip))
            return
        except ValueError:
            pass
        # parse as ip range or raise error
        for ip in ip_network(destination).hosts():
            self._pool.put(str(ip))

            
    @staticmethod
    def _starter(self):
        """Checks the availablity of a destination
        
        This method checks the availablity of all destination in the pool. For
        each available destination, a thread _`WrapperSession` is started for
        establishing a connection. The actual connection is handled by a
        session.
        
        This method is only called by a seperated thread. These are started in
        `__init__`.

        """

        # continue checking destination in the pool until distributor is closed.
        while not self._close_event.is_set():
            try:
                host = self._pool.get(True, 2)
                if self._session_class.is_available(host):
                    self.logger.info("Found {}".format(host))
                    # initalize session
                    session = _WrapperSession(host,
                                              self._port,
                                              self._close_event,
                                              self._session_class,
                                              self._pool,
                                              self._sessions)
                    session.monitor = self.monitor
                    # start session
                    if self._run:
                        session.start(self._tasksets, *self._session_params)
                    session.thread_start()
                    self._sessions.append(session)
                else:
                    self._pool.put(host)
            except Empty:
                pass

            
    @property
    def monitor(self):
        """Getter method for the currently used monitor.
        
        :return: returns the currenctly monitor. If no monitor is set, `None` is
        the return value.

        :rtype: taskgen.monitor.AbstractMonitor or None

        """
        return self._monitor

    
    @monitor.setter
    def monitor(self, monitor):
        """Setter method for a monitor.
        
        :param monitor taskgen.monitor.AbstractMethod: Set `monitor` as handler
        for incoming events.

        """
        if monitor is not None:
            if not isinstance(monitor, AbstractMonitor):
                raise TypeError("monitor must be of type AbstractMonitor")
        self._monitor = monitor
        for session in self._sessions:
            session.monitor = monitor

            
    def start(self, taskset, *session_params, wait=True):
        """Starts the distribution of task-sets

        :param taskset taskgen.taskset.TaskSet: a taskset for the distribution

        :param session_params: optional parameters which are passed to the
        `start` method of the actual session. Pay attention: Theses parameters
        must be implemented by the session class. A good example is the
        `taskgen.sessions.genode.GenodeSession`, which implements a parameter
        for optional admission control configuration.  

        :param wait bool: `False` if the method should not wait until all
        sessions started and the method returns immediately. 

        """
        if taskset is None or not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be TaskSet.")

        # wrap tasksets into an threadsafe iterator
        self._tasksets = _TaskSetQueue(taskset.variants())
        self._session_params = session_params
        self._run = True
        for session in self._sessions:
            session.start(self._tasksets, *session_params)
        if wait: self.wait_finished()

        
    def stop(self, wait=True):
        """Stops the distribution of task-sets

        :param wait bool: `False` if the method should not wait until all
        sessions stopped and the method returns immediately.

        """
        self.logger.info("Stop processing taskset")
        self._run = False
        for session in self._sessions:
            session.stop()
        if wait: self.wait_stopped()

        
    def close(self, wait=True):
        """Closes all connections to distributors.

        After closing this distributor the usage is exhausted. Do not call any
        methods after.  

        :param wait bool: `False` if the method should not wait until all
        sessions are closed and the method returns immediately.

        """
        self._close_event.set()
        self.logger.info("Closing connections...")
        if wait: self.wait_closed()

        
    def wait_closed(self):
        """Waits until all connections to target plattforms are closed."""        
        self.logger.info("Waiting until ping threads are stopped")
        for starter in self._starter:
            starter.join()

        # TODO: when closing, it might happen that a starter thread still opens a connection.
        # the log message then might be disturbing.
        self.logger.info("Waiting until sessions are closed")
        for session in self._sessions:
            session.join()
        
    def wait_stopped(self):
        """Waits until all sessions stopped processing task-sets."""        
        self.logger.info("Waiting until session processings are stopped")
        for session in self._sessions:
            session.wait_stopped()

    def wait_finished(self):
        """Waits until all sessions finished processing task-sets."""
        while not self._close_event.is_set():
            if self._tasksets.empty():
                break
            time.sleep(1)

            
class _TaskSetQueue():
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, iterator):
        self.it = iterator
        self.lock = threading.Lock()
        self.queue = Queue(maxsize=1000)
        self.in_progress = []
        self.processed = 0
        self.logger = logging.getLogger("Distributor")
        
    def get(self):
        # return a regular taskset
        with self.lock:
            taskset = None
            if not self.queue.empty():
                try:
                    taskset = self.queue.get_nowait()
                except Queue.Empty:
                    # ups, another distributor just stole our taskset
                    pass

            # take a new one from the iterator
            if taskset is None:
                taskset = self.it.__next__()

            # keep track of current processed tasksets
            self.in_progress.append(taskset)
            return taskset
            
    def empty(self):
        with self.lock:
            # in progress?
            if len(self.in_progress) > 0:
                return False
            # in queue?
            if not self.queue.empty():
                return False
            # in iterator?
            try:
                self.queue.put(self.it.__next__())
                return False
            except StopIteration:
                return True

    def done(self, taskset):
        """Call this method, if a task-set is finally processed.

        This mechanism keeps references of currenctly processed task-sets.

        """
        with self.lock:
            self.in_progress.remove(taskset)
            self.processed += 1
            self.logger.info("{} taskset variant(s) processed".format(self.processed))
        
    def put(self, taskset):
        """Call this method, if a task-set processing is canceled.

        This mechanism keeps references of currenctly processed task-sets.

        """
        with self.lock:
            try:
                self.in_progress.remove(taskset)
                self.queue.put_nowait(taskset)
            except Full:
                # We don't care about the missed taskset. Actually, there is a bigger
                # problem:
                self.logger.critical("The Push-Back Queue of tasksets is full. This is a"
                    + "indicator, that the underlying session is buggy"
                    + " and is always canceling currently processed tasksets.")

            

class _WrapperSession(threading.Thread):
    """This class handles every connection to a target plattform asynchronously.

    For each destination, which passes the availablity, a session is created and
    maintained with help of this class. Due to the fact that multiple session
    might exist and the main program should not be blocked, every new session is
    initalized in its own thread.

    To keep all session states independent from each other, a state machine is
    implemented in the `run` method.

    Keep in mind, the usage of this class is not intended outside of this
    module.

    Due to the internal character of this class, methods and parameters are not
    described in more detail. 

    Tasks of thes calls: 
    * Keep each session asyncron 
    * Handle raising errors. The whole processing of variants should not stop
      due to a single error of a session.

    """
    def __init__ (self, host, port, close, session_class, pool, sessions):
        
        super().__init__()
        self._host = host
        self._port = port
        self._pool = pool
        self._sessions = sessions
        self._tasksets = None
        self.monitor = None
        self._close = close
        self._session_class = session_class
        self._logger = logging.getLogger("Distributor({})".format(host))
        self._session_params = ()
        self._taskset = None
        self._running = False
        self._restart_lock = threading.Lock()
        self._run = False
        self._restart = False

    def thread_start(self):
        """due to an otherwise usage of the `start` method, the method of the
        underlying `Thread` class needs to be renamed.
        """
        threading.Thread.start(self)

    def wait_stopped(self):
        while self._running and self._run and not self._close.is_set():
            time.sleep(0.5)

    def start(self, tasksets, *session_params):
        with self._restart_lock:
            self._tasksets = tasksets
            self._session_params = session_params
            self._restart = True
            self._run = True

    def stop(self):
        self._run = False

            
    def _internal_start(self, session):
        """Called, whenever a new task-set should be processed.
        
        Workflow:
        1. try to get a new task-set.
        2. Task-set is handled over to Session
        3. Inform monitor about the next task-set
        4. Set state to `running`.

        """
        try:
            with self._restart_lock:
                tasksets = self._tasksets
                params = self._session_params
                
            self._taskset = tasksets.get()
            session.start(self._taskset, *params)
            if self.monitor is not None:
                self.monitor.__taskset_start__(self._taskset)
                
            self._logger.debug("Taskset variant processing started.")
            self._restart = False
            self._running = True
        except StopIteration:
            # all tasksets are processed
            self._logger.debug("All taskset variants are processed")
            self._running = False
            self._restart = False
            self._taskset = None


    def _internal_stop(self, session):
        """Called, whenever the distributor is stopping.

        Workflow:
        1. Session is stopped.
        2. Inform monitor about the stop.
        3. Set state to stopped`.

        """
        session.stop()
        if self._taskset is not None :
            if self.monitor is not None:
                self.monitor.__taskset_stop__(self._taskset)
            self._tasksets.put(self._taskset)
            self._taskset = None
        self._running = False

        
    def _internal_update_handling(self, session):
        
        # let session update the task-set
        taskset_changed = session.run(self._taskset)
        if taskset_changed:
            if self.monitor is not None:
                self.monitor.__taskset_event__(self._taskset)

        # is taskset still running
        target_running = session.is_running(self._taskset)
        if not target_running:
            if self.monitor is not None:
                self.monitor.__taskset_finish__(self._taskset)
            self._tasksets.done(self._taskset)  # notify about the finished taskset
            self._logger.debug("Taskset variant is successfully processed")
            
        return target_running

    
    def run(self):
        # try to connect
        try:
            session = self._session_class(self._host, self._port)
            self._logger.info("Connection established.")
        except socket.error as e:
            self._logger.critical(e)
            self._pool.put(self._host)
            return 

        try:
            while not self._close.is_set():
                # stopping
                if not self._run and self._running:
                    self._internal_stop(session, taskset)
                # restart or still running
                if self._restart or self._running:
                    # try to start next taskset
                    self._internal_start(session)

                    # live requests
                    while (not self._close.is_set() and not self._restart and
                           self._run and self._running):
                        if not self._internal_update_handling(session):
                            break
                # idle
                elif not self._running:
                    time.sleep(0.1)
                else:
                    self._logger.critical("Reached some unknown state")
                    time.sleep(0.1)

            self._internal_stop(session)
        except socket.error as e:
            self._logger.critical(e)
            
            if self._taskset is not None:
                self._tasksets.put(self._taskset)
                self._logger.debug("Taskset variant is pushed back to queue due to" +
                                   " a critical error")
                # notify live handler about the stop.
                if self.monitor is not None:
                    self.monitor.__taskset_stop__(self._taskset)

            # push host back in pool (only, if there was an error). A closing
            # event does not trigger the push back to the host pool.
            self._sessions.remove(self)
            self._pool.put(self._host)

            # if this was the last processing session, you will get notified
            # about missing sessions.
            if not self._tasksets.empty() and len(self._sessions) == 0:
                self._logger.warning("No session is left for processing further" +
                                      " taskset variants. Waiting for new sessions.")
        finally:
            session.close()

