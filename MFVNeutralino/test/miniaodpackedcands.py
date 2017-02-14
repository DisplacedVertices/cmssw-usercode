from JMTucker.Tools.BasicAnalyzer_cfg import *

geometry_etc(process, '80X_dataRun2_2016SeptRepro_v4')
add_analyzer(process, 'MFVPackedCandidates')

process.source.fileNames = ['/store/user/tucker/JetHT2016H2.MiniAOD.9C0A2FFD-B886-E611-BEA7-02163E011B30.root']
process.source.secondaryFileNames = cms.untracked.vstring('/store/user/tucker/JetHT2016H2.8AAACEA3-B786-E611-953E-02163E013547.root')

from FWCore.PythonUtilities.LumiList import LumiList
process.source.lumisToProcess = LumiList('test.json').getVLuminosityBlockRange()

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)
