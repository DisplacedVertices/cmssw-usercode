# for x in $nobackup/overlay/ntk* ; py draw.py $x/merge.root $(basename $x)

import sys, os
from JMTucker.Tools.ROOTTools import *
from binning import binning

fn = sys.argv[1]
out_name = sys.argv[2]
print fn

set_style()
ps = plot_saver(plot_dir('overlay/%s' % out_name), size=(600,600), log=False)
f = ROOT.TFile(fn)

h = f.Get('mfvOverlayHistos/h_dz_true')
h.Draw()
ps.save('h_dz_true')

bins, avgs = binning(out_name)

def rebin(h):
    #return h
    return h.Rebin(len(bins)-1, h.GetName() + '_rebin', bins)
    
def get_h(n):
    h = rebin(f.Get('mfvOverlayHistos/%s' % n))
    h.SetLineWidth(2)
    s = 'VV' if 'dvv' in n else '3D'
    h.GetXaxis().SetTitle('d_{%s} (cm)' % s)
    h.GetYaxis().SetTitle('efficiency')
    return h

def get_h_eff(h_num, h_den):
    h_eff = ROOT.TGraphAsymmErrors(h_num, h_den, 'b(1,1)')
    h_eff.SetLineWidth(2)
    nbins = h_eff.GetN()
    assert nbins == len(avgs)
    for i, x in enumerate(avgs):
        oldx, y = tgraph_getpoint(h_eff, i)
        exl = h_eff.GetErrorXlow(i)
        exh = h_eff.GetErrorXlow(i)
        xl = oldx-exl
        xh = oldx+exh
        h_eff.SetPoint(i, x, y)
        h_eff.SetPointEXlow(i, x-xl)
        h_eff.SetPointEXhigh(i, xh-x)
    s = 'VV' if 'dvv' in h_num.GetName() else '3D'
    h_eff.GetXaxis().SetTitle('d_{%s} (cm)' % s)
    h_eff.GetYaxis().SetTitle('efficiency')
    h_eff.GetYaxis().SetRangeUser(0, 1.4)
    return h_eff

def do_fit(h_eff):
    fcn = ROOT.TF1('fcn', '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', 0., 0.1)
    fcn.SetParNames(*pars)
    fcn.SetParameters(0., 1., 0.02, 0.01)
    fcn.SetParLimits(0, 0., 1.)
    fcn.SetParLimits(1, 0., 1.)
    h_eff.Fit(fcn, 'QR')
    for ipar, par in enumerate(pars):
        x = '%5.3f +- %5.3f' % (fcn.GetParameter(ipar), fcn.GetParError(ipar)),
        print '%20s' % x,
    print
    return fcn

dens = [
    'h_d3d',
    'h_dvv',
    ]

def print_h(h):
    if False:
        print h
        nbins = h.GetNbinsX()
        xax = h.GetXaxis()
        print 'nbinsx', nbins, 'xmin', xax.GetXmin(), 'xmax', xax.GetXmax()
        for ibin in xrange(nbins+2):
            print '  ', ibin, xax.GetBinLowEdge(ibin), h.GetBinContent(ibin)

def check(h_num, h_den):
    for ibin in xrange(h_num.GetNbinsX()+2):
        n = h_num.GetBinContent(ibin)
        d = h_den.GetBinContent(ibin)
        if n > d:
            print 'prob', ibin, h_num, n, h_den, d

for den in dens:
    h_den = get_h('%s_true'  % den)
    print_h(h_den)

    n_nums = [
        'pass_anytwo',
        'pass_twominntk',
        'pass_foundv0andv1',
        'pass_foundv0andv1samentk',
        'pass_foundv0andv1asmanyntk',
        'pass_foundv0andv1bytracks',
    ]

    pars = ('floor', 'ceiling', 'threshold', 'width')

    #print den
    #print '%35s' % '',
    #print '%20s %20s %20s %20s' % pars

    for n_num in n_nums:
        n_num = den + '_' + n_num
        h_num = get_h(n_num)
        print_h(h_num)
        check(h_num, h_den)
        h_eff = get_h_eff(h_num, h_den)
        h_eff.Draw('AP')
#        h_eff.GetXaxis().SetRangeUser(0, 0.3)
        #print '%35s' % n_num,
        #fcn = do_fit(h_eff)
        ps.save(n_num)
