import sys
from JMTucker.Tools import Samples
from JMTucker.Tools import SampleFiles
from JMTucker.Tools.hadd import hadd

ntuple = sys.argv[1]
samples = Samples.registry.from_argv()

for s in samples:
    s.set_curr_dataset(ntuple)
    hadd(s.name + '.root', ['root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos') for fn in s.filenames])
