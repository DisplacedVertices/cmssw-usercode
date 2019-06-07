import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.TrackRescaler import fcns
set_style()

batch = sys.argv[1]
eta = batch.split('tketa')[1]

ps = plot_saver(plot_dir('v0bkgsub_%s/cfrescaled' % batch), size=(600,600), log=False)

eras = fcns.eras[:]
de = eras.index('2017DE')
eras = eras[:de] + ['2017D','2017E'] + eras[de+1:]
for era in eras:
    year = era[:4]

    samples = ['background_%s' % year, 'JetHT' + era]
    fs = [ROOT.TFile(os.path.join(batch, '%s.root' % s)) for s in samples]
    hs = [f.Get('h_tracks_dxyerr_v_pt/hsig') for f in fs]
    mc, data = pfs = [h.ProfileX('%s_%s' % (s, h.GetName())) for s,h in zip(samples,hs)]

    mc.SetLineColor(2)
    data.SetLineColor(1)
    mc.nice, data.nice = year + 'MC', 'JetHT' + era

    for pf in pfs:
        pf.SetLineWidth(2)
        pf.GetYaxis().SetTitle('<dxyerr> (cm)')

    fcn = fcns(era, eta)
    fcn.SetLineWidth(2)
    fcn.SetLineStyle(10)
    fcn.SetLineColor(4)

    rp = ratios_plot('dxyerr_v_pt_%s' % era, pfs,
                     plot_saver=ps,
                     legend=(0.4,0.8,0.8,0.9),
                     x_range=(0.9,25),
                     y_range=(0, 0.011),
                     res_divide_opt={'confint': propagate_ratio, 'force_le_1': False},
                     res_fit=False,
                     res_y_title='data/MC',
                     res_y_range=(0.8,1.8),
                     res_fcns = [fcn],
                     )
