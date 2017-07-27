#!/usr/bin/env python

from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False
repro = False
run_n_tk_seeds = True
minitree_only = False
prepare_vis = False
keep_all = prepare_vis
event_filter = not keep_all
version = 'V15'
batch_name = 'Ntuple' + version
if minitree_only:
    batch_name = 'MiniNtuple'  + version
#batch_name += '_ChangeMeIfSettingsNotDefault'

####

process = pat_tuple_process(None, is_mc, year, H, repro)
remove_met_filters(process)

# speed up by 15%
#del process.packedGenParticles
#del process.prunedGenParticles
#del process.prunedGenParticlesWithStatusOne
#del process.primaryVertexAssociation
#process.patMuons.addGenMatch = False
#process.patElectrons.addGenMatch = False
#process.patJets.addGenJetMatch    = False
#process.patJets.addGenPartonMatch = False
#process.patJets.addTagInfos = False
#process.patJets.addJetCharge = False
#process.patJets.addJetFlavourInfo = False
#process.patJets.getJetMCFlavour = False
#process.patJets.discriminatorSources = ['pfCombinedInclusiveSecondaryVertexV2BJetTags']
#process.patJets.userData.userFloats.src = []
#process.patJets.userData.userFunctionLabels = []
#process.patJets.userData.userFunctions = []
#process.patJets.userData.userInts.src = []

process.out.fileName = 'ntuple.root'
output_commands = [
    'drop *',
    'keep *_mcStat_*_*',
    'keep MFVEvent_mfvEvent__*',
    'keep VertexerPairEffs_mfvVertices_*_*',
    'keep MFVVertexAuxs_mfvVerticesAux_*_*',
    ]

if run_n_tk_seeds:
    for n_tk_seed in 3,4,5:
        output_commands += [
            'keep VertexerPairEffs_mfvVertices%iTkSeed_*_*' % n_tk_seed,
            'keep MFVVertexAuxs_mfvVerticesAux%iTkSeed_*_*' % n_tk_seed,
            ]

process.out.outputCommands = output_commands

tfileservice(process, 'vertex_histos.root')
random_service(process, {'mfvVertices': 1222})

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.p = cms.Path(process.mfvVertexSequenceEx if run_n_tk_seeds else process.mfvVertexSequence)
process.p *= process.mfvTriggerFloats * process.mfvEvent

if event_filter:
    import JMTucker.MFVNeutralino.EventFilter
    JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p', event_filter=True)

if prepare_vis:
    for x in process.mfvSelectedVerticesTight, process.mfvSelectedVerticesTightNtk3, process.mfvSelectedVerticesTightNtk4:
        x.produce_vertices = True
        x.produce_tracks = True

    process.load('JMTucker.MFVNeutralino.VertexRefitter_cfi')
    process.mfvVertexRefitsDrop0 = process.mfvVertexRefits.clone(n_tracks_to_drop = 0)
    process.mfvVertexRefitsDrop2 = process.mfvVertexRefits.clone(n_tracks_to_drop = 2)
    process.p *= process.mfvSelectedVerticesSeq * process.mfvVertexRefits * process.mfvVertexRefitsDrop2 *  process.mfvVertexRefitsDrop0

    output_commands += [
        'keep *_mfvVertices_*_*',
        'keep *_mfvSelectedVerticesTight*_*_*',
        'keep *_mfvVertexRefits_*_*',
        'keep *_mfvVertexRefitsDrop2_*_*',
        'keep *_mfvVertexRefitsDrop0_*_*',
        ]

    if is_mc:
        process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                                 gen_particles_src = cms.InputTag('genParticles'),
                                                 print_info = cms.bool(True),
                                                 )
        process.p *= process.mfvGenParticles
        output_commands += ['keep *_mfvGenParticles_*_*']

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

# If the embedding is on for these, then we can't match leptons by track to vertices.
process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False

#process.options.wantSummary = True
process.maxEvents.input = 100
file_event_from_argv(process)

if minitree_only:
    remove_output_module(process)
    process.TFileService.fileName = 'minintuple.root'
    process.load('JMTucker.MFVNeutralino.MiniTree_cff')
    process.mfvWeight.throw_if_no_mcstat = False
    for p in process.pMiniTree, process.pMiniTreeNtk3, process.pMiniTreeNtk4, process.pMiniTreeNtk3or4:
        p.insert(0, process.pmcStat._seq)
        p.insert(0, process.p._seq)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    if year == 2015:
        samples = \
            Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            Samples.mfv_signal_samples_2015
    elif year == 2016:
        samples = \
            Samples.data_samples + \
            Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
            Samples.mfv_signal_samples + Samples.mfv_ddbar_samples + Samples.mfv_hip_samples + Samples.qcd_hip_samples

    if 'validation' in sys.argv:
        batch_name += '_validation'
        import JMTucker.Tools.SampleFiles as SampleFiles
        samples = [s for s in samples if SampleFiles.has(s.name, 'validation')]
        for s in samples:
            s.files_per = 100000 # let max_output_modifier handle it
    else:
        set_splitting(samples, 'main', 'ntuple')

    skips = {
        'qcdht0700ext_2015': {'lumis': '135728', 'events': '401297681'},
        'qcdht1000ext_2015': {'lumis': '32328',  'events': '108237235'},
        }

    def n_tk_seeds_modifier(sample):
        to_replace = []
        if sample.is_signal:
            magic = 'run_n_tk_seeds = True'
            to_replace.append((magic, 'run_n_tk_seeds = False', 'ntuple template does not contain the magic string "%s"' % magic))
        return [], to_replace

    modify = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier, n_tk_seeds_modifier, event_veto_modifier(skips, 'p'))
    ms = MetaSubmitter(batch_name)
    if 'validation' in sys.argv:
        modify.append(max_output_modifier(500))
        ms.common.dataset = 'validation'
    ms.common.ex = year
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
