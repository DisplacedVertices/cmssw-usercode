import FWCore.ParameterSet.Config as cms

goodOfflinePrimaryVertices = cms.EDFilter('JMTGoodPrimaryVertices',
                                          input_is_miniaod = cms.bool(False),
                                          nfirst = cms.uint32(0),
                                          cut = cms.bool(True),
                                          )
