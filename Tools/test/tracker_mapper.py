import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

settings = CMSSWSettings()
settings.is_mc = True
settings.cross = ''

max_events(process, 1000)
report_every(process, 1000000)
geometry_etc(process, which_global_tag(settings))
tfileservice(process, 'tracker_mapper.root')
sample_files(process, 'qcdht2000_2017', 'miniaod')
file_event_from_argv(process)
#want_summary(process)

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('JMTucker.Tools.GenParticleFilter_cfi')
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.UnpackedCandidateTracks_cfi')
process.load('JMTucker.Tools.WeightProducer_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
process.goodOfflinePrimaryVertices.filter = True

process.jmtGenParticleFilter.gen_particles_src = 'prunedGenParticles'

process.lightFlavor = process.jmtGenParticleFilter.clone(max_flavor_code = 0)
process.heavyFlavor = process.jmtGenParticleFilter.clone(min_flavor_code = 1)
process.bFlavor = process.jmtGenParticleFilter.clone(min_flavor_code = 2)
process.displacedGenPV = process.jmtGenParticleFilter.clone(min_pvrho = 0.0036)

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('jmtUnpackedCandidateTracks'),
                                       heavy_flavor_src = cms.InputTag(''),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                       weight_src = cms.InputTag('jmtWeightMiniAOD'),
                                       use_duplicateMerge = cms.int32(-1),
                                       old_stlayers_cut = cms.bool(False),
                                       )

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
jetsOnly = setup_event_filter(process,
                              path_name = '',
                              trigger_filter = 'jets only',
                              event_filter = 'jets only',
                              event_filter_jes_mult = 0,
                              event_filter_require_vertex = False,
                              input_is_miniaod = True)

common = cms.Sequence(jetsOnly * process.goodOfflinePrimaryVertices * process.jmtUnpackedCandidateTracks * process.jmtWeightMiniAOD)

if False:
    process.load('JMTucker.Tools.RescaledTracks_cfi')
    process.jmtRescaledTracks.tracks_src = 'jmtUnpackedCandidateTracks'
    common *= process.jmtRescaledTracks
    process.TrackerMapper.track_src = 'jmtRescaledTracks'

process.p = cms.Path(common * process.TrackerMapper)

for name, filt in ('LightFlavor', process.lightFlavor), ('HeavyFlavor', process.heavyFlavor): #, ('BFlavor', process.bFlavor), ('DisplacedGenPV', process.displacedGenPV):
    tk = process.TrackerMapper.clone()
    if name == 'HeavyFlavor':
        tk.heavy_flavor_src = cms.InputTag('heavyFlavor', 'heavyFlavor')
    setattr(process, 'TrackerMapper%s' % name, tk)
    setattr(process, 'p%s' % name, cms.Path(common * filt * tk))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.Year import year

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.qcd_samples_2018 + Samples.data_samples_2018

    set_splitting(samples, 'miniaod', 'default', json_path('ana_2017_1pc.json'), 16)

    ms = MetaSubmitter('TrackerMapperV3', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(cross=settings.cross))
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
