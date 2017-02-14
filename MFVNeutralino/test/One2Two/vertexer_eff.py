from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../plots/bkgest/vertexer_eff', size=(700,700), log=False, root=False)

f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/VertexerHistosV10/background.root')
fh = ROOT.TFile('eff.root', 'recreate')

for maxtk in ['maxtk3', 'maxtk4', 'maxtk5']:
    h_merge = f.Get('mfvVertices/h_merge_d2d_%s' % maxtk)
    h_pairs = f.Get('mfvVertices/h_pairs_d2d_%s' % maxtk)
    h_erase = f.Get('mfvVertices/h_erase_d2d_%s' % maxtk)

    h_merge.Rebin(10)
    h_pairs.Rebin(10)
    h_erase.Rebin(10)

    h_add_eff = h_merge.Clone('%s' % maxtk)
    h_add_eff.Add(h_erase)
    h_add_eff.Divide(h_add_eff, h_pairs, 1,1,'B')
    for i in range(1, h_add_eff.GetNbinsX()+2):
        h_add_eff.SetBinContent(i, 1-h_add_eff.GetBinContent(i))
    h_add_eff.Scale(1./h_add_eff.GetBinContent(h_add_eff.GetNbinsX()))
    h_add_eff.SetTitle('%s;d_{VV} (cm);efficiency' % maxtk)
    h_add_eff.GetYaxis().SetRangeUser(0,1.05)
    h_add_eff.SetLineColor(ROOT.kGreen+2)
    h_add_eff.SetStats(0)
    h_add_eff.Draw()

    h_merge_eff = h_merge.Clone('%s_merge' % maxtk)
    h_merge_eff.Divide(h_merge_eff, h_pairs, 1,1,'B')
    for i in range(1, h_merge_eff.GetNbinsX()+2):
        h_merge_eff.SetBinContent(i, 1-h_merge_eff.GetBinContent(i))
    h_merge_eff.Scale(1./h_merge_eff.GetBinContent(h_merge_eff.GetNbinsX()))
    h_merge_eff.SetTitle('%s merge;d_{VV} (cm);efficiency' % maxtk)
    h_merge_eff.GetYaxis().SetRangeUser(0,1.05)
    h_merge_eff.SetLineColor(ROOT.kBlue)
    h_merge_eff.SetStats(0)
    h_merge_eff.Draw('sames')

    l = ROOT.TLegend(0.50,0.55,0.85,0.70)
    l.AddEntry(h_merge_eff, '1 - merge / pairs')
    l.AddEntry(h_add_eff, '1 - (merge + erase) / pairs')
    l.SetFillColor(0)
    l.Draw()

    ps.save('h_eff_%s' % maxtk)
    fh.cd()
    h_add_eff.Write()
    h_merge_eff.Write()

fh.Close()
