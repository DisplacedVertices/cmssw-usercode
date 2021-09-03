from DVCode.Tools.BasicAnalyzer_cfg import *
process.source = cms.Source('EmptySource')
process.maxEvents.input = 1
add_analyzer(process, 'MFVSizeof')

