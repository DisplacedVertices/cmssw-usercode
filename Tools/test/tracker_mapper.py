import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.PileupWeights import pileup_weights
from JMTucker.Tools.Year import year

cmssw_settings = CMSSWSettings()
cmssw_settings.is_mc = True

max_events(process, 1000)
report_every(process, 1000000)
geometry_etc(process, which_global_tag(cmssw_settings))
tfileservice(process, 'tracker_mapper.root')
sample_files(process, 'qcdht2000_2017', 'miniaod')
file_event_from_argv(process)

process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('JMTucker.MFVNeutralino.UnpackedCandidateTracks_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
process.goodOfflinePrimaryVertices.filter = True

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('mfvUnpackedCandidateTracks'),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                       pileup_info_src = cms.InputTag('slimmedAddPileupInfo'),
                                       use_duplicateMerge = cms.int32(-1),
                                       old_stlayers_cut = cms.bool(False),
                                       pileup_weights = cms.vdouble(*pileup_weights[year]),
                                       )

process.TrackerMapperOldStCut = process.TrackerMapper.clone(old_stlayers_cut = True)

process.p = cms.Path(process.goodOfflinePrimaryVertices * process.mfvUnpackedCandidateTracks * process.TrackerMapper * process.TrackerMapperOldStCut)

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
setup_event_filter(process, path_name='p', event_filter=True, event_filter_jes_mult=0, event_filter_require_vertex=False, input_is_miniaod=True)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.Year import year

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017

    set_splitting(samples, 'miniaod', 'default', json_path('ana_2017.json'), 50)

    ms = MetaSubmitter('TrackerMapperV1', dataset='miniaod')
    ms.common.ex = year
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(['TrackerMapper', 'TrackerMapperOldStCut']))
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
