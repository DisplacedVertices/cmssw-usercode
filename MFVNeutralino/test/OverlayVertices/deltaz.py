from JMTucker.MFVNeutralino.MiniTreeBase import *

ROOT.gStyle.SetOptStat('ourm')

ps = plot_saver(plot_dir('deltaz_new'), size=(600,600))

ntracks = 3
tree_path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV14_forpick_Jendontlook'

binning = (100, -0.3, 0.3), (50, -0.3, 0.3)
title = ';#Delta z (sv - pv) (cm);arb. norm.'
h_pvsvdz = ROOT.TH1F('h_pvsvdz_data', title, *binning[0]), ROOT.TH1F('h_pvsvdz_mc', title, *binning[0])
title = ';#Delta z (sv0 - sv1) (cm);arb. norm.'
h_svdz =   ROOT.TH1F('h_svdz_data',   title, *binning[1]), ROOT.TH1F('h_svdz_mc',   title, *binning[1])

for sample in bkg_samples + data_samples:
    f,t = get_f_t(sample, ntracks, tree_path)
    is_mc = sample.is_mc
    weight = sample.partial_weight_orig * ac.int_lumi_2016 * ac.scale_factor_2016 if is_mc else 1

    hn = 'h_pvsvdz_%s' % sample.name
    n = t.Draw('(z0-pvz)>>%s%r' % (hn, binning[0]), '(nvtx == 1 && ntk0 == %i) * weight * %e' % (ntracks, weight))
    print sample.name, n
    if n > 0:
        htemp = getattr(ROOT, hn)
        h_pvsvdz[is_mc].Add(htemp)
        ps.save(hn)

    hn = 'h_svdz_%s' % sample.name
    n = t.Draw('(svdz)>>%s%r' % (hn, binning[1]), '(nvtx == 2 && ntk0 == %i && ntk1 == %i) * weight * %e' % (ntracks, ntracks, weight))
    if not is_mc:
        n = 1e99
    print sample.name, n
    if n > 0:
        htemp = getattr(ROOT, hn)
        h_svdz[is_mc].Add(htemp)
        ps.save(hn)

for hs in h_pvsvdz, h_svdz:
    for i,h in enumerate(hs):
        h.SetBinErrorOption(ROOT.TH1.kPoisson)
        h.SetLineWidth(2)
        h.SetLineColor([ROOT.kBlack, ROOT.kRed][i])
        h.Scale(1/h.Integral())

h_pvsvdz[1].Draw('hist')
h_pvsvdz[0].Draw('e sames')
ps.c.Update()
for i in 0,1:
    differentiate_stat_box(h_pvsvdz[i], i, new_size=(0.3,0.3))
ps.save('pvsvdz')

fit_range = 0.2
fcn = ROOT.TF1('fcn_data', 'gaus', -fit_range, fit_range), ROOT.TF1('fcn_mc', 'gaus', -fit_range, fit_range)
for i in 0,1:
    print ['data','mc'][i]
    h_svdz[i].Fit(fcn[i], 'R')
h_svdz[1].Draw('hist')
h_svdz[0].Draw('e sames')
ps.c.Update()
for i in 0,1:
    differentiate_stat_box(h_svdz[i], i, new_size=(0.3,0.3))
ps.save('svdz')
