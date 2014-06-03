import os, sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['file:ttbarhadronic.root']
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
    if os.path.isfile(arg):
        if arg.endswith('.vertices'):
            process.source = cms.Source('EmptySource')
            process.maxEvents.input = 0
            process.MFVOne2Two.filename = arg
            process.TFileService.fileName = arg.replace('.vertices', '_histos.root')
            print 'running 2nd step with', arg
            break
        elif arg.endswith('.root'):
            process.source.fileNames = ['file:' + arg]
            print 'running 1st step with', arg
            break
