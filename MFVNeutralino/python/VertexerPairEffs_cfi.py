import FWCore.ParameterSet.Config as cms

mfvVertexerPairEffs = cms.EDAnalyzer('MFVVertexerPairEffs',
                                     vpeff_src = cms.InputTag('mfvVertices'),
                                     allow_duplicate_pairs = cms.bool(True),
                                     verbose = cms.untracked.bool(False),
                                     )
