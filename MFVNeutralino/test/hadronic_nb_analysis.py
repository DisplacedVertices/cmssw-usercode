import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root','/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root')
process.TFileService.fileName = 'hadronic_nb_analysis.root'

process.p = cms.EDAnalyzer('HadronicNBAnalysis',
                           trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                           jet_src = cms.InputTag('selectedPatJetsPF'),
                           min_njets = cms.int32(6),
                           min_jet_pt = cms.double(50.0),
                           min_1st_jet_pt = cms.double(150.0),
                           b_discriminator_name = cms.string('combinedSecondaryVertexBJetTags'),
                           min_nbtags = cms.int32(2),
                           bdisc_min = cms.double(0.898),
                           muon_src = cms.InputTag('selectedPatMuonsPF'),
                           electron_src = cms.InputTag('selectedPatElectronsPF'),
                           )
process.p0 = cms.Path(process.p)

def de_mfv():
    if hasattr(process, 'mfvGenParticleFilter'):
        process.mfvGenParticleFilter.cut_invalid = False
    if hasattr(process, 'mfvGenVertices'):
        process.mfvGenVertices.is_mfv = False

if 'qcdht0100' in sys.argv:
    de_mfv()
    process.source.fileNames = '''/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_1_1_Shq.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_2_1_RWX.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_3_1_zX9.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_4_1_YGt.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_5_1_gGr.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_6_1_VQD.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_7_1_mRI.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_8_1_AYq.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_9_1_GKZ.root
/store/user/jchu/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_10_1_4w1.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/QCD_HT-100To250_TuneZ2star_8TeV-madgraph-pythia/AODSIM/PU_S10_START53_V7A-v1/00000/34E4715C-6C0F-E211-B4C1-0026189438BF.root')
    process.TFileService.fileName = 'hadronic_nb_analysis_qcdht0100.root'

if 'qcdht0250' in sys.argv:
    de_mfv()
    process.source.fileNames = '''/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_1_1_E0b.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_2_1_Dgo.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_3_1_sMy.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_4_1_mrO.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_5_1_MSw.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_6_1_am2.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_7_1_5lo.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_8_1_3OG.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_9_1_ePw.root
/store/user/jchu/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_10_1_KHQ.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/QCD_HT-250To500_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00001/C2560F62-2913-E211-BF7D-0024E87663BA.root')
    process.TFileService.fileName = 'hadronic_nb_analysis_qcdht0250.root'

if 'qcdht0500' in sys.argv:
    de_mfv()
    process.source.fileNames = '''/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_1_1_r8X.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_2_1_2Rg.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_3_1_7y6.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_4_1_ZyP.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_5_1_RdF.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_6_1_TTA.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_7_1_K5v.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_8_1_ZEn.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_9_1_Qog.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_10_1_vUx.root
/store/user/jchu/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_11_1_LjE.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00003/1C38BEB3-D728-E211-897B-00266CF9BEF8.root','/store/mc/Summer12_DR53X/QCD_HT-500To1000_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/C28A8612-991F-E211-B35C-0024E8769B6D.root')
    process.TFileService.fileName = 'hadronic_nb_analysis_qcdht0500.root'

if 'qcdht1000' in sys.argv:
    de_mfv()
    process.source.fileNames = '''/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_1_1_uij.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_2_1_OyH.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_3_1_JW6.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_4_1_hSV.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_5_1_Lqm.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_6_1_7Ml.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_7_1_f2A.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_8_1_XxA.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_9_1_a1G.root
/store/user/jchu/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_10_1_SzD.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/0038E6D2-860D-E211-9211-00266CFACC38.root','/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/D4C0816B-870D-E211-B094-00266CF258D8.root')
    process.TFileService.fileName = 'hadronic_nb_analysis_qcdht1000.root'

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples, qcdht1000
    qcdht1000.ana_dataset_override = '/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/jchu-jtuple_no_skimming_cuts_v8-a95b67af6a62c008520600808d84ac2d/USER'

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('HadronicNBAnalysis',
                       total_number_of_events = -1,
                       events_per_job = 10000,
                       use_ana_dataset = True,
                       CMSSW_use_parent = 1,
                       )
    cs.submit_all(mfv_signal_samples + [qcdht1000])
