import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, add_analyzer

process.maxEvents.input = 100
process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau9900um_M0400/jtuple_pfpileupv6/367f847bf22a75c5bbdb69341a18e0cb/aodpat_1_1_tJP.root']
process.TFileService.fileName = 'pileup_play.root'

add_analyzer('PileupRemovalPlay',
             pucands_src = cms.InputTag('pfPileUpPF'),
             pv_src = cms.InputTag('goodOfflinePrimaryVertices'),
             ltmm_src = cms.InputTag('mfvTrackMatches'),
             )

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400, ttbarincl, TupleOnlyMCSample
    samples = [mfv_neutralino_tau0000um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400, ttbarincl]

    mfv_neutralino_tau9900um_M0400.dataset = '/crabfake_mfv_neutralino_tau9900um_M0400_jtuple_v6_547d3313903142038335071634b26604/tucker-crabfake_mfv_neutralino_tau9900um_M0400_jtuple_v6_547d3313903142038335071634b26604-5bdce5833f35b995ab0c308220e77250/USER'
    mfv_neutralino_tau1000um_M0400.dataset = '/crabfake_mfv_neutralino_tau1000um_M0400_jtuple_v6_547d3313903142038335071634b26604/tucker-crabfake_mfv_neutralino_tau1000um_M0400_jtuple_v6_547d3313903142038335071634b26604-5bdce5833f35b995ab0c308220e77250/USER'
    mfv_neutralino_tau0000um_M0400.dataset = '/crabfake_mfv_neutralino_tau0000um_M0400_jtuple_v6_547d3313903142038335071634b26604/tucker-crabfake_mfv_neutralino_tau0000um_M0400_jtuple_v6_547d3313903142038335071634b26604-5bdce5833f35b995ab0c308220e77250/USER'
    for sample in samples:
        sample.scheduler_name = 'condor'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('TrackPlay',
                       total_number_of_events = 100000,
                       events_per_job = 20000,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       )
    cs.submit_all(samples)
