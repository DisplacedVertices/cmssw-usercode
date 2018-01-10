import sys, os, re, random
from collections import Counter
from fnmatch import fnmatch
from pprint import pprint
from JMTucker.Tools import eos, SampleFiles
from JMTucker.Tools.EdmFileInfo import EdmFileInfo

if len(sys.argv) < 4:
    sys.exit('usage: %s dataset sample pattern nfiles\n  where dataset and sample are as registered in SampleFiles, and pattern is a file pattern like "ntuple_*", and nfiles is the number of randomly sampled files. sample can be "*" to mean all samples having the dataset.' % sys.argv[0])

dataset = sys.argv[1]
sample = sys.argv[2]
pattern = sys.argv[3]
nfiles = int(sys.argv[4])
interactive = True
verbosity = 0

if '-f' in sys.argv:
    interactive = False

while '-v' in sys.argv:
    verbosity += 1
    sys.argv.remove('-v')

if '*' in sample or '?' in sample:
    samples = []
    for s, ds in SampleFiles.keys():
        if ds == dataset and fnmatch(s, sample):
            samples.append(s)
else:
    samples = [sample]
samples.sort()

infos = []

for sample in samples:
    if verbosity >= 1:
        print sample
    fns = SampleFiles.get_fns(sample, dataset)
    fns = random.sample(fns, nfiles)
    
    total_size = 0
    total_size_in_events = 0
    
    for fn in fns:
        assert fn.endswith('.root')
        if verbosity >= 2:
            print fn
        if not eos.exists(fn):
            raise IOError('does not exist on eos: %r' % fn)

        bn = os.path.basename(fn)
        if not fnmatch(bn, pattern):
            continue

        size = eos.size(fn)
        info = EdmFileInfo(eos.canon(fn))
        nevents = info.Events.nevents
        size_in_events = info.Events.size()

        if verbosity >= 3:
            print '  size %.0f in %i events %.0f frac %.4f' % (size, nevents, size_in_events, float(size_in_events) / size)

        total_size += size
        total_size_in_events += size_in_events

    infos.append((sample, total_size, total_size_in_events, total_size_in_events / float(total_size)))

infos.sort(key=lambda x:x[-1], reverse=True)
for sample, size, size_in_events, frac_size_in_events in infos:
    print sample.ljust(30), '%15.0f %15.0f %.4f' % (size, size_in_events, frac_size_in_events)
