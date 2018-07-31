import FWCore.ParameterSet.Config as cms

HalfMCByLumi = cms.EDFilter('HalfMCByLumi',
                            n = cms.uint32(8),
                            first = cms.bool(True),
                            )

