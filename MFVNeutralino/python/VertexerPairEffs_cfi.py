import FWCore.ParameterSet.Config as cms

mfvVertexerPairEffs = cms.EDAnalyzer('MFVVertexerPairEffs',
                                     vpeff_src = cms.InputTag('mfvVertices'),
                                     allow_duplicate_pairs = cms.bool(True),
                                     verbose = cms.untracked.bool(False),
                                     )

mfvVertexerPairEffs3TkSeed = mfvVertexerPairEffs.clone(vpeff_src = 'mfvVertices3TkSeed')
mfvVertexerPairEffs4TkSeed = mfvVertexerPairEffs.clone(vpeff_src = 'mfvVertices4TkSeed')
mfvVertexerPairEffs5TkSeed = mfvVertexerPairEffs.clone(vpeff_src = 'mfvVertices5TkSeed')

mfvVertexerPairEffsSeq = cms.Sequence(
    mfvVertexerPairEffs *
    mfvVertexerPairEffs3TkSeed *
    mfvVertexerPairEffs4TkSeed *
    mfvVertexerPairEffs5TkSeed
    )
