#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
set_style()
import JMTucker.Tools.Samples as Samples
samples = Samples.mfv_signal_samples
histNames = ['h_dx', 'h_dy', 'h_dz', 'h_dist2d', 'h_dist3d', 'h_r_p', 'h_f_p', 'h_r_pt', 'h_f_pt', 'h_r_eta', 'h_r_phi', 'h_r_mass', 'h_f_mass', 'h_r_px', 'h_f_px', 'h_r_py', 'h_f_py', 'h_r_pz', 'h_f_pz', 'h_r_rapidity', 'h_r_theta']

for sample in samples:
    ps = plot_saver('plots/MFVResolutionsV15/%s' % sample.name, size=(700,700), root=False)
    file = ROOT.TFile('crab/MFVResolutionsV15/%s.root' % sample.name)
    print sample.name
    print '%15s%40s%40s%40s' % ('', 'tracks only', 'jets only', 'tracks+jets')
    print '%15s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s' % ('', 'mean', 'rms', 'underflow', 'overflow', 'mean', 'rms', 'underflow', 'overflow', 'mean', 'rms', 'underflow', 'overflow')
    for name in histNames:
        trks = file.mfvResolutionsByDistCutTrks.Get(name)
        jets = file.mfvResolutionsByDistCutJets.Get(name)
        trksjets = file.mfvResolutionsByDistCutTrksJets.Get(name)
        hists = [trks, jets, trksjets]
        names = ['trks', 'jets', 'trksjets']
        colors = [ROOT.kRed, ROOT.kBlue, ROOT.kViolet]
        draw_in_order((hists, 'hist'), sames=True)
        ps.c.Update()
        print '%15s' % name,
        for i,hist in enumerate(hists):
             hist.SetLineColor(colors[i])
             hist.SetName(names[i])
             differentiate_stat_box(hist, movement=i, new_size=(0.25,0.25))
             integral = hist.Integral()
             if integral != 0:
                 print '%10.1f%10.1f%10.1f%10.1f' % (hist.GetMean(), hist.GetRMS(), hist.GetBinContent(0)/integral, hist.GetBinContent(hist.GetNbinsX()+1)/integral),
             else:
                 print '%10.1f%10.1f%10.1f%10.1f' % (hist.GetMean(), hist.GetRMS(), hist.GetBinContent(0), hist.GetBinContent(hist.GetNbinsX()+1)),
        print
        ps.save(name)
    print
