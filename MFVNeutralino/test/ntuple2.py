#!/usr/bin/env python

from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

if year == 2015:
    raise NotImplementedError("won't bother to understand 2015 miniaod")

is_mc = True
H = False
repro = False

run_n_tk_seeds = False
minitree_only = False
prepare_vis = False
keep_all = prepare_vis or False
keep_gen = False
event_filter = not keep_all and True
if len(filter(None, (run_n_tk_seeds, minitree_only, prepare_vis))) > 1:
    raise ValueError('only one of run_n_tk_seeds, minitree_only, prepare_vis allowed')

version = 'V17m'
batch_name = 'Ntuple' + version
if run_n_tk_seeds:
    batch_name += '_NTkSeeds'
if minitree_only:
    batch_name = 'MiniNtuple'  + version

####

process = basic_process('Ntuple')
report_every(process, 1000000)
#want_summary(process)
registration_warnings(process)
geometry_etc(process, which_global_tag(is_mc, year, H=False, repro=False))
random_service(process, {'mfvVertices': 1222})
tfileservice(process, 'vertex_histos.root')
input_files(process, '/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/A00610B3-00B7-E611-8546-A0000420FE80.root')
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
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'

process.selectedPatJets.src = 'slimmedJets'
process.selectedPatJets.cut = process.jtupleParams.jetCut

process.selectedPatMuons.src = 'slimmedMuons'
process.selectedPatMuons.cut = process.jtupleParams.muonCut

process.selectedPatElectrons.src = 'slimmedElectrons'
process.selectedPatElectrons.cut = process.jtupleParams.electronCut

process.mfvGenParticles.gen_particles_src = 'prunedGenParticles'
process.mfvGenParticles.last_flag_check = False

process.mfvVertices.track_src = 'mfvUnpackedCandidateTracks'

#process.mfvVerticesToJets.enable = False # have to figure out how to use daughters of slimmed jets and the map we make in UnpackedCandidateTracks
process.mfvVerticesToJets.input_is_miniaod = True
process.mfvVerticesAuxTmp.input_is_miniaod = True
process.mfvVerticesAuxPresel.input_is_miniaod = True

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
    if is_mc:
        output_commands = EventContent.MINIAODSIMEventContent.outputCommands + output_commands_nodrop
    else:
        output_commands = EventContent.MINIAODEventContent.outputCommands + output_commands_nodrop

if prepare_vis:
    process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
    process.p *= process.mfvSelectedVerticesSeq

    for x in process.mfvSelectedVerticesTight, process.mfvSelectedVerticesTightNtk3, process.mfvSelectedVerticesTightNtk4:
        x.produce_vertices = True
        x.produce_tracks = True

    process.load('JMTucker.MFVNeutralino.VertexRefitter_cfi')
    process.mfvVertexRefitsDrop0 = process.mfvVertexRefits.clone(n_tracks_to_drop = 0)
    process.mfvVertexRefitsDrop2 = process.mfvVertexRefits.clone(n_tracks_to_drop = 2)
    process.p *= process.mfvVertexRefits * process.mfvVertexRefitsDrop2 *  process.mfvVertexRefitsDrop0

    output_commands += [
        'keep *_mfvVertices_*_*',
        'keep *_mfvSelectedVerticesTight*_*_*',
        'keep *_mfvVertexRefits_*_*',
        'keep *_mfvVertexRefitsDrop2_*_*',
        'keep *_mfvVertexRefitsDrop0_*_*',
        ]

    if is_mc:
        output_commands += ['keep *_mfvGenParticles_*_*']

if run_n_tk_seeds:
    process.mfvEvent.lightweight = True
    process.out.fileName = 'ntkseeds.root'
    if run_n_tk_seeds != 'full':
        output_commands.remove('keep MFVVertexAuxs_mfvVerticesAux_*_*')
    from JMTucker.MFVNeutralino.Vertexer_cff import modifiedVertexSequence
    output_commands += ['keep VertexerPairEffs_mfvVertices_*_*']
    for n_tk_seed in 3,4,5:
        ex = '%iTkSeed' % n_tk_seed
        process.p *= modifiedVertexSequence(process, ex, n_tracks_per_seed_vertex = n_tk_seed)
        output_commands += ['keep VertexerPairEffs_mfvVertices%s_*_*' % ex]
        if run_n_tk_seeds == 'full':
            output_commands += ['keep MFVVertexAuxs_mfvVerticesAux%s_*_*' % ex]

process.out.outputCommands = output_commands

if event_filter:
    import JMTucker.MFVNeutralino.EventFilter
    JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p', event_filter=True, input_is_miniaod=True)

if minitree_only:
    del process.out
    del process.outp
    process.TFileService.fileName = 'minintuple.root'
    process.load('JMTucker.MFVNeutralino.MiniTree_cff')
    process.mfvWeight.throw_if_no_mcstat = False
    for p in process.pMiniTree, process.pMiniTreeNtk3, process.pMiniTreeNtk4, process.pMiniTreeNtk3or4:
        p.insert(0, process.pmcStat._seq)
        p.insert(0, process.p._seq)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples

    samples = [s for s in
               #Samples.data_samples +
               Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext +
               Samples.mfv_signal_samples + Samples.mfv_ddbar_samples
               if s.has_dataset('miniaod')]

    set_splitting(samples, 'miniaod', 'ntuple')

    if run_n_tk_seeds:
        samples = [s for s in samples if not s.is_signal]

    modify = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier)
    ms = MetaSubmitter(batch_name, dataset='miniaod')
    ms.common.ex = year
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
