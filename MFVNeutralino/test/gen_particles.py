from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'mfv_ddbar_tau01000um_M1600', 'main', 1)
report_every(process, 1)
max_events(process, 10)
file_event_from_argv(process)

process.load('JMTucker.Tools.ParticleListDrawer_cff')
process.load('JMTucker.MFVNeutralino.GenParticles_cff')

process.mfvGenParticles.debug = True
#process.mfvGenParticles.last_flag_check = False

process.primaries   = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'primaries'))
process.secondaries = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'secondaries'))
process.visible     = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'visible'))

process.p = cms.Path(process.ParticleListDrawer * process.mfvGenParticles * process.primaries * process.secondaries * process.visible)
