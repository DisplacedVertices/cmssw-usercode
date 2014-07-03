#!/usr/bin/env python

import os, sys, FWCore.ParameterSet.Config as cms
from pprint import pprint

process = cms.Process('Merge')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:pat.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 50000

process.out = cms.OutputModule('PoolOutputModule', fileName = cms.untracked.string('merge.root'))
process.outp = cms.EndPath(process.out)

# Keeping Run/LumiSummary causes these sparse skims to be majorly
# bloated; not using them right now, so drop them. Also drop
# MEtoEDMConverter junk.
process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.inputCommands = cms.untracked.vstring('keep *', 'drop *_MEtoEDMConverter_*_*')
process.out.outputCommands = cms.untracked.vstring('keep *', 'drop LumiDetails_lumiProducer_*_*', 'drop LumiSummary_lumiProducer_*_*', 'drop RunSummary_lumiProducer_*_*')

# Also don't need per-event metadata.
process.out.dropMetaData = cms.untracked.string('ALL')

def get_input_from_argv(process):
    # Look for just a list of files in argv first.
    files = [x for x in sys.argv if x.startswith('/store') and x.endswith('.root')]
    files += ['file:%s' % x for x in sys.argv if not x.startswith('/store') and os.path.isfile(x) and x.endswith('.root')]
    name = [x for x in sys.argv if not os.path.isfile(x) and x.endswith('.root')]
    name = name[0] if name else 'merged.root'
    if not files:
        # Else, files from crab dir mode.
        from JMTucker.Tools.CRABTools import files_from_crab_dir
        try:
            crab_dir = [x for x in sys.argv if os.path.isdir(x)][0]
        except IndexError:
            raise RuntimeError('need either a list of files or a crab directory in argv!')
        files = files_from_crab_dir(crab_dir)
        name = os.path.join(crab_dir, 'res', 'merged.root')
    
    print 'Files to run over:', len(files)
    pprint(files)
    process.source.fileNames = files
    print 'Merging to', name
    process.out.fileName = name

__all__ = ['cms', 'process', 'get_input_from_argv']

if 'argv' in sys.argv:
    get_input_from_argv(process)

