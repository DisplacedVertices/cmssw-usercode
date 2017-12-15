#!/usr/bin/env python

import sys, ROOT
ROOT.gROOT.SetBatch()

bkg_fully_correlated = 'bkg_fully_correlated' in sys.argv

class namedtuple:
    def __init__(self, **args):
        for k,v in args.iteritems():
            setattr(self, k, v)

def trigmult(x):
    return 0.99
def sf20156(x, pars=(0.9784, -1128., 1444.)):
    return trigmult(x) * (2. - pars[0] * ROOT.TMath.Erf((x-pars[1])/pars[2]))
def one(x):
    return 1.

def make(which):
    inputs = [
        namedtuple(fn='limitsinput_nonhip.root', int_lumi= 2.62, sf=sf20156,  include_stat=False),
        namedtuple(fn='limitsinput_hip.root',    int_lumi=19.70, sf=trigmult, include_stat=True),
        namedtuple(fn='limitsinput_nonhip.root', int_lumi=16.23, sf=trigmult, include_stat=True),
        ]

    #inputs = [namedtuple(fn='limitsinput.root', int_lumi=38.529, sf=one, include_stat=True)]

    for inp in inputs:
        inp.f = ROOT.TFile(inp.fn)

    def _strit(fmt,typ,n,offset=0,mult=1):
        h = f.Get(n)
        return ' '.join(fmt % typ(offset + mult*h.GetBinContent(ibin)) for ibin in xrange(1,nbins+1))
    def intstrit(n, offset=0, mult=1):
        return _strit('%i',int,n,offset,mult)
    def floatstrit(n, offset=0, mult=1):
        return _strit('%.9g',float,n,offset,mult)

    f = inputs[0].f # for background/etc. all same
    nbins = f.Get('h_observed').GetNbinsX()
    int_lumi_check = f.Get('h_int_lumi').GetBinContent(1)
    assert abs(int_lumi_check / 1000 - sum(inp.int_lumi for inp in inputs)) < 0.3 # grr
    ndata = f.Get('h_observed').Integral(0,nbins+2)
    observed = intstrit('h_observed')
    bkg_rate = floatstrit('h_bkg_dvv_rebin', mult=ndata)
    bkg_uncert = floatstrit('h_bkg_uncert', offset=1.)
    f = None

    total_nsig = 0
    sig_rate = [0.]*nbins
    sig_uncert = None
    for inp in inputs:
        f = inp.f

        h_norm = f.Get('h_signal_%i_norm' % which)
        nice_name = h_norm.GetTitle()
        mass = int(nice_name.split('_M')[-1])

        h_dvv = f.Get('h_signal_%i_dvv_rebin' % which)
        nsig = [h_dvv.GetBinContent(ibin) for ibin in xrange(1,nbins+1)]
        ngen = 1e-3 / h_norm.GetBinContent(2)

        if inp.include_stat:
            total_nsig += int(sum(nsig))

        for i in xrange(nbins):
            sig_rate[i] += nsig[i] / ngen * inp.int_lumi * inp.sf(mass)

        su = floatstrit('h_signal_%i_uncert' % which, offset=1.)
        if sig_uncert is not None:
            assert su == sig_uncert
        sig_uncert = su

    total_nsig = total_nsig
    sig_mc = ' '.join('%.9g' % (x/total_nsig) for x in sig_rate)
    sig_rate = ' '.join('%.9g' % x for x in sig_rate)

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
sigMC gmN %(total_nsig)s %(sig_mc)s - - -
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
