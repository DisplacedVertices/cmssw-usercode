import os
from collections import defaultdict
from pprint import pprint
from JMTucker.Tools.CRAB3ToolsSh import crab_dirs_from_argv, crab_hadd_files as crab_files
from modify import get_scanpack

sample_files = defaultdict(list)

for wd in crab_dirs_from_argv():
    bwd = os.path.basename(wd)

    _, scanpack, batch = bwd.split('_')
    batch = int(batch)
    scanpack = get_scanpack(scanpack)

    expected, files = crab_files(wd, True)
    assert expected == scanpack.jobs_per_batch or expected == scanpack.jobs_in_last_batch

    for fn in files:
        bn = os.path.basename(fn)
        if not bn.startswith('minitree'):
            continue

        job = int(bn.rsplit('_',1)[-1].replace('.root', '')) - 1
        kind, tau, mass = scanpack.sample(batch, job)
        sample_name = scanpack.sample_name(kind, tau, mass)
        sample_files[sample].append(fn)

pprint(dict(sample_files))
