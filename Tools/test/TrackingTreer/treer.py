from JMTucker.Tools.BasicAnalyzer_cfg import *

settings = CMSSWSettings()
settings.is_mc = True

max_events(process, 1000)
report_every(process, 1000000)
geometry_etc(process, which_global_tag(settings))
tfileservice(process, 'trackingtreer.root')
sample_files(process, 'qcdht2000_2017', 'miniaod')
file_event_from_argv(process)
#want_summary(process)

process.load('JMTucker.MFVNeutralino.UnpackedCandidateTracks_cfi')
process.load('JMTucker.Tools.MCStatProducer_cff')

process.tt = cms.EDAnalyzer('TrackingTreer',
                            input_is_miniaod = cms.bool(True),
                            pileup_info_src = cms.InputTag('slimmedAddPileupInfo'),
                            beamspot_src = cms.InputTag('offlineBeamSpot'),
                            primary_vertices_src = cms.InputTag('offlineSlimmedPrimaryVertices'),
                            tracks_src = cms.InputTag('mfvUnpackedCandidateTracks'),
                            assert_diag_cov = cms.bool(True),
                            track_sel = cms.bool(True),
                            )

process.p = cms.Path(process.mfvUnpackedCandidateTracks * process.tt)

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
jetsOnly = setup_event_filter(process,
                              path_name = 'p',
                              trigger_filter = 'jets only',
                              event_filter = 'jets only',
                              event_filter_jes_mult = 0,
                              event_filter_require_vertex = False,
                              input_is_miniaod = True)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.Year import year

    if year == 2017:
        samples = Samples.qcd_samples_2017 + Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.qcd_samples_2018 + Samples.data_samples_2018

    set_splitting(samples, 'miniaod', 'default', json_path('ana_2017p8_1pc.json'), 16)

    ms = MetaSubmitter('TrackingTreerV2', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
