import FWCore.ParameterSet.Config as cms

mfvVertexerPairEffs = cms.EDAnalyzer('MFVVertexerPairEffs',
                                     vpeff_src = cms.InputTag('mfvVertices'),
                                     verbose = cms.untracked.bool(False),
                                     )
