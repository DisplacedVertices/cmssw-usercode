#!/usr/bin/env python

from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.Year import year
import JMTucker.MFVNeutralino.NtupleCommon as common

cmssw_settings = CMSSWSettings()
cmssw_settings.is_mc = True

event_histos = True # 'only'
run_n_tk_seeds = False
minitree_only = False
prepare_vis = False
keep_all = prepare_vis or False
keep_gen = False
event_filter = not keep_all

if len(filter(None, (run_n_tk_seeds, minitree_only, prepare_vis, event_histos == 'only'))) > 1:
    raise ValueError('only one of run_n_tk_seeds, minitree_only, prepare_vis, event_histos="only" allowed')

version = 'V20m'
batch_name = 'Ntuple' + version
if run_n_tk_seeds:
    batch_name += '_NTkSeeds'
    event_histos = False
if minitree_only:
    batch_name = 'MiniNtuple'  + version
elif not event_filter:
    batch_name += '_NoEF'
elif event_histos == 'only':
    batch_name += '_EventHistosOnly'

####

process = basic_process('Ntuple')
max_events(process, 10000)
report_every(process, 1000000)
#want_summary(process)
registration_warnings(process)
geometry_etc(process, which_global_tag(cmssw_settings))
random_service(process, {'mfvVertexTracks': 1222})
tfileservice(process, 'vertex_histos.root')
sample_files(process, 'qcdht2000_2017', 'miniaod', 1)
output_file(process, 'ntuple.root', [])
file_event_from_argv(process)

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi')
process.load('PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi')
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.PATTupleSelection_cfi')
process.load('JMTucker.MFVNeutralino.UnpackedCandidateTracks_cfi')
process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.TriggerFilter_cfi')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'

process.selectedPatJets.src = 'slimmedJets'
process.selectedPatJets.cut = process.jtupleParams.jetCut
process.selectedPatMuons.src = 'slimmedMuons'
#process.selectedPatMuons.cut = '' # process.jtupleParams.muonCut
process.selectedPatElectrons.src = 'slimmedElectrons'
#process.selectedPatElectrons.cut = '' # process.jtupleParams.electronCut

process.mfvGenParticles.gen_particles_src = 'prunedGenParticles'
process.mfvGenParticles.last_flag_check = False

process.mfvVertexTracks.tracks_src = 'mfvUnpackedCandidateTracks'

process.mfvVerticesToJets.input_is_miniaod = True
process.mfvVerticesAuxTmp.input_is_miniaod = True
process.mfvVerticesAuxPresel.input_is_miniaod = True
process.mfvEvent.input_is_miniaod = True

process.mfvEvent.gen_particles_src = 'prunedGenParticles' # no idea if this lets gen_flavor_code, gen_bquarks, gen_leptons work. I think for the latter you'd want the packed ones that have status 1 particles
process.mfvEvent.gen_jets_src = 'slimmedGenJets'
process.mfvEvent.pileup_info_src = 'slimmedAddPileupInfo'
process.mfvEvent.met_src = 'slimmedMETs'

process.p = cms.Path(process.goodOfflinePrimaryVertices *
                     process.selectedPatJets *
                     process.selectedPatMuons *
                     process.selectedPatElectrons *
                     process.mfvTriggerFloats *
                     process.mfvUnpackedCandidateTracks *
                     process.mfvVertexSequence *
                     process.mfvEvent)

output_commands = [
    'drop *',
    'keep *_mcStat_*_*',
    'keep MFVVertexAuxs_mfvVerticesAux_*_*',
    'keep MFVEvent_mfvEvent__*',
    ]

if keep_gen:
    output_commands += [
        'keep *_prunedGenParticles_*_*',
        'keep *_slimmedGenJets_*_*'
        ]

if keep_all:
    output_commands_nodrop = [x for x in output_commands if not x.strip().startswith('drop')]
    import Configuration.EventContent.EventContent_cff as EventContent
    if cmssw_settings.is_mc:
        output_commands = EventContent.MINIAODSIMEventContent.outputCommands + output_commands_nodrop
    else:
        output_commands = EventContent.MINIAODEventContent.outputCommands + output_commands_nodrop

common.prepare_vis(process, prepare_vis, output_commands, cmssw_settings)

common.run_n_tk_seeds(process, run_n_tk_seeds, output_commands)

process.out.outputCommands = output_commands

if event_filter:
    import JMTucker.MFVNeutralino.EventFilter
    JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p', event_filter=True, input_is_miniaod=True)

common.event_histos(process, event_histos)
common.minitree_only(process, minitree_only)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples

    if year == 2017:
        samples =  Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017
        samples += Samples.data_samples_2017
        samples += Samples.leptonic_samples_2017

    dataset = 'miniaod'
    #samples = [s for s in samples if s.has_dataset(dataset)]

    set_splitting(samples, dataset, 'ntuple') # , data_json=json_path('ana_2017_1pc.json')) for e.g. EventHistosOnly_1pc

    if run_n_tk_seeds:
        samples = [s for s in samples if not s.is_signal]

    def signals_no_event_filter_modifier(sample):
        to_replace = []
        if sample.is_signal:
            magic = '\x65vent_filter = not keep_all'
            to_replace.append((magic, 'event_filter = False', 'tuple template does not contain the magic string "%s"' % magic))
        return [], to_replace

    modify = chain_modifiers(is_mc_modifier, signals_no_event_filter_modifier)
    ms = MetaSubmitter(batch_name, dataset=dataset)
    ms.common.ex = year
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
