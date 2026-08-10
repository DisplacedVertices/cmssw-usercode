from JMTucker.Tools.BasicAnalyzer_cfg import *

process.TFileService.fileName = 'duplicate_gens.root'
file_event_from_argv(process)

add_analyzer(process, 'JMTDuplicateGenEventChecker')
