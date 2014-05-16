import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/002A756C-FA15-E211-9FA6-485B39800B75.root']
process.TFileService.fileName = 'tracker_mapper.root'

#process.source.fileNames = ['/store/user/tucker/RelValSingleMuPt1000_CMSSW_5_3_6-START53_V14-v2_GEN-SIM-RECO.7C1AEF1C-FF29-E211-BA60-003048678B20.root']

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('generalTracks'),
                                       use_rechits = cms.bool(False)
                                       )
process.p = cms.Path(process.TrackerMapper)

if 1:
    process.source.fileNames = ['file:/uscms/home/tucker/scratch/reco_1_2_L1S.root']
    process.TrackerMapper.use_rechits = True

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    for s in Samples.data_samples:
        s.json = 'ana_5pc.json'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('TrackerMapper',
                       total_number_of_events = -1,
                       events_per_job = 500000,
                       )
    cs.submit_all([Samples.myttbarpydesignnoputkex])
