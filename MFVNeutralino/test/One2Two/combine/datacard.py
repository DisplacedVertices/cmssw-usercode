#!/usr/bin/env python

import sys, ROOT
ROOT.gROOT.SetBatch()

bkg_fully_correlated = 'bkg_fully_correlated' in sys.argv

def make(which):
    fn = 'limitsinput.root'
    f = ROOT.TFile(fn)

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

    h_norm = f.Get('h_signal_%i_norm' % which)
    nice_name = h_norm.GetTitle()
    sig_norm = int_lumi * h_norm.GetBinContent(2)

    sig_name = 'h_signal_%i_dvv_rebin' % which
    sig_rate = floatstrit(sig_name, mult=sig_norm)
    bkg_rate = floatstrit('h_bkg_dvv_rebin', mult=ndata)

    sig_uncert = floatstrit('h_signal_%i_uncert' % which, offset=1.)
    bkg_uncert = floatstrit('h_bkg_uncert', offset=1.)

    h_sig = f.Get(sig_name)
    nsig = int(h_sig.GetEntries())
    sig_mc = ' '.join('%.9g' % (float(x)/nsig) for x in sig_rate.split())

    nsyst = 3 if bkg_fully_correlated else 5

    print '''
# which = %(which)s
# nice name = %(nice_name)s

imax 3
jmax 1
kmax %(nsyst)s
------------
bin             b0  b1  b2
observation     %(observed)s
------------
bin b0 b1 b2 b0 b1 b2
process sig sig sig bkg bkg bkg
process 0 0 0 1 1 1
rate %(sig_rate)s %(bkg_rate)s
------------
sig lnN %(sig_uncert)s - - -
sigMC gmN %(nsig)s %(sig_mc)s - - -
''' % locals()

    if bkg_fully_correlated:
        print '''
bkg lnN - - - %(bkg_uncert)s
''' % locals()
    else:
        bkg_uncert_1, bkg_uncert_2, bkg_uncert_3 = bkg_uncert.split()
        print '''
bkg1 lnN - - - %(bkg_uncert_1)s - -
bkg2 lnN - - - - %(bkg_uncert_2)s -
bkg3 lnN - - - - - %(bkg_uncert_3)s
''' % locals()


if __name__ == '__main__':
    try:
        which = int(sys.argv[1])
    except ValueError:
        from limitsinput import name2isample
        print '# name = %s' % sys.argv[1]
        which = name2isample(ROOT.TFile('limitsinput.root'), sys.argv[1])
    make(which)
