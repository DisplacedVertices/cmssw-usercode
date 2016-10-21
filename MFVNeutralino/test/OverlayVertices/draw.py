from array import array
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetStatW(0.15)
ROOT.gStyle.SetStatH(0.1)

fn = 'overlay_wevent_dist0p005_2'

ps = plot_saver('plots/%s' % fn, size=(600,600), log=False)
f = ROOT.TFile('%s.root' % fn)

def rebin(h):
    a = array('d', [x*0.005 for x in xrange(21)])
    return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)
    
def get_h(n):
    h = rebin(f.Get('mfvOverlayHistos/%s' % n))
    h.SetLineWidth(2)
    h.GetXaxis().SetTitle('d_{VV} (cm)')
    h.GetYaxis().SetTitle('efficiency')
    return h

h_den = get_h('h_dvv_true')

n_nums = [
    'h_dvv_pass_anytwo',
    'h_dvv_pass_twominntk',
    'h_dvv_pass_foundv0andv1',
    'h_dvv_pass_foundv0andv1samentk',
    'h_dvv_pass_foundv0andv1asmanyntk',
]

fcn = ROOT.TF1('fcn', '[0]*(0.5 + 0.5 * TMath::Erf((x - [1])/[2]))', 0, 0.1)
fcn.SetParameters(1., 0.02, 0.01)

for n_num in n_nums:
    h_num = get_h(n_num)
    print n_num, h_num
    h_eff = ROOT.TGraphAsymmErrors(h_num, h_den, 'midp')
    h_eff.Draw('AP')
    h_eff.Fit(fcn, 'QR')
    h_eff.GetYaxis().SetRangeUser(0, 1.4)
    ps.save(n_num)
