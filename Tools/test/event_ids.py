import FWCore.ParameterSet.Config as cms

process = cms.Process('EventIdRecorder')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(''))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.TFileService = cms.Service('TFileService', fileName = cms.string('eid.root'))

process.source.fileNames = files = [x.strip() for x in open('infiles.txt') if x.strip()]

process.eid = cms.EDAnalyzer('EventIdRecorder', notes = cms.string('\n'.join(files))
process.p = cms.Path(process.eid)
