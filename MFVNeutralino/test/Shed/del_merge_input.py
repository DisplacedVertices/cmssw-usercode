import os
from JMTucker.Tools.CondorTools import *

for wd in cs_dirs_from_argv():
    al = set()
    for l in cs_filelist(wd):
        for fn in l:
            dn = os.path.dirname(fn)
            assert os.path.basename(dn) == '0000'
            al.add(os.path.dirname(dn))
    for x in sorted(al):
        print x

