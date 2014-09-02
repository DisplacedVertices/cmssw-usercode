import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/002A756C-FA15-E211-9FA6-485B39800B75.root']
process.TFileService.fileName = 'tracker_mapper.root'

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('generalTracks'),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       use_rechits = cms.bool(False)
                                       )
process.p = cms.Path(process.TrackerMapper)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    for s in Samples.data_samples:
        s.json = '../../MFVNeutralino/test/ana_all.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('TrackerMapper',
                       job_control_from_sample = True,
                       #total_number_of_events = -1,
                       #events_per_job = 500000,
                       )
    cs.submit_all(Samples.data_samples)
