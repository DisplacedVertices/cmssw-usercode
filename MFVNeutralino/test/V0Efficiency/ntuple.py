from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.zerobias = False
assert not settings.zerobias # need to check trigger/event filter
settings.event_filter = 'trigger jets only'

version = settings.version + 'V1'

debug = False

####

process = ntuple_process(settings)
remove_tfileservice(process)
max_events(process, 10000)
report_every(process, 1000000)
#want_summary(process)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'qcdht1500_2017' if settings.is_mc else 'JetHT2017F', dataset, 1)
file_event_from_argv(process)

####

process.load('JMTucker.Tools.FirstGoodPrimaryVertex_cfi')
if settings.is_miniaod:
    process.firstGoodPrimaryVertex.src = 'offlineSlimmedPrimaryVertices'
process.firstGoodPrimaryVertex.cut = True

process.load('JMTucker.MFVNeutralino.SkimmedTracks_cfi')
process.mfvSkimmedTracks.min_pt = 1
process.mfvSkimmedTracks.min_dxybs = 0
process.mfvSkimmedTracks.min_nsigmadxybs = 3
process.mfvSkimmedTracks.tracks_src = 'mfvUnpackedCandidateTracks' if settings.is_miniaod else 'generalTracks'
process.mfvSkimmedTracks.input_is_miniaod = settings.is_miniaod
process.mfvSkimmedTracks.cut = True

process.load('JMTucker.MFVNeutralino.V0Vertexer_cff')
process.mfvV0Vertices.cut = True

if debug:
    if settings.is_miniaod:
        process.mfvUnpackedCandidateTracks.debug = True
    process.mfvSkimmedTracks.debug = True
    process.mfvV0Vertices.debug = True

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')

process.p = cms.Path(process.mfvEventFilterSequence * process.firstGoodPrimaryVertex * process.mfvV0Vertices * process.mfvTriggerFloats)

if settings.is_mc and not settings.is_miniaod:
    process.load('PhysicsTools.PatAlgos.slimming.slimmedAddPileupInfo_cfi')
    process.p *= process.slimmedAddPileupInfo

process.out.outputCommands = [
    'drop *',
    'keep *_mcStat_*_*',
    'keep *_mfvSkimmedTracks_*_*',
    'keep *_mfvV0Vertices_*_*',
    'keep *_mfvTriggerFloats_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_slimmedAddPileupInfo_*_*',
    'keep *_firstGoodPrimaryVertex_*_*',
    'keep *_TriggerResults_*_HLT', # for ZeroBias since I don't wanna mess with MFVTriggerFloats for it
    ]

if settings.zerobias:
    process.mfvTriggerFilter.HLTPaths.append('HLT_ZeroBias_v*') # what are the ZeroBias_part* paths?

ReferencedTagsTaskAdder(process)('p')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.data_samples_2017 + Samples.ttbar_samples_2017 + Samples.qcd_samples_2017
        #samples += [s for s in Samples.auxiliary_data_samples_2017 if s.name.startswith('ZeroBias')]
    elif year == 2018:
        samples = Samples.data_samples_2018 + [s for s in Samples.auxiliary_data_samples_2018 if s.name.startswith('ReRecoJetHT')]
        #samples += [s for s in Samples.auxiliary_data_samples_2018 if s.name.startswith('ZeroBias')]

    #samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8_1pc.json'))

    ms = MetaSubmitter('V0Ntuple' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, zerobias_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
