import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

histos = cms.EDAnalyzer('ResolutionsHistogrammer',
                        reweight_pileup = cms.bool(True),
                        force_weight = cms.double(-1),
                        vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                        met_src = cms.InputTag('patMETsPF'),
                        jet_src = cms.InputTag('selectedPatJetsPF'),
                        b_discriminators = cms.vstring('jetProbabilityBJetTags', 'combinedSecondaryVertexBJetTags'),
                        b_discriminator_mins = cms.vdouble(0.545, 0.679),
                        muon_src = cms.InputTag('selectedPatMuonsPF'),
                        max_muon_dxy = cms.double(1e99),
                        max_muon_dz = cms.double(1e99),
                        muon_semilep_cut = jtupleParams.semilepMuonCut,
                        muon_dilep_cut = jtupleParams.dilepMuonCut,
                        electron_src = cms.InputTag('selectedPatElectronsPF'),
                        max_semilep_electron_dxy = cms.double(1e99),
                        max_dilep_electron_dxy = cms.double(1e99),
                        electron_semilep_cut = jtupleParams.semilepElectronCut,
                        electron_dilep_cut = jtupleParams.dilepElectronCut,
                        print_info = cms.bool(False),
                        )
