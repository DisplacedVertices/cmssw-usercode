import FWCore.ParameterSet.Config as cms

mfvTrackTree = cms.EDAnalyzer('MFVTrackTree',
                               genvtx_src = cms.InputTag('mfvGenParticles', 'decays'),
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                               tracks_src = cms.InputTag('jmtRescaledTracks'),
                               mci_src = cms.InputTag('mfvGenParticles'),
                               no_track_cuts = cms.bool(False),
                               min_track_pt = cms.double(1),
                               min_track_dxy = cms.double(0),
                               min_track_sigmadxy = cms.double(0),
                               min_track_rescaled_sigmadxy = cms.double(4.0), #FIXME default is 4
                               min_track_sigmadxypv = cms.double(0),
                               min_track_hit_r = cms.int32(1),
                               min_track_nhits = cms.int32(0),
                               min_track_npxhits = cms.int32(0),
                               min_track_npxlayers = cms.int32(2),
                               min_track_nstlayers = cms.int32(6),
                               max_track_dxyerr = cms.double(1e9),
                               max_track_dxyipverr = cms.double(-1),
                               max_track_d3dipverr = cms.double(-1),
                               verbose = cms.bool(False),
                               )
