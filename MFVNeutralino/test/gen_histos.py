import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('MFVNeutralino')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:input.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('gen_histos.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                   maxEventsToPrint = cms.untracked.int32(100),
                                   src = cms.InputTag('genParticles'),
                                   printOnlyHardInteraction = cms.untracked.bool(False),
                                   useMessageLogger = cms.untracked.bool(False)
                                   )

process.printTree = cms.EDAnalyzer('ParticleTreeDrawer',
                                   src = cms.InputTag('genParticles'),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(True),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(True),
                                   )

process.GenHistos = cms.EDAnalyzer('MFVNeutralinoGenHistos',
                                   gen_src = cms.InputTag('genParticles'),
                                   gen_jet_src = cms.InputTag('ak5GenJets'),
                                   gen_met_src = cms.InputTag('genMetTrue'),
                                   )

process.p = cms.Path(process.printList * process.GenHistos)
