from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)
set_style()

ps = plot_saver(plot_dir('pileup_efficiency_run2'), size=(600,600), pdf=True)

bins = to_array([0,10,13,15,65])
nbins = len(bins)-1

hists = [
    ('presel', 'mfvEventHistosPreSel'),
    ('onevtx', 'mfvEventHistosOnlyOneVtx'),
    ('twovtx', 'mfvEventHistos'),
    ('sigreg', 'mfvEventHistosSigReg')
    ]

xxx = [
    (3, '/uscms_data/d2/tucker/crab_dirs/HistosV10_ntk3/background.root'),
    (4, '/uscms_data/d2/tucker/crab_dirs/HistosV10_ntk4/background.root'),
    (5, '/uscms_data/d2/tucker/crab_dirs/HistosV10/background.root'),
]

for ntk, fn in xxx:
    print fn
    f = ROOT.TFile(fn)
    geth = lambda s: f.Get(s + '/h_npu')
    #hs = [(n, geth(s).Rebin(nbins, n, bins)) for n,s in hists]
    hs = [(n, geth(s).Clone(n)) for n,s in hists]

    for n, h in hs:
        exec n+'=h'
        if n != 'presel':
            h = ROOT.TGraphAsymmErrors(h, presel, 'n pois')
            h.Draw('AP')
        else:
            h.Draw()
        h.GetXaxis().SetRangeUser(0,40)
        if ntk == 4 and n == 'onevtx':
            h.GetYaxis().SetRangeUser(0,0.005)
        ps.save(n + '_ntk%i' % ntk, log=False)
