from JMTucker.Tools.BasicAnalyzer_cfg import *

remove_tfileservice(process)
report_every(process, 1)
file_event_from_argv(process)

process.load('JMTucker.Tools.ParticleListDrawer_cff')
process.ParticleListDrawer.maxEventsToPrint = -1
process.p = cms.Path(process.ParticleListDrawer)

if 'miniaod' in sys.argv or False:
    process.ParticleListDrawer.src = 'prunedGenParticles'
