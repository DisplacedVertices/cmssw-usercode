from JMTucker.Tools.BasicAnalyzer_cfg import *

import JMTucker.Tools.SampleFiles as sf
#sf.set_process(process, 'qcdht2000', 'main', 4)
sf.set_process(process, 'testqcdht2000', 'main')
process.TFileService.fileName = 'genparticle_histos.root'

add_analyzer(process, 'JMTGenParticleHistos', src = cms.InputTag('genParticles'))

process.maxEvents.input = 11688

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
