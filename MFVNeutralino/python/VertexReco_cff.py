import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi import *
goodOfflinePrimaryVertices.filter = cms.bool(True)

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
                                              clusterMinAngleCosine = cms.double(0.5)
                                              ),
                                          vertexReco = cms.PSet(
                                              seccut = cms.double(3),
                                              primcut = cms.double(1.0),
                                              finder = cms.string('avr'),
                                              smoothing = cms.bool(True)
                                              ),
                                          vertexMinDLenSig = cms.double(0.5),
                                          minPt = cms.double(0.8)
                                          )

mfvVertexMerger = cms.EDProducer('VertexMerger',
                                 minSignificance = cms.double(2),
                                 secondaryVertices = cms.InputTag('mfvInclusiveVertexFinder'),
                                 maxFraction = cms.double(0.7)
                                 )

mfvTrackVertexArbitrator = cms.EDProducer('TrackVertexArbitrator',
                                          dLenFraction = cms.double(0.333),
                                          beamSpot = cms.InputTag('offlineBeamSpot'),
                                          distCut = cms.double(0.04),
                                          secondaryVertices = cms.InputTag('mfvVertexMerger'),
                                          dRCut = cms.double(0.4),
                                          primaryVertices = cms.InputTag('goodOfflinePrimaryVertices'),
                                          tracks = cms.InputTag('generalTracks'),
                                          sigCut = cms.double(5)
                                          )

mfvInclusiveMergedVertices =  cms.EDProducer('VertexMerger',
                                             minSignificance = cms.double(10.0),
                                             secondaryVertices = cms.InputTag('mfvTrackVertexArbitrator'),
                                             maxFraction = cms.double(0.2)
                                             )

mfvInclusiveMergedVerticesFiltered = cms.EDFilter('BVertexFilter',
                                                  primaryVertices = cms.InputTag('goodOfflinePrimaryVertices'),
                                                  minVertices = cms.int32(0),
                                                  useVertexKinematicAsJetAxis = cms.bool(True),
                                                  vertexFilter = cms.PSet(
                                                      distSig3dMax = cms.double(99999.9),
                                                      fracPV = cms.double(0.65),
                                                      distVal2dMax = cms.double(2.5),
                                                      useTrackWeights = cms.bool(True),
                                                      maxDeltaRToJetAxis = cms.double(0.1),
                                                      v0Filter = cms.PSet(
                                                          k0sMassWindow = cms.double(0.05)
                                                          ),
                                                      distSig2dMin = cms.double(3.0),
                                                      multiplicityMin = cms.uint32(2),
                                                      massMax = cms.double(6.5),
                                                      distSig2dMax = cms.double(99999.9),
                                                      distVal3dMax = cms.double(99999.9),
                                                      minimumTrackWeight = cms.double(0.5),
                                                      distVal3dMin = cms.double(-99999.9),
                                                      distVal2dMin = cms.double(0.01),
                                                      distSig3dMin = cms.double(-99999.9)
                                                      ),
                                                  secondaryVertices = cms.InputTag('mfvInclusiveMergedVertices')
                                                  )

mfvVertexReco = cms.Sequence(goodOfflinePrimaryVertices *
                             mfvInclusiveVertexFinder *
                             mfvVertexMerger *
                             mfvTrackVertexArbitrator *
                             mfvInclusiveMergedVertices *
                             mfvInclusiveMergedVerticesFiltered
                             )

def clone_all(process, suffix):
    modules = 'mfvInclusiveVertexFinder mfvVertexMerger mfvTrackVertexArbitrator mfvInclusiveMergedVertices mfvInclusiveMergedVerticesFiltered'.split()
    objs = []
    for module in modules:
        obj = getattr(process, module).clone()
        objs.append((module,obj))
        setattr(process, module + suffix, obj)
    seq_obj = cms.Sequence(reduce(lambda x,y: x[1]*y[1], objs, process.goodOfflinePrimaryVertices))
    setattr(process, 'mfvVertexReco' + suffix, seq_obj)
    objs.append(seq_obj)
    return objs
