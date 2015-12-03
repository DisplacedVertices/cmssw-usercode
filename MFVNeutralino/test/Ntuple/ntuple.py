#!/usr/bin/env python

import sys
from JMTucker.Tools.CMSSWTools import cms, basic_process, geometry_etc, output_file, registration_warnings, set_events_to_process
from JMTucker.Tools.MiniAOD_cfg import global_tag

version = 'v5'

is_mc = True # magic line, don't touch
debug = False
track_histos = False
track_histos_only = False
jumble_tracks = False
remove_tracks = None
track_used_req = None
prepare_vis = False
keep_all = prepare_vis
keep_gen = False
trig_filter = not keep_all

process = basic_process('MFVNtuple')
process.source.fileNames = ['/store/user/tucker/F47E7F59-8A29-E511-8667-002590A52B4A.miniaod100evt.root']
process.source.fileNames = ['file:pat.root']
process.source.fileNames = ['file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/pat.root']
#process.source.fileNames = ['/store/mc/RunIISpring15DR74/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v2/20000/02A00874-7327-E511-B735-0025905964C0.root']
#process.source.fileNames = ['/store/user/tucker/F0BC6027-D801-E511-B122-0CC47A13CCFC.root']
#process.source.fileNames = ['/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/00B2F04A-E301-E511-8CF3-0025905A6090.root']
#set_events_to_process(process, [(1, 149765, 37404137)])
#process.maxEvents.input = 50
#process.options.wantSummary = True

registration_warnings(process)
geometry_etc(process, global_tag(is_mc))

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')

process.p = cms.Path(process.mfvVertexSequence * process.mfvEvent)

output_commands = [
    'drop *',
    'keep *_mcStat_*_*',
    'keep MFVVertexAuxs_mfvVerticesAux_*_*',
    'keep MFVEvent_mfvEvent__*',
    'keep edmTriggerResults_TriggerResults__HLT',
    'keep edmTriggerResults_TriggerResults__PAT',
    ]
output_file(process, 'ntuple.root', output_commands)

if keep_all:
    if is_mc:
        process.out.outputCommands += \
            process.AODSIMEventContent.outputCommands + \
            process.MINIAODSIMEventContent.outputCommands
    else:
        process.out.outputCommands += \
            process.AODEventContent.outputCommands + \
            process.MINIAODEventContent.outputCommands
elif is_mc and keep_gen:
    process.out.outputCommands += ['keep recoGenParticles_genParticles__*']

if prepare_vis:
    process.mfvVertices.write_tracks = True
    process.mfvSelectedVerticesTight.produce_vertices = True
    process.mfvSelectedVerticesTight.produce_tracks = True
    process.mfvSelectedVerticesTightLargeErr.produce_vertices = True
    process.mfvSelectedVerticesTightLargeErr.produce_tracks = True

    process.load('JMTucker.MFVNeutralino.VertexRefitter_cfi')
    process.mfvVertexRefitsDrop0 = process.mfvVertexRefits.clone(n_tracks_to_drop = 0)
    process.mfvVertexRefitsDrop2 = process.mfvVertexRefits.clone(n_tracks_to_drop = 2)
    process.mfvVertexRefitsLargeErr = process.mfvVertexRefits.clone(vertex_src = 'mfvSelectedVerticesTightLargeErr')
    process.mfvVertexRefitsLargeErrDrop2 = process.mfvVertexRefits.clone(vertex_src = 'mfvSelectedVerticesTightLargeErr', n_tracks_to_drop = 2)
    process.p *= process.mfvVertexRefits * process.mfvVertexRefitsDrop2 *  process.mfvVertexRefitsDrop0 * process.mfvVertexRefitsLargeErr * process.mfvVertexRefitsLargeErrDrop2

    if is_mc:
        process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                                 gen_src = cms.InputTag('genParticles'),
                                                 print_info = cms.bool(True),
                                                 )
        process.load('JMTucker.Tools.ParticleListDrawer_cff')
        process.p *= process.mfvGenParticles * process.ParticleListDrawer



if jumble_tracks:
    process.mfvVertices.jumble_tracks = True
    process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService', mfvVertices = cms.PSet(initialSeed = cms.untracked.uint32(1219)))

if remove_tracks:
    process.mfvVertices.remove_tracks_frac = remove_tracks[0]
    process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService', mfvVertices = cms.PSet(initialSeed = cms.untracked.uint32(1219 + remove_tracks[1])))

if track_used_req == 'nopv':
    process.mfvVertices.use_tracks = False
    process.mfvVertices.use_non_pv_tracks = True
elif track_used_req == 'nopvs':
    process.mfvVertices.use_tracks = False
    process.mfvVertices.use_non_pvs_tracks = True

if track_histos or track_histos_only:
    process.TFileService = cms.Service('TFileService', fileName = cms.string('ntuple_histos.root'))
    process.mfvVertices.histos = True
    process.mfvVerticesToJets.histos = True

if track_histos_only:
    process.mfvVertices.track_histos_only = True
    del process.out
    del process.outp

if debug:
    run_events_fn = 'events_to_debug.txt'
    set_events_to_process_by_filter(process, run_events_fn=run_events_fn)
    process.mfvVertices.histos = True
    process.mfvVertices.verbose = True
    process.mfvVertices.phitest = True
    process.TFileService = cms.Service('TFileService', fileName = cms.string('vertexer_debug.root'))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    from JMTucker.Tools.Sample import anon_samples
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.ttbar_samples + Samples.qcd_samples + [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]

    def modify(sample):
        to_add = []
        to_replace = []

        if sample.is_mc:
            if sample.is_fastsim:
                raise NotImplementedError('zzzzzzz')
        else:
            magic = 'is_mcX=XTrue'.replace('X', ' ') # really stupid way to get the checking code in to_replace business to not find the string here...
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))
            # JMTBAD different globaltags?

        return to_add, to_replace

    batch_name = 'Ntuple' + version.upper()

    #batch_name += '_DeleteMe_ForTiming'

    if jumble_tracks:
        batch_name += '_JumbleTks'

    if remove_tracks:
        batch_name += '_RemoveTks%i' % remove_tracks[1]

    if track_used_req == 'nopv':
        batch_name += '_NoPVTks'
    elif track_used_req == 'nopvs':
        batch_name += '_NoPVsTks'

    if prepare_vis:
        batch_name += '_WVis'
    elif keep_all:
        batch_name += '_WAll'

    if track_histos_only:
        batch_name += '_TrackHistosOnly'

    if debug:
        batch_name += '_WDebug'


    cs = CRABSubmitter(batch_name,
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       publish_name = batch_name.lower(),
                       )

#    timing = { 'dyjetstollM10': 0.011203, 'dyjetstollM50': 0.019867, 'qcdbce020': 0.008660, 'qcdbce030': 0.007796, 'qcdbce080': 0.061260, 'qcdbce170': 0.328891, 'qcdbce250': 0.481813, 'qcdbce350': 0.519482, 'qcdem020': 0.010137, 'qcdem030': 0.01, 'qcdem080': 0.037925, 'qcdem170': 0.286123, 'qcdem250': 0.471398, 'qcdem350': 0.686303, 'qcdht0100': 0.008273, 'qcdht0250': 0.116181, 'qcdht0500': 0.738374, 'qcdht1000': 1.002745, 'qcdmu0020': 0.012301, 'qcdmu0030': 0.015762, 'qcdmu0050': 0.018178, 'qcdmu0080': 0.119300, 'qcdmu0120': 0.245562, 'qcdmu0170': 0.32, 'qcdmu0300': 0.419818, 'qcdmu0470': 0.584266, 'qcdmu0600': 0.455305, 'qcdmu0800': 0.879171, 'qcdmu1000': 1.075712, 'singletop_s': 0.093429, 'singletop_s_tbar': 0.146642, 'singletop_tW': 0.327386, 'singletop_tW_tbar': 0.184349, 'singletop_t': 0.092783, 'singletop_t_tbar': 0.060983, 'ttbarhadronic': 0.752852, 'ttbarsemilep': 0.419073, 'ttbardilep': 0.295437, 'ttgjets': 0.861987, 'ttwjets': 0.714156, 'ttzjets': 0.827464, 'wjetstolnu': 0.010842, 'ww': 0.046754, 'wz': 0.049839, 'zz': 0.059791, }
#    timing.update({ 'qcdpt0000': 0.005460, 'qcdpt0005': 0.008174, 'qcdpt0015': 0.007915, 'qcdpt0030': 0.014118, 'qcdpt0050': 0.011146, 'qcdpt0080': 0.040685, 'qcdpt0120': 0.141580, 'qcdpt0170': 0.374554, 'qcdpt0300': 0.509502, 'qcdpt0470': 0.830390, 'qcdpt0600': 0.996345, 'qcdpt0800': 0.428342, 'qcdpt1000': 0.546948, 'qcdpt1400': 0.544585, 'qcdpt1800': 2.078266, })
#    timing.update({ 'bjetsht0100': 0.008273, 'bjetsht0250': 0.116181, 'bjetsht0500': 0.738374, 'bjetsht1000': 1.002745, })
#    timing.update(dict((s.name, 0.752852) for s in Samples.myttbar_samples + Samples.ttbar_systematics_samples))
#    timing.update({ 'myttbarpynopu': 0.25, 'myttbarpydesignnopu': 0.25 })
#    
#    for sample in Samples.all_mc_samples:
#        if timing.has_key(sample.name):
#            sample.events_per = int(3.5*3600/timing[sample.name])
#            sample.timed = True
#            nj = int(sample.nevents_orig / float(sample.events_per)) + 1
#            assert nj < 5000
#
#    for s in Samples.mfv_signal_samples + Samples.mfv_signal_samples_systematics + Samples.exo12038_samples:
#        s.events_per = 2000
#        s.timed = True
#
#    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
#                                 Samples.mfv_neutralino_tau1000um_M0400,
#                                 Samples.mfv_neutralino_tau0300um_M0400,
#                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples + Samples.data_samples)
#
#    for sample in samples:
#        if sample.is_mc:
#            sample.total_events = -1
#            assert hasattr(sample, 'timed')
#        else:
#            sample.json = 'ana_all.json'

    cs.submit_all(samples)
