import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.Year import year
from PileupWeights import pileup_weights

TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                               track_src = cms.InputTag('generalTracks'),
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                               use_duplicateMerge = cms.int32(-1),
                               old_stlayers_cut = cms.bool(False),
                               pileup_weights = cms.vdouble(*pileup_weights[year]),
                               )
