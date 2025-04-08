from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset

version = 'onnormdzulv30bmofftosspreselv8'
#version = 'onnormdzulv30lepmumv8'
dataset = 'trackmover' + version
apply_correction = True
year = '2017p8'
for nl in 3,: # 2, 3:
    for nb in 2,: # 0, 2:
      for tau in [300, 30000]: #[100, 300, 1000, 3000, 10000, 30000]: # 300] : #[100, 300,1000, 3000, 30000] :
        for mg in [800,]: #[15, 40, 55,]: # 40, 55,] : #[15,40,55,]:
          if apply_correction:
            for tm in ["sim", "dat"] :
              w_fn_2d_move = ""
              if tm == "sim":
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, ttbar=True, diboson=True, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
                if mg < 100 :
                    w_fn_2d_move = "reweight_mixeta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root" % (tau, mg, year) 
                else :
                    w_fn_2d_move = "reweight_mixeta_move_sim_vetodr_tau%06ium_M%04i_%s_2D.root" % (tau, mg, year) 
              else:
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=True, JetHT_data=True, BTagCSV_data=True, DisplacedJet_data=True)
                if mg < 100 :
                    w_fn_2d_move = "reweight_mixeta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root" % (tau, mg, year) 
                else :
                    w_fn_2d_move = "reweight_mixeta_move_dat_vetodr_tau%06ium_M%04i_%s_2D.root" % (tau, mg, year) 
              batch_tag = "2DCorrection"
              if mg < 100 :
                  w_fn_2d_kin = "reweight_all_kin_sim_vetodr_tau%06ium_M%02i_2D.root" % (tau, mg) 
              else :
                  w_fn_2d_kin = "reweight_all_kin_sim_vetodr_tau%06ium_M%04i_2D.root" % (tau, mg) 
              correction_args = '--jet-decayweights true --w_fn_2d_kin "%s" --w_fn_2d_move "%s" --tm "%s"' % (w_fn_2d_kin, w_fn_2d_move, tm)
              w_fns = [w_fn_2d_kin, w_fn_2d_move]
              batch = 'TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_M%02i_%s' % (nl, nb, tau, mg, batch_tag)
              args = '-t mfvMovedTree%i%i %s' % (nl, nb, correction_args) 
              NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=w_fns)
          else:
            samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, ttbar=True, diboson=True, Lepton_data=False, BTagCSV_data=True, DisplacedJet_data=True)
            batch_tag = "noCorrection"
            correction_args = "--jet-decayweights false "
            batch = 'TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_%s' % (nl, nb, batch_tag)
            args = '-t mfvMovedTree%i%i %s' % (nl, nb, correction_args) 
            NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=[])
