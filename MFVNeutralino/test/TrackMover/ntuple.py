#!/usr/bin/env python

from JMTucker.Tools.general import named_product
from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.event_filter = 'jets only novtx'

version = settings.version + 'V2'

cfgs = named_product(njets = [2,3],
                     nbjets = [0,1,2],
                     nsigmadxy = [4.0],
                     angle = [0.2], #, 0.1, 0.3],
                     )

####

process = ntuple_process(settings)
tfileservice(process, 'movedtree.root')
max_events(process, 100)
report_every(process, 1000000)
#want_summary(process)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'qcdht2000_2017', dataset, 1)
file_event_from_argv(process)

####

del process.out
del process.outp

from JMTucker.MFVNeutralino.Vertexer_cff import modifiedVertexSequence
from JMTucker.MFVNeutralino.JetTrackRefGetter_cff import mfvJetTrackRefGetter
mfvJetTrackRefGetter.input_is_miniaod = settings.is_miniaod

process.mfvEvent.vertex_seed_tracks_src = ''
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.mfvWeight.throw_if_no_mcstat = False

process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices)
random_dict = {}

for icfg, cfg in enumerate(cfgs):
    ex = '%i%i' % (cfg.njets, cfg.nbjets)
    #ex += ('nsig%.2f' % cfg.nsigmadxy).replace('.', 'p')
    #ex += ('angle%.1f' % cfg.angle).replace('.', 'p')

    tracks_name = 'mfvMovedTracks' + ex
    auxes_name = 'mfvVerticesAux' + ex
    tree_name = 'mfvMovedTree' + ex
    assert not any([hasattr(process, x) for x in tracks_name, auxes_name, tree_name])

    random_dict[tracks_name] = 13068 + icfg

    tracks = cms.EDProducer('MFVTrackMover',
                            mfvJetTrackRefGetter,
                            tracks_src = cms.InputTag('mfvUnpackedCandidateTracks' if settings.is_miniaod else 'generalTracks'),
                            primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                            packed_candidates_src = cms.InputTag('packedPFCandidates'),
                            jets_src = cms.InputTag('selectedPatJets'),
                            min_jet_pt = cms.double(50),
                            min_jet_ntracks = cms.uint32(4),
                            b_discriminator = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
                            b_discriminator_veto = cms.double(0.5803),
                            b_discriminator_tag = cms.double(0.9693),
                            njets = cms.uint32(cfg.njets),
                            nbjets = cms.uint32(cfg.nbjets),
                            tau = cms.double(1.),
                            sig_theta = cms.double(cfg.angle),
                            sig_phi = cms.double(cfg.angle),
                            )

    modifiedVertexSequence(process, ex, tracks_src = tracks_name,
                           min_track_sigmadxy = cfg.nsigmadxy,
                           )

    # hack track-jet association:
    # jets are composed of packedPFCandidates and JetTrackRefGetter knows how to compare those to mfvUnpackedCandidateTracks
    # but since there is a mfvMovedTracks entry for every one of mfvUnpackedCandidateTracks, the keys are the same
    # if this breaks, need to make JetTrackRefGetter know how to compose two maps
    getattr(process, 'mfvVerticesToJets' + ex).unpacked_tracks_src = tracks_name
    getattr(process, 'mfvVerticesAuxPresel' + ex).jets_tracks_keys_only = True

    tree = cms.EDAnalyzer('MFVMovedTracksTreer',
                          event_src = cms.InputTag('mfvEvent'),
                          weight_src = cms.InputTag('mfvWeight'),
                          sel_tracks_src = cms.InputTag('mfvVertexTracks' + ex, 'seed'),
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

ReferencedTagsTaskAdder(process)('p')
random_service(process, random_dict)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.data_samples_2017 + Samples.ttbar_samples_2017 + Samples.qcd_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    #samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'trackmover', data_json=json_path('ana_2017p8.json'))

    ms = MetaSubmitter('TrackMover' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
