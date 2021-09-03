#!/usr/bin/env python

from DVCode.Tools.BasicAnalyzer_cfg import *
from DVCode.Tools.CMSSWTools import file_event_from_argv
del process.TFileService

process.out = cms.OutputModule('PoolOutputModule', fileName = cms.untracked.string('pick.root'))
process.outp = cms.EndPath(process.out)

file_event_from_argv(process)
