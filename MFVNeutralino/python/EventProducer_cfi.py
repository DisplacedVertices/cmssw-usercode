import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvEvent = cms.EDProducer('MFVEventProducer',
                          trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                          cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT'),
                          skip_event_filter = cms.string('pevtsel'),
                          pfjets_src = cms.InputTag('ak5PFJets'),
                          jet_pt_min = cms.double(20),
                          beamspot_src = cms.InputTag('offlineBeamSpot'),
                          primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                          gen_particles_src = cms.InputTag('genParticles'),
                          calojets_src = cms.InputTag('patJets'),
                          jets_src = cms.InputTag('selectedPatJets'),
                          met_src = cms.InputTag('patMETs'),
                          b_discriminator = cms.string('combinedSecondaryVertexBJetTags'),
                          b_discriminator_mins = cms.vdouble(0.244, 0.679, 0.898),
                          muons_src = cms.InputTag('selectedPatMuons'),
                          muon_semilep_cut = jtupleParams.semilepMuonCut,
                          muon_dilep_cut = jtupleParams.dilepMuonCut,
                          electrons_src = cms.InputTag('selectedPatElectrons'),
                          electron_semilep_cut = jtupleParams.semilepElectronCut,
                          electron_dilep_cut = jtupleParams.dilepElectronCut,
                          )
