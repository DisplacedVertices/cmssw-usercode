import FWCore.ParameterSet.Config as cms

process = cms.Process('check')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(''))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.ParticleListDrawer = cms.EDAnalyzer('ParticleListDrawer',
                                            maxEventsToPrint = cms.untracked.int32(100),
                                            src = cms.InputTag('genParticles'),
                                            printOnlyHardInteraction = cms.untracked.bool(False),
                                            useMessageLogger = cms.untracked.bool(False)
                                            )
process.p = cms.Path(process.ParticleListDrawer)
