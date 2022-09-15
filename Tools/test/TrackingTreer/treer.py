from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import use_btag_triggers, use_MET_triggers, use_Lepton_triggers

settings = CMSSWSettings()
settings.is_mc = True

geometry_etc(process, which_global_tag(settings))
tfileservice(process, 'trackingtreer.root')
dataset = 'miniaod'
#sample_files(process, 'qcdmupt15_2017', dataset)
#sample_files(process, 'wjetstolnu_2017', dataset)
#sample_files(process, 'qcdht2000_2017', dataset)
sample_files(process, 'mfv_neu_tau001000um_M0800_2017', dataset)
cmssw_from_argv(process)

process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.NtupleFiller_cff')
process.load('JMTucker.Tools.PATTupleSelection_cfi')
process.load('JMTucker.Tools.UnpackedCandidateTracks_cfi')
process.load('JMTucker.Tools.UpdatedJets_cff')
process.load('JMTucker.Tools.WeightProducer_cfi')

process.selectedPatJets.src = 'updatedJetsMiniAOD'
process.selectedPatJets.cut = process.jtupleParams.jetCut

process.tt = cms.EDAnalyzer('TrackingTreer',
                            process.jmtNtupleFillerMiniAOD,
                            track_cut_level = cms.int32(0), # -1 = all, 0 = pt & pix & strip, 1 = 0 + min_r, 2 = 1 + nsigmadxybs
                            )

process.tt.track_ref_getter.tracks_maps_srcs = []

process.p = cms.Path(process.tt)

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
if use_btag_triggers :
    setup_event_filter(process, input_is_miniaod=True, mode='bjets OR displaced dijet veto HT novtx', event_filter_jes_mult=0)
elif use_MET_triggers :
    setup_event_filter(process, input_is_miniaod=True, mode='met only', event_filter_jes_mult=0, event_filter_require_vertex = False)
elif use_Lepton_triggers :
    setup_event_filter(process, input_is_miniaod=True, mode='leptons only', event_filter_jes_mult=0, event_filter_require_vertex = False)
   
else :
    setup_event_filter(process, input_is_miniaod=True, mode='jets only novtx', event_filter_jes_mult=0)
   # setup_event_filter(process, input_is_miniaod=True, mode='leptons only', event_filter_jes_mult=0)

ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=False, data=False, bjet=True, span_signal=True) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    elif use_MET_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=False, data=False, leptonic=False, bjet=False, splitSUSY=True, Zvv=True, met=True)
        pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    elif use_Lepton_triggers :
        samples = pick_samples(dataset, all_signal=False, qcd_lep=False, leptonic=True, met=False, diboson=False, data=False, Lepton_data=True)
        pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    else :
        samples = pick_samples(dataset, all_signal=False)
        pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())

    #samples = pick_samples(dataset, all_signal=True)
   # set_splitting(samples, dataset, 'default', data_json=json_path('ana_2017p8.json'), limit_ttbar=False)
    set_splitting(samples, dataset, 'default', data_json=json_path('ana_SingleLept_2017_10pc.json'), limit_ttbar=False)

    ms = MetaSubmitter('TrackingTreerULV1_Lepm_wsellep', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
