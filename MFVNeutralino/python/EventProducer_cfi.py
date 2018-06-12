import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvEvent = cms.EDProducer('MFVEventProducer',
                          input_is_miniaod = cms.bool(False),
                          packed_candidates_src = cms.InputTag('packedPFCandidates'),
                          triggerfloats_src = cms.InputTag('mfvTriggerFloats'),
                          beamspot_src = cms.InputTag('offlineBeamSpot'),
                          primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                          gen_info_src = cms.InputTag('generator'),
                          gen_jets_src = cms.InputTag('ak4GenJetsNoNu'),
                          gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
                          gen_particles_src = cms.InputTag('genParticles'),
                          mci_src = cms.InputTag('mfvGenParticles'),
                          pileup_info_src = cms.InputTag('addPileupInfo'),
                          jets_src = cms.InputTag('selectedPatJets'),
                          met_src = cms.InputTag('patMETsNoHF'),
                          b_discriminator = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),  #pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb
                          b_discriminator_mins = cms.vdouble(0.5803, 0.8838, 0.9693),
                          muons_src = cms.InputTag('selectedPatMuons'),
                          muon_cuts = jtupleParams.muonCuts,
                          electrons_src = cms.InputTag('selectedPatElectrons'),
                          electron_EB_cuts = jtupleParams.electronEBCuts,
                          electron_EE_cuts = jtupleParams.electronEECuts,
                          vertex_seed_tracks_src = cms.InputTag('mfvVertices', 'seed'),
                          lightweight = cms.bool(False),
                          )
