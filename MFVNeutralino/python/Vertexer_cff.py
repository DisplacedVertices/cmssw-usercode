import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.Vertexer_cfi import mfvVertices
from JMTucker.MFVNeutralino.GenParticles_cff import mfvGenVertices
from JMTucker.MFVNeutralino.VertexAuxProducer_cfi import mfvVerticesAuxTmp, mfvVerticesAux
from JMTucker.MFVNeutralino.VertexSelector_cfi import mfvSelectedVertices, mfvSelectedVerticesTight
from JMTucker.MFVNeutralino.JetVertexAssociator_cfi import mfvVerticesToJets

mfvVertexSequence = cms.Sequence(mfvVertices *
                                 mfvGenVertices *
                                 mfvVerticesAuxTmp *
                                 mfvSelectedVerticesTight *
                                 mfvVerticesToJets *
                                 mfvVerticesAux)
