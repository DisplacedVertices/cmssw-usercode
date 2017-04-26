#!/usr/bin/env python

import sys
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

# 4 magic lines
is_mc = True
H = False
njets = 2
nbjets = 0

ints = typed_from_argv(int, default_value=[], return_multiple=True)
if len(ints) > 0:
    if len(ints) != 2:
        raise RuntimeError('if you put any ints there must be two')
    njets, nbjets = ints


process = pat_tuple_process(None, is_mc, year, H)
remove_met_filters(process)
remove_output_module(process)

tfileservice(process, 'movedtree.root')
random_service(process, {'mfvVertices': 12179, 'mfvMovedTracks': 13068})

process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False

import JMTucker.MFVNeutralino.EventFilter
JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process, path_name='p')
process.triggerFilter.HLTPaths = ['HLT_PFHT800_v*', 'HLT_PFHT900_v*']

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.mfvVertices.track_src = 'mfvMovedTracks'

process.load('JMTucker.MFVNeutralino.TriggerFloats_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')

process.mfvMovedTracks = cms.EDProducer('MFVTrackMover',
                                        tracks_src = cms.InputTag('generalTracks'),
                                        primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                        jets_src = cms.InputTag('selectedPatJets'),
                                        min_jet_pt = cms.double(50),
                                        min_jet_ntracks = cms.uint32(4),
                                        b_discriminator = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
                                        b_discriminator_veto = cms.double(0.46),
                                        b_discriminator_tag = cms.double(0.935),
                                        njets = cms.uint32(njets),
                                        nbjets = cms.uint32(nbjets),
                                        tau = cms.double(1),
                                        sig_theta = cms.double(0.2),
                                        sig_phi = cms.double(0.2),
                                        )

process.mfvMovedTree = cms.EDAnalyzer('MFVMovedTracksTreer',
                                      event_src = cms.InputTag('mfvEvent'),
                                      weight_src = cms.InputTag('mfvWeight'),
                                      mover_src = cms.string('mfvMovedTracks'),
                                      vertices_src = cms.InputTag('mfvVerticesAux'),
                                      max_dist2move = cms.double(0.02),
                                      apply_presel = cms.bool(True),
                                      njets_req = cms.uint32(njets),
                                      nbjets_req = cms.uint32(nbjets),
                                      for_mctruth = cms.bool(False),
                                      )

process.p *= process.mfvMovedTree

#process.options.wantSummary = True
process.maxEvents.input = 100
file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    def modify(sample):
        to_add = []
        to_replace = []

        to_replace.append(('njetsX= 2\nnbjets = 0'.replace('X', ' '),
                           'njets = %i\nnbjets = %i' % (njets, nbjets),
                           'could not find the magic string for njets/nbjets'))

        if not sample.is_mc:
            magic = 'is_mcX=XTrue'.replace('X', ' ')
            err = 'trying to submit on data, and tuple template does not contain the magic string "%s"' % magic
            to_replace.append((magic, 'is_mc = False', err))

            if sample.name.startswith('JetHT2016H'):
                magic = 'H =XFalse'.replace('X', ' ')
                err = 'trying to submit on 2016H and no magic string "%s"' % magic
                to_replace.append((magic, 'H = True', err))

        return to_add, to_replace

    for s in samples:
        if not s.is_mc:
            s.json = '../ana_2015p6.json'

    ex = '%i%i' % (njets, nbjets)

    cs = CRABSubmitter('TrackMover_' + ex,
                       pset_modifier = modify,
                       job_control_from_sample = True,
                       )

    cs.submit_all(samples)
