#!/usr/bin/env python

from DVCode.Tools.general import named_product
from DVCode.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.event_filter = 'jets only novtx'

version = settings.version + 'v1'

cfgs = named_product(njets = [2,3],
                     nbjets = [0,1,2],
                     nsigmadxy = [4.0],
                     angle = [0.2], #, 0.1, 0.3],
                     )

####

process = ntuple_process(settings)
tfileservice(process, 'movedtree.root')
max_events(process, 100)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'qcdht2000_year', dataset, 1)
cmssw_from_argv(process)

####

remove_output_module(process)

from DVCode.MFVNeutralino.Vertexer_cff import modifiedVertexSequence
from DVCode.Tools.NtupleFiller_cff import jmtNtupleFiller_pset
from DVCode.Tools.TrackRefGetter_cff import jmtTrackRefGetter
jmtTrackRefGetter.input_is_miniaod = settings.is_miniaod

process.mfvEvent.vertex_seed_tracks_src = ''
process.load('DVCode.Tools.WeightProducer_cfi')
process.load('DVCode.MFVNeutralino.WeightProducer_cfi') # JMTBAD
process.mfvWeight.throw_if_no_mcstat = False

process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices)
random_dict = {'jmtRescaledTracks': 1031}

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
                            tracks_src = cms.InputTag('jmtRescaledTracks'),
                            primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                            packed_candidates_src = cms.InputTag('packedPFCandidates'),
                            jets_src = cms.InputTag('selectedPatJets'),
                            track_ref_getter = jmtTrackRefGetter,
                            min_jet_pt = cms.double(50),
                            min_jet_ntracks = cms.uint32(4),
                            njets = cms.uint32(cfg.njets),
                            nbjets = cms.uint32(cfg.nbjets),
                            tau = cms.double(1.),
                            sig_theta = cms.double(cfg.angle),
                            sig_phi = cms.double(cfg.angle),
                            )

    modifiedVertexSequence(process, ex, tracks_src = tracks_name,
                           min_track_sigmadxy = 0,
                           min_track_rescaled_sigmadxy = cfg.nsigmadxy,
                           )

    for x in 'mfvVerticesToJets', 'mfvVerticesAuxTmp', 'mfvVerticesAuxPresel':
        getattr(process, x + ex).track_ref_getter.tracks_maps_srcs.append(cms.InputTag(tracks_name))

    tree = cms.EDAnalyzer('MFVMovedTracksTreer',
                          jmtNtupleFiller_pset(settings.is_miniaod),
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
    from DVCode.Tools.MetaSubmitter import *

    samples = pick_samples(dataset, all_signal=False)
    set_splitting(samples, dataset, 'trackmover', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter('TrackMover' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
