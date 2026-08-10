# don't use this on (MINI)AOD files but rather on ntuples
# on (MINI)AOD use e.g. dasgo "file,lumi dataset="$(samples ds qcdht1000_2017 miniaod) | grep 833,
# run with | egrep -v '^File </tmp/tmp'

import sys, os
from pprint import pprint
from JMTucker.Tools import eos, SampleFiles
from JMTucker.Tools.ROOTTools import ROOT, detree

if len(sys.argv) < 6:
    sys.exit('usage: %s dataset sample run lumi event\n  where dataset and sample are as registered in SampleFiles. sample can be "*" to mean all samples having the dataset.' % sys.argv[0])

dataset = sys.argv[1]
sample = sys.argv[2]
rle = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])

fns = SampleFiles.get_fns(sample, dataset)
nfound = 0

for fn in fns:
    assert fn.endswith('.root')
    if not eos.exists(fn):
        raise IOError('does not exist on eos: %r' % fn)

    f = ROOT.TFile.Open(eos.canon(fn))
    t = f.Get('Events')
    for x in sorted(detree(t, 'EventAuxiliary.id().run():EventAuxiliary.luminosityBlock():EventAuxiliary.id().event()', xform=int)):
        if x == rle:
            print fn
            nfound += 1

if nfound != 1:
    sys.exit('%i found' % nfound)

