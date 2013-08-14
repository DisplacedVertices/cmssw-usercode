import FWCore.ParameterSet.Config as cms

pfPileUpPF = cms.EDProducer('PFPileUp',
                                    PFCandidates = cms.InputTag('particleFlow'),
                                    Vertices = cms.InputTag('goodOfflinePrimaryVertices'),
                                    Enable = cms.bool(True),
                                    checkClosestZVertex = cms.bool(True),
                                    verbose = cms.untracked.bool(False),
                                    )

pfNoPileUpPF = cms.EDProducer('TPPFCandidatesOnPFCandidates',
                                      bottomCollection = cms.InputTag('particleFlow'),
                                      topCollection = cms.InputTag('pfPileUpPF'),
                                      name = cms.untracked.string('pileUpOnPFCandidates'),
                                      enable = cms.bool(True),
                                      verbose = cms.untracked.bool(False),
                                      )

pfPileUpPFNoClosestZVertex = pfPileUpPF.clone(checkClosestZVertex = False)

pfNoPileUpPFNoClosestZVertex = pfNoPileUpPF.clone(topCollection = 'pfPileUpPFNoClosestZVertex')

mfvRedoPURemoval = cms.Sequence(pfPileUpPF * pfNoPileUpPF * pfPileUpPFNoClosestZVertex * pfNoPileUpPFNoClosestZVertex)
