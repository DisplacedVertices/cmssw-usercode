#!/usr/bin/env python

import sys
from FWCore.PythonUtilities.LumiList import LumiList

ll = LumiList(filename=sys.argv[1])
print len(ll.getLumis())

