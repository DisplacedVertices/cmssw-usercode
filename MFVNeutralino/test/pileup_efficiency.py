import os

from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)
set_style()

version = 'V23m'
ps = plot_saver(plot_dir('pileup_efficiency_%s' % version), size=(600,600), pdf=True)

bins = to_array([0,10,13,15,65])
nbins = len(bins)-1

ntks = [
    (3, 'Ntk3'),
    (4, 'Ntk4'),
    (5, ''),
]

hists = [
    ('onevtx', 'mfvEventHistosOnlyOneVtx'),
    ('twovtx', 'mfvEventHistosFullSel'),
    ('sigreg', 'mfvEventHistosSigReg')
    ]

for sample in ['background_2017', 'mfv_neu_tau000100um_M0800_2017', 'mfv_neu_tau000300um_M0800_2017', 'mfv_neu_tau001000um_M0800_2017', 'mfv_neu_tau010000um_M0800_2017']:
    print sample
    f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/Histos%s/%s.root' % (version,sample))
    presel = f.Get('mfvEventHistosPreSel/h_npu').Clone('presel')
    presel.Rebin(5)
    presel.GetXaxis().SetRangeUser(0,70)
    presel.Draw()
    ps.save('presel_' + sample, log=False)

    for ntk, s2 in ntks:
        print '%i-track' % ntk
        hs = [(n, f.Get(s2 + s + '/h_npu').Clone(n)) for n,s in hists]

        for n, h in hs:
            h.Rebin(5)
            h.GetXaxis().SetRangeUser(0,70)
            h.Draw()
            ps.save(n + '_ntk%i_' % ntk + sample, log=False)

            g = histogram_divide(h, presel, use_effective=True)
            g.SetTitle('%s-track %s;true nPU;efficiency' % (ntk,n))
            g.Draw('AP')
            fcn = ROOT.TF1('fcn', 'pol1', 10, 50)
            g.Fit(fcn, 'QR')
            g.GetYaxis().SetRangeUser(0, fcn.GetParameter(0)*5)
            if fcn.GetParameter(0) > 0:
                print n, fcn.GetParameter(1) / fcn.GetParameter(0) * 4
            ps.save(n + '_ntk%i_eff_' % ntk + sample, log=False)
    print
