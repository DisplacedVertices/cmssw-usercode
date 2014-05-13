#!/usr/bin/env python

import sys
from JMTucker.Tools.CMSSWTools import set_events_to_process, set_events_to_process_by_filter
from JMTucker.Tools.PATTuple_cfg import *
tuple_version = version

runOnMC = True # magic line, don't touch
debug = False
track_histos_only = False
jumble_tracks = False
require_pixel_hit = True
track_used_req = None
prepare_vis = False
keep_extra = False
keep_all = prepare_vis
process, common_seq = pat_tuple_process(runOnMC)
#set_events_to_process(process, [])
#process.source.fileNames = ['/store/mc/Summer12_DR53X/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/ACE17BB6-A20E-E211-819A-00266CF9B630.root']

no_skimming_cuts(process)

process.out.fileName = 'ntuple.root'
if keep_all:
    process.out.outputCommands = ['keep *']
else:
    process.out.outputCommands = [
        'drop *',
        'keep MFVEvent_mfvEvent__*',
        'keep MFVVertexAuxs_mfvVerticesAux__*',
        ]

    if keep_extra:
        process.out.outputCommands += [
            'keep recoTracks_generalTracks__*',
            'keep recoVertexs_offlinePrimaryVertices__*',
            'keep recoBeamSpot_offlineBeamSpot__*',
            'keep *_selectedPatJets*_*_*',
            'drop *_selectedPatJetsForMETtype1p2CorrPF_*_*',
            'drop *_selectedPatJetsForMETtype2CorrPF_*_*',
            'drop CaloTowers_*_*_*',
            'keep recoVertexs_mfvVertices__*',
            'keep *_mfvVerticesToJets_*_*',
            ]

    process.out.dropMetaData = cms.untracked.string('ALL')

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.p = cms.Path(common_seq * process.mfvVertexSequence)

if jumble_tracks:
    process.mfvVertices.jumble_tracks = True
    process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService', mfvVertices = cms.PSet(initialSeed = cms.untracked.uint32(1219)))

if require_pixel_hit:
    process.mfvVertices.min_all_track_npxhits = 1

if track_used_req == 'nopv':
    process.mfvVertices.use_tracks = False
    process.mfvVertices.use_non_pv_tracks = True
elif track_used_req == 'nopvs':
    process.mfvVertices.use_tracks = False
    process.mfvVertices.use_non_pvs_tracks = True

if keep_all:
    process.mfvEvent.skip_event_filter = ''
    process.mfvSelectedVerticesTight.produce_vertices = True
    process.mfvSelectedVerticesTightLargeErr.produce_vertices = True
else:
    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.triggerFilter = hltHighLevel.clone()
    process.triggerFilter.HLTPaths = ['HLT_QuadJet50_v*']
    process.triggerFilter.andOr = True # = OR
    for name, path in process.paths.items():
        if not name.startswith('eventCleaning'):
            path.insert(0, process.triggerFilter)
    process.ptrig = cms.Path(process.triggerFilter)
    process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('ptrig'))

del process.outp
process.outp = cms.EndPath(process.mfvEvent * process.out)

# We're not saving the PAT branches, but if the embedding is on then
# we can't match leptons by track to vertices.
process.patMuonsPF.embedTrack = False
process.patElectronsPF.embedTrack = False

if prepare_vis:
    process.load('JMTucker.MFVNeutralino.VertexRefitter_cfi')
    process.mfvVertexRefitsDrop2 = process.mfvVertexRefits.clone(n_tracks_to_drop = 2)
    process.mfvVertexRefitsLargeErr = process.mfvVertexRefits.clone(vertex_src = 'mfvSelectedVerticesTightLargeErr')
    process.mfvVertexRefitsLargeErrDrop2 = process.mfvVertexRefits.clone(vertex_src = 'mfvSelectedVerticesTightLargeErr', n_tracks_to_drop = 2)
    process.p *= process.mfvVertexRefits * process.mfvVertexRefitsDrop2 * process.mfvVertexRefitsLargeErr * process.mfvVertexRefitsLargeErrDrop2

    process.mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                             gen_src = cms.InputTag('genParticles'),
                                             print_info = cms.bool(True),
                                             )

    process.load('JMTucker.Tools.ParticleListDrawer_cff')
    process.pp = cms.Path(process.mfvGenParticles * process.ParticleListDrawer)


if 'histos' in sys.argv or track_histos_only:
    process.TFileService = cms.Service('TFileService', fileName = cms.string('ntuple_histos.root'))
    process.mfvVertices.histos = True
    process.mfvVerticesToJets.histos = True

if track_histos_only:
    process.mfvVertices.track_histos_only = True
    del process.out
    del process.outp

if 'test' in sys.argv:
    process.source.fileNames = [
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_2_2_vbl.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_3_2_yEE.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_4_1_vkj.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_5_3_Tce.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_6_1_a0t.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_7_2_Qv8.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_8_1_3WZ.root',
        '/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_9_1_ANl.root',
    ]
    process.maxEvents.input = 100
    input_is_pythia8(process)
    re_pat(process)
    process.mfvEvent.cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT2')

if debug:
    run_events_fn = 'events_to_debug.txt'
    set_events_to_process_by_filter(process, run_events_fn=run_events_fn)
    process.mfvVertices.histos = True
    process.mfvVertices.verbose = True
    process.mfvVertices.phitest = True
    process.TFileService = cms.Service('TFileService', fileName = cms.string('vertexer_debug.root'))

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.SampleFiles import SampleFiles

    def modify(sample):
        to_add = []
        to_replace = []

        if sample.is_mc:
            if sample.is_fastsim:
                to_add.append('input_is_fastsim(process)')
            if sample.is_pythia8:
                to_add.append('input_is_pythia8(process)')
            if sample.re_pat:
                to_add.append('re_pat(process)')
        else:
            magic = 'runOnMC = True'
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'runOnMC = False', err))

        if sample.is_mc and sample.re_pat:
            to_add.append("process.mfvEvent.cleaning_results_src = cms.InputTag('TriggerResults', '', 'PAT2')") # JMTBAD rework re_pat

        return to_add, to_replace


    batch_name_extra = ''

    if jumble_tracks:
        batch_name_extra += '_JumbleTks'

    if not require_pixel_hit:
        batch_name_extra += '_WOPixel'

    if track_used_req == 'nopv':
        batch_name_extra += '_NoPVTks'
    elif track_used_req == 'nopvs':
        batch_name_extra += '_NoPVsTks'

    if keep_extra:
        batch_name_extra += '_WExtra'
    elif prepare_vis:
        batch_name_extra += '_WVis'
    elif keep_all:
        batch_name_extra += '_WAll'

    if track_histos_only:
        batch_name_extra += '_TrackHistosOnly'

    if debug:
        batch_name_extra += '_WDebug'


    cs = CRABSubmitter('MFVNtuple' + tuple_version.upper() + batch_name_extra,
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       publish_data_name = 'mfvntuple_' + tuple_version + batch_name_extra.lower(),
                       #manual_datasets = SampleFiles['mfv300s'],
                       max_threads = 3,
                       #USER_additional_input_files = run_events_fn,
                       )


    timing = { 'dyjetstollM10': 0.011203, 'dyjetstollM50': 0.019867, 'qcdbce020': 0.008660, 'qcdbce030': 0.007796, 'qcdbce080': 0.061260, 'qcdbce170': 0.328891, 'qcdbce250': 0.481813, 'qcdbce350': 0.519482, 'qcdem020': 0.010137, 'qcdem030': 0.01, 'qcdem080': 0.037925, 'qcdem170': 0.286123, 'qcdem250': 0.471398, 'qcdem350': 0.686303, 'qcdht0100': 0.008273, 'qcdht0250': 0.116181, 'qcdht0500': 0.738374, 'qcdht1000': 1.002745, 'qcdmu0020': 0.012301, 'qcdmu0030': 0.015762, 'qcdmu0050': 0.018178, 'qcdmu0080': 0.119300, 'qcdmu0120': 0.245562, 'qcdmu0170': 0.32, 'qcdmu0300': 0.419818, 'qcdmu0470': 0.584266, 'qcdmu0600': 0.455305, 'qcdmu0800': 0.879171, 'qcdmu1000': 1.075712, 'singletop_s': 0.093429, 'singletop_s_tbar': 0.146642, 'singletop_tW': 0.327386, 'singletop_tW_tbar': 0.184349, 'singletop_t': 0.092783, 'singletop_t_tbar': 0.060983, 'ttbarhadronic': 0.752852, 'ttbarsemilep': 0.419073, 'ttbardilep': 0.295437, 'ttgjets': 0.861987, 'ttwjets': 0.714156, 'ttzjets': 0.827464, 'wjetstolnu': 0.010842, 'ww': 0.046754, 'wz': 0.049839, 'zz': 0.059791, }
    timing.update({ 'qcdpt0000': 0.005460, 'qcdpt0005': 0.008174, 'qcdpt0015': 0.007915, 'qcdpt0030': 0.014118, 'qcdpt0050': 0.011146, 'qcdpt0080': 0.040685, 'qcdpt0120': 0.141580, 'qcdpt0170': 0.374554, 'qcdpt0300': 0.509502, 'qcdpt0470': 0.830390, 'qcdpt0600': 0.996345, 'qcdpt0800': 0.428342, 'qcdpt1000': 0.546948, 'qcdpt1400': 0.544585, 'qcdpt1800': 2.078266, })
    timing.update({ 'bjetsht0100': 0.008273, 'bjetsht0250': 0.116181, 'bjetsht0500': 0.738374, 'bjetsht1000': 1.002745, })
    timing.update({ 'myttbarpythia': 0.752852, 'myttbarpynopu': 0.25, 'myttbarpydesignnopu': 0.25 })

    for sample in Samples.all_mc_samples:
        if timing.has_key(sample.name):
            sample.events_per = int(3.5*3600/timing[sample.name])
            sample.timed = True
            nj = int(sample.nevents_orig / float(sample.events_per)) + 1
            assert nj < 5000

    for s in Samples.mfv_signal_samples:
        s.events_per = 500
        s.timed = True


    x = Samples.mfv_signal_samples
    Samples.mfv_signal_samples = []
    Samples.mfv300 = []
    for y in x:
        if '300' in y.name:
            Samples.mfv300.append(y)
        else:
            Samples.mfv_signal_samples.append(y)

    
    if 'smaller' in sys.argv:
        samples = Samples.smaller_background_samples
    elif 'leptonic' in sys.argv:
        samples = Samples.leptonic_background_samples
    elif 'qcdpt' in sys.argv:
        samples = [s for s in Samples.auxiliary_background_samples if s.name.startswith('qcdpt')]
    elif 'bjets' in sys.argv:
        samples = [s for s in Samples.auxiliary_background_samples if s.name.startswith('bjets')]
    elif 'qcdlep' in sys.argv:
        samples = []
        for s in Samples.auxiliary_background_samples:
            if (s.name != 'qcdmupt15' and 'qcdmu' in s.name) or 'qcdem' in s.name or 'qcdbce' in s.name:
                samples.append(s)
    elif 'data' in sys.argv:
        samples = Samples.data_samples
        for sample in samples:
            sample.json = 'ana_5pc.json'
    elif 'auxdata' in sys.argv:
        samples = Samples.auxiliary_data_samples
    elif '100k' in sys.argv:
        samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples
    elif 'few' in sys.argv:
        samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400, Samples.ttbarhadronic, Samples.qcdht1000]
    elif 'mfv300' in sys.argv:
        samples = Samples.mfv300
    elif 'tthad' in sys.argv:
        samples = [Samples.ttbarhadronic]
    elif 'signal' in sys.argv:
        samples = Samples.mfv_signal_samples
    elif 'myttbar' in sys.argv:
        samples = [Samples.myttbarpynopu] #Samples.myttbar_samples
    else:
        samples = Samples.mfv_signal_samples + Samples.ttbar_samples + Samples.qcd_samples


    for sample in samples:
        if sample.is_mc:
            sample.total_events = -1
            assert hasattr(sample, 'timed')


    cs.submit_all(samples)
