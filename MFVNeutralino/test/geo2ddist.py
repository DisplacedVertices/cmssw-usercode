from JMTucker.Tools.ROOTTools import *

set_style()
ps = plot_saver('plots/AN-16-394/geo2ddist', size=(700,700), root=False, log=False)

#f = ROOT.TFile('~/crabdirs/HistosV6p1_76x_nstlays3_27/background.root')
#f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/HistosV10/background_noqcdext.root')
#f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/HistosV10/ntk5/background.root')
f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/HistosV11_15/background.root')
h = f.Get('vtxHst1VNoGeo2ddist/h_sv_pos_2d_0xy')
h.SetStats(0)
h.SetTitle(';Vertex x (cm);Vertex y (cm)')
h.Draw('colz')

e = ROOT.TEllipse(-0.1048,-0.1687,2)
e.SetLineColor(ROOT.kRed)
e.SetLineWidth(5)
e.SetFillColorAlpha(0,0)
e.Draw()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

subtr = 0.02
lum_pos = 0.625
stupid = 0
lum = write(42, 0.04, lum_pos+stupid, 0.930-subtr, '39.5 fb^{-1} (13 TeV)')
cms = write(61, 0.04, 0.098+stupid, 0.930-subtr, 'CMS')
exlab_str = 'Simulation Preliminary'
exlab = write(52, 0.035, 0.185, 0.930-subtr, exlab_str)

ps.save('onevtx_geo2ddist')
