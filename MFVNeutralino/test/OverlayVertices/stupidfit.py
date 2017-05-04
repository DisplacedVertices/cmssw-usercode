import sys
from math import ceil
from JMTucker.Tools.ROOTTools import *
set_style()

ROOT.gStyle.SetPadTopMargin(0.01)
ROOT.gStyle.SetPadBottomMargin(0.04)
ROOT.gStyle.SetPadLeftMargin(0.04)
ROOT.gStyle.SetPadRightMargin(0.01)

fout = ROOT.TFile('export.root', 'recreate')

ps = plot_saver(plot_dir('spline_new_2'), log=False, size=(800,400))

exs = [
    'ntk3',
    'ntk4',
    'ntk5',
    ]

for ex in exs:
    fn = '/publicweb/t/tucker/asdf/plots/overlay/%s/h_dvv_pass_foundv0andv1bytracks.root' % ex
    f = ROOT.TFile(fn)
    g = f.Get('c0').FindObject('divide_h_dvv_pass_foundv0andv1bytracks_rebin_by_h_dvv_true_rebin').Clone('g')
    lasty = -1
    i = 0
    while i < g.GetN():
        x,y = tgraph_getpoint(g, i)
        if y < lasty:
            g.RemovePoint(i)
        else:
            lasty = y
            i += 1
    lastx, lasty = tgraph_getpoint(g, -1)
    if lasty < 4:
        n = g.GetN()
        g.Set(n+1)
        g.SetPoint(n, 4., lasty)
    print ex
    for i in xrange(g.GetN()):
        print i, tgraph_getpoint(g,i)
    print
#    fcn = ROOT.TF1('fcn_%s' % ex, '[0]*TMath::Erf((x-[3])/[1]) + [2] + [4]*TMath::Erf((x-[5])/[6])', 0, 4 if 'ntk5' in ex else 0.3)
#    fcn.SetParLimits(0, 0, 1)
#    fcn.SetParLimits(1, 0, 100)
#    fcn.SetParLimits(2, 0, 1)
#    fcn.SetParLimits(3, -10, 10)
#    fcn.SetParLimits(4, 0, 1)
#    fcn.SetParLimits(5, -10, 10)
#    fcn.SetParLimits(6, 0, 100)
#    g.Fit(fcn, 'R')
#    print fcn.Eval(0), fcn.Eval(4)
#    print
#    ps.c.cd()
#    fcn.SetRange(0,4)
    ps.c.cd()
    g.Draw('APL')
#    fcn.Draw('same')
    
    nbins = 400
    fout.cd()
    heff = ROOT.TH1D('overlay_%s' % ex, '', nbins, 0, 4)
    for ibin in xrange(1,nbins+1):
        x = heff.GetBinCenter(ibin)
        heff.SetBinContent(ibin, g.Eval(x))
    heff.SetBinContent(nbins+1, heff.GetBinContent(nbins))
    heff.Write()

    ps.save(ex)

