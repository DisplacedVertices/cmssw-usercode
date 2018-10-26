#!/usr/bin/env python

from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.MiniAOD_cfg import *
import JMTucker.MFVNeutralino.NtupleCommon as common

cmssw_settings = CMSSWSettings()
cmssw_settings.is_mc = True

event_histos = True # 'only'
run_n_tk_seeds = False
minitree_only = False
prepare_vis = not run_n_tk_seeds and False
keep_all = prepare_vis
keep_gen = False
event_filter = not keep_all

if len(filter(None, (run_n_tk_seeds, minitree_only, prepare_vis, event_histos == 'only'))) > 1:
    raise ValueError('only one of run_n_tk_seeds, minitree_only, prepare_vis, event_histos="only" allowed')

version = 'V20'
batch_name = 'Ntuple' + version
if minitree_only:
    batch_name = 'MiniNtuple'  + version
elif keep_gen:
    batch_name += '_WGen'
elif not event_filter:
    batch_name += '_NoEF'
elif event_histos == 'only':
    batch_name += '_EventHistosOnly'

####

process = pat_tuple_process(cmssw_settings)
remove_met_filters(process)

process.out.fileName = 'ntuple.root'
output_commands = [
    'drop *',
    'keep *_mcStat_*_*',
    'keep MFVEvent_mfvEvent__*',
    'keep MFVVertexAuxs_mfvVerticesAux_*_*',
    ]

if keep_gen:
    output_commands += ['keep *_genParticles_*_HLT', 'keep *_ak4GenJetsNoNu_*_HLT']

tfileservice(process, 'vertex_histos.root')
random_service(process, {'mfvVertexTracks': 1222})

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.TriggerFilter_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.p = cms.Path(process.mfvVertexSequence)
process.p *= process.mfvTriggerFloats * process.mfvEvent

common.run_n_tk_seeds(process, run_n_tk_seeds, output_commands)

if event_filter:
    import JMTucker.MFVNeutralino.EventFilter
    JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p', event_filter=True)

common.prepare_vis(process, prepare_vis, output_commands, cmssw_settings)

if keep_all:
    def dedrop(l):
        return [x for x in l if not x.strip().startswith('drop')]
    if is_mc:
        process.out.outputCommands += \
            process.AODSIMEventContent.outputCommands + \
            dedrop(process.MINIAODSIMEventContent.outputCommands) + \
            dedrop(output_commands)
    else:
        process.out.outputCommands += \
            process.AODEventContent.outputCommands + \
            dedrop(process.MINIAODEventContent.outputCommands) + \
            dedrop(output_commands)
    # for some reason taus crash with this cfg in 8025, and you have to drop met too then (then have to kill it in EventProducer)
    process.mfvEvent.met_src = ''
    process.out.outputCommands = [x for x in process.out.outputCommands if 'tau' not in x.lower() and 'MET' not in x]
    for x in dir(process):
        xl = x.lower()
        if 'tau' in xl or 'MET' in x:
            delattr(process, x)
else:
    process.out.outputCommands = output_commands

# If the embedding is on for these, then we can't match leptons by track to vertices.
process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False

want_summary(process, False)
max_events(process, 1000)
file_event_from_argv(process)

common.event_histos(process, event_histos)
common.minitree_only(process, minitree_only)

associate_paths_to_task(process)

#bef, aft, diff = ReferencedTagsTaskAdder().modules_to_add('patJets', 'patMuons', 'patElectrons', 'mfvEvent')
#print 'may need to add:', ' '.join(diff)
# but remove things already in AOD

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples
    from JMTucker.Tools.Year import year

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017
        #samples += Samples.leptonic_samples_2017

    set_splitting(samples, 'main', 'ntuple')

    if run_n_tk_seeds:
        batch_name += '_NTkSeeds'
        samples = [s for s in samples if not s.is_signal]

    def signals_no_event_filter_modifier(sample):
        to_replace = []
        if sample.is_signal:
            magic = '\x65vent_filter = not keep_all'
            to_replace.append((magic, 'event_filter = False', 'tuple template does not contain the magic string "%s"' % magic))
        return [], to_replace

    modify = chain_modifiers(is_mc_modifier, signals_no_event_filter_modifier)
    ms = MetaSubmitter(batch_name)
    ms.common.ex = year
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
