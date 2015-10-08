import sys, FWCore.ParameterSet.Config as cms
from JMTucker.Tools.CMSSWTools import files_from_file, file_event_from_argv, add_analyzer as _add_analyzer

process = cms.Process('BasicAnalyzer')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:pat.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.TFileService = cms.Service('TFileService', fileName = cms.string('tfileservice.root'))

def global_tag(process, tag):
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, tag, '')

def geometry_etc(process, tag):
    global_tag(process, tag)
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
    process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
    
def add_analyzer(process, name, **kwargs):
    return _add_analyzer(process, name, **kwargs)

def report_every(process, i):
    process.MessageLogger.cerr.FwkReport.reportEvery = i

__all__ = [
    'cms',
    'process',
    'files_from_file',
    'file_event_from_argv',
    'geometry_etc',
    'global_tag',
    'add_analyzer',
    'report_every'
    ]
