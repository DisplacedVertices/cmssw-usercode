import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.TrackRefGetter_cff import jmtTrackRefGetter
from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params

mfvVerticesAuxTmp = cms.EDProducer('MFVVertexAuxProducer',
                                   kvr_params = kvr_params,
                                   beamspot_src = cms.InputTag('offlineBeamSpot'),
                                   primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                   muons_src = cms.InputTag('selectedPatMuons'),
                                   electrons_src = cms.InputTag('selectedPatElectrons'),
                                   gen_vertices_src = cms.InputTag('mfvGenParticles', 'decays'),
                                   vertex_src = cms.InputTag('mfvVertices'),
                                   vertex_seed_tracks_src = cms.InputTag('mfvVertices', 'seed'), 
                                   sv_to_jets_src = cms.string('dummy'),
                                   track_ref_getter = jmtTrackRefGetter,
                                   sort_by = cms.string('ntracks_then_mass'),
                                   verbose = cms.untracked.bool(False),
                                   )

mfvVerticesAux = mfvVerticesAuxTmp.clone(sv_to_jets_src = 'mfvVerticesToJets')
