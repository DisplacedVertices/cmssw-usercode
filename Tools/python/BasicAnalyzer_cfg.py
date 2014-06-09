import sys, FWCore.ParameterSet.Config as cms
from JMTucker.Tools.CMSSWTools import file_event_from_argv, add_analyzer as _add_analyzer

process = cms.Process('BasicAnalyzer')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:pat.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.TFileService = cms.Service('TFileService', fileName = cms.string('tfileservice.root'))

def geometry_etc(process, tag):
    process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
    process.load('Configuration.Geometry.GeometryIdeal_cff')
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
    process.GlobalTag.globaltag = tag
    process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
    
def add_analyzer(name, **kwargs):
    return _add_analyzer(process, name, **kwargs)

def report_every(i):
    process.MessageLogger.cerr.FwkReport.reportEvery = i

__all__ = [
    'cms',
    'process',
    'file_event_from_argv',
    'geometry_etc',
    'add_analyzer',
    'report_every'
    ]
