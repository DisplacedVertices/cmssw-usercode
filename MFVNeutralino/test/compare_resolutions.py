#!/usr/bin/env python

from DVCode.Tools.ROOTTools import *
set_style()
import DVCode.Tools.Samples as Samples
samples = [Samples.mfv_neu_tau01000um_M0800]
histNames = ['h_lsp0nmatch_lsp1nmatch', 'h_vtxmatch_vtxtotal', 'h_dx', 'h_dy', 'h_dz', 'h_dist2d', 'h_dist3d', 'h_s_dx_dy', 'h_s_dx_dz', 'h_s_dy_dz', 'h_pull_dz', 'h_pull_dist2d', 'h_rp_rmass', 'h_fp_fmass', 'h_s_p_mass', 'h_rp_renergy', 'h_fp_fenergy', 'h_s_p_energy', 'h_r_p', 'h_f_p', 'h_s_p', 'h_r_pt', 'h_f_pt', 'h_s_pt', 'h_r_eta', 'h_s_eta', 'h_r_phi', 'h_s_phi', 'h_r_mass', 'h_f_mass', 'h_s_mass', 'h_r_msptm', 'h_f_msptm', 'h_s_msptm', 'h_r_msptm_mass', 'h_f_msptm_mass', 'h_s_msptm_mass', 'h_r_energy', 'h_f_energy', 'h_s_energy', 'h_r_px', 'h_s_px', 'h_r_py', 'h_s_py', 'h_r_pz', 'h_s_pz', 'h_r_rapidity', 'h_s_rapidity', 'h_r_theta', 'h_s_theta', 'h_r_betagamma', 'h_s_betagamma', 'h_r_avgbetagammalab', 'h_s_avgbetagammalab', 'h_r_avgbetagammacmz', 'h_s_avgbetagammacmz']

for sample in samples:
    ps = plot_saver('~/plots/MFVResolutions/ntracks5_3dcut_84um/FullSelByDistCut/%s' % sample.name, size=(700,700), root=False)
    file = ROOT.TFile('resolutions/ntracks5_final/%s.root' % sample.name)
    print sample.name
    print '%20s%40s%40s%40s' % ('', 'tracks only', 'jets only', 'tracks+jets')
    print '%20s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s' % ('', 'mean', 'rms', 'underflow', 'overflow', 'mean', 'rms', 'underflow', 'overflow', 'mean', 'rms', 'underflow', 'overflow')
    for name in histNames:
        trks = file.mfvResolutionsFullSelByDistCutTrks.Get(name)
        jets = file.mfvResolutionsFullSelByDistCutJets.Get(name)
        trksjets = file.mfvResolutionsFullSelByDistCutTrksJets.Get(name)
        hists = [trks, jets, trksjets]
        names = ['trks', 'jets', 'trksjets']
        colors = [ROOT.kRed, ROOT.kBlue, ROOT.kViolet]
        if name.startswith('h_d') or name.startswith('h_pull_') or name.startswith('h_r_') or name.startswith('h_f_'):
            draw_in_order((hists, 'hist'), sames=True)
            ps.c.Update()
            scale = 1
            if name.startswith('h_d'):
                 scale = 10000
            print '%20s' % name,
            for i,hist in enumerate(hists):
                 hist.SetLineColor(colors[i])
                 hist.SetName(names[i])
                 differentiate_stat_box(hist, movement=i, new_size=(0.25,0.25))
                 integral = hist.Integral()
                 if integral != 0:
                     print '%10.1f%10.1f%10.1f%10.1f' % (scale*hist.GetMean(), scale*hist.GetRMS(), hist.GetBinContent(0)/integral, hist.GetBinContent(hist.GetNbinsX()+1)/integral),
                 else:
                     print '%10.1f%10.1f%10.1f%10.1f' % (scale*hist.GetMean(), scale*hist.GetRMS(), hist.GetBinContent(0), hist.GetBinContent(hist.GetNbinsX()+1)),
            print
            ps.save(name)
        elif name.startswith('h_s') or name.startswith('h_r') or name.startswith('h_f'):
            for i,hist in enumerate(hists):
                hist.Draw('colz')
                ps.c.Update()
#                differentiate_stat_box(hist, movement=(1,0))
                hist.SetStats(0)
                ps.save('%s_%s' %(name, names[i]), logz=True)
        else:
            trks.Draw('colz')
            ps.c.Update()
            differentiate_stat_box(trks, movement=(1,0))
            ps.save(name, logz=True)
    print
