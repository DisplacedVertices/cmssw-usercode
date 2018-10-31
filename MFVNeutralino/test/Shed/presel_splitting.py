import sys, os
from math import ceil
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import SampleFiles as sf

used_half_mc = True
target_nevents = 50000 # the number of presel events that make it to the vertexer per job

for fn in sys.argv[1:]:
    sname = os.path.basename(fn).replace('.root','')
    f = ROOT.TFile(fn)
    mcstat = f.Get('mcStat/h_sums').GetBinContent(1)
    if used_half_mc and not sname.startswith('JetHT'):
        mcstat /= 2
    npresjet = f.Get('mfvEventHistosJetPreSel/h_npv').GetEntries()
    npreslep = f.Get('mfvEventHistosLeptonPreSel/h_npv').GetEntries()
    nfns = len(sf.get_fns(sname, 'miniaod'))
    tfns = min(int(ceil(target_nevents / npresjet * nfns)), 50)
    evsfromtfns = (2 if used_half_mc else 1) * mcstat * tfns / nfns
    print '%30s %12.0f/%12.0f = %10.6f -> %3i/%4i (%8i) (lep %12.0f -> %10.6f)' % (sname, npresjet, mcstat, npresjet/mcstat, tfns, nfns, evsfromtfns, npreslep, npreslep/mcstat)
