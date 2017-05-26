from functools import partial
from JMTucker.MFVNeutralino.MiniTreeBase import *

set_style()
ps = plot_saver(plot_dir('hip_simulation_templates'), size=(600,600))
ratios_plot = partial(ratios_plot,
                      plot_saver = ps,
                      res_y_range = (0, 0.5),
                      legend = (0.507, 0.855, 0.890, 0.963),
                      draw_normalized = True)

tree_path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15'

def doit(sample, nice, binning, yunit, include_retest=False):
    hists = []
    kinds = ['', 'retest', 'hip1p0', 'hip1p0_mit']
    nices = [nice, 'private simulation', '+ hip simulation', '+ hip simulation + mitigation']
    colors = [ROOT.kBlack, ROOT.kGreen+2, ROOT.kRed, ROOT.kBlue]
    for i, kind in enumerate(kinds):
        if not include_retest and kind == 'retest':
            continue
        ex = '_' if kind else ''
        name = sample + ex + kind
        fn = os.path.join(tree_path, name + '.root')
        f, t = get_f_t(fn, min_ntracks=5)
        t.Draw('svdist>>%s%s' % (name,binning), 'nvtx >= 2')
        h = getattr(ROOT,name)
        hists.append(h)

        h.Sumw2()
        h.SetName('official' if not kind else kind)
        h.SetTitle(';d_{VV} (cm);events/%s' % yunit)
        h.SetLineColor(colors[i])
        h.SetLineWidth(2)
        h.SetStats(0)
        h.nice = nices[i]

    ratios_plot(sample, hists)

doit('mfv_neu_tau00300um_M0400', 'multijet, #tau = 300 #mum, M = 400 GeV', (20,0,1), '500 #mum')
doit('mfv_neu_tau01000um_M0400', 'multijet, #tau = 1 mm, M = 400 GeV',     (20,0,1), '500 #mum')
doit('mfv_neu_tau10000um_M0400', 'multijet, #tau = 10 mm, M = 400 GeV',    (20,0,4), '2 mm')
doit('mfv_neu_tau00300um_M0800', 'multijet, #tau = 300 #mum, M = 800 GeV', (80,0,1), '125 #mum')
doit('mfv_neu_tau01000um_M0800', 'multijet, #tau = 1 mm, M = 800 GeV',     (80,0,1), '125 #mum')
doit('mfv_neu_tau10000um_M0800', 'multijet, #tau = 10 mm, M = 800 GeV',    (80,0,4), '500 #mum')
