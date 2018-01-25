#!/usr/local/bin/python3
import logging
import sys
sys.path.append('../../')
import time
from taskgen.tasksets.hey import HeyTaskSet
from taskgen.distributor import Distributor

from pprint import pprint as pp


logging.basicConfig(level=logging.DEBUG)



ts = HeyTaskSet()

d = Distributor("172.25.1.0/24")

d.start(ts, wait=False)
d.close()

