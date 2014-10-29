#!/usr/bin/env python

import os, sys
from JMTucker.Tools.CRABTools import *

if 'lists' in sys.argv:
    for d in sys.argv:
        if is_crab_working_dir(d):
            print d
            lst_fn = os.path.basename(d).replace('crab_', '') + '.lst'
            os.system('crtools -outputFromFJR %s noraise | grep root > %s' % (d, lst_fn))

elif 'draws' in sys.argv:
    pass
