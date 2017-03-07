import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

import JMTucker.Tools.SampleFiles as sf
sf.set_process(process, 'testqcdht2000', 'main', 4)
process.TFileService.fileName = 'tracker_mapper.root'

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('generalTracks'),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                                       use_duplicateMerge = cms.int32(-1),
                                       pileup_weights = cms.vdouble(*([1]*100)),
                                       )

process.tmNoDuplicateMerge = process.TrackerMapper.clone(use_duplicateMerge = 0)
process.tmDuplicateMerge = process.TrackerMapper.clone(use_duplicateMerge = 1)

process.p = cms.Path(process.triggerFilter * process.TrackerMapper * process.tmNoDuplicateMerge * process.tmDuplicateMerge)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    samples = Samples.my_qcd_test_samples[1:2]
    for s in samples:
        s.files_per = 10

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('TrackerMapper_testqcdht2000_15_v4')
    ms.submit(samples)
