import FWCore.ParameterSet.Config as cms
process = cms.Process('dummy')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('EmptySource')
