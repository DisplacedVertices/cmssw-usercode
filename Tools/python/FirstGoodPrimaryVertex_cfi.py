import FWCore.ParameterSet.Config as cms

firstGoodPrimaryVertex = cms.EDFilter('JMTFirstGoodPrimaryVertex',
                                      src = cms.InputTag("offlinePrimaryVertices"),
                                      cut = cms.bool(False),
                                      )
