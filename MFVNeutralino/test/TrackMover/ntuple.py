#!/usr/bin/env python

import sys
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

tau = 1.
version = 2
# rest are magic lines for the submitter
is_mc = True
H = False
repro = False

if version >= 3:
    # btag wp changed for rereco https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    raise ValueError('change the btag working points before running next version')

process = pat_tuple_process(None, is_mc, year, H, repro)
remove_met_filters(process)
remove_output_module(process)

tfileservice(process, 'movedtree.root')
random_dict = {}

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

for njets in 2,3:
    for nbjets in 0,1,2:
        ex = '%i%i' % (njets, nbjets)
        tracks_name = 'mfvMovedTracks' + ex
        auxes_name = 'mfvVerticesAux' + ex
        tree_name = 'mfvMovedTree' + ex

        random_dict[tracks_name] = 13068 + njets*10 + nbjets

        tracks = cms.EDProducer('MFVTrackMover',
                                tracks_src = cms.InputTag('generalTracks'),
                                primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                jets_src = cms.InputTag('selectedPatJets'),
                                min_jet_pt = cms.double(50),
                                min_jet_ntracks = cms.uint32(4),
                                b_discriminator = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
                                b_discriminator_veto = cms.double(0.46), # change to 0.5426
                                b_discriminator_tag = cms.double(0.935), #   "     " 0.9535
                                njets = cms.uint32(njets),
                                nbjets = cms.uint32(nbjets),
                                tau = cms.double(tau),
                                sig_theta = cms.double(0.2),
                                sig_phi = cms.double(0.2),
                                )

        modifiedVertexSequence(process, ex, track_src = tracks_name)

        tree = cms.EDAnalyzer('MFVMovedTracksTreer',
                              event_src = cms.InputTag('mfvEvent'),
                              weight_src = cms.InputTag('mfvWeight'),
                              mover_src = cms.string(tracks_name),
                              vertices_src = cms.InputTag(auxes_name),
                              max_dist2move = cms.double(0.02),
                              apply_presel = cms.bool(True),
                              njets_req = cms.uint32(njets),
                              nbjets_req = cms.uint32(nbjets),
                              for_mctruth = cms.bool(False),
                              )

        setattr(process, tracks_name, tracks)
        setattr(process, tree_name, tree)
        process.p *= tree

random_service(process, random_dict)

#process.options.wantSummary = True
process.maxEvents.input = 100
#file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples 

    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    samples = Samples.data_samples + [Samples.qcdht1000, Samples.qcdht1500] + Samples.qcd_hip_samples[-2:]

    set_splitting(samples, 'main', 'trackmover', data_json='../ana_2015p6.json')

    modify = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier)

    ex = {1.: '', 0.1: '_1mm', 0.03: '_300um'}[tau]
    batch_name = 'TrackMoverV%i%s' % (version, ex)
    ms = MetaSubmitter(batch_name)
    ms.common.ex = year
    ms.common.pset_modifier = modify
    ms.common.publish_name = batch_name
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
