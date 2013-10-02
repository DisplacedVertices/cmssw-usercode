def use_pf_candidates(vertex_producer, src):
    vertex_producer.use_tracks = False
    vertex_producer.use_pf_jets = False
    vertex_producer.use_pat_jets = False
    vertex_producer.use_pf_candidates = True
    vertex_producer.pf_candidate_src = src

def use_jets(vertex_producer, kind):
    vertex_producer.use_tracks = False
    vertex_producer.use_pf_candidates = False
    if kind == 'pat':
        vertex_producer.use_pf_jets = False
        vertex_producer.use_pat_jets = True
    elif kind == 'pf':
        vertex_producer.use_pf_jets = True
        vertex_producer.use_pat_jets = False
    else:
        raise ValueError("don't know anything about kind = %r" % kind)


mfvVerticesFromCands = mfvVertices.clone()
use_pf_candidates(mfvVerticesFromCands, 'particleFlow')

mfvVerticesFromNoPUCands = mfvVertices.clone()
use_pf_candidates(mfvVerticesFromNoPUCands, 'pfNoPileUpPF')

mfvVerticesFromNoPUZCands = mfvVertices.clone()
use_pf_candidates(mfvVerticesFromNoPUZCands, 'pfNoPileUpPFClosestZVertex')

mfvVerticesFromJets = mfvVertices.clone()
use_jets(mfvVerticesFromJets, 'pat')

mfvVerticesFromPFJets = mfvVertices.clone()
use_jets(mfvVerticesFromPFJets, 'pf')

mfvPFCandVertexSequence = cms.Sequence(mfvVerticesFromCands + mfvVerticesFromNoPUCands + mfvVerticesFromNoPUZCands)
mfvJetVertexSequence = cms.Sequence(mfvVerticesFromJets + mfvVerticesFromPFJets)
mfvExtraVertexSequence = cms.Sequence(mfvPFCandVertexSequence + mfvJetVertexSequence)

mfvNonPATJetVertexSequence = cms.Sequence(mfvVerticesFromPFJets)
mfvNonPATExtraVertexSequence = cms.Sequence(mfvPFCandVertexSequence + mfvNonPATJetVertexSequence)
