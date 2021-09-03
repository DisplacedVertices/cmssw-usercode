import sys, os, re, random
from collections import Counter
from fnmatch import fnmatch
from pprint import pprint
from DVCode.Tools import eos, SampleFiles
from DVCode.Tools.ROOTTools import ROOT

if len(sys.argv) < 3:
    sys.exit('usage: %s dataset sample\n  where dataset and sample are as registered in SampleFiles. sample can be "*" to mean all samples having the dataset.' % sys.argv[0])

dataset = sys.argv[1]
sample = sys.argv[2]
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

    nevents = []
    
    for fn in fns:
        assert fn.endswith('.root')
        if not eos.exists(fn):
            raise IOError('does not exist on eos: %r' % fn)

        f = ROOT.TFile.Open(eos.canon(fn))
        nev = f.Get('Events').GetEntriesFast()
        nevents.append(nev)

        if verbosity >= 2:
            print fn, nevents[-1]

    infos.append((sample, nevents))

infos.sort()
for sample, nevents in infos:
    print sample.ljust(30), 'nevents = %15i, average per file = %15.1f' % (sum(nevents), sum(nevents)/len(nevents))

