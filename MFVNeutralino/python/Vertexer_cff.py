import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.GenParticles_cff import mfvGenParticles
from JMTucker.MFVNeutralino.Vertexer_cfi import mfvVertices
from JMTucker.MFVNeutralino.VertexAuxProducer_cfi import mfvVerticesAuxTmp, mfvVerticesAux
from JMTucker.MFVNeutralino.VertexSelector_cfi import mfvSelectedVertices
from JMTucker.MFVNeutralino.JetVertexAssociator_cfi import mfvVerticesToJets

mfvSelectedVerticesTmp = mfvSelectedVertices.clone(vertex_aux_src = 'mfvVerticesAuxTmp',
                                                   produce_refs = True,
                                                   min_ntracks = 3)

mfvVerticesAuxPresel = mfvVerticesAux
mfvVerticesAux = mfvSelectedVertices.clone(vertex_aux_src = 'mfvVerticesAuxPresel', min_ntracks = 3)

x = (mfvGenParticles *
     mfvVertices *
     mfvVerticesAuxTmp *
     mfvSelectedVerticesTmp *
     mfvVerticesToJets *
     mfvVerticesAuxPresel *
     mfvVerticesAux)

mfvVertexSequence   = cms.Sequence(x)
mfvVertexSequenceEx = cms.Sequence(x) # no clone for sequences?

for n_tk_seed in 3,4,5:
    exec '''
mfvVerticesNTKTkSeed = mfvVertices.clone(n_tracks_per_seed_vertex = n_tk_seed)
mfvVerticesAuxTmpNTKTkSeed = mfvVerticesAuxTmp.clone(vertex_src = 'mfvVerticesNTKTkSeed')
mfvSelectedVerticesTmpNTKTkSeed = mfvSelectedVerticesTmp.clone(vertex_aux_src = 'mfvVerticesAuxTmpNTKTkSeed')
mfvVerticesToJetsNTKTkSeed = mfvVerticesToJets.clone(vertex_src = 'mfvSelectedVerticesTmpNTKTkSeed')
mfvVerticesAuxPreselNTKTkSeed = mfvVerticesAuxPresel.clone(vertex_src = 'mfvVerticesNTKTkSeed',
                                                           sv_to_jets_src = 'mfvVerticesToJetsNTKTkSeed')
mfvVerticesAuxNTKTkSeed = mfvVerticesAux.clone(vertex_aux_src = 'mfvVerticesAuxPreselNTKTkSeed')
mfvVertexSequenceEx *= (mfvVerticesNTKTkSeed *
                        mfvVerticesAuxTmpNTKTkSeed *
                        mfvSelectedVerticesTmpNTKTkSeed *
                        mfvVerticesToJetsNTKTkSeed *
                        mfvVerticesAuxPreselNTKTkSeed *
                        mfvVerticesAuxNTKTkSeed)
'''.replace('NTK', str(n_tk_seed))
