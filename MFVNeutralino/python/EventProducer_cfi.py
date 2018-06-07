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
                          calojets_src = cms.InputTag(''),
                          jets_src = cms.InputTag('selectedPatJets'),
                          met_src = cms.InputTag('patMETsNoHF'),
                          b_discriminator = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
                          b_discriminator_mins = cms.vdouble(0.46, 0.8, 0.935),
                          muons_src = cms.InputTag('selectedPatMuons'),
                          muon_cut = jtupleParams.muonCut,
                          electrons_src = cms.InputTag('selectedPatElectrons'),
                          electron_cut = jtupleParams.electronCut,
                          vertex_seed_tracks_src = cms.InputTag('mfvVertices', 'seed'),
                          lightweight = cms.bool(False),
                          )
