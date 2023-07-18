#!/usr/bin/env python

from JMTucker.Tools.general import named_product
from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True
#settings.event_filter = 'electrons only novtx'
settings.event_filter = 'muons only novtx'

version = settings.version + 'v6'

# for stat extension
#version = settings.version + 'ext1'
#version = settings.version + 'ext2'
#version = settings.version + 'ext3'
#version = settings.version + 'ext4'
#version = settings.version + 'ext5'
#version = settings.version + 'ext6'

cfgs = named_product(njets = [2], #FIXME
                     nbjets = [0], #FIXME
                     nsigmadxy = [4.0],
                     angle = [0.2], #, 0.1, 0.3],
                     )

# Only needed stat ext for (3,2) events
#cfgs = named_product(njets = [3],
#                     nbjets = [2],
#                     nsigmadxy = [4.0],
#                     angle = [0.2], #, 0.1, 0.3],
#                     )

####

process = ntuple_process(settings)
tfileservice(process, 'movedtree.root')
#max_events(process, 100)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#input_files(process, '/store/mc/RunIISummer20UL17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/280000/BB6E40E3-1F43-6C41-AEF8-5A7B96D0C5E5.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAOD/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/100000/034AE4F2-7180-7F40-81D6-740D15738CBA.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/4724838F-73AF-F040-9290-AC3B1CA485A7.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/DE019DB3-A431-7546-8BC1-30ABC37AD495.root')
#input_files(process, '~/nobackup/crabdirs/TTJets_UL2017_MINIAOD.root')
#sample_files(process, 'qcdbctoept080_2017', dataset, 1)
#sample_files(process, 'qcdmupt15_2017', dataset, 1)
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/A8C3978F-4BE4-A844-BEE8-8DEE129A02B7.root')
cmssw_from_argv(process)

####

remove_output_module(process)

from JMTucker.MFVNeutralino.Vertexer_cff import modifiedVertexSequence
from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset
from JMTucker.Tools.TrackRefGetter_cff import jmtTrackRefGetter
jmtTrackRefGetter.input_is_miniaod = settings.is_miniaod

process.mfvEvent.vertex_seed_tracks_src = ''
process.load('JMTucker.Tools.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi') # JMTBAD
process.mfvWeight.throw_if_no_mcstat = False

process.p = cms.Path(process.mfvEventFilterSequence * process.goodOfflinePrimaryVertices)
random_dict = {'jmtRescaledTracks': 1031}

if version.endswith('ext1') :
    random_dict = {'jmtRescaledTracks': 1991}
elif version.endswith('ext2') :
    random_dict = {'jmtRescaledTracks': 2930}
elif version.endswith('ext3') :
    random_dict = {'jmtRescaledTracks': 5770}
elif version.endswith('ext4') :
    random_dict = {'jmtRescaledTracks': 2892}
elif version.endswith('ext5') :
    random_dict = {'jmtRescaledTracks': 7809}
elif version.endswith('ext6') :
    random_dict = {'jmtRescaledTracks': 6586}

for icfg, cfg in enumerate(cfgs):
    ex = '%i%i' % (cfg.njets, cfg.nbjets)
    #ex += ('nsig%.2f' % cfg.nsigmadxy).replace('.', 'p')
    #ex += ('angle%.1f' % cfg.angle).replace('.', 'p')

    tracks_name = 'mfvMovedTracks' + ex
    auxes_name = 'mfvVerticesAux' + ex
    tree_name = 'mfvMovedTree' + ex
    assert not any([hasattr(process, x) for x in tracks_name, auxes_name, tree_name])

    random_dict[tracks_name] = 13068 + icfg

    if version.endswith('ext1') :
        random_dict[tracks_name] = 12991 + icfg
    elif version.endswith('ext2') :
        random_dict[tracks_name] = 10675 + icfg
    elif version.endswith('ext3') :
        random_dict[tracks_name] = 25423 + icfg
    elif version.endswith('ext4') :
        random_dict[tracks_name] = 27709 + icfg
    elif version.endswith('ext5') :
        random_dict[tracks_name] = 14456 + icfg
    elif version.endswith('ext6') :
        random_dict[tracks_name] = 12670 + icfg

    tracks = cms.EDProducer('MFVTrackMover',
                            tracks_src = cms.InputTag('jmtRescaledTracks'),
                            primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                            packed_candidates_src = cms.InputTag('packedPFCandidates'),
                            jets_src = cms.InputTag('selectedPatJets'),
                            track_ref_getter = jmtTrackRefGetter,
                            min_jet_pt = cms.double(0.0), #FIXMEi : 50GeV
                            min_jet_ntracks = cms.uint32(2), #FIXME : 4 tracks
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
                          apply_presel = cms.bool(True), #not a usual preselection cuts -- TM moved-jet cuts
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
    samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=False)
    #samples = [getattr(Samples, 'dyjetstollM50_2017')]
    #samples = [getattr(Samples, 'qcdbctoept250_2017')]
    set_splitting(samples, dataset, 'trackmover', data_json=json_path('ana_SingleLept_2017_10pc.json'), limit_ttbar=True)

    ms = MetaSubmitter('TrackMover' + version, dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, per_sample_pileup_weights_modifier())
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
