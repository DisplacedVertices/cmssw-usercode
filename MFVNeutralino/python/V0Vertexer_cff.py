import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.Vertexer_cfi import kvr_params

mfvV0Vertices = cms.EDFilter('MFVV0Vertexer',
                             kvr_params = kvr_params,
                             tracks_src = cms.InputTag('mfvSkimmedTracks'),
                             max_chi2ndf = cms.double(5),
                             cut = cms.bool(False),
                             debug = cms.untracked.bool(False)
                             )
