import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi import *
goodOfflinePrimaryVertices.filter = cms.bool(False)

########################################################################

mfvInclusiveVertexFinder = cms.EDProducer('MFVInclusiveVertexFinder',
                                          beamSpot = cms.InputTag('offlineBeamSpot'),
                                          minHits = cms.uint32(8),
                                          vertexMinDLen2DSig = cms.double(2.5),
                                          maximumLongitudinalImpactParameter = cms.double(0.3),
                                          maxNTracks = cms.uint32(30),
                                          primaryVertices = cms.InputTag('goodOfflinePrimaryVertices'),
                                          tracks = cms.InputTag('generalTracks'),
                                          vertexMinAngleCosine = cms.double(0.95),
                                          clusterizer = cms.PSet(
                                              seedMin3DIPValue = cms.double(0.005),
                                              clusterMaxDistance = cms.double(0.05),
                                              seedMin3DIPSignificance = cms.double(1.2),
                                              clusterScale = cms.double(1),
                                              clusterMaxSignificance = cms.double(4.5),
                                              clusterMinAngleCosine = cms.double(0.5),
                                              do_histos = cms.bool(True),
                                              ),
                                          vertexReco = cms.PSet(
                                              seccut = cms.double(3),
                                              primcut = cms.double(1.0),
                                              finder = cms.string('avr'),
                                              smoothing = cms.bool(True)
                                              ),
                                          vertexMinDLenSig = cms.double(0.5),
                                          minPt = cms.double(0.8),
                                          do_histos = cms.bool(True),
                                          )

########################################################################

mfvVertexMerger =  cms.EDProducer('MFVVertexMerger',
                                  minSignificance = cms.double(2),
                                  secondaryVertices = cms.InputTag('mfvInclusiveVertexFinder'),
                                  maxFraction = cms.double(0.7),
                                  do_histos = cms.bool(True),
                                  )

mfvTrackVertexArbitrator = cms.EDProducer('MFVTrackVertexArbitrator',
                                          dLenFraction = cms.double(0.333),
                                          beamSpot = cms.InputTag('offlineBeamSpot'),
                                          distCut = cms.double(0.04),
                                          secondaryVertices = cms.InputTag('mfvVertexMerger'),
                                          dRCut = cms.double(0.4),
                                          primaryVertices = cms.InputTag('goodOfflinePrimaryVertices'),
                                          tracks = cms.InputTag('generalTracks'),
                                          sigCut = cms.double(5),
                                          do_histos = cms.bool(True),
                                          )

mfvInclusiveMergedVertices =  cms.EDProducer('MFVVertexMerger',
                                             minSignificance = cms.double(10.0),
                                             secondaryVertices = cms.InputTag('mfvTrackVertexArbitrator'),
                                             maxFraction = cms.double(0.2),
                                             do_histos = cms.bool(True),
                                             )

########################################################################

mfvVertexMergerShared = cms.EDProducer('MFVVertexMergerSharedTracks',
                                       vertex_reco = mfvInclusiveVertexFinder.vertexReco,
                                       secondaryVertices = cms.InputTag('mfvInclusiveVertexFinder'),
                                       min_track_weight = cms.double(0.5),
                                       max_frac = cms.double(0.7),
                                       min_sig = cms.double(2),
                                       max_new_chi2dof = cms.double(10),
                                       debug = cms.untracked.bool(False),
                                       )

mfvTrackVertexArbitratorShared   = mfvTrackVertexArbitrator  .clone(secondaryVertices = 'mfvVertexMergerShared')
mfvInclusiveMergedVerticesShared = mfvInclusiveMergedVertices.clone(secondaryVertices = 'mfvTrackVertexArbitratorShared')

mfvVertexReco = cms.Sequence(goodOfflinePrimaryVertices *
                             mfvInclusiveVertexFinder *
                             mfvVertexMerger *
                             mfvTrackVertexArbitrator *
                             mfvInclusiveMergedVertices *
                             mfvVertexMergerShared *
                             mfvTrackVertexArbitratorShared *
                             mfvInclusiveMergedVerticesShared
                             )

def get_all(process, suffix):
    modules = 'mfvInclusiveVertexFinder mfvVertexMerger mfvTrackVertexArbitrator mfvInclusiveMergedVertices mfvVertexMergerShared mfvTrackVertexArbitratorShared mfvInclusiveMergedVerticesShared'.split()
    return [(name + suffix, getattr(process, name)) for name in modules]

def clone_all(process, suffix):
    objs = []
    for i, (module, orig_obj) in enumerate(get_all(process, '')):
        obj = orig_obj.clone()
        if i > 0:
            obj.secondaryVertices = obj.secondaryVertices.value() + suffix
        objs.append(obj)
        setattr(process, module + suffix, obj)
    seq_obj = cms.Sequence(process.goodOfflinePrimaryVertices * reduce(lambda x,y: x*y, objs))
    setattr(process, 'mfvVertexReco' + suffix, seq_obj)
    objs.append(seq_obj)
    return objs
