import FWCore.ParameterSet.Config as cms

QuarterMCByLumi = cms.EDFilter('QuarterMCByLumi',
                                n = cms.uint32(16),
                                first = cms.bool(True),
                                second = cms.bool(False),
                                third = cms.bool(False),
                                fourth = cms.bool(False),
                                )

