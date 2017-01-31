#!/usr/bin/env python

import sys
from JMTucker.Tools.DBS import dasgo_ll_for_dataset as ll_for_dataset
#from JMTucker.Tools.DBS import ll_for_dataset

print str(ll_for_dataset(sys.argv[1]))
