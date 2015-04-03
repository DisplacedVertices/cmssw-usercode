import FWCore.ParameterSet.Config as cms

process = cms.Process('DROPEM')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:raw.root'))

process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('raw2.root'),
    outputCommands = cms.untracked.vstring('drop *', 'keep *_*_*_DIGI2RAW'),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    splitLevel = cms.untracked.int32(0)
)
process.eout = cms.EndPath(process.out)
