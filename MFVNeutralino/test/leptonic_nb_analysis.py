import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.source.fileNames = ['/store/user/jchu/mfv_neutralino_tau1000um_M0400/jtuple_v7/5d4c2a74c85834550d3f9609274e8548/pat_1_1_hdB.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_891_1_sZ9.root','/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_948_2_lgB.root')
process.TFileService.fileName = 'leptonic_nb_analysis.root'

process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START53_V21::All'
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.goodOfflinePrimaryVertices.filter = cms.bool(True)
process.load('JMTucker.MFVNeutralino.Vertexer_cff')

process.p = cms.EDAnalyzer('LeptonicNBAnalysis',
                           trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                           primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                           secondary_vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                           muon_src = cms.InputTag('selectedPatMuonsPF'),
                           min_nmuons = cms.int32(1),
                           jet_src = cms.InputTag('selectedPatJetsPF'),
                           min_jet_pt = cms.double(30.0),
                           max_jet_eta = cms.double(2.4),
                           min_njets = cms.int32(6),
                           b_discriminator_name = cms.string('combinedSecondaryVertexBJetTags'),
                           bdisc_min = cms.double(0.679),
                           min_nbtags = cms.int32(1),
                           muon_stations_min = cms.bool(True),
                           muon_trackerhits_min = cms.bool(True),
                           muon_pixelhits_min = cms.bool(True),
                           muon_dxy_max = cms.bool(True),
                           muon_dz_max = cms.bool(True),
                           muon_eta_max = cms.bool(True),
                           muon_tkpterror_max = cms.bool(True),
                           muon_trkkink_max = cms.bool(True),
                           muon_pt_min = cms.bool(True),
                           muon_iso_max = cms.bool(True),
                           )

process.no_stations_min = process.p.clone(muon_stations_min = False)
process.no_trackerhits_min = process.p.clone(muon_trackerhits_min = False)
process.no_pixelhits_min = process.p.clone(muon_pixelhits_min = False)
process.no_dxy_max = process.p.clone(muon_dxy_max = False)
process.no_dz_max = process.p.clone(muon_dz_max = False)
process.no_eta_max = process.p.clone(muon_eta_max = False)
process.no_tkpterror_max = process.p.clone(muon_tkpterror_max = False)
process.no_trkkink_max = process.p.clone(muon_trkkink_max = False)
process.no_pt_min = process.p.clone(muon_pt_min = False)
process.no_iso_max = process.p.clone(muon_iso_max = False)

process.p0 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.p)
process.p1 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_stations_min)
process.p2 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_trackerhits_min)
process.p3 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_pixelhits_min)
process.p4 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_dxy_max)
process.p5 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_dz_max)
process.p6 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_eta_max)
process.p7 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_tkpterror_max)
process.p8 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_trkkink_max)
process.p9 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_pt_min)
process.p10 = cms.Path(process.goodOfflinePrimaryVertices * process.mfvVertexSequence * process.no_iso_max)

def de_mfv():
    if hasattr(process, 'mfvGenParticleFilter'):
        process.mfvGenParticleFilter.cut_invalid = False
    if hasattr(process, 'mfvGenVertices'):
        process.mfvGenVertices.is_mfv = False

def sample_ttbar():
    de_mfv()
    if hasattr(process, 'mfvGenVertices'):
        process.mfvGenVertices.is_ttbar = True

if 'ttbarhadronic' in sys.argv:
    sample_ttbar()
    process.source.fileNames = '''/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_1_1_N3F.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_2_1_W1v.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_3_1_TEb.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_4_1_as5.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_5_1_cAb.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_6_1_ZMk.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_7_1_FQE.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_8_1_4rS.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_9_1_eTU.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_10_1_81U.root
/store/user/jchu/TTJets_HadronicMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_11_1_EJW.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/562EF878-5017-E211-976D-E0CB4E5536A7.root','/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00001/BCE41FBC-BE17-E211-9679-00259073E3FC.root','/store/mc/Summer12_DR53X/TTJets_HadronicMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v1/00000/AABB22F7-E515-E211-A4D3-E0CB4E19F95B.root')
    process.TFileService.fileName = 'leptonic_nb_analysis_ttbarhadronic.root'

if 'ttbarsemilep' in sys.argv:
    sample_ttbar()
    process.source.fileNames = '''/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_1_1_Wl2.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_2_1_oi1.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_3_1_WDC.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_4_1_ySW.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_5_1_RJP.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_6_1_dc2.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_7_1_TJI.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_8_1_pBD.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_9_1_ZGk.root
/store/user/jchu/TTJets_SemiLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_10_1_nuP.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/TTJets_SemiLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A_ext-v1/00000/66DA98B8-5B24-E211-8DA5-003048D476C4.root')
    process.TFileService.fileName = 'leptonic_nb_analysis_ttbarsemilep.root'

if 'ttbardilep' in sys.argv:
    sample_ttbar()
    process.source.fileNames = '''/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_1_2_y4F.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_2_1_Gr1.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_3_1_47Y.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_4_1_9xi.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_5_1_vCZ.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_6_1_7o2.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_7_1_7Tm.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_8_1_QGa.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_9_1_rLc.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_10_1_2gY.root
/store/user/jchu/TTJets_FullLeptMGDecays_8TeV-madgraph/jtuple_no_skimming_cuts_v8/a95b67af6a62c008520600808d84ac2d/pat_11_1_Gam.root'''.split('\n')
    process.source.secondaryFileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/TTJets_FullLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v2/00001/80BF45BD-BB1D-E211-B8A0-E41F13181808.root','/store/mc/Summer12_DR53X/TTJets_FullLeptMGDecays_8TeV-madgraph/AODSIM/PU_S10_START53_V7A-v2/00000/B29D0A87-A21A-E211-AC8D-E61F131915F3.root')
    process.TFileService.fileName = 'leptonic_nb_analysis_ttbardilep.root'

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter

    cs = CRABSubmitter('LeptonicNBAnalysis',
                       total_number_of_events = -1,
                       events_per_job = 10000,
                       use_ana_dataset = True,
                       CMSSW_use_parent = 1,
                       )
    cs.submit_all(mfv_signal_samples)
