import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['file:qcdht1000.root']
process.source.noEventSort = cms.untracked.bool(True)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
process.TFileService.fileName = 'one2two.root'
report_every(100)

add_analyzer('MFVOne2Two',
             filename = cms.string(''),
             event_src = cms.InputTag('mfvEvent'),
             vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
             wrep = cms.bool(True),
             )

for arg in sys.argv:
    if arg.endswith('.vertices') and os.path.isfile(arg):
        process.source = cms.Source('EmptySource')
        process.maxEvents.input = 0
        process.MFVOne2Two.filename = arg
