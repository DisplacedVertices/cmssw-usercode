#!/usr/bin/env python

import sys
import ROOT; ROOT.gROOT.SetBatch()
from signal_efficiency import SignalEfficiencyCombiner

bkg_fully_correlated = 'bkg_fully_correlated' in sys.argv

template = '''
# which = {0.which}
# nice name = {0.nice_name}

imax 3
jmax 1
kmax {0.nsyst}
------------
bin             b0  b1  b2
observation     {0.observed}
------------
bin b0 b1 b2 b0 b1 b2
process sig sig sig bkg bkg bkg
process 0 0 0 1 1 1
rate {0.sig_rate} {0.bkg_rate}
------------
sig lnN {0.sig_uncert} - - -
sigMC gmN {0.total_nsig} {0.sig_mc} - - -
'''
if bkg_fully_correlated:
    template += '''
bkg lnN - - - {0.bkg_uncert}
'''
else:
    template += '''
bkg1 lnN - - - {0.bkg_uncert_1} - -
bkg2 lnN - - - - {0.bkg_uncert_2} -
bkg3 lnN - - - - - {0.bkg_uncert_3}
'''

def make(which):
    combiner = SignalEfficiencyCombiner(simple=False)
    r = combiner.combine(which)

    def _strit(fmt,typ,n,offset=0,mult=1):
        return ' '.join(fmt % typ(x) for x in combiner._get(f.Get(n), offset, mult))
    def intstrit(n, offset=0, mult=1):
        return _strit('%i',int,n,offset,mult)
    def floatstrit(n, offset=0, mult=1):
        return _strit('%.9g',float,n,offset,mult)

    f = combiner.inputs[0].f # for background/etc. all same
    combiner.check(f.Get('h_observed').GetNbinsX(), f.Get('h_int_lumi').GetBinContent(1) / 1000)
    r.observed = intstrit('h_observed')
    r.bkg_rate = floatstrit('h_bkg_dvv_rebin', mult=f.Get('h_observed').Integral())
    r.bkg_uncert = floatstrit('h_bkg_uncert', offset=1.)
    r.bkg_uncert_1, r.bkg_uncert_2, r.bkg_uncert_3 = r.bkg_uncert.split()
    r.nsyst = 3 if bkg_fully_correlated else 5
    r.sig_mc = ' '.join('%.9g' % (x/r.total_nsig) for x in r.sig_rate)
    r.sig_rate = ' '.join('%.9g' % x for x in r.sig_rate)
    r.sig_uncert = ' '.join('%.9g' % x for x in r.sig_uncert)

    print template.format(r)

if __name__ == '__main__':
    try:
        which = int(sys.argv[1])
    except ValueError:
        from limitsinput import name2isample
        which = name2isample(ROOT.TFile('limitsinput.root'), sys.argv[1])
    make(which)
