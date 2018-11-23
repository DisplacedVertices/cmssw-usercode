import sys, os
from pprint import pprint
from JMTucker.Tools.ROOTTools import *
from efficiencies import efficiencies as effs

set_style()
ps = plot_saver(plot_dir('TrackMover_V21mV2_effs'), size=(600,600), log=False)

def p(name, title, data, mc):
    print name
    data, mc = tgraph(data), tgraph(mc)
    data.SetLineWidth(2)
    data.SetMarkerStyle(20)
    data.SetMarkerSize(0.8)
    data.SetLineColor(ROOT.kBlack)
    mc.SetFillStyle(3001)
    mc.SetMarkerStyle(24)
    mc.SetMarkerSize(0.8)
    mc.SetMarkerColor(2)
    mc.SetLineColor(2)
    mc.SetFillColor(2)
    mc.Draw('APE2')
    data.Draw('P')
    for g in data,mc:
        g.GetYaxis().SetRangeUser(0,1.01)
        g.SetTitle(title)
    ps.save(name)

for cutset in 'nocuts', 'ntracks', 'all':
    for tau in 100,300,1000,10000,30000:
        for njets in 2,3:
            for nbjets in 0,1,2:
                name = '%s_tau%06ium_%i%i' % (cutset, tau, njets, nbjets)
                title = '%s, #tau = %s, n_{l} = %i, n_{b} = %i;nsigmadxy cut;efficiency' % (cutset, {100:'100 #mum', 300:'300 #mum', 1000:'1 mm', 10000:'10 mm', 30000:'30 mm'}[tau], njets, nbjets)
                nsigs = [4.]
                p(name, title,
                  [(nsig,) + effs(cutset=cutset, nsigmadxy=nsig, tau=tau, njets=njets, nbjets=nbjets, mc=False).eff for nsig in nsigs],
                  [(nsig,) + effs(cutset=cutset, nsigmadxy=nsig, tau=tau, njets=njets, nbjets=nbjets, mc=True).eff for nsig in nsigs],
                  )
