import FWCore.ParameterSet.Config as cms

process = cms.Process('BasicAnalyzer')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:pat.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.TFileService = cms.Service('TFileService', fileName = cms.string('tfileservice.root'))

def add_analyzer(name, **kwargs):
    obj = cms.EDAnalyzer(name, **kwargs)
    setattr(process, name, obj)
    setattr(process, 'p' + name, cms.Path(obj))
