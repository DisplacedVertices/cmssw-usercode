from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = '''/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_2_2_vbl.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_3_2_yEE.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_4_1_vkj.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_5_3_Tce.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_6_1_a0t.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_7_2_Qv8.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_8_1_3WZ.root
/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_9_1_ANl.root'''.split('\n')
process.TFileService.fileName = 'gen_ntuple.root'

add_analyzer('MFVGenNtupleDumper', gen_src = cms.InputTag('genParticles'))

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples as samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    cs = CRABSubmitter('GenNtuple',
                       total_number_of_events = -1,
                       events_per_job = 20000,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*'
                       )
    cs.submit_all(samples)
