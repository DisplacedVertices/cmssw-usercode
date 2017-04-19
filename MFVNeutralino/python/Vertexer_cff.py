import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.Vertexer_cfi import mfvVertices
from JMTucker.MFVNeutralino.GenParticles_cff import mfvGenParticles
from JMTucker.MFVNeutralino.VertexAuxProducer_cfi import mfvVerticesAuxTmp, mfvVerticesAux
from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.JetVertexAssociator_cfi import mfvVerticesToJets

mfvSelectedVerticesTmp = mfvSelectedVertices.clone(vertex_aux_src = 'mfvVerticesAuxTmp',
                                                   produce_refs = True,
                                                   min_ntracks = 3)

mfvVerticesAuxPresel = mfvVerticesAux
mfvVerticesAux = mfvSelectedVertices.clone(vertex_aux_src = 'mfvVerticesAuxPresel', min_ntracks = 3)

mfvVertexSequence = cms.Sequence(mfvVertices *
                                 mfvGenParticles *
                                 mfvVerticesAuxTmp *
                                 mfvSelectedVerticesTmp *
                                 mfvVerticesToJets *
                                 mfvVerticesAuxPresel *
                                 mfvVerticesAux)
