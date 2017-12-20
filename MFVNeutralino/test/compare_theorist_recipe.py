#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
set_style()
import JMTucker.Tools.Samples as Samples
samples = [Samples.mfv_neu_tau01000um_M0800]

for sample in samples:
    ps = plot_saver('plots/theorist_recipe/mfvTheoristRecipeNoCuts/%s' % sample.name, size=(700,700), root=False)
    f = ROOT.TFile('~/crabdirs/TheoristRecipeV11/%s.root' % sample.name)
    print sample.name

    for j,name in enumerate(['njets', 'jet_pt', 'jet_eta', 'jet_phi', 'jet_pt40', 'ht40', 'dxy', 'ntracks', 'dbv', 'dvv']):
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
