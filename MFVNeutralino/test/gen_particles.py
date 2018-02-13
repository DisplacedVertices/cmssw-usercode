from JMTucker.Tools.BasicAnalyzer_cfg import *

debug = False
dataset = 'main' # 'miniaod'

tfileservice(process, 'gen_particles.root')
sample_files(process, 'mfv_ddbar_tau01000um_M1600', dataset)
max_events(process, 1000)
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.GenParticles_cff')
process.mfvGenParticles.debug = debug
process.mfvGenParticles.histos = True
#process.mfvGenParticles.last_flag_check = False
if dataset == 'miniaod':
    process.mfvGenParticles.last_flag_check = False
    process.mfvGenParticles.gen_particles_src = 'prunedGenParticles'

if debug:
    report_every(process, 1)
    process.load('JMTucker.Tools.ParticleListDrawer_cff')
    if dataset == 'miniaod':
        process.ParticleListDrawer.src = 'prunedGenParticles'
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
    samples = [s for s in samples if s.has_dataset(dataset)]
    for s in samples:
        s.datasets[dataset].split_by = 'events'
        s.datasets[dataset].events_per = 5000

    batch_name = 'GenParticlesValidCheck'
    if dataset == 'miniaod':
        batch_name += '_MiniAOD'
    ms = MetaSubmitter(batch_name, dataset)
    ms.crab.job_control_from_sample = True
    ms.submit(samples)
