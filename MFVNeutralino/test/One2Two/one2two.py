from JMTucker.Tools.BasicAnalyzer_cfg import *

process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
process.source.fileNames = ['/store/user/tucker/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/mfvminintuple_v18/59dbce4c4744ce2cb534302fb0e499de/merged.root']
process.source.noEventSort = cms.untracked.bool(True)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
process.TFileService.fileName = 'one2two.root'
report_every(100)

add_analyzer('MFVOne2Two',
             event_src = cms.InputTag('mfvEvent'),
             vertex_src = cms.InputTag('mfvSelectedVerticesTight')
             )
