import FWCore.ParameterSet.Config as cms

from SimGeneral.HepPDTESSource.pythiapdt_cfi import *

ParticleListDrawer = cms.EDAnalyzer('JMTParticleListDrawer',
                                    src = cms.InputTag('genParticles'),
                                    maxEventsToPrint = cms.untracked.int32(100),
                                    printVertex = cms.untracked.bool(True),
                                    useMessageLogger = cms.untracked.bool(False),
                                    )
