from JMTucker.MFVNeutralino.MiniTreeBase import *

ps = plot_saver(plot_dir('ht_nm1'), size=(600,600))

int_lumi = 38529.
binning = 50,500,3000

for nv in (2,): # 1,2:
    for ntk in 3,4,5: #,7,5:
        if nv == 1:
            if ntk == 7:
                continue
            cut = 'nvtx == 1'
        elif nv == 2:
            cut = 'nvtx >= 2'

        h_ht = ROOT.TH1D('h_ht_%i%i' % (ntk, nv), '%i-track %i-vertex events;H_{T} (GeV);events/50 GeV' % (ntk, nv), *binning)
        h_ht.SetStats(0)
        for sample in bkg_samples:
            fn = 'root://cmseos.fnal.gov//store/user/tucker/MiniNtupleV16_NoJetCuts/%s.root' % sample.name
            f,t = get_f_t(fn, ntk)
            hn = 'h_ht_%i%i_%s' % (ntk, nv, sample.name)
            weight = sample.partial_weight(f) * int_lumi
            print sample.name, t.Draw('jetht>>%s%r' % (hn, binning), '(%s) * weight * %e' % (cut, weight))
            htemp = getattr(ROOT, hn)
            h_ht.Add(htemp)
        h_ht.Draw()
        ttb = getattr(ROOT, 'h_ht_%i%i_ttbar' % (ntk, nv))
        ttb.SetLineColor(ROOT.kRed)
        ttb.Draw('same')

        leg = ROOT.TLegend(0.453, 0.702, 0.860, 0.866)
        leg.SetTextFont(42)
        leg.SetBorderSize(0)
        leg.AddEntry(h_ht, 'QCD multijet + t#bar{t}', 'LE')
        leg.AddEntry(ttb,  't#bar{t}', 'LE')
        leg.Draw()

        ps.save('ht_%i%i' % (ntk,nv))
