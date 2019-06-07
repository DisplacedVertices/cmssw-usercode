import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.TrackRescaler import fcns
set_style()

batch = sys.argv[1]
eta = batch.split('tketa')[1]
incl = '/uscms_data/d3/dquach/crab3dirs/TrackingTreerHistsV23mv3_eta%s' % eta

ps = plot_saver(plot_dir('v0bkgsub_%s/cfrescaled' % batch), size=(600,600), log=False)

eras = fcns.eras[:]
de = eras.index('2017DE')
eras = eras[:de] + ['2017D','2017E'] + eras[de+1:]

for era in eras:
    year = era[:4]

    samples = ['background_%s' % year, 'JetHT' + era]

    fs = [ROOT.TFile(os.path.join(batch, '%s.root' % s)) for s in samples]
    hs = [f.Get('h_tracks_dxyerr_v_pt/hsig') for f in fs]

    incl_fs = [ROOT.TFile(os.path.join(incl, '%s.root' % s)) for s in samples]
    hs += [f.Get('h_sel_tracks_dxyerr_v_pt') for f in incl_fs]

    mc, data, incl_mc, incl_data = pfs = [h.ProfileX('%s_%s_%i' % (s, h.GetName(), i)) for i,(s,h) in enumerate(zip(samples*2,hs))]

    mc.nice = year + 'MC'
    data.nice = 'JetHT' + era
    incl_mc.nice = 'inclusive ' + year + 'MC'
    incl_data.nice = 'inclusive JetHT' + era

    for pf,c in zip(pfs, [2,1,6,12]):
        pf.SetLineWidth(2)
        pf.SetLineColor(c)
        pf.GetYaxis().SetTitle('<dxyerr> (cm)')

    fcn = fcns(era, eta)
    fcn.SetLineWidth(2)
    fcn.SetLineColor(4)

    rp = ratios_plot('dxyerr_v_pt_%s' % era, pfs,
                     plot_saver=ps,
                     legend=(0.4,0.7,0.9,0.9),
                     x_range=(0.9,25),
                     y_range=(0, 0.011),
                     res_divide_opt={'confint': propagate_ratio, 'force_le_1': False},
                     res_fit=False,
                     res_y_title='data/MC',
                     res_y_range=(0.9,1.5),
                     res_fcns = [(fcn, 'prescribed rescaling')],
                     )
