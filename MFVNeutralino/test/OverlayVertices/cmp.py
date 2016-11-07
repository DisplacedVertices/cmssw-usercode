import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
set_style()

class F:
    def __init__(self, fn):
        self.fn = fn
        self.x = x = fn.split('/')[2].split('_')[1:3]
        self.n = n = '_'.join(x)
        self.sample = x[0]
        self.ntracks = int(x[1][-1])
        self.f = f = ROOT.TFile(fn)
        self.g = g = f.Get('c0').FindObject('divide_h_dvv_pass_foundv0andv1bytracks_rebin_by_h_dvv_true_rebin').Clone(n)
        color = {
            'ttbar_ntk3': ROOT.kRed,
            'ttbar_ntk4': ROOT.kRed-7,
            'ttbar_ntk5': ROOT.kRed-9,
            'qcdht1500_ntk3': ROOT.kBlue,
            'qcdht1500_ntk4': ROOT.kBlue-7,
            'qcdht1500_ntk5': ROOT.kBlue-9,
            }[n]
        #print n
        #for i in xrange(41):
        #    x,y = ROOT.Double(), ROOT.Double()
        #    g.GetPoint(i if i <= 10 else 10, x,y)
        #    print 'h_eff->SetBinContent(%i, %f);' % (i+1, y)
        g.SetLineColor(color)
        g.GetListOfFunctions()[0].SetBit(ROOT.TF1.kNotDraw)
        x = g.GetListOfFunctions()[1]
        x.SetLineColor(0), x.SetTextColor(0), x.SetX1NDC(1), x.SetY1NDC(1), x.SetX2NDC(1), x.SetY2NDC(1) # grr

files = '''plots/overlay/overlay_qcdht1500_ntk3_Zdeltasv_dist0p008_first1000/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/overlay_qcdht1500_ntk4_Zdeltasv_dist0p008_first1000/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/overlay_qcdht1500_ntk5_Zdeltasv_dist0p008_first454/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/overlay_ttbar_ntk3_Zdeltasv_dist0p008_first1000/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/overlay_ttbar_ntk4_Zdeltasv_dist0p008_first1000/h_dvv_pass_foundv0andv1bytracks.root
plots/overlay/overlay_ttbar_ntk5_Zdeltasv_dist0p008_first194/h_dvv_pass_foundv0andv1bytracks.root'''.split('\n')

fs = [F(fn) for fn in files]

ps = plot_saver('plots/overlay/compare', log=False)

scales = [
    0.791, 0.659, 0.486,
    0.815, 0.652, 0.378,
    ]

do_scale = False

for i,f in enumerate(fs):
    g = f.g
    print i, f.n, g, g.GetN()
    if do_scale:
        scale = 1./scales[i]
        for j in xrange(g.GetN()):
            x,y = ROOT.Double(), ROOT.Double()
            g.GetPoint(j, x,y)
            g.SetPoint(j, x, y*scale)
    g.GetXaxis().SetLimits(0, 0.115)
    g.GetYaxis().SetRangeUser(0, 1.5)
    g.Draw('AP' if i == 0 else 'P same')

leg = ROOT.TLegend(0.131, 0.810, 0.525, 0.863)
leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.AddEntry(fs[0].g, 'qcdht1500', 'L')
leg.AddEntry(fs[3].g, 'ttbar', 'L')
leg.Draw()

txt = ROOT.TLatex()
txt.SetTextSize(0.04)
txt.SetTextFont(42)
for i,ntk in enumerate([3,4,5]):
    f = fs[i]
    g = f.g
    #fcn = ROOT.TF1('fcn', 'pol1', 0.05, 0.1)
    #res = g.Fit(fcn, 'RQS')
    #res.Print()
    #print f.n, fcn.Eval(0.1)
    x,y = ROOT.Double(), ROOT.Double()
    g.GetPoint(g.GetN()-1, x,y)
    txt.DrawLatex(x+0.005, y, 'n_{tk}=%i' % ntk)

ps.save('cmp')
