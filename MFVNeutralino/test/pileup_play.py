import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer

process.maxEvents.input = 100
process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau9900um_M0400/jtuple_pileupremovalstudiesv6/66e8ed2d65a6b86d5a5bb40c50df93ea/aodpat_1_1_1oX.root']
process.TFileService.fileName = 'pileup_play.root'

add_analyzer('PileupRemovalPlay',
             pucands_src = cms.InputTag('pfPileUpPF'),
             nonpucands_src = cms.InputTag('pfNoPileUpPF'),
             pv_src = cms.InputTag('goodOfflinePrimaryVertices'),
             ltmm_src = cms.InputTag('mfvTrackMatches'),
             )

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import *
    mfv_neutralino_tau9900um_M0400.ana_dataset_override = '/mfv_neutralino_tau9900um_M0400/jchu-jtuple_pileupremovalstudiesv6-66e8ed2d65a6b86d5a5bb40c50df93ea/USER'
    #samples = [mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau0010um_M0400, mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400]
    samples = [mfv_neutralino_tau9900um_M0400]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('PileupPlay',
                       total_number_of_events = 99250,
                       events_per_job = 20000,
                       )
    cs.submit_all(samples)
