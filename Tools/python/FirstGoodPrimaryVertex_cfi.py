import FWCore.ParameterSet.Config as cms

firstGoodPrimaryVertex = cms.EDFilter('JMTFirstGoodPrimaryVertex',
                                      cut = cms.bool(False),
                                      )
