import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvEvent = cms.EDProducer('MFVEventProducer',
                          trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                          pfjets_src = cms.InputTag('ak5PFJets'),
                          jet_pt_min = cms.double(20),
                          primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                          is_mc = cms.bool(True),
                          gen_particles_src = cms.InputTag('genParticles'),
                          jets_src = cms.InputTag('selectedPatJetsPF'),
                          b_discriminator = cms.string('combinedSecondaryVertexBJetTags'),
                          b_discriminator_min = cms.double(0.679),
                          muons_src = cms.InputTag('selectedPatMuonsPF'),
                          muon_semilep_cut = jtupleParams.semilepMuonCut,
                          muon_dilep_cut = jtupleParams.dilepMuonCut,
                          electrons_src = cms.InputTag('selectedPatElectronsPF'),
                          electron_semilep_cut = jtupleParams.semilepElectronCut,
                          electron_dilep_cut = jtupleParams.dilepElectronCut,
                          )
