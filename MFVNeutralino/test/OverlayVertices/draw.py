import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetStatW(0.15)
ROOT.gStyle.SetStatH(0.1)

fn = sys.argv[1]
print fn

ps = plot_saver('plots/%s' % os.path.basename(fn).replace('.root', ''), size=(600,600), log=False)
f = ROOT.TFile(fn)

def rebin(h):
    #return h
    a = array('d', [x*0.002 for x in xrange(26)] + [0.05 + x*0.01 for x in range(6)])
    return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)
    
def get_h(n):
    h = rebin(f.Get('mfvOverlayHistos/%s' % n))
    h.SetLineWidth(2)
    h.GetXaxis().SetTitle('d_{VV} (cm)')
    h.GetYaxis().SetTitle('efficiency')
    return h

def get_h_eff(h_num, h_den):
    h_eff = ROOT.TGraphAsymmErrors(h_num, h_den, 'midp')
    h_eff.SetLineWidth(2)
    h_eff.GetXaxis().SetTitle('d_{VV} (cm)')
    h_eff.GetYaxis().SetTitle('efficiency')
    h_eff.GetYaxis().SetRangeUser(0, 1.4)
    return h_eff

h_den = get_h('h_dvv_true')

n_nums = [
    'h_dvv_pass_anytwo',
    'h_dvv_pass_twominntk',
    'h_dvv_pass_foundv0andv1',
    'h_dvv_pass_foundv0andv1samentk',
    'h_dvv_pass_foundv0andv1asmanyntk',
    'h_dvv_pass_foundv0andv1bytracks',
]

pars = ('floor', 'ceiling', 'threshold', 'width')

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

print '%35s' % '',
print '%20s %20s %20s %20s' % pars

for n_num in n_nums:
    h_num = get_h(n_num)
    #print n_num, h_num
    h_eff = get_h_eff(h_num, h_den)
    h_eff.Draw('AP')
    print '%35s' % n_num,
    fcn = do_fit(h_eff)
    ps.save(n_num)
