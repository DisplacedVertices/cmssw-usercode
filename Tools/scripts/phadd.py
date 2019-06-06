#!/usr/bin/env python

import sys
from JMTucker.Tools.CMSSWTools import cmssw_base
from JMTucker.Tools.CondorSubmitter import CondorSubmitter

def phadd(batch_name, dataset, samples, output_fn='phadd.root'):
    meat = '''
job=$(<cs_job)
fns=$(python -c 'from cs_filelist import get; print " ".join(get('$job'))')
cmd="./hadd.py __OUTPUT_FN__ $fns"

if false; then
  echo $cmd
  meatexit=0
  touch __OUTPUT_FN__
else
  $cmd 2>&1
  meatexit=$?
fi
'''.replace('__OUTPUT_FN__', output_fn)

    cs = CondorSubmitter(batch_name = batch_name,
                         dataset = dataset,
                         meat = meat,
                         pset_template_fn = '',
                         input_files = [cmssw_base('src/JMTucker/Tools/scripts/hadd.py')],
                         output_files = [output_fn, output_fn + '.haddlog'],
                         stageout_files = 'all',
                         )
    cs.submit_all(samples)


if __name__ == '__main__':
    from JMTucker.Tools import Samples, SampleFiles
    from JMTucker.Tools.general import int_ceil, typed_from_argv

    def usage():
        sys.exit('''usage: phadd.py batch_name dataset <samples list parseable by registry> [nfiles1=1 ...] [output_fn=phadd.root]
Hadd files registered in SampleFiles for the specified samples and dataset using CondorSubmitter.
The samples list is sorted by the registry, and the nfiles numbers specified will apply in that order.
If nfiles not specified, it is assumed 1--the nfiles list can be shorter than the samples list. 
''')

    if len(sys.argv) < 4:
        print sys.argv
        usage()

    batch_name = sys.argv[1]
    datasets = Samples.registry.datasets_from_argv()
    if len(datasets) != 1:
        raise ValueError('expect exactly one dataset in argv')
    dataset = datasets[0]

    samples = [s for s in Samples.registry.from_argv() if s.has_dataset(dataset)]

    output_fn = [x for x in sys.argv[2:] if x.endswith('.root')]
    output_fn = output_fn[0] if output_fn else 'phadd.root'

    nfileses = typed_from_argv(int, return_multiple=True)
    d = len(samples) - len(nfileses)
    if d < 0:
        raise ValueError('too many nfiles %s for # samples %i' % (nfileses, len(samples)))
    elif d > 0:
        nfileses.extend([1]*d)

    for sample, nfiles in zip(samples, nfileses):
        sample.set_curr_dataset(dataset)
        sample.split_by = 'files'
        sample.files_per = int_ceil(len(sample.filenames), nfiles)
        sample.njobs = nfiles
        print 'sample %s dataset %s nfiles %i -> %i' % (sample.name, dataset, len(sample.filenames), nfiles)

    phadd(batch_name, dataset, samples, output_fn)
