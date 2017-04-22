from JMTucker.MFVNeutralino.MiniTreeBase import *

ps = plot_saver('plots/deltaz')

int_lumi = 26000.
min_ntracks = 3
tree_path = 'trees'

binning = (100, -0.3, 0.3)

h_pvsvdz = ROOT.TH1F('h_pvsvdz', '', *binning)
h_svdz = ROOT.TH1F('h_svdz', '', *binning)

for sample in bkg_samples:
    f,t = get_f_t(sample, min_ntracks, tree_path)
    weight = sample.partial_weight_orig * int_lumi

    hn = 'h_pvsvdz_%s' % sample.name
    print sample.name, t.Draw('(z0-pvz)>>%s%r' % (hn, binning), '(nvtx == 1 && ntk0 >= %i) * weight * %e' % (min_ntracks, weight))
    htemp = getattr(ROOT, hn)
    h_pvsvdz.Add(htemp)
    ps.save(hn)

    hn = 'h_svdz_%s' % sample.name
    print sample.name, t.Draw('(svdz)>>%s%r' % (hn, binning), '(nvtx == 2 && min_ntracks_ok) * weight * %e' % weight)
    htemp = getattr(ROOT, hn)
    h_svdz.Add(htemp)
    ps.save(hn)

h_pvsvdz.Draw()
ps.save('pvsvdz')

fcn = ROOT.TF1('fcn', 'gaus', -0.035, 0.035)
h_svdz.Fit(fcn, 'QR')
ps.save('svdz')
