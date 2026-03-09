from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

version = 'onnormdzulv30lepmumv8'
dataset = 'trackmover' + version
apply_correction = False
year = '2017p8'
for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
      for tau in [1000, ] : #[100, 300,1000, 3000, 30000] :
        for mg in [55, ] : #[15,40,55,]:
          if tau==100 and mg==40:
            continue
          if apply_correction:
            for tm in ["sim","dat"] :
              w_fn_2d_move = ""
              if tm == "sim":
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, ttbar=True, diboson=True, Lepton_data=False)
                w_fn_2d_move = "reweight_v2p4_alleta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root" % (tau, mg, year) 
              else:
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=True)
                w_fn_2d_move = "reweight_v2p4_alleta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root" % (tau, mg, year) 
              batch_tag = "2Dmovedist3movedist2jetdrllpsumpcoarse60alletaCorrection"
              w_fn_2d_kin = "reweight_v2p4_alleta_kin_sim_vetodr_tau%06ium_M%02i_2D.root" % (tau, mg) 
              correction_args = '--jet-decayweights true --w_fn_2d_kin "%s" --w_fn_2d_move "%s" --tm "%s"' % (w_fn_2d_kin, w_fn_2d_move, tm)
              w_fns = [w_fn_2d_kin, w_fn_2d_move]
              batch = 'TrackMover_StudyV2p4_AllEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_M%02i_%s' % (nl, nb, tau, mg, batch_tag)
              args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
              NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=w_fns)
          else:
            samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, ttbar=True, diboson=True, Lepton_data=True)
            #samples = [getattr(Samples, 'wjetstolnu_2j_20161')]
            batch_tag = "noCorrection"
            correction_args = "--jet-decayweights false "
            batch = 'TrackMover_StudyV2p4_AllEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_%s' % (nl, nb, tau, batch_tag)
            args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
            NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=[])
