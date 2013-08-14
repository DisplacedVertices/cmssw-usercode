import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer

process.maxEvents.input = 100
#process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau9900um_M0400/jtuple_pileupremovalstudiesv6/66e8ed2d65a6b86d5a5bb40c50df93ea/aodpat_1_1_1oX.root']
#process.source.fileNames = ['file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/pat.root']
#process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root')
process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau9900um_M0400/jtuple_pileupremovalstudies_v6/5c257295836d18fbf020b73449ad9b5f/pat_1_1_luH.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_254_2_JTs.root','/store/user/tucker/mfv_neutralino_tau9900um_M0400/mfv_neutralino_tau9900um_M0400/3c4ccd1d95a3d8658f6b5a18424712b3/aodpat_255_1_nvB.root')
process.TFileService.fileName = 'pileup_play.root'

add_analyzer('PileupRemovalPlay',
             pucands_src = cms.InputTag('pfPileUpPF'),
             nonpucands_src = cms.InputTag('pfNoPileUpPF'),
             pv_src = cms.InputTag('goodOfflinePrimaryVertices'),
             ltmm_src = cms.InputTag('mfvTrackMatches'),
             pt_cut = cms.double(0),
             )

process.PileupRemovalPlayNoZCheck = process.PileupRemovalPlay.clone(pucands_src = 'pfPileUpNoClosestZVertexPF',
                                                                    nonpucands_src = 'pfNoPileUpNoClosestZVertexPF')
process.PileupRemovalPlayPt5 = process.PileupRemovalPlay.clone(pt_cut = 5)
process.PileupRemovalPlayNoZCheckPt5 = process.PileupRemovalPlayNoZCheck.clone(pt_cut = 5)
process.pPileupRemovalPlay *= process.PileupRemovalPlayNoZCheck * process.PileupRemovalPlayPt5 * process.PileupRemovalPlayNoZCheckPt5

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import *

    mfv_neutralino_tau0000um_M0400.ana_dataset_override = '/mfv_neutralino_tau0000um_M0400/jchu-jtuple_pileupremovalstudies_v6-5c257295836d18fbf020b73449ad9b5f/USER'
    mfv_neutralino_tau0100um_M0400.ana_dataset_override = '/mfv_neutralino_tau0100um_M0400/jchu-jtuple_pileupremovalstudies_v6-5c257295836d18fbf020b73449ad9b5f/USER'
    mfv_neutralino_tau1000um_M0400.ana_dataset_override = '/mfv_neutralino_tau1000um_M0400/jchu-jtuple_pileupremovalstudies_v6-5c257295836d18fbf020b73449ad9b5f/USER'
    mfv_neutralino_tau1000um_M1000.ana_dataset_override = '/mfv_neutralino_tau1000um_M1000/jchu-jtuple_pileupremovalstudies_v6-5c257295836d18fbf020b73449ad9b5f/USER'
    mfv_neutralino_tau9900um_M0400.ana_dataset_override = '/mfv_neutralino_tau9900um_M0400/jchu-jtuple_pileupremovalstudies_v6-5c257295836d18fbf020b73449ad9b5f/USER'
 
    samples = [mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau1000um_M1000, mfv_neutralino_tau9900um_M0400]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('PileupPlay',
                       total_number_of_events = 99250,
                       events_per_job = 20000,
                       use_ana_dataset = True,
                       use_parent = True,
                       )
    cs.submit_all(samples)
