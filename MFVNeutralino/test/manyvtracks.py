from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

process = ntuple_process(settings)
max_events(process, 10000)
report_every(process, 1000000)
want_summary(process)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'qcdht2000_2017' if settings.is_mc else 'JetHT2017F', dataset, 1)
file_event_from_argv(process)

process.mfvVertexTracks.min_n_seed_tracks = 35

process.p = cms.Path(process.goodOfflinePrimaryVertices *
                     process.mfvUnpackedCandidateTracks *
                     process.mfvVertexTracks)

del process.out.SelectEvents
event_filter(process, 'jets only novtx', settings, [], event_filter_jes_mult=0)

import Configuration.EventContent.EventContent_cff as ec
if settings.is_mc:
    process.out.outputCommands = ec.MINIAODSIMEventContent.outputCommands
else:
    process.out.outputCommands = ec.MINIAODEventContent.outputCommands


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.data_samples_2017 #+ Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'))

    ms = MetaSubmitter('ManyVTracks%s' % settings.version.capitalize(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
