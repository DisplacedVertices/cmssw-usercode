import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, file_event_from_argv, files_from_file

#file_event_from_argv(process)
files_from_file(process, "1600GeV_1mm_files.txt")
process.TFileService.fileName = 'simple_trigEff_1600GeV_1mm.root'

process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1219))

#import prescales
process.load('JMTucker.Tools.SimpleTriggerEfficiency_cfi')
process.SimpleTriggerEfficiency.prescale_paths  = cms.vstring()  #*prescales.prescales.keys()),
process.SimpleTriggerEfficiency.prescale_values = cms.vuint32()  #*[o for l,h,o in prescales.prescales.itervalues()]),

process.p = cms.Path(process.SimpleTriggerEfficiency)

for x in sys.argv:
    if x.startswith('process='):
        process_name = x.replace('process=', '')
        process.SimpleTriggerEfficiency.trigger_results_src = cms.InputTag('TriggerResults', '', process_name)
