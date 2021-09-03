from DVCode.MFVNeutralino.MiniTreeBase import *

ps = plot_saver('plots/duh')

int_lumi = 26000.
min_ntracks = 3
tree_path = 'trees'

nbins = 6
h_dphi = ROOT.TH1F('h_dphi', '', nbins, 0, 3.15)
#h_dphi.SetStats(0)


for sample in bkg_samples:
    f,t = get_f_t(sample, min_ntracks, tree_path)
    weight = sample.partial_weight_orig * int_lumi
    hn = 'h_dphi_%s' % sample.name
    print sample.name, t.Draw('svdphi>>%s(%i,-3.15,3.15)' % (hn,nbins), '(nvtx >= 2 && min_ntracks_ok) * weight * %e' % weight)
    htemp = getattr(ROOT, hn)
    h_dphi.Add(htemp)

h_dphi.Fit('pol2')
ps.save('dphi', log=False)

