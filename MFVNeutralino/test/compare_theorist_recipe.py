#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples

set_style()
ps = plot_saver('plots/theorist_recipe/compare_theorist_recipe', size=(700,700), root=False)

samples = [Samples.mfv_neu_tau01000um_M0800, Samples.mfv_ddbar_tau01000um_M0800, Samples.mfv_bbbar_tau01000um_M0800, Samples.mfv_neuuds_tau01000um_M0800, Samples.mfv_neuudmu_tau01000um_M0800, Samples.mfv_neuude_tau01000um_M0800]

histNames = [('genJet_njets',          'mfvTheoristRecipeNoCuts/h_rec_njets',         'mfvTheoristRecipeNoCuts/h_genJet_njets'),
             ('genJet_ht40',           'mfvTheoristRecipeNoCuts/h_rec_ht40',          'mfvTheoristRecipeNoCuts/h_genJet_ht40'),
             ('parton_njets',          'mfvTheoristRecipeNoCuts/h_rec_njets',         'mfvTheoristRecipeNoCuts/h_gen_parton_njets'),
             ('parton_ht40',           'mfvTheoristRecipeNoCuts/h_rec_ht40',          'mfvTheoristRecipeNoCuts/h_gen_parton_ht40'),
             ('parton_accepted_njets', 'mfvTheoristRecipeNoCuts/h_rec_njets',         'mfvTheoristRecipeNoCuts/h_gen_parton_accepted_njets'),
             ('parton_accepted_ht40',  'mfvTheoristRecipeNoCuts/h_rec_ht40',          'mfvTheoristRecipeNoCuts/h_gen_parton_accepted_ht40'),
             ('quark_njets',           'mfvTheoristRecipeNoCuts/h_rec_njets',         'mfvTheoristRecipeNoCuts/h_gen_quark_njets'),
             ('quark_ht40',            'mfvTheoristRecipeNoCuts/h_rec_ht40',          'mfvTheoristRecipeNoCuts/h_gen_quark_ht40'),
             ('quark_accepted_njets',  'mfvTheoristRecipeNoCuts/h_rec_njets',         'mfvTheoristRecipeNoCuts/h_gen_quark_accepted_njets'),
             ('quark_accepted_ht40',   'mfvTheoristRecipeNoCuts/h_rec_ht40',          'mfvTheoristRecipeNoCuts/h_gen_quark_accepted_ht40'),
             ('dxy',                   'mfvTheoristRecipeNoCuts/h_rec_dxy',           'mfvTheoristRecipeNoCuts/h_gen_dxy'),
             ('match_dxy',             'mfvTheoristRecipeNoCuts/h_rec_match_dxy',     'mfvTheoristRecipeNoCuts/h_gen_match_dxy'),
             ('ntracks',               'mfvTheoristRecipeNoCuts/h_rec_ntracks',       'mfvTheoristRecipeNoCuts/h_gen_ntracks'),
             ('match_ntracks',         'mfvTheoristRecipeNoCuts/h_rec_match_ntracks', 'mfvTheoristRecipeNoCuts/h_gen_match_ntracks'),
             ('dbv',                   'mfvTheoristRecipeNoCuts/h_rec_dbv',           'mfvTheoristRecipeNoCuts/h_gen_dbv'),
             ('match_dbv',             'mfvTheoristRecipeNoCuts/h_rec_match_dbv',     'mfvTheoristRecipeNoCuts/h_gen_match_dbv'),
             ('dvv',                   'mfvTheoristRecipeNoCuts/h_rec_dvv',           'mfvTheoristRecipeNoCuts/h_gen_dvv'),
             ]

for sample in samples:
    f = ROOT.TFile('~/crabdirs/TheoristRecipeV42/%s.root' % sample.name)
    print sample.name

    for name,h1,h2 in histNames:
        rec = f.Get(h1)
        gen = f.Get(h2)
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
        ps.save('%s_%s' % (sample.name, name))

    h_num = f.Get('mfvTheoristRecipeBs2derr/h_gen_match_sumpt')
    h_den = f.Get('mfvTheoristRecipeGeo2ddist/h_gen_match_sumpt')
    h_num.Rebin(5)
    h_den.Rebin(5)
    h_eff = histogram_divide(h_num, h_den)
    h_eff.SetTitle('ntracks + bs2derr efficiency;%s;efficiency' % h_num.GetXaxis().GetTitle())
    h_eff.Draw('AP')
    ps.save('%s_efficiency_vs_sumpt' % sample.name)
