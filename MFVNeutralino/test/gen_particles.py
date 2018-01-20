from JMTucker.Tools.BasicAnalyzer_cfg import *

debug = False

tfileservice(process, 'gen_particles.root')
sample_files(process, 'mfv_ddbar_tau01000um_M1600', 'main', 1)
max_events(process, 10)
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
process.mfvGenParticles.debug = debug
process.mfvGenParticles.histos = True
#process.mfvGenParticles.last_flag_check = False

if debug:
    report_every(process, 1)
    process.load('JMTucker.Tools.ParticleListDrawer_cff')
    process.primaries   = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'primaries'))
    process.secondaries = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'secondaries'))
    process.visible     = process.ParticleListDrawer.clone(src = cms.InputTag('mfvGenParticles', 'visible'))
    process.p = cms.Path(process.ParticleListDrawer * process.mfvGenParticles * process.primaries * process.secondaries * process.visible)
else:
    process.p = cms.Path(process.mfvGenParticles)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples

    samples = Samples.mfv_signal_samples + Samples.mfv_ddbar_samples + Samples.mfv_bbbar_samples
    for s in samples:
        s.split_by = 'events'
        s.events_per = 5000

    ms = MetaSubmitter('GenParticlesValidCheck')
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
