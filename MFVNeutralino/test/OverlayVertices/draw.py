from array import array
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('plots/overlay')

f = ROOT.TFile('overlay.root')

def rebin(h):
    a = array('d', [x*0.01 for x in xrange(11)])
    return h.Rebin(len(a)-1, h.GetName() + '_rebin', a)
    
def get_h(n):
    return rebin(f.Get('mfvOverlayHistos/%s' % n))

h_den = get_h('h_dvv_true')

n_nums = [
    'h_dvv_pass_anytwo',
    'h_dvv_pass_twominntk',
    'h_dvv_pass_foundv0',
    'h_dvv_pass_foundv0samentk',
    'h_dvv_pass_foundv0andv1',
    'h_dvv_pass_foundv0andv1samentk',
]

fcn = ROOT.TF1('fcn', '[0] + [1]*(0.5 + 0.5 * TMath::Erf((x - [2])/[3]))', 0, 0.05)
fcn.SetParameters(0., 1., 0.02, 0.01)

for n_num in n_nums:
    h_num = get_h(n_num)
    print n_num, h_num
    h_eff = ROOT.TGraphAsymmErrors(h_num, h_den, 'midp')
    h_eff.Draw('AP')
    h_eff.Fit(fcn, 'QR')
    ps.save(n_num)
