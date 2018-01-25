
"""
All files of `taskgen/attrs/*` are imported. For usage:
```
from taskgen.attrs import *

pi.Custom(...)
priority.Low 
"""

import os
import glob
import random

all_list = list()
for f in glob.glob(os.path.dirname(__file__)+"/*.py"):
    if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
        all_list.append(os.path.basename(f)[:-3])

__all__ = all_list  


