import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/000DE054-260E-E211-A375-00266CF9B9F0.root']
process.TFileService.fileName = 'mc_pileup.root'

process.MCPileupDist = cms.EDAnalyzer('PileupDist', binning = cms.vdouble(100, 0, 100))
process.MCPileupDistQuadJet50 = process.MCPileupDist.clone()

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.triggerFilter = hltHighLevel.clone()
process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
process.triggerFilter.andOr = True # = OR

process.p = cms.Path(process.MCPileupDist * process.triggerFilter * process.MCPileupDistQuadJet50)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples 
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    cs = CRABSubmitter('PileupDist',
                       total_number_of_events = -1,
                       events_per_job = 500000,
                       )
    cs.submit_all([Samples.qcdht1000, Samples.mfv_neutralino_tau1000um_M0400])
