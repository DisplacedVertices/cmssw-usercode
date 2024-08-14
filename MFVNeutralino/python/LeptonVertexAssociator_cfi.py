import FWCore.ParameterSet.Config as cms


mfvVerticesToLeptons = cms.EDProducer('MFVLeptonVertexAssociator',
                                   enable = cms.bool(True),
                                   beamspot_src = cms.InputTag('offlineBeamSpot'),
                                   muons_src = cms.InputTag('slimmedMuons'),
                                   electrons_src = cms.InputTag('slimmedElectrons'),
                                   muon_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'museed'),
                                   electron_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'eleseed'), 
                                   vertex_src = cms.InputTag('mfvSelectedVerticesTmp'),
                                   gen_info_src = cms.InputTag('generator'),
                                   gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
                                   gen_particles_src = cms.InputTag('prunedGenParticles'),
                                   input_is_refs = cms.bool(True),
                                   min_vertex_track_weight = cms.double(0.5),
                                   histos = cms.untracked.bool(True),
                                   verbose = cms.untracked.bool(False),
                                   )