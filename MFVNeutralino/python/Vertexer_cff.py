import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.Vertexer_cfi import mfvVertices
from JMTucker.MFVNeutralino.GenParticles_cff import mfvGenVertices
from JMTucker.MFVNeutralino.VertexAuxProducer_cfi import mfvVerticesAuxTmp, mfvVerticesAux
from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.JetVertexAssociator_cfi import mfvVerticesToJets

mfvSelectedVerticesTmp = mfvSelectedVerticesLoose.clone(vertex_aux_src = 'mfvVerticesAuxTmp',
                                                        produce_refs = True)

mfvVertexSequence = cms.Sequence(mfvVertices *
                                 mfvGenVertices *
                                 mfvVerticesAuxTmp *
                                 mfvSelectedVerticesTmp *
                                 mfvVerticesToJets *
                                 mfvVerticesAux *
                                 mfvSelectedVerticesSeq)

################################################################################

mfvVerticesAsymSeed = mfvVertices.clone(min_all_track_pt = 0.75,
                                        min_all_track_dxy = 0.003,
                                        min_seed_track_pt = 5,
                                        min_seed_track_dxy = 0.003)

mfvVerticesAsymSeedAuxTmp = mfvVerticesAuxTmp.clone(vertex_src = 'mfvVerticesAsymSeed')
mfvSelectedVerticesAsymSeedTmp = mfvSelectedVerticesTmp.clone(vertex_src = 'mfvVerticesAsymSeed', vertex_aux_src = 'mfvVerticesAsymSeedAuxTmp')
mfvVerticesAsymSeedToJets = mfvVerticesToJets.clone(vertex_src = 'mfvSelectedVerticesAsymSeedTmp')
mfvVerticesAsymSeedAux = mfvVerticesAux.clone(vertex_src = 'mfvVerticesAsymSeed', sv_to_jets_src = 'mfvVerticesAsymSeedToJets')
mfvSelectedVerticesAsymSeedTight = mfvSelectedVerticesTight.clone(vertex_src = 'mfvVerticesAsymSeed', vertex_aux_src = 'mfvVerticesAsymSeedAux')

mfvVertexAsymSeedSequence = cms.Sequence(mfvVerticesAsymSeed *
                                         mfvGenVertices *
                                         mfvVerticesAsymSeedAuxTmp *
                                         mfvSelectedVerticesAsymSeedTmp *
                                         mfvVerticesAsymSeedToJets *
                                         mfvVerticesAsymSeedAux *
                                         mfvSelectedVerticesAsymSeedTight)

################################################################################

mfvVerticesSumSeed = mfvVertices.clone(min_all_track_dxy = 0.,
                                       seed_by_sums = True,
                                       min_seed_sum_pt = 5,
                                       min_seed_sum_adxy = 0.01)

mfvVerticesSumSeedAuxTmp = mfvVerticesAuxTmp.clone(vertex_src = 'mfvVerticesSumSeed')
mfvSelectedVerticesSumSeedTmp = mfvSelectedVerticesTmp.clone(vertex_src = 'mfvVerticesSumSeed', vertex_aux_src = 'mfvVerticesSumSeedAuxTmp')
mfvVerticesSumSeedToJets = mfvVerticesToJets.clone(vertex_src = 'mfvSelectedVerticesSumSeedTmp')
mfvVerticesSumSeedAux = mfvVerticesAux.clone(vertex_src = 'mfvVerticesSumSeed', sv_to_jets_src = 'mfvVerticesSumSeedToJets')
mfvSelectedVerticesSumSeedTight = mfvSelectedVerticesTight.clone(vertex_src = 'mfvVerticesSumSeed', vertex_aux_src = 'mfvVerticesSumSeedAux')

mfvVertexSumSeedSequence = cms.Sequence(mfvVerticesSumSeed *
                                        mfvGenVertices *
                                        mfvVerticesSumSeedAuxTmp *
                                        mfvSelectedVerticesSumSeedTmp *
                                        mfvVerticesSumSeedToJets *
                                        mfvVerticesSumSeedAux *
                                        mfvSelectedVerticesSumSeedTight)
