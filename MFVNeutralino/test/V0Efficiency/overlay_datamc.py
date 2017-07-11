import sys
from JMTucker.Tools.ROOTTools import *
set_style()

ps = plot_saver(plot_dir('v0bkgsub_datavmc'), size=(600,600))

def getit(fn):
    f = ROOT.TFile(fn)
    c = f.Get('c0')
    g = c.GetListOfPrimitives()[1]
    assert g.Class().GetName() == 'TGraphAsymmErrors'
    return f,c,g

fdata, cdata, gdata = getit('data.root')
fmc, cmc, gmc = getit('mc.root')

ps.c.cd()

gdata.SetLineColor(1)
gmc.SetLineColor(2)

gdata.SetLineWidth(2)
gdata.SetMarkerStyle(20)
gdata.SetMarkerSize(0.8)
gdata.SetLineColor(1)

gmc.SetFillStyle(3001)
gmc.SetMarkerStyle(24)
gmc.SetMarkerSize(0.8)
gmc.SetMarkerColor(2)
gmc.SetLineColor(2)
gmc.SetFillColor(2)

gmc.GetYaxis().SetTitle('ratio of ratios')

gmc.Draw('APE2')
gdata.Draw('P')
ps.save('rrr')


