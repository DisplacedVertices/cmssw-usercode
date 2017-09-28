#!/usr/bin/env python

import sys
from JMTucker.Tools.general import named_product, typed_from_argv
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

version = 4
cfgs = named_product(njets = [2,3],
                     nbjets = [0,1,2],
                     nsigmadxy = [4.0, 4.1],
                     btagwp = [0,1],  # old, new
                     )
# rest are magic lines for the submitter
is_mc = True
H = False
repro = False

if version >= 5:
    raise ValueError('get rid of the two btag working points before running next version')

process = pat_tuple_process(None, is_mc, year, H, repro)
remove_met_filters(process)
remove_output_module(process)

tfileservice(process, 'movedtree.root')
random_dict = {} # create after loop below gets all the seeds

process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False

import JMTucker.MFVNeutralino.EventFilter
JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p')
process.triggerFilter.HLTPaths = ['HLT_PFHT800_v*', 'HLT_PFHT900_v*']

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
from JMTucker.MFVNeutralino.Vertexer_cff import modifiedVertexSequence
process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.mfvWeight.throw_if_no_mcstat = False

for icfg, cfg in enumerate(cfgs):
    nsigmadxy_name = ('nsig%.1f' % cfg.nsigmadxy).replace('.', 'p')
    btagwp_name = 'btagold' if cfg.btagwp == 0 else 'btagnew'
    ex = '%i%i%s%s' % (cfg.njets, cfg.nbjets, nsigmadxy_name, btagwp_name)

    tracks_name = 'mfvMovedTracks' + ex
    auxes_name = 'mfvVerticesAux' + ex
    tree_name = 'mfvMovedTree' + ex

    random_dict[tracks_name] = 13068 + icfg

    if cfg.btagwp == 0:
        b_discriminator_veto = 0.46
        b_discriminator_tag = 0.935
    else:
        b_discriminator_veto = 0.5426
        b_discriminator_tag = 0.9535

    tracks = cms.EDProducer('MFVTrackMover',
                            tracks_src = cms.InputTag('generalTracks'),
                            primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                            jets_src = cms.InputTag('selectedPatJets'),
                            min_jet_pt = cms.double(50),
                            min_jet_ntracks = cms.uint32(4),
                            b_discriminator = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
                            b_discriminator_veto = cms.double(b_discriminator_veto),
                            b_discriminator_tag = cms.double(b_discriminator_tag),
                            njets = cms.uint32(cfg.njets),
                            nbjets = cms.uint32(cfg.nbjets),
                            tau = cms.double(1.),
                            sig_theta = cms.double(0.2),
                            sig_phi = cms.double(0.2),
                            )

    modifiedVertexSequence(process, ex,
                           track_src = tracks_name,
                           min_all_track_sigmadxy = cfg.nsigmadxy,
                           min_seed_track_sigmadxy = cfg.nsigmadxy)

    tree = cms.EDAnalyzer('MFVMovedTracksTreer',
                          event_src = cms.InputTag('mfvEvent'),
                          weight_src = cms.InputTag('mfvWeight'),
                          mover_src = cms.string(tracks_name),
                          vertices_src = cms.InputTag(auxes_name),
                          max_dist2move = cms.double(0.02),
                          apply_presel = cms.bool(True),
                          njets_req = cms.uint32(cfg.njets),
                          nbjets_req = cms.uint32(cfg.nbjets),
                          for_mctruth = cms.bool(False),
                          )

    setattr(process, tracks_name, tracks)
    setattr(process, tree_name, tree)
    process.p *= tree

random_service(process, random_dict)

#want_summary(process)
process.maxEvents.input = 100
file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    if year == 2015:
        samples = Samples.data_samples_2015 + [Samples.qcdht1000_2015, Samples.qcdht1500_2015]
    elif year == 2016:
        samples = Samples.data_samples + [Samples.qcdht1000, Samples.qcdht1500] + Samples.qcd_hip_samples[-2:]

    set_splitting(samples, 'main', 'trackmover', data_json='../ana_2015p6.json')

    modify = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier)

    batch_name = 'TrackMoverV%i' % version
    ms = MetaSubmitter(batch_name)
    ms.common.ex = year
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
