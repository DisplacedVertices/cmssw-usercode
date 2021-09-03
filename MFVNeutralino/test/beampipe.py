from DVCode.Tools.ROOTTools import *
from DVCode.Tools.Samples import *

set_style()
ps = plot_saver(plot_dir('beampipe_nobssub'), size=(600,600), log=False, pdf=False)

# need to run non-beamspot subtracted minitrees or modify the detree below to undo the bs subtraction, it only matters slightly with 2017/8 beamspots
# beampipe fits from https://indico.cern.ch/event/750054/contributions/3181607/attachments/1740361/2816115/2018.10.17_2018Data_kropiv.pdf slide 8
def circles(sample):
    beampipe_style = 8,1,41
    new_cut_style = 6,6,41
    old_cut_circle = 0, 0, 2, 6,1,39

    beampipe_2017 = 0.113, -0.180, 2.21
    beampipe_2018 = 0.171, -0.175, 2.21

    new_cut = lambda bp: bp[:-1] + (bp[-1] - 0.12,)
    new_cut_2017 = new_cut(beampipe_2017)
    new_cut_2018 = new_cut(beampipe_2018)

    beampipe_mc2017 = 0, 0, 2.21
    beampipe_mc2018 = 0, 0, 2.21

    new_cut_mc2017 = new_cut(beampipe_mc2017)
    new_cut_mc2018 = new_cut(beampipe_mc2018)

    if sample.startswith('JetHT2017'):
        return [old_cut_circle, new_cut_2017 + new_cut_style, beampipe_2017 + beampipe_style]
    elif sample.startswith('JetHT2018'):
        return [old_cut_circle, new_cut_2018 + new_cut_style, beampipe_2018 + beampipe_style]
    else:
        assert 'qcdht' in sample or 'ttbarht' in sample or sample.startswith('MC201')
        if sample.endswith('2017'):
            return [old_cut_circle, new_cut_mc2017 + new_cut_style, beampipe_mc2017 + beampipe_style]
        elif sample.endswith('2018'):
            return [old_cut_circle, new_cut_mc2018 + new_cut_style, beampipe_mc2018 + beampipe_style]

    return []

if 1:
    data_samples = ['JetHT2017', 'JetHT2018'] 
    mc_samples = ['MC2017', 'MC2018']
else:
    data_samples = [s.name for s in data_samples_2017 + data_samples_2018]
    mc_samples = [s.name for s in qcd_samples_2017 + ttbar_samples_2017 + qcd_samples_2018 + ttbar_samples_2018]

for sample in data_samples + mc_samples:
    f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/MiniTreeV25m_nofiducial_nobssub/%s.root' % sample)
    t = f.Get('mfvMiniTreeNtk3/t')
    l = list(detree(t, 'x0:y0', 'dist0>0.3', float))

    g = tgraph(l)
    g.SetTitle('%s;x (cm);y (cm)' % sample)
    g.SetMarkerSize(0.3)
    g.SetMarkerStyle(20)
    g.Draw('AP')
    g.GetXaxis().SetLimits(-2.5, 2.5)
    g.GetYaxis().SetRangeUser(-2.5, 2.5)
    g.GetYaxis().SetTitleOffset(1.2)

    sv = []
    for x,y,r,c,s,m in circles(sample):
        e = ROOT.TEllipse(x,y,r,r)
        p = tgraph([(x,y)])
        sv.append((e,p))

        e.SetLineColor(c)
        e.SetLineStyle(s)
        e.SetLineWidth(2)
        e.SetFillStyle(0)
        e.Draw()

        p.SetMarkerStyle(m)
        p.SetMarkerColor(c)
        p.SetMarkerSize(1)
        p.Draw('P')

    g2 = tgraph([(0,0)])
    g2.SetMarkerSize(1)
    g2.SetMarkerStyle(45)
    g2.SetMarkerColor(4)
    g2.Draw('P')

    ps.save(sample)
