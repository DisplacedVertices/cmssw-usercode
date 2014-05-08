import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/002A756C-FA15-E211-9FA6-485B39800B75.root']
process.TFileService.fileName = 'effcheck.root'

process.p = cms.EDAnalyzer('EffCheck',
                           track_src = cms.InputTag('generalTracks'),
                           )
process.p0 = cms.Path(process.p)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import ttbarhadronic

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('EffCheck',
                       total_number_of_events = -1,
                       events_per_job = 10000,
                       )
    cs.submit_all([ttbarhadronic])
