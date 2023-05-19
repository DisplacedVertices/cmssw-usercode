import FWCore.ParameterSet.Config as cms

mfvSelectedVertices = cms.EDProducer('MFVVertexSelector',
                                     mevent_src = cms.InputTag(''),
                                     vertex_aux_src = cms.InputTag('mfvVerticesAux'),
                                     produce_vertices = cms.bool(False),
                                     produce_tracks = cms.bool(False),
                                     produce_refs = cms.bool(False),
                                     vertex_src = cms.InputTag(''), # used when produce_vertices or produce_refs is true
                                     use_mva = cms.bool(False),
                                     mva_cut = cms.double(0.7),
                                     match_to_vertices_src = cms.InputTag(''), # cms.InputTag('mfvGenParticles','genVertex') ,
                                     max_match_distance = cms.double(0.0120),
                                     min_match_distance = cms.double(0),
                                     exclude_beampipe = cms.bool(True), #FIXME true by default
                                     min_ntracks          = cms.int32(0),
                                     max_ntracks          = cms.int32(1000000),
                                     min_ntracksptgt2     = cms.int32(0),
                                     min_ntracksptgt3     = cms.int32(0),
                                     min_ntracksptgt5     = cms.int32(0),
                                     min_ntracksptgt10    = cms.int32(0),
                                     min_ntracknsigma4    = cms.int32(0), 
                                     min_njetsntks        = cms.int32(0),
                                     max_njetsntks        = cms.int32(1000000),
                                     max_chi2dof          = cms.double(1e9),
                                     min_tkonlypt         = cms.double(0),
                                     max_abstkonlyeta     = cms.double(1e9),
                                     min_tkonlymass       = cms.double(0),
                                     min_jetsntkpt        = cms.double(0),
                                     max_absjetsntketa    = cms.double(1e9),
                                     min_jetsntkmass      = cms.double(0),
                                     min_tksjetsntkpt     = cms.double(0),
                                     max_abstksjetsntketa = cms.double(1e9),
                                     min_tksjetsntkmass   = cms.double(0),
                                     min_costhtkonlymombs = cms.double(-3),
                                     min_costhjetsntkmombs = cms.double(-3),
                                     min_costhtksjetsntkmombs = cms.double(-3),
                                     min_missdisttkonlypvsig = cms.double(0),
                                     min_missdistjetsntkpvsig = cms.double(0),
                                     min_missdisttksjetsntkpvsig = cms.double(0),
                                     min_sumpt2           = cms.double(0),
                                     min_maxtrackpt       = cms.double(0),
                                     min_maxm1trackpt     = cms.double(0),
                                     max_trackdxyerrmin   = cms.double(1e9),
                                     max_trackdxyerrmax   = cms.double(1e9),
                                     max_trackdxyerravg   = cms.double(1e9),
                                     max_trackdxyerrrms   = cms.double(1e9),
                                     max_trackdzerrmin    = cms.double(1e9),
                                     max_trackdzerrmax    = cms.double(1e9),
                                     max_trackdzerravg    = cms.double(1e9),
                                     max_trackdzerrrms    = cms.double(1e9),
                                     min_trackpairdphimax = cms.double(0),
                                     min_drmin            = cms.double(0),
                                     max_drmin            = cms.double(1e9),
                                     min_drmax            = cms.double(0),
                                     max_drmax            = cms.double(1e9),
                                     max_jetpairdrmin     = cms.double(1e9),
                                     max_jetpairdrmax     = cms.double(1e9),
                                     max_err2d            = cms.double(1e9),
                                     max_err3d            = cms.double(1e9),
                                     min_gen3ddist        = cms.double(0),
                                     max_gen3ddist        = cms.double(1e9),
                                     min_gen3dsig         = cms.double(0),
                                     max_gen3dsig         = cms.double(1e6),
                                     min_bs2ddist         = cms.double(0),
                                     max_bs2ddist         = cms.double(1e9),
                                     min_bsbs2ddist       = cms.double(0),
                                     max_bsbs2ddist       = cms.double(1e9),
                                     min_bs2derr          = cms.double(0),
                                     max_bs2derr          = cms.double(1e9),
                                     min_rescale_bs2derr  = cms.double(0),
                                     max_rescale_bs2derr  = cms.double(1e9),
                                     min_bs2dsig          = cms.double(0),
                                     min_bs3ddist         = cms.double(0),
                                     min_geo2ddist        = cms.double(0),
                                     max_geo2ddist        = cms.double(1e9),
                                     max_sumnhitsbehind   = cms.int32(1000000),
                                     max_ntrackssharedwpv = cms.int32(1000000),
                                     max_ntrackssharedwpvs = cms.int32(1000000),
                                     max_npvswtracksshared = cms.int32(1000000),
                                     min_thetaoutlier     = cms.double(0),
                                     max_thetaoutlier     = cms.double(1e9),
                                     min_zoutlier             = cms.double(0),
                                     max_zoutlier             = cms.double(1e9),
                                     max_zoutlier_maxdphi0pi  = cms.double(1e9),
                                     use_cluster_cuts         = cms.bool(False),
                                     min_nclusters            = cms.int32(0),
                                     max_nsingleclusters      = cms.int32(1000000),
                                     max_fsingleclusters      = cms.double(1e9),
                                     min_nclusterspertk       = cms.double(0),
                                     max_nsingleclusterspertk = cms.double(1e9),
                                     max_nsingleclusterspb025 = cms.int32(1000000),
                                     max_nsingleclusterspb050 = cms.int32(1000000),
                                     min_avgnconstituents     = cms.double(0),
                                     sort_by = cms.string('ntracks_then_mass'),
                                     )

mfvSelectedVerticesExtraLoose = mfvSelectedVertices.clone(
    mevent_src = 'mfvEvent',
    min_ntracks = 3,
    #min_bsbs2ddist = 0.005,
    #max_rescale_bs2derr = 0.0025,
    )

mfvSelectedVerticesLoose = mfvSelectedVertices.clone(
    mevent_src = 'mfvEvent',
    exclude_beampipe = True,
    min_ntracks = 3,
    min_bsbs2ddist = 0.01,
    max_rescale_bs2derr = 0.005,
    )

mfvSelectedVerticesTight = mfvSelectedVertices.clone(
    mevent_src = 'mfvEvent',
    exclude_beampipe = True,
    min_ntracks = 5,
    min_bsbs2ddist = 0.01,
    max_rescale_bs2derr = 0.005,
    )


mfvSelectedVerticesTightNtk3    = mfvSelectedVerticesTight.clone(min_ntracks = 3, max_ntracks = 3)
mfvSelectedVerticesTightNtk4    = mfvSelectedVerticesTight.clone(min_ntracks = 4, max_ntracks = 4)
mfvSelectedVerticesTightNtk3or4 = mfvSelectedVerticesTight.clone(min_ntracks = 3, max_ntracks = 4)
mfvSelectedVerticesTightNtk3or5 = mfvSelectedVerticesTight.clone(min_ntracks = 3, max_ntracks = 5)
mfvSelectedVerticesTightNtk4or5 = mfvSelectedVerticesTight.clone(min_ntracks = 4, max_ntracks = 5)
mfvSelectedVerticesTightNtk5    = mfvSelectedVerticesTight.clone() # for looping convenience


mfvSelectedVerticesLooseMinNtk3 = mfvSelectedVerticesLoose.clone(min_ntracks = 3)
mfvSelectedVerticesLooseMinNtk4 = mfvSelectedVerticesLoose.clone(min_ntracks = 4)
mfvSelectedVerticesLoosetNtk5    = mfvSelectedVerticesLoose.clone() # for looping convenience

mfvSelectedVerticesSeq = cms.Sequence(
    mfvSelectedVerticesExtraLoose *
    mfvSelectedVerticesLoose *
    mfvSelectedVerticesTight *
    mfvSelectedVerticesTightNtk3 *
    mfvSelectedVerticesTightNtk4 *
    mfvSelectedVerticesTightNtk3or4 *
    mfvSelectedVerticesTightNtk3or5 *
    mfvSelectedVerticesTightNtk4or5
    )

