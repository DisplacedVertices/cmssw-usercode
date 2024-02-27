import FWCore.ParameterSet.Config as cms

kvr_params = cms.PSet(
    maxDistance = cms.double(0.01),
    maxNbrOfIterations = cms.int32(10),
    doSmoothing = cms.bool(True),
)

mfvVertexTracks = cms.EDFilter('MFVVertexTracks',
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                               disregard_event = cms.bool(False),
                               use_tracks = cms.bool(True),
                               tracks_src = cms.InputTag('jmtRescaledTracks'),
                               use_non_pv_tracks = cms.bool(False),
                               use_non_pvs_tracks = cms.bool(False),
                               use_pf_candidates = cms.bool(False),
                               pf_candidate_src = cms.InputTag('particleFlow'),
                               use_pf_jets = cms.bool(False),
                               pf_jet_src = cms.InputTag('ak4PFJets'),
                               use_pat_jets = cms.bool(False),
                               pat_jet_src = cms.InputTag('selectedPatJets'),
                               use_second_tracks = cms.bool(False),
                               second_tracks_src = cms.InputTag('nothing'),
                               min_n_seed_tracks = cms.int32(0),
                               no_track_cuts = cms.bool(False),
                               min_seed_jet_pt = cms.double(30),
                               min_track_pt = cms.double(1),
                               min_track_dxy = cms.double(0),
                               min_track_sigmadxy = cms.double(0),
                               min_track_rescaled_sigmadxy = cms.double(2), # default is 4
                               min_track_sigmadxypv = cms.double(0),
                               min_track_hit_r = cms.int32(1),
                               min_track_nhits = cms.int32(0),
                               min_track_npxhits = cms.int32(0),
                               min_track_npxlayers = cms.int32(2),
                               min_track_nstlayers = cms.int32(6),
                               max_track_dxyerr = cms.double(1e9),
                               max_track_dxyipverr = cms.double(-1),
                               max_track_d3dipverr = cms.double(-1),
                               jumble_tracks = cms.bool(False),
                               remove_tracks_frac = cms.double(-1),
                               histos = cms.untracked.bool(True),
                               verbose = cms.untracked.bool(False),
                               )

mfvVertices = cms.EDProducer('MFVVertexer',
                             kvr_params = kvr_params,
                             do_track_refinement = cms.bool(False), # remove tracks + trim out tracks with IP significance larger than trackrefine_sigmacut and trackrefine_trimmax, respectively   
                             resolve_split_vertices_loose = cms.bool(False), # an alternative merging routine with `loose` criteria, to merge any nearby vertices within a given dist or significance
                             resolve_split_vertices_tight = cms.bool(True), # merging routine, based on vtx dphi and dVV 
                             investigate_merged_vertices = cms.bool(True), # investigate quality cuts on merged vertices from tight merging 
                             resolve_shared_jets = cms.bool(True),       # shared-jet mitigation
                             resolve_shared_jets_src = cms.InputTag('selectedPatJets'), 
                             extrapolate_ghost_tracks = cms.bool(False), # allow vertices to form by ghost tracks after shared-jet mitigation 
                             ghost_track_bjets_src = cms.InputTag('selectedPatJets'),
                             tracks_src = cms.InputTag('jmtRescaledTracks'), 
                             beamspot_src = cms.InputTag('offlineBeamSpot'),
                             seed_tracks_src = cms.InputTag('mfvVertexTracks', 'seed'),
                             all_tracks_src = cms.InputTag('mfvVertexTracks', 'all'),
                             mci_src = cms.InputTag('mfvGenParticles'),
                             n_tracks_per_seed_vertex = cms.int32(2),
                             max_seed_vertex_chi2 = cms.double(5),
                             use_2d_vertex_dist = cms.bool(False),
                             use_2d_track_dist = cms.bool(False),
                             merge_anyway_dist = cms.double(-1),
                             merge_anyway_sig = cms.double(4), # merging criteria for loose merging (*only* if resolve_split_vertices_loose is True)
                             merge_shared_dist = cms.double(-1),
                             merge_shared_sig = cms.double(4), # 4 is default merging shared-track vertices  
                             max_track_vertex_dist = cms.double(-1),
                             max_track_vertex_sig = cms.double(5), # 5 is default track arbitration
                             min_track_vertex_sig_to_remove = cms.double(1.5), # 1.5 is default track arbitration
                             remove_one_track_at_a_time = cms.bool(True),
                             max_nm1_refit_dist3 = cms.double(-1),
                             max_nm1_refit_distz = cms.double(0.005),
                             max_nm1_refit_count = cms.int32(-1),
                             trackrefine_sigmacut = cms.double(5), # track refinement criteria (*only* if do_track_refinement = True)
                             trackrefine_trimmax = cms.double(5), # track refinement criteria (*only* if do_track_refinement = True)
                             histos = cms.untracked.bool(True),
                             histos_noshare = cms.untracked.bool(True),   # make plots of no shared-track vertices 
                             histos_output_afterdzfit = cms.untracked.bool(True),   # make plots of output vertices after the default vertexing 
                             histos_output_aftermerge = cms.untracked.bool(True),   # make plots of output vertices after the default vertexing  + tight merging routine turned on
                             histos_output_aftersharedjets = cms.untracked.bool(True),   # make plots of output vertices after the default vertexing  + tight merging routine turned on  + shared-jet mitigation turned on 
                             verbose = cms.untracked.bool(False),
                             )
