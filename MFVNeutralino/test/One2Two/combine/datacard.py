#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()

def make(which):
    out_fn = 'limits_input.root'
    f = ROOT.TFile(out_fn)

    def _strit(fmt,typ,n,offset=0,mult=1):
        h = f.Get(n)
        return ' '.join(fmt % typ(offset + mult*h.GetBinContent(ibin)) for ibin in xrange(1,nbins+1))
    def intstrit(n, offset=0, mult=1):
        return _strit('%i',int,n,offset,mult)
    def floatstrit(n, offset=0, mult=1):
        return _strit('%.9f',float,n,offset,mult)

    nbins = f.Get('h_observed').GetNbinsX()
    int_lumi = f.Get('h_int_lumi').GetBinContent(1)

    ndata = f.Get('h_observed').Integral(0,nbins+2)
    observed = intstrit('h_observed')

    sig_norm = int_lumi * f.Get('h_signal_%i_norm' % which).GetBinContent(2)

    sig_name = 'h_signal_%i_dvv_rebin' % which
    sig_rate = floatstrit(sig_name, mult=sig_norm)
    bkg_rate = floatstrit('h_bkg_dvv_rebin', mult=ndata)

    sig_uncert = floatstrit('h_signal_%i_uncert' % which, offset=1.)
    bkg_uncert = floatstrit('h_bkg_uncert', offset=1.)

    h_sig = f.Get(sig_name)
    nsig = int(h_sig.GetEntries())
    sig_mc = ' '.join('%.9g' % (float(x)/nsig) for x in sig_rate.split())

    print '''
imax 3
jmax 1
kmax 3
------------
bin             0  1  2
observation     %(observed)s
------------
bin 0 1 2 0 1 2
process sig sig sig bkg bkg bkg
process 0 0 0 1 1 1
rate %(sig_rate)s %(bkg_rate)s
------------
sig lnN %(sig_uncert)s - - -
sigMC gmN %(nsig)s %(sig_mc)s - - -
bkg lnN - - - %(bkg_uncert)s
''' % locals()

if __name__ == '__main__':
    import sys
    which = int(sys.argv[1])
    make(which)
