import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev16'
sample_files(process, 'mfv_neu_tau01000um_M0800', dataset, -1)
process.TFileService.fileName = 'resolutions.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                which_mom = cms.int32(0),
                                max_dr = cms.double(-1),
                                max_dist = cms.double(0.0084),
                                max_dist_2d = cms.double(1e9),
                                max_dist_2d_square = cms.double(1e9)
                                )

process.p = cms.Path(process.mfvSelectedVerticesSeq)

process.mfvResolutionsByDistCutTrks = mfvResolutions.clone()
process.p *= process.mfvResolutionsByDistCutTrks

process.mfvResolutionsByDistCutJets = mfvResolutions.clone(which_mom = 1)
process.p *= process.mfvResolutionsByDistCutJets

process.mfvResolutionsByDistCutTrksJets = mfvResolutions.clone(which_mom = 2)
process.p *= process.mfvResolutionsByDistCutTrksJets

process.p *= process.mfvAnalysisCuts

process.mfvResolutionsFullSelByDistCutTrks = mfvResolutions.clone()
process.p *= process.mfvResolutionsFullSelByDistCutTrks

process.mfvResolutionsFullSelByDistCutJets = mfvResolutions.clone(which_mom = 1)
process.p *= process.mfvResolutionsFullSelByDistCutJets

process.mfvResolutionsFullSelByDistCutTrksJets = mfvResolutions.clone(which_mom = 2)
process.p *= process.mfvResolutionsFullSelByDistCutTrksJets


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.mfv_signal_samples + Samples.mfv_ddbar_samples

    for sample in samples:
        sample.datasets[dataset].files_per = 1000

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('ResolutionsV16', dataset = dataset)
    cs.submit_all(samples)

elif __name__ == '__main__' and hasattr(sys, 'argv') and 'derivecut' in sys.argv:
    from math import pi
    from JMTucker.Tools.ROOTTools import *
    set_style()
    ps = plot_saver(plot_dir('resolutionsv14'), size=(800,500))
    for fn in sys.argv[1:]:
        if fn.endswith('.root'):
            print fn
            f = ROOT.TFile(fn)
            h = f.Get('mfvResolutionsFullSelByDistCutTrksJets/h_dist3d')
            h.Draw()
            ps.save(os.path.basename(fn).replace('.root', ''))
            integ = lambda a,b: get_integral(h, a, b, include_last_bin=False)
            a,b = 0.018, 0.02
            bkg_est, e_bkg_est = integ(a,b)
            vol_bkg = 4*pi/3 * (b**3 - a**3)
            vol_tot = 4*pi/3 * b**3
            n_tot, e_n_tot = integ(0,b)
            bkg_tot   = bkg_est   * vol_tot / vol_bkg
            e_bkg_tot = e_bkg_est * vol_tot / vol_bkg
            sig_tot   = n_tot - bkg_tot
            e_sig_tot = (e_n_tot**2 + e_bkg_tot**2)**0.5
            print 'bkg %.1f +- %.1f density in %.3f-%.3f cm = %.2e +- %.2e / cm^3' % (bkg_est, e_bkg_est, a,b, bkg_est/vol_bkg, e_bkg_est/vol_bkg)
            print 'n tot %.1f +- %.1f bkg est %.1f +- %.1f -> sig_tot %.1f +- %.1f' % (n_tot, e_n_tot, bkg_tot, e_bkg_tot, sig_tot, e_sig_tot)
            prev = None
            for ibin in xrange(1, h.GetNbinsX()+1):
                c = h.GetBinLowEdge(ibin+1)
                n, e_n = integ(0,c)
                vf = 4*pi/3 * c**3 / vol_bkg
                bkg, e_bkg = bkg_est * vf, e_bkg_est * vf
                sig, e_sig = n - bkg, (e_n**2 + e_bkg**2)**0.5
                frac_sig = sig/sig_tot
                e_frac_sig = frac_sig * ((e_sig/sig)**2 + (e_sig_tot/sig_tot)**2)
                if frac_sig > 0.95:
                    print 'ibin %3i high %6.4f integ %7.1f +- %7.1f bkg %7.1f +- %7.1f subtr %7.1f +- %7.1f frac sig_tot %.3f +- %.3f' % (ibin, c, n, e_n, bkg, e_bkg, sig, e_sig, frac_sig, e_frac_sig)
                    pc, pf, epf = prev
                    z = (frac_sig - pf)/(c-pc)
                    extrap = (0.95 - frac_sig)/z + c
                    e_extrap = frac_sig/z * ((e_frac_sig/frac_sig)**2 + (e_frac_sig**2 + epf**2)/z**2)**0.5
                    print '  -> %0.5f +- %0.5f' % (extrap, e_extrap)
                    break
                prev = c, frac_sig, e_frac_sig
            print
