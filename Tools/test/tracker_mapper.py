import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

import JMTucker.Tools.SampleFiles as sf
sf.set_process(process, 'qcdht2000', 'main', 1)
process.TFileService.fileName = 'tracker_mapper.root'

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('generalTracks'),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                                       pileup_weights = cms.vdouble(*([1]*100)),
                                       )

process.p = cms.Path(process.triggerFilter * process.TrackerMapper)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    for s in Samples.ttbar_samples + Samples.qcd_samples:
        s.events_per = 500000
    for s in Samples.data_samples:
        s.json = '../../MFVNeutralino/test/ana_all.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('TrackerMapper',
                       job_control_from_sample = True,
                       )
    cs.submit_all(Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)
