#!/usr/bin/env python

import os, sys
from collections import defaultdict
from pprint import pprint
from JMTucker.Tools.DBS import files_in_dataset
from JMTucker.Tools.general import bool_from_argv

ana01 = bool_from_argv('ana01')
ana02 = bool_from_argv('ana02')
ana03 = bool_from_argv('ana03')

datasets = [x for x in sys.argv[1:] if x.count('/') == 3]

for dataset in datasets:
    d = defaultdict(list)
    files = files_in_dataset(dataset, ana01=ana01, ana02=ana02, ana03=ana03)
    print dataset, 'has', len(files), 'files'
    for f in files:
        num = os.path.basename(f).split('_')[1]
        d[num].append(f)
    for k,v in d.iteritems():
        if len(v) > 1:
            print 'duplicate(s) for %s:' % k
            pprint(v)
