import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer
from JMTucker.Tools.CMSSWTools import set_events_to_process

process.maxEvents.input = 100
process.options.wantSummary = True
process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau1000um_M0200/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_11_1_css.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0200/mfv_neutralino_tau1000um_M0200/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1048_1_yBl.root')
set_events_to_process(process, [(1,1048,26)])

process.TFileService.fileName = 'pileup_play.root'

add_analyzer('PileupRemovalPlay',
             pucands_src = cms.InputTag('pfPileUpPF'),
             nonpucands_src = cms.InputTag('pfNoPileUpPF'),
             pf_jets_src = cms.InputTag('ak4PFJets'),
             pat_jets_src = cms.InputTag('selectedPatJetsPF'),
             pv_src = cms.InputTag('goodOfflinePrimaryVertices'),
             ltmm_src = cms.InputTag('mfvTrackMatches'),
             pt_cut = cms.double(0),
             verbose = cms.bool(True),
             )

process.PileupRemovalPlayNoZCheck = process.PileupRemovalPlay.clone(pucands_src = 'pfPileUpNoClosestZVertexPF',
                                                                    nonpucands_src = 'pfNoPileUpNoClosestZVertexPF')
process.PileupRemovalPlayPt5 = process.PileupRemovalPlay.clone(pt_cut = 5)
process.PileupRemovalPlayNoZCheckPt5 = process.PileupRemovalPlayNoZCheck.clone(pt_cut = 5)
#process.pPileupRemovalPlay *= process.PileupRemovalPlayNoZCheck * process.PileupRemovalPlayPt5 * process.PileupRemovalPlayNoZCheckPt5

process.load('JMTucker.MFVNeutralino.RedoPURemoval_cff')
process.pPileupRemovalPlay.replace(process.PileupRemovalPlay, process.mfvRedoPURemoval * process.PileupRemovalPlay)

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
