import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetStatW(0.15)
ROOT.gStyle.SetStatH(0.1)

fn = sys.argv[1]
out_name = sys.argv[2]
print fn

ps = plot_saver('plots/overlay/%s' % out_name, size=(600,600), log=False)
f = ROOT.TFile(fn)

h = f.Get('mfvOverlayHistos/h_dz_true')
h.Draw()
ps.save('h_dz_true')

def rebin(h):
    #return h
    if 'ntk5' in out_name:
        bins = [ 0.0000, 0.0040, 0.0080, 0.0110, 0.0140, 0.0170, 0.0190, 0.0210, 0.0230, 0.0250, 0.0270, 0.0300, 0.0330, 0.0370, 0.0430, 0.0520, 0.1000, ]
    elif 'ntk4' in out_name:
        bins = [ 0.0000, 0.0010, 0.0020, 0.0030, 0.0040, 0.0050, 0.0060, 0.0070, 0.0080, 0.0090, 0.0100, 0.0110, 0.0120, 0.0130, 0.0140, 0.0150, 0.0160, 0.0170, 0.0180, 0.0190, 0.0200, 0.0210, 0.0220, 0.0230, 0.0240, 0.0250, 0.0260, 0.0270, 0.0280, 0.0290, 0.0300, 0.0310, 0.0320, 0.0330, 0.0340, 0.0350, 0.0360, 0.0370, 0.0380, 0.0390, 0.0400, 0.0410, 0.0420, 0.0430, 0.0440, 0.0450, 0.0460, 0.0470, 0.0480, 0.0490, 0.0500, 0.0510, 0.0520, 0.0530, 0.0540, 0.0550, 0.0560, 0.0570, 0.0580, 0.0590, 0.0600, 0.0610, 0.0620, 0.0630, 0.0640, 0.0650, 0.0660, 0.0670, 0.0680, 0.0690, 0.0700, 0.0710, 0.0720, 0.0730, 0.0740, 0.0750, 0.0760, 0.0770, 0.0780, 0.0790, 0.0800, 0.0810, 0.0820, 0.0830, 0.0840, 0.0850, 0.0860, 0.0870, 0.0880, 0.0890, 0.0900, 0.0910, 0.0920, 0.0930, 0.0940, 0.0950, 0.0960, 0.0980, 0.1000, ]
    elif 'ntk3' in out_name:
        bins = [ 0.0000, 0.0010, 0.0020, 0.0030, 0.0040, 0.0050, 0.0060, 0.0070, 0.0080, 0.0090, 0.0100, 0.0110, 0.0120, 0.0130, 0.0140, 0.0150, 0.0160, 0.0170, 0.0180, 0.0190, 0.0200, 0.0210, 0.0220, 0.0230, 0.0240, 0.0250, 0.0260, 0.0270, 0.0280, 0.0290, 0.0300, 0.0310, 0.0320, 0.0330, 0.0340, 0.0350, 0.0360, 0.0370, 0.0380, 0.0390, 0.0400, 0.0410, 0.0420, 0.0430, 0.0440, 0.0450, 0.0460, 0.0470, 0.0480, 0.0490, 0.0500, 0.0510, 0.0520, 0.0530, 0.0540, 0.0550, 0.0560, 0.0570, 0.0580, 0.0590, 0.0600, 0.0610, 0.0620, 0.0630, 0.0640, 0.0650, 0.0660, 0.0670, 0.0680, 0.0690, 0.0700, 0.0710, 0.0720, 0.0730, 0.0740, 0.0750, 0.0760, 0.0770, 0.0780, 0.0790, 0.0800, 0.0810, 0.0820, 0.0830, 0.0840, 0.0850, 0.0860, 0.0870, 0.0880, 0.0890, 0.0900, 0.0910, 0.0920, 0.0930, 0.0940, 0.0950, 0.0960, 0.0970, 0.0980, 0.0990, 0.1000, ]
    else:
        raise ValueError('ntk not in name? %s' % out_name)
    return h.Rebin(len(bins)-1, h.GetName() + '_rebin', array('d', bins))
    
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
        h_eff.GetXaxis().SetRangeUser(0, 0.3)
        #print '%35s' % n_num,
        #fcn = do_fit(h_eff)
        ps.save(n_num)
