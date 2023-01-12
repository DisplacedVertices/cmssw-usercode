import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.GenParticles_cff import mfvGenParticles
from JMTucker.MFVNeutralino.Vertexer_cfi import mfvVertexTracks, mfvVertices
from JMTucker.MFVNeutralino.VertexAuxProducer_cfi import mfvVerticesAuxTmp, mfvVerticesAux
from JMTucker.MFVNeutralino.VertexSelector_cfi import mfvSelectedVertices
from JMTucker.MFVNeutralino.JetVertexAssociator_cfi import mfvVerticesToJets
from JMTucker.Tools.RescaledTracks_cfi import jmtRescaledTracks

mfvSelectedVerticesTmp = mfvSelectedVertices.clone(vertex_aux_src = 'mfvVerticesAuxTmp',
                                                   produce_refs = True,
                                                   vertex_src = 'mfvVertices',
                                                   min_ntracks = 3) #FIXME : for matching b-quarks and b-SVs that are loose 

mfvVerticesAuxPresel = mfvVerticesAux
mfvVerticesAux = mfvSelectedVertices.clone(vertex_aux_src = 'mfvVerticesAuxPresel', min_ntracks = 3) #FIXME : for matching b-quarks and b-SVs that are loose

mfvVertexSequenceBare = cms.Sequence(
    mfvGenParticles *
    jmtRescaledTracks *
    mfvVertexTracks *
    mfvVertices
    )

#mfvVertexSequenceBare = cms.Sequence(
#    jmtRescaledTracks *
#    mfvVertexTracksGen *
#    mfvVertices
#    )

mfvVertexSequence = cms.Sequence(
    mfvVertexSequenceBare *
    mfvVerticesAuxTmp *
    mfvSelectedVerticesTmp *
    mfvVerticesToJets *
    mfvVerticesAuxPresel *
    mfvVerticesAux
    )

def modifiedVertexSequence(process, name, **kwargs):
    kwargs_tracks, kwargs_vertices = {}, {}
    for k,v in kwargs.iteritems():
        if hasattr(process.mfvVertexTracks, k):
            kwargs_tracks[k] = v
        if hasattr(process.mfvVertices, k):
            kwargs_vertices[k] = v

    mfvVertexTracksNew = process.mfvVertexTracks.clone(**kwargs_tracks)
    mfvVerticesNew = process.mfvVertices.clone(seed_tracks_src = cms.InputTag('mfvVertexTracks%s' % name, 'seed'), **kwargs_vertices)
    mfvVerticesAuxTmpNew = process.mfvVerticesAuxTmp.clone(vertex_src = 'mfvVertices%s' % name)
    mfvSelectedVerticesTmpNew = process.mfvSelectedVerticesTmp.clone(vertex_aux_src = 'mfvVerticesAuxTmp%s' % name,
                                                                     vertex_src = 'mfvVertices%s' % name)
    mfvVerticesToJetsNew = process.mfvVerticesToJets.clone(vertex_src = 'mfvSelectedVerticesTmp%s' % name)
    mfvVerticesAuxPreselNew = process.mfvVerticesAuxPresel.clone(vertex_src = 'mfvVertices%s' % name,
                                                                 sv_to_jets_src = 'mfvVerticesToJets%s' % name)
    mfvVerticesAuxNew = process.mfvVerticesAux.clone(vertex_aux_src = 'mfvVerticesAuxPresel%s' % name)

    setattr(process, 'mfvVertexTracks%s'        % name, mfvVertexTracksNew)
    setattr(process, 'mfvVertices%s'            % name, mfvVerticesNew)
    setattr(process, 'mfvVerticesAuxTmp%s'      % name, mfvVerticesAuxTmpNew)
    setattr(process, 'mfvSelectedVerticesTmp%s' % name, mfvSelectedVerticesTmpNew)
    setattr(process, 'mfvVerticesToJets%s'      % name, mfvVerticesToJetsNew)
    setattr(process, 'mfvVerticesAuxPresel%s'   % name, mfvVerticesAuxPreselNew)
    setattr(process, 'mfvVerticesAux%s'         % name, mfvVerticesAuxNew)

    seq = cms.Sequence(
        mfvVertexTracksNew *
        mfvVerticesNew *
        mfvVerticesAuxTmpNew *
        mfvSelectedVerticesTmpNew *
        mfvVerticesToJetsNew *
        mfvVerticesAuxPreselNew *
        mfvVerticesAuxNew)
    return seq
