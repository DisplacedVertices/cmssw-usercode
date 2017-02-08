import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.Vertexer_cfi import mfvVertices
from JMTucker.MFVNeutralino.GenParticles_cff import mfvGenVertices
from JMTucker.MFVNeutralino.VertexAuxProducer_cfi import mfvVerticesAuxTmp, mfvVerticesAux
from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.JetVertexAssociator_cfi import mfvVerticesToJets

mfvSelectedVerticesTmp = mfvSelectedVertices.clone(vertex_aux_src = 'mfvVerticesAuxTmp',
                                                   produce_refs = True,
                                                   min_ntracks = 5)

mfvVertexSequence = cms.Sequence(mfvVertices *
                                 mfvGenVertices *
                                 mfvVerticesAuxTmp *
                                 mfvSelectedVerticesTmp *
                                 mfvVerticesToJets *
                                 mfvVerticesAux *
                                 mfvSelectedVerticesSeq)
