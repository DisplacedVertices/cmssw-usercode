from DVCode.Tools.ROOTTools import *
import DVCode.MFVNeutralino.AnalysisConstants as ac

year = '2017p8'
version = 'V23m'
set_style()
ps = plot_saver(plot_dir('geo2ddist_%s_%s' % (version, year)), size=(700,700), root=False, log=False)

f = ROOT.TFile('/uscms_data/d3/dquach/crab3dirs/HistosV23m/background_%s.root' % year)
h = f.Get('vtxHst1VNoGeo2ddist/h_sv_pos_bs2dxy')
h.SetStats(0)
h.SetTitle(';Vertex x (cm);Vertex y (cm)')
h.Draw('colz1')

e = ROOT.TEllipse(0.02479,-0.06929,2)
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
lum = write(42, 0.04, lum_pos+stupid, 0.930-subtr, ac.int_lumi_nice_2017p8)
cms = write(61, 0.04, 0.098+stupid, 0.930-subtr, 'CMS')
exlab_str = 'Simulation Preliminary'
exlab = write(52, 0.035, 0.185, 0.930-subtr, exlab_str)

ps.save('onevtx_geo2ddist')
