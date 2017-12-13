#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
set_style()
import JMTucker.Tools.Samples as Samples
samples = [Samples.mfv_neu_tau01000um_M0800]

for sample in samples:
    ps = plot_saver('plots/theorist_recipe/mfvTheoristRecipeNoCuts/%s' % sample.name, size=(700,700), root=False)
    f = ROOT.TFile('~/crabdirs/TheoristRecipeV9/%s.root' % sample.name)
    print sample.name

    for name in ['p', 'pt', 'pz', 'E', 'Et']:
        h1 = f.Get('mfvTheoristRecipeNoCuts/h_gen_lsp_sum%s' % name)
        h2 = f.Get('mfvTheoristRecipeNoCuts/h_gen_lsp_net%s' % name)
        hists = [h1, h2]
        names = ['sum', 'net']
        colors = [ROOT.kRed, ROOT.kBlue]
        title = ';%s / %s;events' % (h1.GetXaxis().GetTitle(), h2.GetXaxis().GetTitle())
        draw_in_order((hists, 'hist'), sames=True)
        ps.c.Update()
        print name
        for i,hist in enumerate(hists):
            hist.SetName(names[i])
            hist.SetLineColor(colors[i])
            hist.SetTitle(title)
            differentiate_stat_box(hist, movement=i, new_size=(0.25,0.25))
        ps.save(name)

    xtitles = ['number of jets', 'H_{T} (GeV)', 'H_{T}(40) (GeV)']
    for j,name in enumerate(['njets', 'ht', 'ht40']):
        h1 = f.Get('mfvTheoristRecipeNoCuts/h_gen_parton_%s' % name)
        h2 = f.Get('mfvTheoristRecipeNoCuts/h_gen_parton_accepted_%s' % name)
        h3 = f.Get('mfvTheoristRecipeNoCuts/h_gen_quark_%s' % name)
        h4 = f.Get('mfvTheoristRecipeNoCuts/h_gen_%s' % name)
        hists = [h1, h2, h3, h4]
        names = ['partons', 'accepted partons', 'quarks', 'accepted quarks']
        colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta]
        draw_in_order((hists, 'hist'), sames=True)
        ps.c.Update()
        print name
        for i,hist in enumerate(hists):
            hist.SetName(names[i])
            hist.SetLineColor(colors[i])
            hist.SetTitle(';%s;events' % xtitles[j])
            differentiate_stat_box(hist, movement=i, new_size=(0.2,0.2))
        ps.save('compare_%s' % name)

    for j,name in enumerate(['njets', 'jet_pt', 'jet_pt40', 'ht40', 'jet_eta', 'jet_phi', 'dxy', 'match_dxy', 'ntracks', 'match_ntracks', 'dbv', 'match_dbv', 'dvv']):
        rec = f.Get('mfvTheoristRecipeNoCuts/h_rec_%s' % name)
        gen = f.Get('mfvTheoristRecipeNoCuts/h_gen_%s' % name)
        hists = [rec, gen]
        names = ['rec', 'gen']
        colors = [ROOT.kRed, ROOT.kBlue]
        title = ';%s / %s;%s / %s' % (rec.GetXaxis().GetTitle(), gen.GetXaxis().GetTitle(), rec.GetYaxis().GetTitle(), gen.GetYaxis().GetTitle())
        draw_in_order((hists, 'hist'), sames=True)
        ps.c.Update()
        print name
        for i,hist in enumerate(hists):
            hist.SetName(names[i])
            hist.SetLineColor(colors[i])
            hist.SetTitle(title)
            differentiate_stat_box(hist, movement=i, new_size=(0.25,0.25))
        ps.save(name)

        if j < 4:
            rec_v_gen = f.Get('mfvTheoristRecipeNoCuts/h_rec_v_gen_%s' % name)
            rec_v_gen.Draw('colz')
            ps.c.Update()
            differentiate_stat_box(rec_v_gen, new_size=(0.25,0.25))
            ps.save('rec_v_gen_%s' % name)

            rec_v_gen_pfx = rec_v_gen.ProfileX()
            rec_v_gen_pfx.GetYaxis().SetTitle('mean %s' % rec_v_gen.GetYaxis().GetTitle())
            rec_v_gen_pfx.Draw()
            rec_v_gen_pfx.Fit('pol1')
            ps.c.Update()
            differentiate_stat_box(rec_v_gen_pfx, new_size=(0.25,0.25))
            ps.save('rec_v_gen_pfx_%s' % name)
