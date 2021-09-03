import sys, os
from math import ceil
from DVCode.Tools.ROOTTools import *
from DVCode.Tools import SampleFiles as sf

used_half_mc = False
target_nevents = 50000 # the number of presel events that make it to the vertexer per job

print '%30s %12s/%12s = %10s -> %10s (%10s)' % ('sample','npresel','nmcstat','frac','targnfns','evsfromtgt')
for fn in sys.argv[1:]:
    sname = os.path.basename(fn).replace('.root','')
    f = ROOT.TFile(fn)
    mcstat = f.Get('mcStat/h_sums').GetBinContent(1)
    if used_half_mc and not sname.startswith('JetHT'):
        mcstat /= 2
    npresjet = f.Get('mfvEventHistosJetPreSel/h_npv').GetEntries()
    #npreslep = f.Get('mfvEventHistosLeptonPreSel/h_npv').GetEntries()
    nfns = len(sf.get_fns(sname, 'miniaod')) if sf.has(sname, 'miniaod') else -1
    tfns = min(int(ceil(target_nevents / npresjet * nfns)), 50)
    evsfromtfns = (2 if used_half_mc else 1) * mcstat * tfns / nfns
    print '%30s %12.0f/%12.0f = %10.6f -> %4i/%5i (%10i)' % (sname, npresjet, mcstat, npresjet/mcstat, tfns, nfns, evsfromtfns)    #(lep %12.0f -> %10.6f)' % (, npreslep, npreslep/mcstat)
