import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvEvent = cms.EDProducer('MFVEventProducer',
                          trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                          cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT'),
                          skip_event_filter = cms.string('ptrig'),
                          pfjets_src = cms.InputTag('ak5PFJets'),
                          jet_pt_min = cms.double(20),
                          primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                          gen_particles_src = cms.InputTag('genParticles'),
                          jets_src = cms.InputTag('selectedPatJetsPF'),
                          met_src = cms.InputTag('patMETsPF'),
                          b_discriminator = cms.string('combinedSecondaryVertexBJetTags'),
                          b_discriminator_mins = cms.vdouble(0.244, 0.679, 0.898),
                          muons_src = cms.InputTag('selectedPatMuonsPF'),
                          muon_semilep_cut = jtupleParams.semilepMuonCut,
                          muon_dilep_cut = jtupleParams.dilepMuonCut,
                          electrons_src = cms.InputTag('selectedPatElectronsPF'),
                          electron_semilep_cut = jtupleParams.semilepElectronCut,
                          electron_dilep_cut = jtupleParams.dilepElectronCut,
                          )
