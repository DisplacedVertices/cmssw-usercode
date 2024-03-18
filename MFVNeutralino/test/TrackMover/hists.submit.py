from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

version = 'onnormdzulv30bmv6'
dataset = 'trackmover' + version
apply_correction = False
year = 2017
#samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, met=True, diboson=True, Lepton_data=False)
#samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=False, diboson=False, Lepton_data=True)
samples = Samples.DisplacedJet_data_samples_2017 + Samples.BTagCSV_data_samples_2017 + Samples.qcd_samples_2017 + [Samples.ttbar_2017,] 
for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
      if apply_correction:
        for tau in 1000, :
          for mg in 55,:
            #batch_tag = "1DcosthetaCorrection"
            #batch_tag = "2Djetcosthetajet1sumpCorrection"
            #batch_tag = "2Djetdrjet1sumpCorrection"
            #batch_tag = "2Djetdrmovedist3Correction"
            batch_tag = "2Djetdrjet1sump1Dmovedist3Correction"
            #batch_tag = "2Djetcosthetajet1sump1Dmovedist3Correction"
            #batch_tag = "1Djetdr1Djet1sump1Dmovedist3Correction"
            #batch_tag = "1Dnseedtks1D2logm1Dmovedist3Correction"
            w_fn_2d = "reweight_tau%imm_M%02i_%i_2D.root" % (tau/1000, mg, year)
            w_fn_1d = "reweight_tau%imm_M%02i_%i_1D.root" % (tau/1000, mg, year)
            correction_args = '--jet-decayweights true --w_fn_2d "%s" --w_fn_1d "%s" ' % (w_fn_2d, w_fn_1d)
            w_fns = [w_fn_2d, w_fn_1d]
            batch = 'TrackMoverJetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_%s' % (nl, nb, tau, batch_tag)
            args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) #FIXME
            NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=w_fns)
      else:
        for tau in 1000, : # 100, 300, 1000, 10000, 30000, 100000,
          batch_tag = "noCorrection"
          correction_args = "--jet-decayweights false "
          batch = 'TrackMoverJetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_%s' % (nl, nb, tau, batch_tag)
          args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) #FIXME
          NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=[])
