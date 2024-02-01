import FWCore.ParameterSet.Config as cms
#from JMTucker.Tools.NtupleFiller_cff import jmtNtupleFiller_pset

kvr_params = cms.PSet(
    maxDistance = cms.double(0.01),
    maxNbrOfIterations = cms.int32(10),
    doSmoothing = cms.bool(True),
)

mfvVertexTracksGen = cms.EDFilter('MFVVertexTracksGen',
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               tracks_src = cms.InputTag('jmtRescaledTracks'),
                               mci_src = cms.InputTag('mfvGenParticles'),
                               track_gen_matching = cms.bool(False),
                               jet_gen_matching = cms.bool(False),
                               track_genjet_matching = cms.bool(False),
                               jets_src = cms.InputTag('selectedPatJets'),
                               gen_jets_src = cms.InputTag('slimmedGenJets'),
                               min_n_seed_tracks = cms.int32(0),
                               min_track_pt = cms.double(0.9),
                               min_track_hit_r = cms.int32(1),
                               min_track_nhits = cms.int32(0),
                               min_track_npxhits = cms.int32(0),
                               min_track_npxlayers = cms.int32(2),
                               min_track_nstlayers = cms.int32(6),
                               track_genjet_match_thres = cms.double(0.01),
                               min_genparticle_pt = cms.double(0),
                               verbose = cms.untracked.bool(False),
                               histos = cms.untracked.bool(True),
                               )


mfvVertexTracks = cms.EDFilter('MFVVertexTracks',
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                               disregard_event = cms.bool(False),
                               use_tracks = cms.bool(True),
                               use_separated_leptons = cms.bool(True), #use lepton tracks -> if they were separated at unpackedcandidates
                               tracks_src = cms.InputTag('jmtRescaledTracks'),
                               electron_tracks_src = cms.InputTag('jmtRescaledTracks', "electrons"),
                               muon_tracks_src = cms.InputTag('jmtRescaledTracks', "muons"),
                               save_quality_tracks = cms.bool(False),#trackattach
                               match_jets = cms.bool(False),
                               match_jet_src = cms.InputTag('selectedPatJets'),
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
                               min_track_pt_loose = cms.double(0.9), # loose track selection when match_jets is True
                               min_track_dxy = cms.double(0),
                               min_track_sigmadxy = cms.double(0),
                               min_track_rescaled_sigmadxy = cms.double(4),
                               min_leptrack_rescaled_sigmadxy = cms.double(3),
                               min_track_rescaled_sigmadxy_loose = cms.double(3.5), # loose track selection when match_jets is True
                               min_track_sigmadxypv = cms.double(0),
                               min_track_hit_r = cms.int32(1),
                               min_leptrack_hit_r = cms.int32(2),
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
                             #jmtNtupleFiller_pset(True, True, False),
                             kvr_params = kvr_params,
                             do_track_refinement = cms.bool(False), # remove tracks + trim out tracks with IP significance larger than trackrefine_sigmacut and trackrefine_trimmax, respectively   
                             resolve_split_vertices_loose = cms.bool(False), # an alternative merging routine with `loose` criteria, to merge any nearby vertices within a given dist or significance
                             resolve_split_vertices_tight = cms.bool(True), # merging routine, based on vtx dphi and dVV 
                             investigate_merged_vertices = cms.bool(False), # investigate quality cuts on merged vertices from tight merging 
                             resolve_shared_jets = cms.bool(True),       # shared-jet mitigation
                             resolve_shared_jets_src = cms.InputTag('selectedPatJets'), 
                             beamspot_src = cms.InputTag('offlineBeamSpot'),
                             seed_tracks_src = cms.InputTag('mfvVertexTracks', 'seed'),
                             all_tracks_src = cms.InputTag('mfvVertexTracks', 'all'),
                             muon_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'museed'),
                             electron_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'eleseed'), # these two are used just to check if the seed track is a lepton or not 
                             n_tracks_per_seed_vertex = cms.int32(2),
                             max_seed_vertex_chi2 = cms.double(5),
                             use_2d_vertex_dist = cms.bool(False),
                             use_2d_track_dist = cms.bool(False),
                             track_attachment = cms.bool(False), #trackattach
                             quality_tracks_src = cms.InputTag('mfvVertexTracks', 'quality'),
                             track_attachment_chi2 = cms.double(5),
                             merge_anyway_dist = cms.double(-1),
                             merge_anyway_sig = cms.double(4), # merging criteria for loose merging (*only* if resolve_split_vertices_loose is True)
                             merge_shared_dist = cms.double(-1),
                             merge_shared_sig = cms.double(4), # default merging shared-track vertices  
                             max_track_vertex_dist = cms.double(-1),
                             max_track_vertex_sig = cms.double(5), # default track arbitration
                             min_track_vertex_sig_to_remove = cms.double(1.5), # default track arbitration
                             remove_one_track_at_a_time = cms.bool(True),
                             max_nm1_refit_dist3 = cms.double(-1),
                             max_nm1_refit_distz = cms.double(-1), #(0.005), #0.03#0.005 might be too tight so try to relex it
                             ignore_lep_in_refit_distz = cms.bool(True), #do not consider dropping tracks at dz refit step if they are leptons w/ pt > 20 GeV. 
                             max_nm1_refit_distz_error = cms.double(-1), #0.02#0.015 might be too tight so try to relex it
                             max_nm1_refit_distz_sig = cms.double(-1), #-1), #0.005 #might be too tight so try to relex it
                             max_nm1_refit_count = cms.int32(-1),
                             trackrefine_sigmacut = cms.double(5), # track refinement criteria (*only* if do_track_refinement = True)
                             trackrefine_trimmax = cms.double(5), # track refinement criteria (*only* if do_track_refinement = True)
                             histos = cms.untracked.bool(True),
                             histos_noshare = cms.untracked.bool(False),   # make plots of no shared-track vertices 
                             histos_output_beforedzfit = cms.untracked.bool(False),
                             histos_output_afterdzfit = cms.untracked.bool(False),   # make plots of output vertices after the default vertexing 
                             histos_output_aftermerge = cms.untracked.bool(False),   # make plots of output vertices after the default vertexing  + tight merging routine turned on
                             histos_output_aftersharedjets = cms.untracked.bool(False),   # make plots of output vertices after the default vertexing  + tight merging routine turned on  + shared-jet mitigation turned on 
                             histos_output_aftertrackattach = cms.untracked.bool(False),   # make plots of output vertices after the default vertexing  + tight merging routine turned on  + shared-jet mitigation turned on + track attachment turned on
                             verbose = cms.untracked.bool(False),
                             )
