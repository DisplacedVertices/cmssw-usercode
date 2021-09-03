#!/usr/bin/env python

import os, sys
from collections import defaultdict
from pprint import pprint
from DVCode.Tools.DBS import files_in_dataset
from DVCode.Tools.general import typed_from_argv

instance = typed_from_argv(int)
if instance is None:
    instance = 'global'

datasets = [x for x in sys.argv[1:] if x.count('/') == 3]

for dataset in datasets:
    d = defaultdict(list)
    files = files_in_dataset(dataset, instance)
    print dataset, 'has', len(files), 'files'
    for f in files:
        num = os.path.basename(f).split('_')[1]
        d[num].append(f)
    for k,v in d.iteritems():
        if len(v) > 1:
            print 'duplicate(s) for %s:' % k
            pprint(v)
