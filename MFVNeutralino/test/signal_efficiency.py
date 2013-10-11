import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root','/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root')
process.TFileService.fileName = 'signal_efficiency.root'

def ttbarhadronic():
    process.source.fileNames = '''/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_1_1_dmH.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_2_1_LLZ.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_3_1_Qnk.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_4_1_2GS.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_5_1_lsc.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_6_1_O0r.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_7_1_55J.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_8_1_T6j.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_9_1_M6j.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_10_1_D64.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/F67C1297-9618-E211-AA98-001EC9D8A8D4.root','/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/FA7398AB-A618-E211-A744-90E6BA19A227.root')
    process.TFileService.fileName = 'signal_efficiency_ttbarhadronic.root'

def ttbarsemilep():
    process.source.fileNames = '''/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_1_1_4BU.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_2_1_mB5.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_3_1_qkE.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_4_1_kHq.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_5_1_FRM.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_6_1_j2P.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_7_1_gwy.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_8_2_NgD.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_9_1_vkK.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_10_2_j9H.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/TTJets_SemiLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A_ext-v1/00000/66DA98B8-5B24-E211-8DA5-003048D476C4.root')
    process.TFileService.fileName = 'signal_efficiency_ttbarsemilep.root'

def ttbardilep():
    process.source.fileNames = '''/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_1_1_I2j.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_2_1_ilZ.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_3_1_y3B.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_4_1_XkZ.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_5_1_IGv.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_6_1_hyX.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_7_1_YYJ.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_8_1_ODM.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_9_1_Poo.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_10_1_WxO.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v7/1507a4277dcbc3e001c67e44d7006d62/pat_11_1_aVn.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/TTJets_FullLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v2/00001/80BF45BD-BB1D-E211-B8A0-E41F13181808.root','/store/mc/Summer12_DR53X/TTJets_FullLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v2/00000/48D3D464-B11A-E211-9323-001A645C1B04.root')
    process.TFileService.fileName = 'signal_efficiency_ttbardilep.root'

ttbardilep()

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(True)

process.p = cms.EDAnalyzer('SignalEfficiency',
                           trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                           jet_src = cms.InputTag('selectedPatJetsPF'),
                           min_jet_pt = cms.double(30.0),
                           max_jet_eta = cms.double(2.4),
                           primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                           muon_src = cms.InputTag('selectedPatMuonsPF'),
                           min_nmuons = cms.int32(1),
                           b_discriminator_name = cms.string('combinedSecondaryVertexBJetTags'),
                           bdisc_min = cms.double(0.679),
                           min_nbtags = cms.int32(1),
                           )

process.p0 = cms.Path(process.goodOfflinePrimaryVertices * process.p)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    cs = CRABSubmitter('SignalEfficiency',
                       total_number_of_events = -1,
                       events_per_job = 10000,
                       use_ana_dataset = True,
                       CMSSW_use_parent = 1,
                       )
    cs.submit_all(mfv_signal_samples)
