#!/usr/bin/env python

import os, sys, FWCore.ParameterSet.Config as cms
from pprint import pprint

process = cms.Process('Merge')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:pat.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 500

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
    from JMTucker.Tools.general import typed_from_argv

    # Look for just a list of files in argv first.
    def leave_alone(x):
        return x.startswith('/store') or x.startswith('root://')
    files = [x for x in sys.argv if leave_alone(x) and x.endswith('.root')]
    files += ['file:%s' % x for x in sys.argv if not leave_alone(x) and os.path.isfile(x) and x.endswith('.root')]

    if not files:
        # else, files from txt file
        list_fn = os.path.expanduser(typed_from_argv(str, name='list'))
        if list_fn is None:
            raise ValueError('no files to run on')
        files = [x.strip() for x in open(list_fn).read().split() if x.strip()]
    
    print 'Files to run over:', len(files)
    pprint(files)
    process.source.fileNames = files

    process.out.fileName = 'merged.root'
    out = typed_from_argv(str, name='out')
    if out is not None:
        process.out.fileName = os.path.expanduser(out)
    print 'Merging to', process.out.fileName.value()

    max_events = typed_from_argv(int, name='max_events')
    if max_events is not None:
        print 'Max events =', max_events
        process.maxEvents.input = max_events
    skip_events = typed_from_argv(int, name='skip_events')
    if skip_events is not None:
        print 'Skip events =', skip_events
        process.source.skipEvents = cms.untracked.uint32(skip_events)

__all__ = ['cms', 'process', 'get_input_from_argv']

if 'argv' in sys.argv:
    get_input_from_argv(process)

