import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('ParticleListDrawer')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(''))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.ParticleListDrawer = cms.EDAnalyzer('ParticleListDrawer',
                                            maxEventsToPrint = cms.untracked.int32(1000000),
                                            src = cms.InputTag('genParticles'),
                                            printOnlyHardInteraction = cms.untracked.bool(True),
                                            useMessageLogger = cms.untracked.bool(False)
                                            )
process.p = cms.Path(process.ParticleListDrawer)

process.source.fileNames = [x.strip() for x in open('infiles.txt') if x.strip()]
