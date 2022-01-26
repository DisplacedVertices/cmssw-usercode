#include "TH2.h"
#include "TMath.h"
#include <math.h>  
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexerPairEff.h"
#include "JMTucker/MFVNeutralino/interface/VertexerParams.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVVertexer : public edm::EDProducer {
public:
  MFVVertexer(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  typedef std::set<reco::TrackRef> track_set;
  typedef std::vector<reco::TrackRef> track_vec;

  bool match_track_jet(const reco::Track& tk, const pat::Jet& jet, const pat::JetCollection& jets, const int& idx);

  void finish(edm::Event&, const std::vector<reco::TransientTrack>&, std::unique_ptr<reco::VertexCollection>, std::unique_ptr<VertexerPairEffs>, const std::vector<std::pair<track_set, track_set>>&);

  template <typename T>
  void print_track_set(const T& ts) const {
    for (auto r : ts)
      printf(" %u", r.key());
  }

  template <typename T>
  void print_track_set(const T& ts, const reco::Vertex& v) const {
    for (auto r : ts)
      printf(" %u%s", r.key(), (v.trackWeight(r) < mfv::track_vertex_weight_min ? "!" : ""));
  }

  void print_track_set(const reco::Vertex& v) const {
    for (auto r = v.tracks_begin(), re = v.tracks_end(); r != re; ++r)
      printf(" %lu%s", r->key(), (v.trackWeight(*r) < mfv::track_vertex_weight_min ? "!" : ""));
  }

  bool is_track_subset(const track_set& a, const track_set& b) const {
    bool is_subset = true;
    const track_set& smaller = a.size() <= b.size() ? a : b;
    const track_set& bigger  = a.size() <= b.size() ? b : a;
    
    for (auto t : smaller)
      if (bigger.count(t) < 1) {
        is_subset = false;
        break;
      }

    return is_subset;
  }

  track_set vertex_track_set(const reco::Vertex& v, const double min_weight = mfv::track_vertex_weight_min) const {
    track_set result;

    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      const double w = v.trackWeight(*it);
      const bool use = w >= min_weight;
      assert(use);
      //if (verbose) ("trk #%2i pt %6.3f eta %6.3f phi %6.3f dxy %6.3f dz %6.3f w %5.3f  use? %i\n", int(it-v.tracks_begin()), (*it)->pt(), (*it)->eta(), (*it)->phi(), (*it)->dxy(), (*it)->dz(), w, use);
      if (use)
        result.insert(it->castTo<reco::TrackRef>());
    }

    return result;
  }

  track_vec vertex_track_vec(const reco::Vertex& v, const double min_weight = mfv::track_vertex_weight_min) const {
    track_set s = vertex_track_set(v, min_weight);
    return track_vec(s.begin(), s.end());
  }

  Measurement1D vertex_dist(const reco::Vertex& v0, const reco::Vertex& v1) const {
    if (use_2d_vertex_dist)
      return vertex_dist_2d.distance(v0, v1);
    else
      return vertex_dist_3d.distance(v0, v1);
  }

  Measurement1D miss_dist(const reco::Vertex& sv, const AlgebraicVector3& ref, const AlgebraicVector3& mom) {
	  // miss distance is magnitude of (jet direction (= n) cross (tv - sv) ( = d))
	  // to calculate uncertainty, use |n X d|^2 = (|n||d|)^2 - (n . d)^2
	  AlgebraicVector3 n = ROOT::Math::Unit(mom);
	  AlgebraicVector3 d(sv.x() - ref(0),
		  sv.y() - ref(1),
		  sv.z() - ref(2));
	  AlgebraicVector3 n_cross_d = ROOT::Math::Cross(n, d);
	  double n_dot_d = ROOT::Math::Dot(n, d);
	  double val = ROOT::Math::Mag(n_cross_d);
	  AlgebraicVector3 jac(2 * d(0) - 2 * n_dot_d * n(0),
		  2 * d(1) - 2 * n_dot_d * n(1),
		  2 * d(2) - 2 * n_dot_d * n(2));
	  return Measurement1D(val, sqrt(ROOT::Math::Similarity(jac, sv.covariance())) / 1 / val); // modified err from 2->1 of sv
  }

  std::pair<bool, Measurement1D> track_dist(const reco::TransientTrack& t, const reco::Vertex& v) const {
    if (use_2d_track_dist)
      return IPTools::absoluteTransverseImpactParameter(t, v);
    else
      return IPTools::absoluteImpactParameter3D(t, v);
  }

  VertexDistanceXY vertex_dist_2d;
  VertexDistance3D vertex_dist_3d;
  std::unique_ptr<KalmanVertexFitter> kv_reco;

  std::vector<TransientVertex> kv_reco_dropin(std::vector<reco::TransientTrack>& ttks) {
    if (ttks.size() < 2)
      return std::vector<TransientVertex>();
    std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
<<<<<<< HEAD
    if (v[0].normalisedChiSquared() > 5) //PK: need to change for new config
=======
    if (v[0].normalisedChiSquared() > 5) //PK: we used to try different values {8 or 4} 
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
      return std::vector<TransientVertex>();
    return v;
  }

  std::vector<TransientVertex> kv_reco_dropin_nocut(std::vector<reco::TransientTrack>& ttks) {
	  if (ttks.size() < 2)
		  return std::vector<TransientVertex>();
	  std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
	  return v;
  }
  const bool do_track_refinement;
<<<<<<< HEAD
  const bool resolve_split_vertices_loose;
  const bool resolve_split_vertices_tight;
  const bool investigate_merged_vertices;
  const bool resolve_shared_jets;
=======
  const bool resolve_shared_jets;
  const bool resolve_split_vertices_loose;
  const bool resolve_split_vertices_tight;
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
  const edm::EDGetTokenT<pat::JetCollection> shared_jet_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> seed_tracks_token;
  const int n_tracks_per_seed_vertex;
  const double max_seed_vertex_chi2;
  const bool use_2d_vertex_dist;
  const bool use_2d_track_dist;
  const double merge_anyway_dist;
  const double merge_anyway_sig;
  const double merge_shared_dist;
  const double merge_shared_sig;
  const double max_track_vertex_dist;
  const double max_track_vertex_sig;
  const double min_track_vertex_sig_to_remove;
  const bool remove_one_track_at_a_time;
  const double max_nm1_refit_dist3;
  const double max_nm1_refit_distz;
  const int max_nm1_refit_count;
  const double trackrefine_sigmacut;
  const double trackrefine_trimmax;
  const bool histos;
  const bool histos_noshare;
  const bool histos_output0;
  const bool histos_output1;
  const bool histos_output2;
  const bool verbose;
  const std::string module_label;

  TH1F* h_n_seed_vertices;
  TH1F* h_seed_vertex_track_weights;
  TH1F* h_seed_vertex_chi2;
  TH1F* h_seed_vertex_ndof;
  TH1F* h_seed_vertex_x;
  TH1F* h_seed_vertex_y;
  TH1F* h_seed_vertex_rho;
  TH1F* h_seed_vertex_phi;
  TH1F* h_seed_vertex_z;
  TH1F* h_seed_vertex_r;
  TH1F* h_seed_vertex_paird2d;
  TH1F* h_seed_vertex_pairdphi;
  TH1F* h_n_resets;
  TH1F* h_n_onetracks;
  TH1F* h_noshare_vertex_tkvtxdist;		// vertices after_do_track_refinement if do_track_refinement turned on 
  TH1F* h_noshare_vertex_tkvtxdisterr;	// vertices after_do_track_refinement if do_track_refinement turned on 
  TH1F* h_noshare_vertex_tkvtxdistsig;	 // vertices after_do_track_refinement if do_track_refinement turned on 
  TH1F* h_noshare_vertex_tkvtxdist_before_do_track_refinement;
  TH1F* h_noshare_vertex_tkvtxdisterr_before_do_track_refinement;
  TH1F* h_noshare_vertex_tkvtxdistsig_before_do_track_refinement;


  TH1F* h_n_noshare_vertices;
  TH1F* h_noshare_vertex_ntracks;
  TH1F* h_noshare_vertex_mass;
  TH1F* h_noshare_vertex_track_weights;
  TH1F* h_noshare_vertex_chi2;
  TH1F* h_noshare_vertex_ndof;
  TH1F* h_noshare_vertex_x;
  TH1F* h_noshare_vertex_y;
  TH1F* h_noshare_vertex_rho;
  TH1F* h_noshare_vertex_phi;
  TH1F* h_noshare_vertex_z;
  TH1F* h_noshare_vertex_r;
  TH1F* h_noshare_vertex_paird2d;
  TH1F* h_noshare_vertex_pairdphi;
  TH1F* h_noshare_track_multiplicity;
  TH1F* h_max_noshare_track_multiplicity;
  TH1F* h_n_output_vertices;
  TH1F* h_n_at_least_5trk_output_vertices;

  
  TH1F* h_noshare_trackrefine_sigmacut_vertex_chi2;
  TH1F* h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig;
  TH1F* h_noshare_trackrefine_sigmacut_vertex_distr_shift;

  TH1F* h_noshare_trackrefine_trimmax_vertex_chi2;
  TH1F* h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig;
  TH1F* h_noshare_trackrefine_trimmax_vertex_distr_shift;

  TH1F* h_output0_vertex_tkvtxdist;		 
  TH1F* h_output0_vertex_tkvtxdisterr;	
  TH1F* h_output0_vertex_tkvtxdistsig;
  TH1F* h_n_at_least_5trk_output0_vertices;
  TH1F* h_at_least_5trk_output0_vertex_dBV;
  TH1F* h_at_least_5trk_output0_vertex_bs2derr;
  TH1F* h_output0_vertex_ntracks;
  TH1F* h_output0_vertex_mass;
  TH1F* h_output0_vertex_track_weights;
  TH1F* h_output0_vertex_chi2;
  TH1F* h_output0_vertex_ndof;
  TH1F* h_output0_vertex_x;
  TH1F* h_output0_vertex_y;
  TH1F* h_output0_vertex_rho;
  TH1F* h_output0_vertex_phi;
  TH1F* h_output0_vertex_z;
  TH1F* h_output0_vertex_r;
  TH1F* h_output0_vertex_paird2d;
  TH1F* h_output0_vertex_paird2dsig;
  TH1F* h_output0_vertex_pairdphi;

  TH1F* h_output1_vertex_tkvtxdist;
  TH1F* h_output1_vertex_tkvtxdisterr;
  TH1F* h_output1_vertex_tkvtxdistsig;
  TH1F* h_n_at_least_5trk_output1_vertices;
  TH1F* h_at_least_5trk_output1_vertex_dBV;
  TH1F* h_at_least_5trk_output1_vertex_bs2derr;
  TH1F* h_output1_vertex_ntracks;
  TH1F* h_output1_vertex_mass;
  TH1F* h_output1_vertex_track_weights;
  TH1F* h_output1_vertex_chi2;
  TH1F* h_output1_vertex_ndof;
  TH1F* h_output1_vertex_x;
  TH1F* h_output1_vertex_y;
  TH1F* h_output1_vertex_rho;
  TH1F* h_output1_vertex_phi;
  TH1F* h_output1_vertex_z;
  TH1F* h_output1_vertex_r;
  TH1F* h_output1_vertex_paird2d;
  TH1F* h_output1_vertex_paird2dsig;
  TH1F* h_output1_vertex_pairdphi;
<<<<<<< HEAD

  TH1F* h_output1_after_merged_criteria_vertex_chi2;
  TH1F* h_output1_after_merged_criteria_vertex_ntracks;
  TH1F* h_output1_after_merged_criteria_vertex_bs2derr;
  TH1F* h_output1_after_merged_criteria_vertex_dBV;

   
  TH1F* h_output1_most_track_vertices_shared_jets_or_not; 
  
  //PK: study of tracks and chi2
  TH2F* h_2D_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2;
  //TProfile* h_2Dpfx_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2;
  TH1F* h_at_least_5trk_output1_no_shared_tracks_pair_shift_unnorm_chi2;
  //PK: XYZ mitigation starts here
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_YandX;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_YandX;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_Y;
  // case X {1,1} 

  TH1F* h_qualify_most_track_vertices_nsharedjet;
  TH1F* h_qualify_most_track_vertices_X_nsharedjet;
  TH1F* h_qualify_most_5trk_track_vertices_Xa_nsharedjet;
  TH1F* h_qualify_most_5trk_track_vertices_Xb_nsharedjet;
  TH1F* h_qualify_most_5trk_track_vertices_Xc_nsharedjet;
  TH1F* h_qualify_most_track_vertices_Y_nsharedjet;
  TH2F* h_2D_qualify_most_track_vertices_XandY_nsharedjet;

  
  TH2F* h_2D_most_5trk_track_vertices_X_Deltachi2_SV0_SV1;
  TH2F* h_2D_most_5trk_track_vertices_Xa_Deltachi2_SV0_SV1;
  TH2F* h_2D_most_5trk_track_vertices_Xb_Deltachi2_SV0_SV1;
  TH2F* h_2D_most_5trk_track_vertices_Xc_Deltachi2_SV0_SV1;

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_X;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X;
  
  

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet;
  
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet;
  

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_sig_X;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_X;
  

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X;
  

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet;
  
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet;
  

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_sig_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_X;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_X_nsv_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_X;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dPhi_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_X;
  TH2F* h_2D_at_least_5trk_output1_shared_track_vtx0_shared_track_vtx1_dPhi_X;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xa;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xa;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xa;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xb;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xb;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xb;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xc;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xc;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xc;
  

  // case Y {1,n>1} 

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_Y;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_Y;
  

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet;

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_sig_Y;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_Y;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_Y;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_err_Y;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_Y;
  

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRoutjet;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRoutjet;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_sig_Y;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_Y;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_dR_shared_tracks_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_err_Y;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y;

  
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_sumpT_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_shared_ntrack_Y;

  //TH1F* h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_onejet_by_sumpT_Y;
  //TH1F* h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_onejet_by_shared_ntrack_Y;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_sumpT_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_shared_ntrack_Y;


  TH1F* h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_sumpT_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_sumpT_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_shared_ntrack_Y;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_shared_ntrack_Y;

  // case Z {n>1,m>1}

  


  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZnonC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet;

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet;

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZO;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZO;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZO;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet;
  
  
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRinjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRoutjet;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRoutjet;


  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZnonC;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_diff_shared_tracks_ZnonC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_ZnonC;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_diff_shared_tracks_ZnonC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZnonC;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_diff_shared_tracks_ZnonC;

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZC;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_ZC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_ZC;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_ZC;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZC;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_ZC;

  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZO;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_ZO;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO;
  TH1F* h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZO;
  TH2F* h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZA;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZA;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZA;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZA;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRoutjet;
  

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZB;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZB;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZB;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZB;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRoutjet;
  

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZC;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZC;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet;

  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet;



  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZO;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZO;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZO;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZO;
  
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet;
  
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet;
 


  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZA;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_ZA;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZA;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZB;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_ZB;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZB;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZC;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_ZC;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZC;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZO;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_ZO;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO;
  TH1F* h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZO;
  TH2F* h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO;

 
 


  



  
  // : all of these have applied all three cuts 
  Double_t edges[4] = { 0.0, 0.0400, 0.0700, 0.1 };
  TH1F* h_qualify_svdist2d_three_bins;
  TH1F* h_qualify_by_sum_pT_svdist2d_three_bins;
  TH1F* h_qualify_only_small_dR_by_sum_pT_svdist2d_three_bins;
  TH1F* h_qualify_by_median_tkvtxdist_svdist2d_three_bins;
  TH1F* h_qualify_only_small_dR_by_median_tkvtxdist_svdist2d_three_bins;
  TH1F* h_qualify_by_median_tkvtxdistsig_svdist2d_three_bins;
  TH1F* h_qualify_only_small_dR_by_median_tkvtxdistsig_svdist2d_three_bins;
  TH1F* h_qualify_only_small_dR_by_2sigma_median_tkvtxdistsig_svdist2d_three_bins;
  
  
  TH1F* h_output2_vertex_tkvtxdist;
  TH1F* h_output2_vertex_tkvtxdisterr;
  TH1F* h_output2_vertex_tkvtxdistsig;
  TH1F* h_n_at_least_5trk_output2_vertices;
  TH1F* h_at_least_5trk_output2_vertex_dBV;
  TH1F* h_at_least_5trk_output2_vertex_bs2derr;
  TH1F* h_output2_vertex_ntracks;
  TH1F* h_output2_vertex_mass;
  TH1F* h_output2_vertex_track_weights;
  TH1F* h_output2_vertex_chi2;
  TH1F* h_output2_vertex_ndof;
  TH1F* h_output2_vertex_x;
  TH1F* h_output2_vertex_y;
  TH1F* h_output2_vertex_rho;
  TH1F* h_output2_vertex_phi;
  TH1F* h_output2_vertex_z;
  TH1F* h_output2_vertex_r;
  TH1F* h_output2_vertex_paird2d;
  TH1F* h_output2_vertex_paird2dsig;
  TH1F* h_output2_vertex_pairdphi;

=======
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
  

};

MFVVertexer::MFVVertexer(const edm::ParameterSet& cfg)
  : 
	kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
	do_track_refinement(cfg.getParameter<bool>("do_track_refinement")),
<<<<<<< HEAD
	resolve_split_vertices_loose(cfg.getParameter<bool>("resolve_split_vertices_loose")),
	resolve_split_vertices_tight(cfg.getParameter<bool>("resolve_split_vertices_tight")),
	investigate_merged_vertices(cfg.getParameter<bool>("investigate_merged_vertices")),
	resolve_shared_jets(cfg.getParameter<bool>("resolve_shared_jets")),
=======
	resolve_shared_jets(cfg.getParameter<bool>("resolve_shared_jets")),
	resolve_split_vertices_loose(cfg.getParameter<bool>("resolve_split_vertices_loose")),
	resolve_split_vertices_tight(cfg.getParameter<bool>("resolve_split_vertices_tight")),
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
	shared_jet_token(resolve_shared_jets ? consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("resolve_shared_jets_src")) : edm::EDGetTokenT<pat::JetCollection>()),
	beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    seed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("seed_tracks_src"))),
    n_tracks_per_seed_vertex(cfg.getParameter<int>("n_tracks_per_seed_vertex")),
    max_seed_vertex_chi2(cfg.getParameter<double>("max_seed_vertex_chi2")),
    use_2d_vertex_dist(cfg.getParameter<bool>("use_2d_vertex_dist")),
    use_2d_track_dist(cfg.getParameter<bool>("use_2d_track_dist")),
    merge_anyway_dist(cfg.getParameter<double>("merge_anyway_dist")),
    merge_anyway_sig(cfg.getParameter<double>("merge_anyway_sig")),
    merge_shared_dist(cfg.getParameter<double>("merge_shared_dist")),
    merge_shared_sig(cfg.getParameter<double>("merge_shared_sig")),
    max_track_vertex_dist(cfg.getParameter<double>("max_track_vertex_dist")),
    max_track_vertex_sig(cfg.getParameter<double>("max_track_vertex_sig")),
    min_track_vertex_sig_to_remove(cfg.getParameter<double>("min_track_vertex_sig_to_remove")),
    remove_one_track_at_a_time(cfg.getParameter<bool>("remove_one_track_at_a_time")),
    max_nm1_refit_dist3(cfg.getParameter<double>("max_nm1_refit_dist3")),
    max_nm1_refit_distz(cfg.getParameter<double>("max_nm1_refit_distz")),
    max_nm1_refit_count(cfg.getParameter<int>("max_nm1_refit_count")),
	trackrefine_sigmacut(cfg.getParameter<double>("trackrefine_sigmacut")),
	trackrefine_trimmax(cfg.getParameter<double>("trackrefine_trimmax")),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
	histos_noshare(cfg.getUntrackedParameter<bool>("histos_noshare", false)),
	histos_output0(cfg.getUntrackedParameter<bool>("histos_output0", false)),
	histos_output1(cfg.getUntrackedParameter<bool>("histos_output1", false)),
	histos_output2(cfg.getUntrackedParameter<bool>("histos_output2", false)),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false)),
    module_label(cfg.getParameter<std::string>("@module_label"))
{
  if (n_tracks_per_seed_vertex < 2 || n_tracks_per_seed_vertex > 5)
    throw cms::Exception("MFVVertexer", "n_tracks_per_seed_vertex must be one of 2,3,4,5");

  produces<reco::VertexCollection>();
  produces<VertexerPairEffs>();
  produces<reco::TrackCollection>("seed"); // JMTBAD remove me
  produces<reco::TrackCollection>("inVertices");

  if (histos) {
    edm::Service<TFileService> fs;

    h_n_seed_vertices                = fs->make<TH1F>("h_n_seed_vertices",                "",  50,   0,    200);
    h_seed_vertex_track_weights      = fs->make<TH1F>("h_seed_vertex_track_weights",      "",  21,   0,      1.05);
    h_seed_vertex_chi2               = fs->make<TH1F>("h_seed_vertex_chi2",               "",  20,   0, max_seed_vertex_chi2);
    h_seed_vertex_ndof               = fs->make<TH1F>("h_seed_vertex_ndof",               "",  10,   0,     20);
    h_seed_vertex_x                  = fs->make<TH1F>("h_seed_vertex_x",                  "", 20,  -1,      1);
    h_seed_vertex_y                  = fs->make<TH1F>("h_seed_vertex_y",                  "", 20,  -1,      1);
    h_seed_vertex_rho                = fs->make<TH1F>("h_seed_vertex_rho",                "", 20,   0,      2);
    h_seed_vertex_phi                = fs->make<TH1F>("h_seed_vertex_phi",                "",  20,  -3.15,   3.15);
    h_seed_vertex_z                  = fs->make<TH1F>("h_seed_vertex_z",                  "",  20, -20,     20);
    h_seed_vertex_r                  = fs->make<TH1F>("h_seed_vertex_r",                  "", 20,   0,      2);
    h_seed_vertex_paird2d            = fs->make<TH1F>("h_seed_vertex_paird2d",            "", 20,   0,      0.2);
    h_seed_vertex_pairdphi           = fs->make<TH1F>("h_seed_vertex_pairdphi",           "", 20,  0,   3.14);

    h_n_resets                       = fs->make<TH1F>("h_n_resets",                       "", 50,   0,   500);
    h_n_onetracks                    = fs->make<TH1F>("h_n_onetracks",                    "",  5,   0,     5);

    h_n_noshare_vertices             = fs->make<TH1F>("h_n_noshare_vertices",             ";# of noshare vertices", 20,   0,    50);
    h_noshare_vertex_tkvtxdist       = fs->make<TH1F>("h_noshare_vertex_tkvtxdist",       ";tkvtxdist (cm.)", 20,  0,   0.1);
    h_noshare_vertex_tkvtxdisterr    = fs->make<TH1F>("h_noshare_vertex_tkvtxdisterr",    ";tkvtxdisterr (cm.)", 20,  0,   0.1);
    h_noshare_vertex_tkvtxdistsig    = fs->make<TH1F>("h_noshare_vertex_tkvtxdistsig",    ";tkvtxdistsig", 20,  0,     6);
	h_noshare_vertex_tkvtxdist_before_do_track_refinement = fs->make<TH1F>("h_noshare_vertex_tkvtxdist_before_do_track_refinement", ";tkvtxdist (cm.)", 20, 0, 0.1);
	h_noshare_vertex_tkvtxdisterr_before_do_track_refinement = fs->make<TH1F>("h_noshare_vertex_tkvtxdisterr_before_do_track_refinement", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
	h_noshare_vertex_tkvtxdistsig_before_do_track_refinement = fs->make<TH1F>("h_noshare_vertex_tkvtxdistsig_before_do_track_refinement", ";tkvtxdistsig", 20, 0, 6);

	
    h_noshare_vertex_ntracks         = fs->make<TH1F>("h_noshare_vertex_ntracks",         ";ntracks/vtx",  30,  0, 30);
	h_noshare_vertex_mass = fs->make<TH1F>("h_noshare_vertex_mass", ";mass/vtx (GeV)", 20, 0, 1000);
    h_noshare_vertex_track_weights   = fs->make<TH1F>("h_noshare_vertex_track_weights",   ";vertex track weights",  21,   0,      1.05);
<<<<<<< HEAD
    h_noshare_vertex_chi2            = fs->make<TH1F>("h_noshare_vertex_chi2",            ";normalized chi2", 20,   0, max_seed_vertex_chi2);
=======
    h_noshare_vertex_chi2            = fs->make<TH1F>("h_noshare_vertex_chi2",            ";chi2", 20,   0, max_seed_vertex_chi2);
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
    h_noshare_vertex_ndof            = fs->make<TH1F>("h_noshare_vertex_ndof",            ";ndof", 10,   0,     20);
    h_noshare_vertex_x               = fs->make<TH1F>("h_noshare_vertex_x",               ";vtxbsdist_x (cm.)", 20,  -1,      1);
    h_noshare_vertex_y               = fs->make<TH1F>("h_noshare_vertex_y",               ";vtxbsdist_y (cm.)", 20,  -1,      1);
    h_noshare_vertex_rho             = fs->make<TH1F>("h_noshare_vertex_rho",             ";vtx rho", 20,   0,      2);
    h_noshare_vertex_phi             = fs->make<TH1F>("h_noshare_vertex_phi",             ";vtx phi", 20,  -3.15,   3.15);
    h_noshare_vertex_z               = fs->make<TH1F>("h_noshare_vertex_z",               ";vtxbsdist_z (cm.)", 20, -20,     20);
    h_noshare_vertex_r               = fs->make<TH1F>("h_noshare_vertex_r",               ";vtxbsdist_r (cm.)", 20,   0,      2);
    h_noshare_vertex_paird2d         = fs->make<TH1F>("h_noshare_vertex_paird2d",            ";svdist2d (cm.) every pair", 20,   0,      0.2);
    h_noshare_vertex_pairdphi        = fs->make<TH1F>("h_noshare_vertex_pairdphi",           ";|dPhi(vtx0,vtx1)| every pair", 20,  0,   3.15);
    h_noshare_track_multiplicity     = fs->make<TH1F>("h_noshare_track_multiplicity",     "",  20,   0,     40);
    h_max_noshare_track_multiplicity = fs->make<TH1F>("h_max_noshare_track_multiplicity", "",  20,   0,     40);
    h_n_output_vertices           = fs->make<TH1F>("h_n_output_vertices",           ";# of output vertices", 50, 0, 50);
	h_n_at_least_5trk_output_vertices = fs->make<TH1F>("h_n_at_least_5trk_output_vertices", ";# of output vertices w/ >=5trk/vtx", 20, 0, 20);

	
	h_noshare_trackrefine_sigmacut_vertex_chi2 = fs->make<TH1F>("h_noshare_trackrefine_sigmacut_vertex_chi2", ";chi2/dof", 20, 0, max_seed_vertex_chi2);
	h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig = fs->make<TH1F>("h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig", ";missdist sig", 20, 0, 6);
	h_noshare_trackrefine_sigmacut_vertex_distr_shift = fs->make<TH1F>("h_noshare_trackrefine_sigmacut_vertex_distr_shift", ";vtx after sigmacut'r - vtx before sigmacut'r (cm)", 20, -0.08, 0.08);

	h_noshare_trackrefine_trimmax_vertex_chi2 = fs->make<TH1F>("h_noshare_trackrefine_trimmax_vertex_chi2", ";chi2/dof", 20, 0, max_seed_vertex_chi2);
	h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig = fs->make<TH1F>("h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig", ";missdist sig", 20, 0, 6);
	h_noshare_trackrefine_trimmax_vertex_distr_shift = fs->make<TH1F>("h_noshare_trackrefine_trimmax_vertex_distr_shift", ";vtx after trimmax'r - vtx before trimmax'r (cm)", 20, -0.08, 0.08);

	h_n_at_least_5trk_output0_vertices = fs->make<TH1F>("h_n_at_least_5trk_output0_vertices", ";# of >=5trk-vertices", 20, 0, 20);
<<<<<<< HEAD
	h_at_least_5trk_output0_vertex_dBV = fs->make<TH1F>("h_at_least_5trk_output0_vertex_dBV", ";dBV (cm.) of >=5trk-vertex", 100, 0, 1.0);
=======
	h_at_least_5trk_output0_vertex_dBV = fs->make<TH1F>("h_at_least_5trk_output0_vertex_dBV", ";dBV (cm.) of >=5trk-vertex", 20, 0, 1.0);
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
	h_at_least_5trk_output0_vertex_bs2derr = fs->make<TH1F>("h_at_least_5trk_output0_vertex_bs2derr", ";bs2derr (cm.) of >=5trk-vertex", 20, 0, 0.05);
	h_output0_vertex_tkvtxdist = fs->make<TH1F>("h_output0_vertex_tkvtxdist", ";tkvtxdist (cm.)", 20, 0, 0.1);
	h_output0_vertex_tkvtxdisterr = fs->make<TH1F>("h_output0_vertex_tkvtxdisterr", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
	h_output0_vertex_tkvtxdistsig = fs->make<TH1F>("h_output0_vertex_tkvtxdistsig", ";tkvtxdistsig", 20, 0, 6);
	h_output0_vertex_ntracks = fs->make<TH1F>("h_output0_vertex_ntracks", ";ntracks/vtx", 30, 0, 30);
	h_output0_vertex_mass = fs->make<TH1F>("h_output0_vertex_mass", ";mass/vtx (GeV)", 20, 0, 1000);
	h_output0_vertex_track_weights = fs->make<TH1F>("h_output0_vertex_track_weights", ";vertex track weights", 21, 0, 1.05);
<<<<<<< HEAD
	h_output0_vertex_chi2 = fs->make<TH1F>("h_output0_vertex_chi2", ";normalized chi2", 20, 0, max_seed_vertex_chi2);
=======
	h_output0_vertex_chi2 = fs->make<TH1F>("h_output0_vertex_chi2", ";chi2", 20, 0, max_seed_vertex_chi2);
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
	h_output0_vertex_ndof = fs->make<TH1F>("h_output0_vertex_ndof", ";ndof", 10, 0, 20);
	h_output0_vertex_x = fs->make<TH1F>("h_output0_vertex_x", ";vtxbsdist_x (cm.)", 20, -1, 1);
	h_output0_vertex_y = fs->make<TH1F>("h_output0_vertex_y", ";vtxbsdist_y (cm.)", 20, -1, 1);
	h_output0_vertex_rho = fs->make<TH1F>("h_output0_vertex_rho", ";vtx rho", 20, 0, 2);
	h_output0_vertex_phi = fs->make<TH1F>("h_output0_vertex_phi", ";vtx phi", 20, -3.15, 3.15);
	h_output0_vertex_z = fs->make<TH1F>("h_output0_vertex_z", ";vtxbsdist_z (cm.)", 20, -20, 20);
	h_output0_vertex_r = fs->make<TH1F>("h_output0_vertex_r", ";vtxbsdist_r (cm.)", 20, 0, 2);
	h_output0_vertex_paird2d = fs->make<TH1F>("h_output0_vertex_paird2d", ";svdist2d (cm.) every pair", 20, 0, 0.2);
	h_output0_vertex_paird2dsig = fs->make<TH1F>("h_output0_vertex_paird2dsig", ";svdist2d significance every pair", 20, 0, 20);
	h_output0_vertex_pairdphi = fs->make<TH1F>("h_output0_vertex_pairdphi", ";|dPhi(vtx0,vtx1)| every pair", 20, 0, 3.15);
<<<<<<< HEAD
	
	h_n_at_least_5trk_output1_vertices = fs->make<TH1F>("h_n_at_least_5trk_output1_vertices", ";# of >=5trk-vertices", 20, 0, 20);
	h_at_least_5trk_output1_vertex_dBV = fs->make<TH1F>("h_at_least_5trk_output1_vertex_dBV", ";dBV (cm.) of >=5trk-vertex", 100, 0, 1.0);
=======

	h_n_at_least_5trk_output1_vertices = fs->make<TH1F>("h_n_at_least_5trk_output1_vertices", ";# of >=5trk-vertices", 20, 0, 20);
	h_at_least_5trk_output1_vertex_dBV = fs->make<TH1F>("h_at_least_5trk_output1_vertex_dBV", ";dBV (cm.) of >=5trk-vertex", 20, 0, 1.0);
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
	h_at_least_5trk_output1_vertex_bs2derr = fs->make<TH1F>("h_at_least_5trk_output1_vertex_bs2derr", ";bs2derr (cm.) of >=5trk-vertex", 20, 0, 0.05);
	h_output1_vertex_tkvtxdist = fs->make<TH1F>("h_output1_vertex_tkvtxdist", ";tkvtxdist (cm.)", 20, 0, 0.1);
	h_output1_vertex_tkvtxdisterr = fs->make<TH1F>("h_output1_vertex_tkvtxdisterr", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
	h_output1_vertex_tkvtxdistsig = fs->make<TH1F>("h_output1_vertex_tkvtxdistsig", ";tkvtxdistsig", 20, 0, 6);
	h_output1_vertex_ntracks = fs->make<TH1F>("h_output1_vertex_ntracks", ";ntracks/vtx", 30, 0, 30);
	h_output1_vertex_mass = fs->make<TH1F>("h_output1_vertex_mass", ";mass/vtx (GeV)", 20, 0, 1000);
	h_output1_vertex_track_weights = fs->make<TH1F>("h_output1_vertex_track_weights", ";vertex track weights", 21, 0, 1.05);
<<<<<<< HEAD
	h_output1_vertex_chi2 = fs->make<TH1F>("h_output1_vertex_chi2", ";normalized chi2", 20, 0, max_seed_vertex_chi2);
=======
	h_output1_vertex_chi2 = fs->make<TH1F>("h_output1_vertex_chi2", ";chi2", 20, 0, max_seed_vertex_chi2);
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
	h_output1_vertex_ndof = fs->make<TH1F>("h_output1_vertex_ndof", ";ndof", 10, 0, 20);
	h_output1_vertex_x = fs->make<TH1F>("h_output1_vertex_x", ";vtxbsdist_x (cm.)", 20, -1, 1);
	h_output1_vertex_y = fs->make<TH1F>("h_output1_vertex_y", ";vtxbsdist_y (cm.)", 20, -1, 1);
	h_output1_vertex_rho = fs->make<TH1F>("h_output1_vertex_rho", ";vtx rho", 20, 0, 2);
	h_output1_vertex_phi = fs->make<TH1F>("h_output1_vertex_phi", ";vtx phi", 20, -3.15, 3.15);
	h_output1_vertex_z = fs->make<TH1F>("h_output1_vertex_z", ";vtxbsdist_z (cm.)", 20, -20, 20);
	h_output1_vertex_r = fs->make<TH1F>("h_output1_vertex_r", ";vtxbsdist_r (cm.)", 20, 0, 2);
	h_output1_vertex_paird2d = fs->make<TH1F>("h_output1_vertex_paird2d", ";svdist2d (cm.) every pair", 20, 0, 0.2);
	h_output1_vertex_paird2dsig = fs->make<TH1F>("h_output1_vertex_paird2dsig", ";svdist2d significance every pair", 20, 0, 20);
	h_output1_vertex_pairdphi = fs->make<TH1F>("h_output1_vertex_pairdphi", ";|dPhi(vtx0,vtx1)| every pair", 20, 0, 3.15);
	
<<<<<<< HEAD
	h_output1_after_merged_criteria_vertex_chi2 = fs->make<TH1F>("h_output1_after_merged_criteria_vertex_chi2", ";normalized chi2 w/ n-1 cuts applied", 20, 0, 20);
	h_output1_after_merged_criteria_vertex_ntracks = fs->make<TH1F>("h_output1_after_merged_criteria_vertex_ntracks", ";ntracks/vtx w/ n-1 cuts applied", 30, 0, 30);
	h_output1_after_merged_criteria_vertex_bs2derr = fs->make<TH1F>("h_output1_after_merged_criteria_vertex_bs2derr", ";bs2derr (cm.) w/ n-1 cuts applied", 20, 0, 0.05);
	h_output1_after_merged_criteria_vertex_dBV = fs->make<TH1F>("h_output1_after_merged_criteria_vertex_dBV", ";dBV (cm.) w/ n-1 cuts applied", 100, 0, 1.0);

	h_output1_most_track_vertices_shared_jets_or_not = fs->make<TH1F>("h_output1_most_track_vertices_shared_jets_or_not", ";two most-track vertices share jet?", 2, 0, 2);
	
	//case X {1,1}

    h_qualify_most_track_vertices_nsharedjet = fs->make<TH1F>("h_qualify_most_track_vertices_nsharedjet", ";nsharedjet/two qualify most-track vertices", 20, 0, 20);
	h_qualify_most_track_vertices_X_nsharedjet = fs->make<TH1F>("h_qualify_most_track_vertices_X_nsharedjet", "only {1,1} events; {1,1} nsharedjet", 20, 0, 20);
	h_qualify_most_5trk_track_vertices_Xa_nsharedjet = fs->make<TH1F>("h_qualify_most_5trk_track_vertices_Xa_nsharedjet", "only {1,1} events w/ (a) 5-trk x 5-trk; {1,1} nsharedjet", 20, 0, 20);
	h_qualify_most_5trk_track_vertices_Xb_nsharedjet = fs->make<TH1F>("h_qualify_most_5trk_track_vertices_Xb_nsharedjet", "only {1,1} events w/ (b) 5-trk x >5-trk;{1,1} nsharedjet", 20, 0, 20);
	h_qualify_most_5trk_track_vertices_Xc_nsharedjet = fs->make<TH1F>("h_qualify_most_5trk_track_vertices_Xc_nsharedjet", "only {1,1} events w/ (c) >5-trk x >5-trk;{1,1} nsharedjet", 20, 0, 20);
	h_qualify_most_track_vertices_Y_nsharedjet = fs->make<TH1F>("h_qualify_most_track_vertices_Y_nsharedjet", "only {1,n>1} events ;{1,n>1} nsharedjet", 20, 0, 20);
	h_2D_qualify_most_track_vertices_XandY_nsharedjet = fs->make<TH2F>("h_2D_qualify_most_track_vertices_XandY_nsharedjet", "only {1,1}+{1,n>1} events ;{1,1} nsharedjet;{1,n>1} nsharedjet", 20, 0, 20, 20, 0, 20);

	h_2D_most_5trk_track_vertices_X_Deltachi2_SV0_SV1 = fs->make<TH2F>("h_2D_most_5trk_track_vertices_X_Deltachi2_SV0_SV1", "only {1,1} events;Delta-non-normalized-chi2(SV0);Delta-non-normalized-chi2(SV1)",200, -200, 0, 200, -200, 0);
	h_2D_most_5trk_track_vertices_Xa_Deltachi2_SV0_SV1 = fs->make<TH2F>("h_2D_most_5trk_track_vertices_Xa_Deltachi2_SV0_SV1", "only {1,1} events w/ (a) 5-trk x 5-trk ;Delta-non-normalized-chi2(SV0);Delta-non-normalized-chi2(SV1)", 200, -200, 0, 200, -200, 0);
	h_2D_most_5trk_track_vertices_Xb_Deltachi2_SV0_SV1 = fs->make<TH2F>("h_2D_most_5trk_track_vertices_Xb_Deltachi2_SV0_SV1", "only {1,1} events w/ (b) 5-trk x >5-trk ;Delta-non-normalized-chi2(SV0);Delta-non-normalized-chi2(SV1)", 200, -200, 0, 200, -200, 0);
	h_2D_most_5trk_track_vertices_Xc_Deltachi2_SV0_SV1 = fs->make<TH2F>("h_2D_most_5trk_track_vertices_Xc_Deltachi2_SV0_SV1", "only {1,1} events w/ (c) >5-trk x >5-trk ;Delta-non-normalized-chi2(SV0);Delta-non-normalized-chi2(SV1)", 200, -200, 0, 200, -200, 0);


	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_X = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_X", "{1,1} shared jets w/ >=3trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet", "{1,1} shared jets w/ >=3trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet", "{1,1} shared jets w/ >=3trk/vtx && 0.2 < dR ; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);

	h_at_least_3trk_output1_shared_tracks_pair_dR_sig_X = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_sig_X", "{1,1} shared jets w/ >=3trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_at_least_3trk_output1_shared_tracks_pair_dR_X = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_X", "{1,1} shared jets w/ >=3trk/vtx; dR of a shared-track pair", 500, 0, 1);
	
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X", "{1,1} shared jets w/ >=3trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet", "{1,1} shared jets w/ >=3trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet", "{1,1} shared jets w/ >=3trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);

	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_X", "{1,1} shared jets w/ >=5trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_X", "{1,1} shared jets w/ >=5trk/vtx && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);

	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet", "{1,1} shared jets w/ >=5trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRinjet", "{1,1} shared jets w/ >=5trk/vtx && dR < 0.2 && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);

	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet", "{1,1} shared jets w/ >=5trk/vtx && 0.2 < dR ; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRoutjet", "{1,1} shared jets w/ >=5trk/vtx && 0.2 < dR && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);

	h_at_least_5trk_output1_shared_tracks_pair_dR_sig_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_sig_X", "{1,1} shared jets w/ >=5trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_at_least_5trk_output1_shared_tracks_pair_dR_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_X", "{1,1} shared jets w/ >=5trk/vtx; dR of a shared-track pair", 500, 0, 1);
	
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X", "{1,1} shared jets w/ >=5trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);

	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet", "{1,1} shared jets w/ >=5trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet", "{1,1} shared jets w/ >=5trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);

	h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_X", "remove {1,1} shared jets by non-normalized chi2;shift in non-normalized chi2", 2000, -200, 0);
	h_at_least_5trk_output1_shared_tracks_pair_X_nsv_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_X_nsv_X", "remove {1,1} shared jets by non-normalized chi2;nsv(only {1,1} events)", 3, 0, 3);
	h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_X", "only {1,1} events ;old non-normalized chi2 ", 2000, 0, 200);
	h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_X", "only {1,1} events ;new non-normalized chi2 ", 2000, 0, 200);
    
	h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_X", "only {1,1} events;|dPhi(vtx0,vtx1)|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_dPhi_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dPhi_X", "only {1,1} events;|dPhi of two lone shared tracks|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_X = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_X", "only {1,1} events;|dPhi(jet,closest-vtx)|", 200, 0, 3.15);

	h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xa = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xa", "only {1,1} events w/ (a) 5-trk x 5-trk;|dPhi of two lone shared tracks|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xb = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xb", "only {1,1} events w/ (b) >5-trk x 5-trk;|dPhi of two lone shared tracks|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xc = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xc", "only {1,1} events w/ (c) >5-trk x >5-trk;|dPhi of two lone shared tracks|", 200, 0, 3.15);

	h_2D_at_least_5trk_output1_shared_track_vtx0_shared_track_vtx1_dPhi_X = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_track_vtx0_shared_track_vtx1_dPhi_X", "only {1,1} events;|dPhi(SV0,its lone shared track)|;|dPhi(SV1,its lone shared track)|", 200, 0, 3.15, 200, 0, 3.15);
	
	h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xa = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xa", "only {1,1} events w/ (a) 5-trk x 5-trk;|dPhi(vtx0,vtx1)|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xb = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xb", "only {1,1} events w/ (b) >5-trk x 5-trk;|dPhi(vtx0,vtx1)|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xc = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xc", "only {1,1} events w/ (c) >5-trk x >5-trk;|dPhi(vtx0,vtx1)|", 200, 0, 3.15);

	h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xa = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xa", "only {1,1} events w/ (a) 5-trk x 5-trk;|dPhi(jet,closest-vtx)|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xb = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xb", "only {1,1} events w/ (b) >5-trk x 5-trk;|dPhi(jet,closest-vtx)|", 200, 0, 3.15);
	h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xc = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xc", "only {1,1} events w/ (c) >5-trk x >5-trk;|dPhi(jet,closest-vtx)|", 200, 0, 3.15);


	//case Y {1,n>1} 

	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_Y = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_Y", "{1,n>1} shared jets w/ >=3trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet", "{1,n>1} shared jets w/ >=3trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet", "{1,n>1} shared jets w/ >=3trk/vtx && 0.2 < dR ; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	
	h_at_least_3trk_output1_shared_tracks_pair_dR_sig_Y = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_sig_Y", "{1,n>1} shared jets w/ >=3trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y", "{1,n>1} shared jets w/ >=3trk/vtx; dR significance of a shared-track pair; SV0(1)'s shared ntrack", 50, 0, 10, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_Y = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_Y", "{1,n>1} shared jets w/ >=3trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_Y = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_Y", "{1,n>1} shared jets w/ >=3trk/vtx; dR of a shared-track pair; SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_err_Y = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_err_Y", "{1,n>1} shared jets w/ >=3trk/vtx; dR err of the n-shared tracks", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y", "{1,n>1} shared jets w/ >=3trk/vtx; dR err of the n-shared tracks; SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);

	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_Y = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_Y", "{1,n>1} shared jets w/ >=3trk/vtx; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet", "{1,n>1} shared jets w/ >=3trk/vtx && dR < 0.2; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet", "{1,n>1} shared jets w/ >=3trk/vtx && 0.2 < dR ; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	

	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y", "{1,n>1} shared jets w/ >=3trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet", "{1,n>1} shared jets w/ >=3trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet", "{1,n>1} shared jets w/ >=3trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet", "{1,n>1} shared jets w/ >=3trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet", "{1,n>1} shared jets w/ >=3trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_Y", "{1,n>1} shared jets w/ >=5trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_Y", "{1,n>1} shared jets w/ >=5trk/vtx && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
    h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet", "{1,n>1} shared jets w/ >=5trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRinjet", "{1,n>1} shared jets w/ >=5trk/vtx && dR < 0.2 && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet", "{1,n>1} shared jets w/ >=5trk/vtx && 0.2 < dR ; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRoutjet", "{1,n>1} shared jets w/ >=5trk/vtx && 0.2 < dR && |diff MDS| > 4 ; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRinjet", "{1,n>1} case A: w/ >=5trk/vtx && dR < 0.2; #frac{tight SVa's sum pT - tight SVb's sum pT}{tight SVa's sum pT + tight SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRinjet", "{1,n>1} case A: w/ >=5trk/vtx && dR < 0.2 && diff MDS < -4; #frac{tight SVa's sum pT - tight SVb's sum pT}{tight SVa's sum pT + tight SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRoutjet", "{1,n>1} case A: w/ >=5trk/vtx && 0.2 < dR ; #frac{tight SVa's sum pT - tight SVb's sum pT}{tight SVa's sum pT + tight SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRoutjet", "{1,n>1} case A: w/ >=5trk/vtx && 0.2 < dR && diff MDS < -4; #frac{tight SVa's sum pT - tight SVb's sum pT}{tight SVa's sum pT + tight SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRinjet", "{1,n>1} case B: w/ >=5trk/vtx && dR < 0.2; #frac{loose SVa's sum pT - loose SVb's sum pT}{loose SVa's sum pT + loose SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRinjet", "{1,n>1} case B: w/ >=5trk/vtx && dR < 0.2 && diff MDS < -4; #frac{loose SVa's sum pT - loose SVb's sum pT}{loose SVa's sum pT + loose SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRoutjet", "{1,n>1} case B: w/ >=5trk/vtx && 0.2 < dR ; #frac{loose SVa's sum pT - loose SVb's sum pT}{loose SVa's sum pT + loose SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRoutjet", "{1,n>1} case B: w/ >=5trk/vtx && 0.2 < dR && diff MDS < -4; #frac{loose SVa's sum pT - loose SVb's sum pT}{loose SVa's sum pT + loose SVb's sum pT}", 20, -1, 1);

	h_at_least_5trk_output1_shared_tracks_pair_dR_sig_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_sig_Y", "{1,n>1} shared jets w/ >=5trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y", "{1,n>1} shared jets w/ >=5trk/vtx; dR significance of a shared-track pair; SV0(1)'s shared ntrack", 50, 0, 10, 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_dR_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_Y", "{1,n>1} shared jets w/ >=5trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_2D_at_least_5trk_output1_shared_tracks_pair_dR_shared_tracks_Y = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_dR_shared_tracks_Y", "{1,n>1} shared jets w/ >=5trk/vtx; dR of a shared-track pair; SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_dR_err_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_err_Y", "{1,n>1} shared jets w/ >=5trk/vtx; dR err of the n-shared tracks", 500, 0, 1);
	h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y", "{1,n>1} shared jets w/ >=5trk/vtx; dR err of the n-shared tracks; SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);

	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_Y", "{1,n>1} shared jets w/ >=5trk/vtx; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet", "{1,n>1} shared jets w/ >=5trk/vtx && 0.2 < dR; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet", "{1,n>1} shared jets w/ >=5trk/vtx && 0.2 < dR ; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRinjet", "{1,n>1} case A: w/ >=5trk/vtx && dR < 0.2; tight SVa's shared ntrack - tight SVb's shared ntrack", 60, -30, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRoutjet", "{1,n>1} case A: w/ >=5trk/vtx && 0.2 < dR ; tight SVa's shared ntrack - tight SVb's shared ntrack", 60, -30, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRinjet", "{1,n>1} case B: w/ >=5trk/vtx && dR < 0.2; loose SVa's shared ntrack - loose SVb's shared ntrack", 60, -30, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRoutjet", "{1,n>1} case B: w/ >=5trk/vtx && 0.2 < dR ; loose SVa's shared ntrack - loose SVb's shared ntrack", 60, -30, 30);

	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y", "{1,n>1} shared jets w/ >=5trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet", "{1,n>1} shared jets w/ >=5trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet", "{1,n>1} shared jets w/ >=5trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRinjet", "{1,n>1} case A: w/ >=5trk/vtx && dR < 0.2; tight SVa's median miss-dist sig - tight SVb's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRoutjet", "{1,n>1} case A: w/ >=5trk/vtx && 0.2 < dR; tight SVa's median miss-dist sig - tight SVb's median miss-dist sig", 30, -6, 6);
    h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRinjet", "{1,n>1} case B: w/ >=5trk/vtx && dR < 0.2; loose SVa's median miss-dist sig - loose SVb's median miss-dist sig", 30, -6, 6);
    h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRoutjet", "{1,n>1} case B: w/ >=5trk/vtx && 0.2 < dR; loose SVa's median miss-dist sig - loose SVb's median miss-dist sig", 30, -6, 6);
          
	h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_sumpT_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_sumpT_Y", "remove {1,n} shared jets by sum pT;shift in non-normalized chi2", 2000, -200, 0);
	h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_shared_ntrack_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_shared_ntrack_Y", "remove {1,n} shared jets by a single shared ntrack;shift in non-normalized chi2", 2000, -200, 0);
	
	h_2D_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2 = fs->make<TH2F>("h_2D_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2", "two-most track vertices w/o shared jets; ntrack; non-normalized chi2", 50,0,50, 2000, 0, 200);
	//h_2Dpfx_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2 = fs->make<TH2F>("h_2Dpfx_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2", "remove the first track of two-most track vertices w/o shared jets; ntrack; mean non-normalized chi2", 50, 0, 50, 0, 100,"h");
	h_at_least_5trk_output1_no_shared_tracks_pair_shift_unnorm_chi2 = fs->make<TH1F>("h_at_least_5trk_output1_no_shared_tracks_pair_shift_unnorm_chi2", "remove the first track of two-most track vertices w/o shared jets;shift in non-normalized chi2", 1000, -100, 0);
	//h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_onejet_by_sumpT_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_onejet_by_sumpT_Y", "remove only one {1,n} shared jets by sum pT;shift in non-normalized chi2", 20, -200, 0);
	//h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_onejet_by_shared_ntrack_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_onejet_by_shared_ntrack_Y", "remove only one {1,n} shared jets by a single shared ntrack;shift in non-normalized chi2", 20, -200, 0);


	h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_Y", "remove {1,n>1} shared jets by sum pT;nsv", 3, 0, 3);
	h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_Y", "remove {1,n>1} shared jets by a single shared ntrack;nsv", 3, 0, 3);
	h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_YandX = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_YandX", "remove {1,1} && {1,n>1} shared jets by sum pT;nsv", 3, 0, 3);
	h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_YandX = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_YandX", "remove {1,1} && {1,n>1} shared jets by a single shared ntrack;nsv", 3, 0, 3);

	h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_sumpT_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_sumpT_Y", "remove {1,n>1} shared jets by sum pT;nsv(only {1,n>1} events)", 3, 0, 3);
	h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_shared_ntrack_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_shared_ntrack_Y", "remove {1,n>1} shared jets by a single shared ntrack;nsv(only {1,n>1} events)", 3, 0, 3);


	h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_sumpT_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_sumpT_Y", "only {1,n>1} events to be resolved by sum pT;old non-normalized chi2", 2000, 0, 200);
	h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_sumpT_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_sumpT_Y", "only {1,n>1} events to be resolved by sum pT;new non-normalized chi2", 2000, 0, 200);
	h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_shared_ntrack_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_ntrack_Y", "only {1,n>1} events to be resolved by a lone shared trk;old non-normalized chi2", 2000, 0, 200);
	h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_shared_ntrack_Y = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_ntrack_Y", "only {1,n>1} events to be resolved by a lone shared trk;new non-normalized chi2", 2000, 0, 200);
	//case Z {n>1,m>1}
	

	
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx && 0.2 < dR; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
        h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRinjet", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRoutjet", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx && 0.2 < dR; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);

	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZO = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet", "{n>1,m>1} shared jets w/ >=3trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet", "{n>1,m>1} shared jets w/ >=3trk/vtx && 0.2 < dR; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	
	h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZnonC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_diff_shared_tracks_ZnonC = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_diff_shared_tracks_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; dR significance of a shared-track pair; SVa's shared ntrack - SVb's shared ntrack", 50, 0, 10, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_ZnonC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_diff_shared_tracks_ZnonC = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_diff_shared_tracks_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; dR of a shared-track pair; SVa's shared ntrack - SVb's shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZnonC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; dR err of a shared-track pair", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_diff_shared_tracks_ZnonC = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_diff_shared_tracks_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; dR err of a shared-track pair; SVa's shared ntrack - SVb's shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_ZC = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; dR significance of a shared-track pair; SV0(1)'s shared ntrack", 50, 0, 10, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_ZC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_ZC = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; dR of a shared-track pair; SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; dR err of a shared-track pair", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_ZC = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; dR err of a shared-track pair; SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZO = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; dR significance of a shared-track pair; [2x] SV0(1)'s shared ntrack", 50, 0, 10, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_ZO = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO", "{n>1,m>1} case shared jets trk: w/ >=3trk/vtx; dR of a shared-track pair; [2x] SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZO = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; dR err of a shared-track pair", 500, 0, 1);
	h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; dR err of a shared-track pair; [2x] SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);

	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet", "{n>1,m>1} shared jets w/ >=3trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet", "{n>1,m>1} shared jets w/ >=3trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
          h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
        h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonC", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
        h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRinjet", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRoutjet", "{n>1,m>1} case non-equal shared trk: w/ >=3trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);


	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZO = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; SV0's median shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_2D_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZO", "{n>1,m>1} shared jets w/ >=3trk/vtx; SV0's shared ntrack; SV1's shared ntrack", 30, 0, 30, 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet", "{n>1,m>1} shared jets w/ >=3trk/vtx && dR < 0.2; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet", "{n>1,m>1} shared jets w/ >=3trk/vtx && 0.2 < dR; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZC", "{n>1,m>1} case equal shared trk: w/ >=3trk/vtx; SV0(1)'s shared ntrack ", 30, 0, 30);
	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonC = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonC", "{n>1,m>1} non-equal shared jets w/ >=3trk/vtx; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRinjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRinjet", "{n>1,m>1} non-equal shared jets w/ >=3trk/vtx && dR < 0.2; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRoutjet = fs->make<TH1F>("h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRoutjet", "{n>1,m>1} non-equal shared jets w/ >=3trk/vtx && 0.2 < dR; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);

	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRinjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && dR < 0.2 && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && 0.2 < dR ; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRoutjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && 0.2 < dR && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);

	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && dR < 0.2; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && 0.2 < dR; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);


	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZA = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZA", "{n>1,m>1} case A: w/ >=5trk/vtx; #frac{tight SVa's sum pT - tight SVb's sum pT}{tight SVa's sum pT + tight SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRinjet", "{n>1,m>1} case A: w/ >=5trk/vtx && dR < 0.2; #frac{tight SVa's sum pT - tight SVb's sum pT}{tight SVa's sum pT + tight SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRoutjet", "{n>1,m>1} case A: w/ >=5trk/vtx && 0.2 < dR; #frac{tight SVa's sum pT - tight SVb's sum pT}{tight SVa's sum pT + tight SVb's sum pT}", 20, -1, 1);
	
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZB = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZB", "{n>1,m>1} case B: w/ >=5trk/vtx; #frac{loose SVa's sum pT - loose SVb's sum pT}{loose SVa's sum pT + loose SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRinjet", "{n>1,m>1} case B: w/ >=5trk/vtx && dR < 0.2; #frac{loose SVa's sum pT - loose SVb's sum pT}{loose SVa's sum pT + loose SVb's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRoutjet", "{n>1,m>1} case B: w/ >=5trk/vtx && 0.2 < dR ; #frac{loose SVa's sum pT - loose SVb's sum pT}{loose SVa's sum pT + loose SVb's sum pT}", 20, -1, 1);
	
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZC = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZC", "{n>1,m>1} case C: w/ >=5trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet", "{n>1,m>1} case C: w/ >=5trk/vtx && dR < 0.2; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet", "{n>1,m>1} case C: w/ >=5trk/vtx && 0.2 < dR; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZO = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZO = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx && dR < 0.2 && |diff MDS| > 4; #frac{SV0's sum pT - SV1's sum pT}{SV0's sum pT + SV1's sum pT}", 20, -1, 1);
	
	h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZA = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZA", "{n>1,m>1} case A: w/ >=5trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_at_least_5trk_output1_shared_tracks_pair_dR_ZA = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_ZA", "{n>1,m>1} case A: w/ >=5trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZA = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZA", "{n>1,m>1} case A: w/ >=5trk/vtx; dR err of a shared-track pair", 500, 0, 1);
	h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZB = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZB", "{n>1,m>1} case B: w/ >=5trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_at_least_5trk_output1_shared_tracks_pair_dR_ZB = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_ZB", "{n>1,m>1} case B: w/ >=5trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZB = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZB", "{n>1,m>1} case B: w/ >=5trk/vtx; dR err of a shared-track pair", 500, 0, 1);
	h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZC = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZC", "{n>1,m>1} case C: w/ >=5trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_at_least_5trk_output1_shared_tracks_pair_dR_ZC = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_ZC", "{n>1,m>1} case C: w/ >=5trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZC = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZC", "{n>1,m>1} case C: w/ >=5trk/vtx; dR err of a shared-track pair", 500, 0, 1);
	h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZO = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; dR significance of a shared-track pair", 50, 0, 10);
	h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; dR significance of a shared-track pair; [2x] SV0(1)'s shared ntrack", 50, 0, 10, 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_dR_ZO = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; dR of a shared-track pair", 500, 0, 1);
	h_2D_at_least_5trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO", "{n>1,m>1} case shared jets trk: w/ >=5trk/vtx; dR of a shared-track pair; [2x] SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZO = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; dR err of a shared-track pair", 500, 0, 1);
	h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO", "{n>1,m>1} case equal shared trk: w/ >=5trk/vtx; dR err of a shared-track pair; [2x] SV0(1)'s shared ntrack", 500, 0, 1, 30, 0, 30);

	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZA = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZA", "{n>1,m>1} case A: w/ >=5trk/vtx; tight SVa's median miss-dist sig - tight SVb's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRinjet", "{n>1,m>1} case A: w/ >=5trk/vtx && dR < 0.2; tight SVa's median miss-dist sig - tight SVb's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRoutjet", "{n>1,m>1} case A: w/ >=5trk/vtx && 0.2 < dR; tight SVa's median miss-dist sig - tight SVb's median miss-dist sig", 30, -6, 6);
	
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZB = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZB", "{n>1,m>1} case B: w/ >=5trk/vtx; loose SVa's median miss-dist sig - loose SVb's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRinjet", "{n>1,m>1} case B: w/ >=5trk/vtx && dR < 0.2; loose SVa's median miss-dist sig - loose SVb's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRoutjet", "{n>1,m>1} case B: w/ >=5trk/vtx && 0.2 < dR; loose SVa's median miss-dist sig - loose SVb's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC", "{n>1,m>1} case C: w/ >=5trk/vtx; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet", "{n>1,m>1} case C: w/ >=5trk/vtx && dRsig < 1; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet", "{n>1,m>1} case C: w/ >=5trk/vtx && 1 < dRsig < 1.5; SV0's median miss-dist sig - SV1's median miss-dist sig", 30, -6, 6);
	
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZO = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && dR < 0.2; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
          h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet", "{n>1,m>1} shared jets w/ >=5trk/vtx && 0.2 < dR; SV0's shared ntrack - SV1's shared ntrack", 60, -30, 30);
        
        h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZO = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZO", "{n>1,m>1} shared jets w/ >=5trk/vtx; SV0's shared ntrack; SV1's shared ntrack", 30, 0, 30, 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZA = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZA", "{n>1,m>1} case A: w/ >=5trk/vtx; tight SVa's shared ntrack - tight SVb's shared ntrack", 60, -30, 30);
	h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZA = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZA", "{n>1,m>1} case A: w/ >=5trk/vtx; tight SVa's shared ntrack; tight SVb's shared ntrack", 30, 0, 30, 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRinjet", "{n>1,m>1} case A: w/ >=5trk/vtx && dR < 0.2; tight SVa's shared ntrack - tight SVb's shared ntrack", 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRoutjet", "{n>1,m>1} case A: w/ >=5trk/vtx && 0.2 < dR; tight SVa's shared ntrack - tight SVb's shared ntrack", 30, 0, 30);
	
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZB = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZB", "{n>1,m>1} case B: w/ >=5trk/vtx; loose SVa's shared ntrack - loose SVb's shared ntrack", 30, 0, 30);
	h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZB = fs->make<TH2F>("h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZB", "{n>1,m>1} case B: w/ >=5trk/vtx; loose SVa's shared ntrack; loose SVb's shared ntrack", 30, 0, 30, 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRinjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRinjet", "{n>1,m>1} case B: w/ >=5trk/vtx && dR < 0.2; loose SVa's shared ntrack - loose SVb's shared ntrack", 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRoutjet = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRoutjet", "{n>1,m>1} case B: w/ >=5trk/vtx && 0.2 < dR; loose SVa's shared ntrack - loose SVb's shared ntrack", 30, 0, 30);
	h_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZC = fs->make<TH1F>("h_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZC", "{n>1,m>1} case C: w/ >=5trk/vtx; SV0(1)'s shared ntrack ", 30, 0, 30);


	

	h_qualify_svdist2d_three_bins = fs->make<TH1F>("h_qualify_svdist2d_three_bins", "no shared-jet mitigation;dist2d(sv #0, #1) (cm);arb. units", 3, edges);
	h_qualify_by_sum_pT_svdist2d_three_bins = fs->make<TH1F>("h_qualify_by_sum_pT_svdist2d_three_bins", "shared-jet mitigation w/ sum pT;dist2d(sv #0, #1) (cm);arb. units", 3, edges);
	h_qualify_only_small_dR_by_sum_pT_svdist2d_three_bins = fs->make<TH1F>("h_qualify_only_small_dR_by_sum_pT_svdist2d_three_bins", "shared-jet mitigation w/ sum pT (only events dR sig <1);dist2d(sv #0, #1) (cm);arb. units", 3, edges);
	h_qualify_by_median_tkvtxdist_svdist2d_three_bins = fs->make<TH1F>("h_qualify_by_median_tkvtxdist_svdist2d_three_bins", "shared-jet mitigation w/ median_tkvtxdist;dist2d(sv #0, #1) (cm);arb. units", 3, edges);
	h_qualify_only_small_dR_by_median_tkvtxdist_svdist2d_three_bins = fs->make<TH1F>("h_qualify_only_small_dR_by_median_tkvtxdist_svdist2d_three_bins", "shared-jet mitigation w/ median tkvtxdist (only events dR sig <1);dist2d(sv #0, #1) (cm);arb. units", 3, edges);
	h_qualify_by_median_tkvtxdistsig_svdist2d_three_bins = fs->make<TH1F>("h_qualify_by_median_tkvtxdistsig_svdist2d_three_bins", "shared-jet mitigation w/ median_tkvtxdistsig;dist2d(sv #0, #1) (cm);arb. units", 3, edges);
	h_qualify_only_small_dR_by_median_tkvtxdistsig_svdist2d_three_bins = fs->make<TH1F>("h_qualify_only_small_dR_by_median_tkvtxdistsig_svdist2d_three_bins", "shared-jet mitigation w/ median tkvtxdistsig (only events dR sig <1);dist2d(sv #0, #1) (cm);arb. units", 3, edges);
	h_qualify_only_small_dR_by_2sigma_median_tkvtxdistsig_svdist2d_three_bins = fs->make<TH1F>("h_qualify_only_small_dR_by_2sigma_median_tkvtxdistsig_svdist2d_three_bins", "shared-jet mitigation w/ 2#sigma median tkvtxdistsig (only events dR sig <1);dist2d(sv #0, #1) (cm);arb. units", 3, edges);

	
	h_n_at_least_5trk_output2_vertices = fs->make<TH1F>("h_n_at_least_5trk_output2_vertices", ";# of >=5trk-vertices", 20, 0, 20);
	h_at_least_5trk_output2_vertex_dBV = fs->make<TH1F>("h_at_least_5trk_output2_vertex_dBV", ";dBV (cm.) of >=5trk-vertex", 100, 0, 1.0);
	h_at_least_5trk_output2_vertex_bs2derr = fs->make<TH1F>("h_at_least_5trk_output2_vertex_bs2derr", ";bs2derr (cm.) of >=5trk-vertex", 20, 0, 0.05);
	h_output2_vertex_tkvtxdist = fs->make<TH1F>("h_output2_vertex_tkvtxdist", ";tkvtxdist (cm.)", 20, 0, 0.1);
	h_output2_vertex_tkvtxdisterr = fs->make<TH1F>("h_output2_vertex_tkvtxdisterr", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
	h_output2_vertex_tkvtxdistsig = fs->make<TH1F>("h_output2_vertex_tkvtxdistsig", ";tkvtxdistsig", 20, 0, 6);
	h_output2_vertex_ntracks = fs->make<TH1F>("h_output2_vertex_ntracks", ";ntracks/vtx", 30, 0, 30);
	h_output2_vertex_mass = fs->make<TH1F>("h_output2_vertex_mass", ";mass/vtx (GeV)", 20, 0, 1000);
	h_output2_vertex_track_weights = fs->make<TH1F>("h_output2_vertex_track_weights", ";vertex track weights", 21, 0, 1.05);
	h_output2_vertex_chi2 = fs->make<TH1F>("h_output2_vertex_chi2", ";normalized chi2", 20, 0, max_seed_vertex_chi2);
	h_output2_vertex_ndof = fs->make<TH1F>("h_output2_vertex_ndof", ";ndof", 10, 0, 20);
	h_output2_vertex_x = fs->make<TH1F>("h_output2_vertex_x", ";vtxbsdist_x (cm.)", 20, -1, 1);
	h_output2_vertex_y = fs->make<TH1F>("h_output2_vertex_y", ";vtxbsdist_y (cm.)", 20, -1, 1);
	h_output2_vertex_rho = fs->make<TH1F>("h_output2_vertex_rho", ";vtx rho", 20, 0, 2);
	h_output2_vertex_phi = fs->make<TH1F>("h_output2_vertex_phi", ";vtx phi", 20, -3.15, 3.15);
	h_output2_vertex_z = fs->make<TH1F>("h_output2_vertex_z", ";vtxbsdist_z (cm.)", 20, -20, 20);
	h_output2_vertex_r = fs->make<TH1F>("h_output2_vertex_r", ";vtxbsdist_r (cm.)", 20, 0, 2);
	h_output2_vertex_paird2d = fs->make<TH1F>("h_output2_vertex_paird2d", ";svdist2d (cm.) every pair", 20, 0, 0.2);
	h_output2_vertex_paird2dsig = fs->make<TH1F>("h_output2_vertex_paird2dsig", ";svdist2d significance every pair", 20, 0, 20);
	h_output2_vertex_pairdphi = fs->make<TH1F>("h_output2_vertex_pairdphi", ";|dPhi(vtx0,vtx1)| every pair", 20, 0, 3.15);
=======
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
}
}

void MFVVertexer::finish(edm::Event& event, const std::vector<reco::TransientTrack>& seed_tracks, std::unique_ptr<reco::VertexCollection> vertices, std::unique_ptr<VertexerPairEffs> vpeffs, const std::vector<std::pair<track_set, track_set>>& vpeffs_tracks) {
  std::unique_ptr<reco::TrackCollection> tracks_seed      (new reco::TrackCollection);
  std::unique_ptr<reco::TrackCollection> tracks_inVertices(new reco::TrackCollection);

  if (verbose) printf("finish:\nseed tracks:\n");

  std::map<std::pair<unsigned, unsigned>, unsigned char> seed_track_ref_map;
  unsigned char itk = 0;
  for (const reco::TransientTrack& ttk : seed_tracks) {
    tracks_seed->push_back(ttk.track());
    const reco::TrackBaseRef& tk(ttk.trackBaseRef());
    seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())] = uint2uchar_clamp(itk++);

    if (verbose) printf("id: %i key: %lu pt: %f\n", tk.id().id(), tk.key(), tk->pt());
  }

  assert(vpeffs->size() == vpeffs_tracks.size());
  for (size_t i = 0, ie = vpeffs->size(); i < ie; ++i) {
    for (auto tk : vpeffs_tracks[i].first)  (*vpeffs)[i].tracks_push_back(0, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
    for (auto tk : vpeffs_tracks[i].second) (*vpeffs)[i].tracks_push_back(1, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
  }

  if (verbose) printf("vertices:\n");
  int count_5trk_vertices = 0;
  for (const reco::Vertex& v : *vertices) {
    if (verbose) printf("x: %f y %f z %f\n", v.x(), v.y(), v.z());
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      reco::TrackRef tk = it->castTo<reco::TrackRef>();
      if (verbose) printf("id: %i key: %u <%f,%f,%f,%f,%f>\n", tk.id().id(), tk.key(), tk->charge()*tk->pt(), tk->eta(), tk->phi(), tk->dxy(), tk->dz());
      tracks_inVertices->push_back(*tk);
    }
	if (v.nTracks() >= 5)
		++count_5trk_vertices;
  }

  if (verbose)
    printf("n_output_vertices: %lu\n", vertices->size());
  if (histos) {
    h_n_output_vertices->Fill(vertices->size());
	h_n_at_least_5trk_output_vertices->Fill(count_5trk_vertices);
  }

  event.put(std::move(vertices));
  event.put(std::move(vpeffs));
  event.put(std::move(tracks_seed),       "seed");
  event.put(std::move(tracks_inVertices), "inVertices");
}

void MFVVertexer::produce(edm::Event& event, const edm::EventSetup& setup) {
	if (verbose)
		std::cout << "MFVVertexer " << module_label << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

	edm::Handle<reco::BeamSpot> beamspot;
	event.getByToken(beamspot_token, beamspot);
	const double bsx = beamspot->position().x();
	const double bsy = beamspot->position().y();
	const double bsz = beamspot->position().z();
        
       
	edm::ESHandle<TransientTrackBuilder> tt_builder;
	setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

	edm::Handle<std::vector<reco::TrackRef>> seed_track_refs;
	event.getByToken(seed_tracks_token, seed_track_refs);

	std::vector<reco::TransientTrack> seed_tracks;
	std::map<reco::TrackRef, size_t> seed_track_ref_map;

	for (const reco::TrackRef& tk : *seed_track_refs) {
		seed_tracks.push_back(tt_builder->build(tk));
		seed_track_ref_map[tk] = seed_tracks.size() - 1;
	}

	const size_t ntk = seed_tracks.size();
	if (verbose)
		printf("n_seed_tracks: %5lu\n", ntk);

	//////////////////////////////////////////////////////////////////////
	// Form seed vertices from all pairs of tracks whose vertex fit
	// passes cuts.
	//////////////////////////////////////////////////////////////////////

	std::unique_ptr<reco::VertexCollection> vertices(new reco::VertexCollection);
	std::unique_ptr<VertexerPairEffs> vpeffs(new VertexerPairEffs);
	std::vector<std::pair<track_set, track_set>> vpeffs_tracks;

	if (ntk == 0) {
		if (verbose)
			printf("no seed tracks -> putting empty vertex collection into event\n");
		finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
		return;
	}

	std::vector<size_t> itks(n_tracks_per_seed_vertex, 0);

	auto try_seed_vertex = [&]() {
		std::vector<reco::TransientTrack> ttks(n_tracks_per_seed_vertex);
		for (int i = 0; i < n_tracks_per_seed_vertex; ++i)
			ttks[i] = seed_tracks[itks[i]];

		TransientVertex seed_vertex = kv_reco->vertex(ttks);
		if (seed_vertex.isValid() && seed_vertex.normalisedChiSquared() < max_seed_vertex_chi2) {
			vertices->push_back(reco::Vertex(seed_vertex));

			if (verbose || histos) {
				const reco::Vertex& v = vertices->back();
				const double vchi2 = v.normalizedChi2();
				const double vndof = v.ndof();
				const double vx = v.position().x() - bsx;
				const double vy = v.position().y() - bsy;
				const double vz = v.position().z() - bsz;
				const double phi = atan2(vy, vx);
				const double rho = mag(vx, vy);
				const double r = mag(vx, vy, vz);
				if (verbose) {
					printf("from tracks");
					for (auto itk : itks)
						printf(" %lu", itk);
					printf(": vertex #%3lu: chi2/dof: %7.3f dof: %7.3f pos: <%7.3f, %7.3f, %7.3f>  rho: %7.3f  phi: %7.3f  r: %7.3f\n", vertices->size() - 1, vchi2, vndof, vx, vy, vz, rho, phi, r);
				}
				if (histos) {
					for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it)
						h_seed_vertex_track_weights->Fill(v.trackWeight(*it));
					h_seed_vertex_chi2->Fill(vchi2);
					h_seed_vertex_ndof->Fill(vndof);
					h_seed_vertex_x->Fill(vx);
					h_seed_vertex_y->Fill(vy);
					h_seed_vertex_rho->Fill(rho);
					h_seed_vertex_phi->Fill(phi);
					h_seed_vertex_z->Fill(vz);
					h_seed_vertex_r->Fill(r);
				}
			}
		}
	};

	// ha
	for (size_t itk = 0; itk < ntk; ++itk) {
		itks[0] = itk;
		for (size_t jtk = itk + 1; jtk < ntk; ++jtk) {
			itks[1] = jtk;
			if (n_tracks_per_seed_vertex == 2) { try_seed_vertex(); continue; }
			for (size_t ktk = jtk + 1; ktk < ntk; ++ktk) {
				itks[2] = ktk;
				if (n_tracks_per_seed_vertex == 3) { try_seed_vertex(); continue; }
				for (size_t ltk = ktk + 1; ltk < ntk; ++ltk) {
					itks[3] = ltk;
					if (n_tracks_per_seed_vertex == 4) { try_seed_vertex(); continue; }
					for (size_t mtk = ltk + 1; mtk < ntk; ++mtk) {
						itks[4] = mtk;
						try_seed_vertex();
					}
				}
			}
		}
	}

	if (histos) {
		for (std::vector<reco::Vertex>::const_iterator v0 = vertices->begin(); v0 != vertices->end(); ++v0) {
			const double v0x = v0->position().x() - bsx;
			const double v0y = v0->position().y() - bsy;
			const double phi0 = atan2(v0y, v0x);
			for (std::vector<reco::Vertex>::const_iterator v1 = v0 + 1; v1 != vertices->end(); ++v1) {
				const double v1x = v1->position().x() - bsx;
				const double v1y = v1->position().y() - bsy;
				const double phi1 = atan2(v1y, v1x);
				h_seed_vertex_paird2d->Fill(mag(v0x - v1x, v0y - v1y));
				h_seed_vertex_pairdphi->Fill(fabs(reco::deltaPhi(phi0, phi1)));
			}
		}
	}

	if (verbose)
		printf("n_seed_vertices: %lu\n", vertices->size());
	if (histos)
		h_n_seed_vertices->Fill(vertices->size());
<<<<<<< HEAD
                
=======

>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
	//////////////////////////////////////////////////////////////////////
	// Take care of track sharing. If a track is in two vertices, and
	// the vertices are "close", refit the tracks from the two together
	// as one vertex. If the vertices are not close, keep the track in
	// the vertex to which it is "closer".
	//////////////////////////////////////////////////////////////////////

	if (verbose)
		printf("fun time!\n");

	track_set discarded_tracks;
	int n_resets = 0;
	int n_onetracks = 0;
	std::vector<reco::Vertex>::iterator v[2];
	std::vector<reco::Vertex>::iterator nv[2];
	size_t ivtx[2];
	for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
		track_set tracks[2];
		ivtx[0] = v[0] - vertices->begin();
		tracks[0] = vertex_track_set(*v[0]);

		if (tracks[0].size() < 2) {
			if (verbose)
				printf("track-sharing: vertex-0 #%lu is down to one track, junking it\n", ivtx[0]);
			v[0] = vertices->erase(v[0]) - 1;
			++n_onetracks;
			continue;
		}

		bool duplicate = false;
		bool merge = false;
		bool refit = false;
		track_set tracks_to_remove_in_refit[2];
		VertexerPairEff* vpeff = 0;
		const size_t max_vpeffs_size = 20000; // enough for 200 vertices to share tracks

		for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {
			ivtx[1] = v[1] - vertices->begin();
			tracks[1] = vertex_track_set(*v[1]);

			if (tracks[1].size() < 2) {
				if (verbose)
					printf("track-sharing: vertex-1 #%lu is down to one track, junking it\n", ivtx[1]);
				v[1] = vertices->erase(v[1]) - 1;
				++n_onetracks;
				continue;
			}

			if (verbose) {
				printf("track-sharing: # vertices = %lu. considering vertices #%lu (chi2/dof %.3f prob %.2e, track set", vertices->size(), ivtx[0], v[0]->chi2() / v[0]->ndof(), TMath::Prob(v[0]->chi2(), int(v[0]->ndof())));
				print_track_set(tracks[0], *v[0]);
				printf(") and #%lu (chi2/dof %.3f prob %.2e, track set", ivtx[1], v[1]->chi2() / v[1]->ndof(), TMath::Prob(v[1]->chi2(), int(v[1]->ndof())));
				print_track_set(tracks[1], *v[1]);
				printf("):\n");
			}

			if (is_track_subset(tracks[0], tracks[1])) {
				if (verbose)
					printf("   subset/duplicate vertices %lu and %lu, erasing second and starting over\n", ivtx[0], ivtx[1]);
				duplicate = true;
				break;
			}

			if (vpeffs->size() < max_vpeffs_size) {
				std::pair<track_set, track_set> vpeff_tracks(tracks[0], tracks[1]);
				auto it = std::find(vpeffs_tracks.begin(), vpeffs_tracks.end(), vpeff_tracks);
				if (it != vpeffs_tracks.end()) {
					vpeffs->at(it - vpeffs_tracks.begin()).inc_weight();
					vpeff = 0;
				}
				else {
					vpeffs->push_back(VertexerPairEff());
					vpeff = &vpeffs->back();
					vpeff->set_vertices(*v[0], *v[1]);
					vpeffs_tracks.push_back(vpeff_tracks);
				}
			}
			else
				vpeff = 0;

			reco::TrackRefVector shared_tracks;
			for (auto tk : tracks[0])
				if (tracks[1].count(tk) > 0)
					shared_tracks.push_back(tk);

			if (verbose) {
				if (shared_tracks.size()) {
					printf("   shared tracks are: ");
					print_track_set(shared_tracks);
					printf("\n");
				}
				else
					printf("   no shared tracks\n");
			}

			if (shared_tracks.size() > 0) {
				if (vpeff)
					vpeff->kind(VertexerPairEff::share);

				Measurement1D v_dist = vertex_dist(*v[0], *v[1]);
				if (verbose)
					printf("   vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, v_dist.value(), v_dist.significance());

				if (v_dist.value() < merge_shared_dist || v_dist.significance() < merge_shared_sig) {
					if (verbose) printf("          dist < %7.3f || sig < %7.3f, will try using merge result first before arbitration\n", merge_shared_dist, merge_shared_sig);
					merge = true;
				}
				else
					refit = true;

				if (verbose) printf("   checking for arbitration refit:\n");
				for (auto tk : shared_tracks) {
					const reco::TransientTrack& ttk = seed_tracks[seed_track_ref_map[tk]];
					std::pair<bool, Measurement1D> t_dist_0 = track_dist(ttk, *v[0]);
					std::pair<bool, Measurement1D> t_dist_1 = track_dist(ttk, *v[1]);
					if (verbose) {
						printf("      track-vertex0 dist (2d? %i) calc success? %i  dist %7.3f  sig %7.3f\n", use_2d_track_dist, t_dist_0.first, t_dist_0.second.value(), t_dist_0.second.significance());
						printf("      track-vertex1 dist (2d? %i) calc success? %i  dist %7.3f  sig %7.3f\n", use_2d_track_dist, t_dist_1.first, t_dist_1.second.value(), t_dist_1.second.significance());
					}

					t_dist_0.first = t_dist_0.first && (t_dist_0.second.value() < max_track_vertex_dist || t_dist_0.second.significance() < max_track_vertex_sig);
					t_dist_1.first = t_dist_1.first && (t_dist_1.second.value() < max_track_vertex_dist || t_dist_1.second.significance() < max_track_vertex_sig);
					bool remove_from_0 = !t_dist_0.first;
					bool remove_from_1 = !t_dist_1.first;
					if (t_dist_0.second.significance() < min_track_vertex_sig_to_remove && t_dist_1.second.significance() < min_track_vertex_sig_to_remove) {
						if (tracks[0].size() > tracks[1].size())
							remove_from_1 = true;
						else
							remove_from_0 = true;
					}
					else if (t_dist_0.second.significance() < t_dist_1.second.significance())
						remove_from_1 = true;
					else
						remove_from_0 = true;

					if (verbose) {
						printf("   for tk %u:\n", tk.key());
						printf("      track-vertex0 dist < %7.3f || sig < %7.3f ? %i  remove? %i\n", max_track_vertex_dist, max_track_vertex_sig, t_dist_0.first, remove_from_0);
						printf("      track-vertex1 dist < %7.3f || sig < %7.3f ? %i  remove? %i\n", max_track_vertex_dist, max_track_vertex_sig, t_dist_1.first, remove_from_1);
					}

					if (remove_from_0) tracks_to_remove_in_refit[0].insert(tk);
					if (remove_from_1) tracks_to_remove_in_refit[1].insert(tk);

					if (remove_one_track_at_a_time) {
						if (verbose)
							printf("   arbitrate only one track at a time\n");
						break;
					}
				}

				if (verbose)
					printf("   breaking to refit\n");

				break;
			}

			if (verbose) printf("   moving on to next vertex pair.\n");
		}

		if (duplicate) {
			vertices->erase(v[1]);
		}
		else if (merge) {
			if (verbose)
				printf("      before merge, # total vertices = %lu\n", vertices->size());

			track_set tracks_to_fit;
			for (int i = 0; i < 2; ++i)
				for (auto tk : tracks[i])
					tracks_to_fit.insert(tk);

			if (verbose) {
				printf("   merging vertices %lu and %lu with these tracks:", ivtx[0], ivtx[1]);
				print_track_set(tracks_to_fit);
				printf("\n");
			}

			std::vector<reco::TransientTrack> ttks;
			for (auto tk : tracks_to_fit)
				ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);

			reco::VertexCollection new_vertices;
<<<<<<< HEAD

=======
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
			for (const TransientVertex& tv : kv_reco_dropin(ttks))
				new_vertices.push_back(reco::Vertex(tv));

			if (verbose) {
				printf("      got %lu new vertices out of the av fit\n", new_vertices.size());
				printf("      these (chi2/dof : prob | track sets):");
				for (const auto& nv : new_vertices) {
					printf(" (%.3f : %.2e | ", nv.chi2() / nv.ndof(), TMath::Prob(nv.chi2(), int(nv.ndof())));
					print_track_set(nv);
					printf(" ),");
				}
				printf("\n");
			}

			// If we got two new vertices, maybe it took A B and A C D and made a better one from B C D, and left a broken one A B! C! D!.
			// If we get one that is truly the merger of the track lists, great. If it is just something like A B , A C -> A B C!, or we get nothing, then default to arbitration.
			if (new_vertices.size() > 1) {
				if (verbose)
					printf("   jiggled again?\n");
				assert(new_vertices.size() == 2);
				*v[1] = reco::Vertex(new_vertices[1]);
				*v[0] = reco::Vertex(new_vertices[0]);
			}
			else if (new_vertices.size() == 1 && vertex_track_set(new_vertices[0], 0) == tracks_to_fit) {
				if (verbose)
					printf("   merge worked!\n");

				if (vpeff)
					vpeff->kind(VertexerPairEff::merge);

				vertices->erase(v[1]);
				*v[0] = reco::Vertex(new_vertices[0]); // ok to use v[0] after the erase(v[1]) because v[0] is by construction before v[1]
			}
			else {
				if (verbose)
					printf("   merge didn't work, trying arbitration refits\n");
				refit = true;
			}

			if (verbose)
				printf("   vertices size is now %lu\n", vertices->size());
		}

		if (refit) {
			bool erase[2] = { false };
			reco::Vertex vsave[2] = { *v[0], *v[1] };

			for (int i = 0; i < 2; ++i) {
				if (tracks_to_remove_in_refit[i].empty())
					continue;

				if (verbose) {
					printf("   refit vertex%i %lu with these tracks:", i, ivtx[i]);
					print_track_set(tracks[i]);
					printf("   but skip these:");
					print_track_set(tracks_to_remove_in_refit[i]);
					printf("\n");
				}

				std::vector<reco::TransientTrack> ttks;
				for (auto tk : tracks[i])
					if (tracks_to_remove_in_refit[i].count(tk) == 0)
						ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);

				reco::VertexCollection new_vertices;
				for (const TransientVertex& tv : kv_reco_dropin(ttks))
					new_vertices.push_back(reco::Vertex(tv));
				if (verbose) {
					printf("      got %lu new vertices out of the av fit for v%i\n", new_vertices.size(), i);
					printf("      these track sets:");
					for (const auto& nv : new_vertices) {
						printf(" (");
						print_track_set(nv);
						printf(" ),");
					}
					printf("\n");
				}
				if (new_vertices.size() == 1)
					* v[i] = new_vertices[0];
				else
					erase[i] = true;
			}

			if (vpeff && (erase[0] || erase[1]))
				vpeff->kind(VertexerPairEff::erase);

			if (erase[1]) vertices->erase(v[1]);
			if (erase[0]) vertices->erase(v[0]);

			if (verbose)
				printf("      vertices size is now %lu\n", vertices->size());
		}

		// If we changed the vertices at all, start loop over completely.
		if (duplicate || merge || refit) {
			v[0] = vertices->begin() - 1;  // -1 because about to ++sv
			++n_resets;
			if (verbose) printf("   resetting from vertices %lu and %lu. # of resets: %i\n", ivtx[0], ivtx[1], n_resets);

			//if (n_resets == 3000)
			//  throw "I'm dumb";
		}
	}

	if (verbose)
		printf("n_resets: %i  n_onetracks: %i  n_noshare_vertices: %lu\n", n_resets, n_onetracks, vertices->size());
	if (histos) {
		h_n_resets->Fill(n_resets);
		h_n_onetracks->Fill(n_onetracks);
		h_n_noshare_vertices->Fill(vertices->size());
	}

	if (histos_noshare || verbose || do_track_refinement) {
		std::map<reco::TrackRef, int> track_use;
		for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
			reco::Vertex& v = vertices->at(i);
			const int ntracks = v.nTracks();
			const double vchi2 = v.normalizedChi2();
			const double vndof = v.ndof();
			const double vx = v.position().x() - bsx;
			const double vy = v.position().y() - bsy;
			const double vz = v.position().z() - bsz;
			const double rho = mag(vx, vy);
			const double phi = atan2(vy, vx);
			const double r = mag(vx, vy, vz);
			for (const auto& r : vertex_track_set(v)) {
				if (track_use.find(r) != track_use.end())
					track_use[r] += 1;
				else
					track_use[r] = 1;
			}

			if (verbose)
				printf("no-share vertex #%3lu: ntracks: %i chi2/dof: %7.3f dof: %7.3f pos: <%7.3f, %7.3f, %7.3f>  rho: %7.3f  phi: %7.3f  r: %7.3f\n", i, ntracks, vchi2, vndof, vx, vy, vz, rho, phi, r);

			if (do_track_refinement) {

				track_set set_trackrefine_sigmacut_tks;
				std::vector<reco::TransientTrack> trackrefine_sigmacut_ttks;
				track_set set_trackrefine_trimmax_tks;
				std::vector<reco::TransientTrack> trackrefine_trimmax_ttks;
				std::vector<double> trackrefine_trim_ttks_missdist_sig;
				for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {

					reco::TransientTrack seed_track;
					seed_track = tt_builder->build(*it.operator*());
					std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v);

					AlgebraicVector3 mom_tk(seed_track.track().px(), seed_track.track().py(), seed_track.track().pz());
					AlgebraicVector3 ref_tk(seed_track.track().vx(), seed_track.track().vy(), seed_track.track().vz());
					Measurement1D tkvtx_dist_before_do_track_refinement = miss_dist(v, ref_tk, mom_tk);
					h_noshare_vertex_tkvtxdist_before_do_track_refinement->Fill(tkvtx_dist_before_do_track_refinement.value());
					h_noshare_vertex_tkvtxdisterr_before_do_track_refinement->Fill(tkvtx_dist_before_do_track_refinement.error());
					h_noshare_vertex_tkvtxdistsig_before_do_track_refinement->Fill(tkvtx_dist_before_do_track_refinement.significance());


					if (tk_vtx_dist.second.significance() < trackrefine_sigmacut) {
						set_trackrefine_sigmacut_tks.insert(it->castTo<reco::TrackRef>());

					}
				}


				for (auto tk : set_trackrefine_sigmacut_tks) {
					trackrefine_sigmacut_ttks.push_back(tt_builder->build(tk));
				}

				// if tracks's miss distance significance is larger than trackrefine_sigmacut, we first remove all those tracks and refit a new vertex 
				double trackrefine_sigmacut_v0x = v.position().x() - bsx;
				double trackrefine_sigmacut_v0y = v.position().y() - bsy;
				double trackrefine_sigmacut_v0r = mag(trackrefine_sigmacut_v0x, trackrefine_sigmacut_v0y);

				reco::Vertex trackrefine_sigmacut_v;
				for (const TransientVertex& tv : kv_reco_dropin(trackrefine_sigmacut_ttks))
					trackrefine_sigmacut_v = reco::Vertex(tv);
				double trackrefine_sigmacut_vchi2 = trackrefine_sigmacut_v.normalizedChi2();
				h_noshare_trackrefine_sigmacut_vertex_chi2->Fill(trackrefine_sigmacut_vchi2);

				double trackrefine_sigmacut_v1x = trackrefine_sigmacut_v.position().x() - bsx;
				double trackrefine_sigmacut_v1y = trackrefine_sigmacut_v.position().y() - bsy;
				double trackrefine_sigmacut_v1r = mag(trackrefine_sigmacut_v1x, trackrefine_sigmacut_v1y);

				// just to check how the new vertex is shifted by removing tracks by trackrefine_sigmacut
				double sigmacut_vertex_distr = trackrefine_sigmacut_v1r - trackrefine_sigmacut_v0r;
				h_noshare_trackrefine_sigmacut_vertex_distr_shift->Fill(sigmacut_vertex_distr);

				for (auto it = trackrefine_sigmacut_v.tracks_begin(), ite = trackrefine_sigmacut_v.tracks_end(); it != ite; ++it) {
					reco::TransientTrack trackrefine_sigmacut_track;
					trackrefine_sigmacut_track = tt_builder->build(*it.operator*());
					std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(trackrefine_sigmacut_track, trackrefine_sigmacut_v);
					h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
					trackrefine_trim_ttks_missdist_sig.push_back(tk_vtx_dist.second.significance());
					set_trackrefine_trimmax_tks.insert(it->castTo<reco::TrackRef>());
				}



				int n_trackrefine_trimmax = 0;
				reco::Vertex trackrefine_trimmax_v = trackrefine_sigmacut_v;

				for (auto tk : set_trackrefine_trimmax_tks) {
					trackrefine_trimmax_ttks.push_back(tt_builder->build(tk));
				}


				while (trackrefine_trimmax_ttks.size() > 2 && *std::max_element(trackrefine_trim_ttks_missdist_sig.begin(), trackrefine_trim_ttks_missdist_sig.end()) > trackrefine_trimmax) {
					++n_trackrefine_trimmax;

					int max_missdist_sig_idx = std::max_element(trackrefine_trim_ttks_missdist_sig.begin(), trackrefine_trim_ttks_missdist_sig.end()) - trackrefine_trim_ttks_missdist_sig.begin();
					// trimmax only one track with the largest miss distance significance at a time
					trackrefine_trimmax_ttks.erase(trackrefine_trimmax_ttks.begin() + max_missdist_sig_idx);
					double trackrefine_trimmax_v0x = trackrefine_trimmax_v.position().x() - bsx;
					double trackrefine_trimmax_v0y = trackrefine_trimmax_v.position().y() - bsy;
					double trackrefine_trimmax_v0r = mag(trackrefine_trimmax_v0x, trackrefine_trimmax_v0y);

					// while we still find a track with max miss distance significance larger than trackrefine_trimmax, we trim it out, namely trimmax, and refit a new vertex until the max miss distance significance is under trackrefine_trimmax
					for (const TransientVertex& tv : kv_reco_dropin(trackrefine_trimmax_ttks))
						trackrefine_trimmax_v = reco::Vertex(tv);


					double trackrefine_trimmax_v1x = trackrefine_trimmax_v.position().x() - bsx;
					double trackrefine_trimmax_v1y = trackrefine_trimmax_v.position().y() - bsy;
					double trackrefine_trimmax_v1r = mag(trackrefine_trimmax_v1x, trackrefine_trimmax_v1y);

					// just to check how the new vertex is shifted by removing a trimmax track
					double trimmax_vertex_distr = trackrefine_trimmax_v1r - trackrefine_trimmax_v0r;
					h_noshare_trackrefine_trimmax_vertex_distr_shift->Fill(trimmax_vertex_distr);

					trackrefine_trim_ttks_missdist_sig.clear();

					for (auto it = trackrefine_trimmax_v.tracks_begin(), ite = trackrefine_trimmax_v.tracks_end(); it != ite; ++it) {
						reco::TransientTrack trackrefine_trimmax_track;
						trackrefine_trimmax_track = tt_builder->build(*it.operator*());
						std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(trackrefine_trimmax_track, trackrefine_trimmax_v);
						trackrefine_trim_ttks_missdist_sig.push_back(tk_vtx_dist.second.significance());
					}

				}


				if (verbose) printf("   trimming the trimmax track from a vertex w/ # of trimming: %i\n", n_trackrefine_trimmax);


				double trackrefine_trimmax_vchi2 = trackrefine_trimmax_v.normalizedChi2();
				h_noshare_trackrefine_trimmax_vertex_chi2->Fill(trackrefine_trimmax_vchi2);

				for (unsigned int j = 0, je = trackrefine_trim_ttks_missdist_sig.size(); j < je; ++j) {
					h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig->Fill(trackrefine_trim_ttks_missdist_sig[j]);
				}


				// the end of track refinement in two steps -- (1) sigmacut and (2) trimmax
				// we replace the noshare vertex by the vertex after the track refinement
				v = trackrefine_trimmax_v;
			}


			if (histos_noshare) {
				h_noshare_vertex_ntracks->Fill(ntracks);

				for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
					h_noshare_vertex_track_weights->Fill(v.trackWeight(*it));

					reco::TransientTrack seed_track;
					seed_track = tt_builder->build(*it.operator*());
					std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v);
					h_noshare_vertex_tkvtxdist->Fill(tk_vtx_dist.second.value());
					h_noshare_vertex_tkvtxdisterr->Fill(tk_vtx_dist.second.error());
					h_noshare_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
				}

				h_noshare_vertex_chi2->Fill(vchi2);
				h_noshare_vertex_ndof->Fill(vndof);
				h_noshare_vertex_x->Fill(vx);
				h_noshare_vertex_y->Fill(vy);
				h_noshare_vertex_rho->Fill(rho);
				h_noshare_vertex_phi->Fill(phi);
				h_noshare_vertex_z->Fill(vz);
				h_noshare_vertex_r->Fill(r);

				for (size_t j = i + 1, je = vertices->size(); j < je; ++j) {
					const reco::Vertex& vj = vertices->at(j);
					const double vjx = vj.position().x() - bsx;
					const double vjy = vj.position().y() - bsy;
					const double phij = atan2(vjy, vjx);
					h_noshare_vertex_paird2d->Fill(mag(vx - vjx, vy - vjy));
					h_noshare_vertex_pairdphi->Fill(fabs(reco::deltaPhi(phi, phij)));
				}

			}
		}

		if (verbose)
			printf("track multiple uses:\n");

		int max_noshare_track_multiplicity = 0;
		for (const auto& p : track_use) {
			if (verbose && p.second > 1)
				printf("track %3u used %3i times\n", p.first.key(), p.second);
			if (histos)
				h_noshare_track_multiplicity->Fill(p.second);
			if (p.second > max_noshare_track_multiplicity)
				max_noshare_track_multiplicity = p.second;
		}
		if (histos)
			h_max_noshare_track_multiplicity->Fill(max_noshare_track_multiplicity);
	}

	//////////////////////////////////////////////////////////////////////
	// Merge vertices that are still "close". JMTBAD this doesn't do anything currently, only run in verbose mode
	//////////////////////////////////////////////////////////////////////

	if (verbose)
		printf("fun2! before merge loop, # vertices = %lu\n", vertices->size());

	if (resolve_split_vertices_loose) {

		if (merge_anyway_sig > 0 || merge_anyway_dist > 0) {
			double v0x;
			double v0y;
			//double v0z;
			double phi0;

			for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
				ivtx[0] = v[0] - vertices->begin();

				double v1x;
				double v1y;
				//double v1z;
				double phi1;

				for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {


					ivtx[1] = v[1] - vertices->begin();

					if (verbose)
						printf("close-merge: # vertices = %lu. considering vertices #%lu (ntk = %i) and #%lu (ntk = %i):", vertices->size(), ivtx[0], v[0]->nTracks(), ivtx[1], v[1]->nTracks());

					Measurement1D v_dist = vertex_dist(*v[0], *v[1]);
					if (verbose)
						printf("   vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, v_dist.value(), v_dist.significance());

					v0x = v[0]->x() - bsx;
					v0y = v[0]->y() - bsy;
					//v0z = v[0]->z() - bsz;
					phi0 = atan2(v0y, v0x);
					v1x = v[1]->x() - bsx;
					v1y = v[1]->y() - bsy;
					//v1z = v[1]->z() - bsz;
					phi1 = atan2(v1y, v1x);

					if (v_dist.value() < merge_anyway_dist || v_dist.significance() < merge_anyway_sig) {
						if (verbose)
							printf("          dist < %7.3f || sig < %7.3f, breaking to merge\n", merge_anyway_dist, merge_anyway_sig);



						std::vector<reco::TransientTrack> ttks;

						for (int i = 0; i < 2; ++i) {


							for (auto tk : vertex_track_set(*v[i])) {

								ttks.push_back(tt_builder->build(tk));

							}

						}


						reco::VertexCollection merged_vertices;
						for (const TransientVertex& tv : kv_reco_dropin(ttks))
						{
							merged_vertices.push_back(reco::Vertex(tv));


							for (auto it = merged_vertices[0].tracks_begin(), ite = merged_vertices[0].tracks_end(); it != ite; ++it) {

								reco::TransientTrack seed_track;
								seed_track = tt_builder->build(*it.operator*());
								std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, merged_vertices[0]);

							}


						}


						if (verbose) {
							printf("      got %lu new vertices out of the av fit\n", merged_vertices.size());
							printf("      these track sets:");
							for (const auto& nv : merged_vertices) {
								printf(" (");
								print_track_set(nv);
								printf(" ),");
							}
							printf("\n");
						}


						if (merged_vertices.size() == 1)
						{

							if (verbose) {
								printf(" sv2ddist between a merging pair is %7.3f \n", v_dist.value());
								printf(" |dPhi(vtx0,vtx1) between a merging pair is %4.3f \n", fabs(reco::deltaPhi(phi0, phi1)));
								printf(" # of tracks per vtx0 is %u \n", v[0]->nTracks());
								printf(" # of tracks per vtx1 is %u \n", v[1]->nTracks());
								printf(" ---------------- merge the two vertices if chi2/dof < 8 ----------------- \n");
								printf(" # of tracks per a new merged vertex is %u \n", merged_vertices[0].nTracks());
							}

							//std::cout << "check no mem out of ranges (before) : " << v[1] - vertices->begin() << std::endl;
							*v[0] = merged_vertices[0];
							//std::cout << "check no mem out of ranges (after) : " << v[1] - vertices->begin() << std::endl;

							v[1] = vertices->erase(v[1]) - 1;

						}

					}
				}

			}


			for (nv[0] = vertices->begin(); nv[0] != vertices->end(); ++nv[0]) {


				for (nv[1] = nv[0] + 1; nv[1] != vertices->end(); ++nv[1]) {


					Measurement1D nv_dist = vertex_dist(*nv[0], *nv[1]);
					if (verbose)
						printf("  new vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, nv_dist.value(), nv_dist.significance());


				}

			}
		}

	}

	//////////////////////////////////////////////////////////////////////
	// Drop tracks that "move" the vertex too much by refitting without each track.
	//////////////////////////////////////////////////////////////////////

	if (max_nm1_refit_dist3 > 0 || max_nm1_refit_distz > 0) {
		std::vector<int> refit_count(vertices->size(), 0);

		int iv = 0;
		for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0], ++iv) {
			if (max_nm1_refit_count > 0 && refit_count[iv] >= max_nm1_refit_count)
				continue;

			const track_vec tks = vertex_track_vec(*v[0]);
			const size_t ntks = tks.size();
			if (ntks < 3)
				continue;

			if (verbose) {
				printf("doing n-%i refit on vertex at %7.4f %7.4f %7.4f with %lu tracks\n", refit_count[iv] + 1, v[0]->x(), v[0]->y(), v[0]->z(), ntks);
				for (size_t i = 0; i < ntks; ++i)
					printf("  refit %lu will drop tk pt %7.4f +- %7.4f eta %7.4f +- %7.4f phi %7.4f +- %7.4f dxy %7.4f +- %7.4f dz %7.4f +- %7.4f\n", i, tks[i]->pt(), tks[i]->ptError(), tks[i]->eta(), tks[i]->etaError(), tks[i]->phi(), tks[i]->phiError(), tks[i]->dxy(), tks[i]->dxyError(), tks[i]->dz(), tks[i]->dzError());
			}

			std::vector<reco::TransientTrack> ttks(ntks - 1);
			for (size_t i = 0; i < ntks; ++i) {
				for (size_t j = 0; j < ntks; ++j)
					if (j != i)
						ttks[j - (j >= i)] = tt_builder->build(tks[j]);

				reco::Vertex vnm1(TransientVertex(kv_reco->vertex(ttks)));
				const double dist3_2 = mag2(vnm1.x() - v[0]->x(), vnm1.y() - v[0]->y(), vnm1.z() - v[0]->z());
				const double distz = mag(vnm1.z() - v[0]->z());
				if (verbose) printf("  refit %lu chi2 %7.4f vtx %7.4f %7.4f %7.4f dist3 %7.4f distz %7.4f\n", i, vnm1.chi2(), vnm1.x(), vnm1.y(), vnm1.z(), sqrt(dist3_2), distz);

				if (vnm1.chi2() < 0 ||
					(max_nm1_refit_dist3 > 0 && mag2(vnm1.x() - v[0]->x(), vnm1.y() - v[0]->y(), vnm1.z() - v[0]->z()) > pow(max_nm1_refit_dist3, 2)) ||
					(max_nm1_refit_distz > 0 && distz > max_nm1_refit_distz)) {
					if (verbose) {
						printf("    replacing");
						if (refit_count[iv] < max_nm1_refit_count - 1)
							printf(" and reconsidering");
						printf("\n");
					}

					*v[0] = vnm1;
					++refit_count[iv];
					--v[0], --iv;
					break;
				}
			}
		}

	}


	if (histos_output0) {
		std::map<reco::TrackRef, int> track_use;
		int count_5trk_vertices = 0;
<<<<<<< HEAD
                //std::cout << "yes histos_output0" << std::endl;

		typedef std::vector<reco::TrackRef> track_vec;
		
		const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

		std::vector<int> vertex_ntracks; //// PK:shared-jet 
=======

		
		const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
		for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
			reco::Vertex& v = vertices->at(i);
			const int ntracks = v.nTracks();
			const double vchi2 = v.normalizedChi2();
			const double vndof = v.ndof();
			const double vx = v.position().x() - bsx;
			const double vy = v.position().y() - bsy;
			const double vz = v.position().z() - bsz;
			const double rho = mag(vx, vy);
			const double phi = atan2(vy, vx);
			const double r = mag(vx, vy, vz);
			for (const auto& r : vertex_track_set(v)) {
				if (track_use.find(r) != track_use.end())
					track_use[r] += 1;
				else
					track_use[r] = 1;
			}

			h_output0_vertex_ntracks->Fill(ntracks);
<<<<<<< HEAD
			vertex_ntracks.push_back(ntracks);	 //// PK:shared-jet 
=======
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
			if (ntracks >= 5) {
				count_5trk_vertices++;
				Measurement1D dBV_Meas1D = vertex_dist_2d.distance(v, fake_bs_vtx);
				double dBV = dBV_Meas1D.value();
				double bs2derr = dBV_Meas1D.error();
				h_at_least_5trk_output0_vertex_dBV->Fill(dBV);
				h_at_least_5trk_output0_vertex_bs2derr->Fill(bs2derr);

			}

			for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
				h_output0_vertex_track_weights->Fill(v.trackWeight(*it));

				reco::TransientTrack seed_track;
				seed_track = tt_builder->build(*it.operator*());
				std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v);
				h_output0_vertex_tkvtxdist->Fill(tk_vtx_dist.second.value());
				h_output0_vertex_tkvtxdisterr->Fill(tk_vtx_dist.second.error());
				h_output0_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
			}

			h_output0_vertex_chi2->Fill(vchi2);
			h_output0_vertex_ndof->Fill(vndof);
			h_output0_vertex_x->Fill(vx);
			h_output0_vertex_y->Fill(vy);
			h_output0_vertex_rho->Fill(rho);
			h_output0_vertex_phi->Fill(phi);
			h_output0_vertex_z->Fill(vz);
			h_output0_vertex_r->Fill(r);

			for (size_t j = i + 1, je = vertices->size(); j < je; ++j) {
				const reco::Vertex& vj = vertices->at(j);
				const double vjx = vj.position().x() - bsx;
				const double vjy = vj.position().y() - bsy;
				const double phij = atan2(vjy, vjx);
				Measurement1D v_dist = vertex_dist(vj, v);
				h_output0_vertex_paird2d->Fill(mag(vx - vjx, vy - vjy));
				h_output0_vertex_paird2dsig->Fill(v_dist.significance());
				h_output0_vertex_pairdphi->Fill(fabs(reco::deltaPhi(phi, phij)));
			}


		}

		h_n_at_least_5trk_output0_vertices->Fill(count_5trk_vertices);

	}


	
	//////////////////////////////////////////////////////////////////////
	// Merge ever pair of output vertices that satisfy the following criteria to resolve split-vertices:
	//   - >=2trk/vtx
	//   - dBV > 100 um
	//   - |dPhi(vtx0,vtx1)| < 0.5 
	//   - svdist2d < 300 um
	// Note that the merged vertex must pass chi2/dof < 8 (applied to all vertices in this code (above and beyond) -- it's used to be chi2/dof < 5)
	//////////////////////////////////////////////////////////////////////

	if (resolve_split_vertices_tight) {
			int merge_pair_count = 0;
			const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());
<<<<<<< HEAD
			reco::VertexCollection potential_merged_vertices;
			
=======
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806

			for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {

				track_set tracks[2];
				tracks[0] = vertex_track_set(*v[0]);

				bool merge = false;
				for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {
					if (vertices->size() >= 2 && v[0]->nTracks() >= 2 && v[1]->nTracks() >= 2) {

						tracks[1] = vertex_track_set(*v[1]);

						Measurement1D v_dist = vertex_dist_2d.distance(*v[0], *v[1]);
						Measurement1D dBV0_Meas1D = vertex_dist_2d.distance(*v[0], fake_bs_vtx);
						double dBV0 = dBV0_Meas1D.value();


						Measurement1D dBV1_Meas1D = vertex_dist_2d.distance(*v[1], fake_bs_vtx);
						double dBV1 = dBV1_Meas1D.value();


						double v0x = v[0]->x() - bsx;
						double v0y = v[0]->y() - bsy;

						double phi0 = atan2(v0y, v0x);

						double v1x = v[1]->x() - bsx;
						double v1y = v[1]->y() - bsy;

						double phi1 = atan2(v1y, v1x);

						if (fabs(reco::deltaPhi(phi0, phi1)) < 0.5 && v_dist.value() < 0.0300 && dBV0 > 0.0100 && dBV1 > 0.0100) {
							track_set tracks_to_fit;
							for (int i = 0; i < 2; ++i)
								for (auto tk : tracks[i])
									tracks_to_fit.insert(tk);
							std::vector<reco::TransientTrack> ttks;
							for (auto tk : tracks_to_fit)
								ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);

<<<<<<< HEAD
							if (investigate_merged_vertices) {
								std::vector<TransientVertex> tv(1, kv_reco->vertex(ttks));
								potential_merged_vertices.push_back(reco::Vertex(tv[0]));
                                                                //std::cout << "ntrack in potental merged: " << potential_merged_vertices.back().nTracks() << std::endl;
                            }
=======
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
							reco::VertexCollection merged_vertices;
							for (const TransientVertex& tv : kv_reco_dropin(ttks))
								merged_vertices.push_back(reco::Vertex(tv));

							if (merged_vertices.size() == 1 && vertex_track_set(merged_vertices[0], 0) == tracks_to_fit) {

								merge_pair_count += 1;
								merge = true;

								if (verbose) {
									printf(" sv2ddist between a merging pair is %7.3f \n", v_dist.value());
									printf(" |dPhi(vtx0,vtx1) between a merging pair is %4.3f \n", fabs(reco::deltaPhi(phi0, phi1)));
									printf(" # of tracks per vtx0 is %u \n", v[0]->nTracks());
									printf(" # of tracks per vtx1 is %u \n", v[1]->nTracks());
									printf(" ---------------- merge the two vertices if chi2/dof < 8 ----------------- \n");
									printf(" # of tracks per a new merged vertex is %u \n", merged_vertices[0].nTracks());
								}

								v[1] = vertices->erase(v[1]) - 1;
								*v[0] = reco::Vertex(merged_vertices[0]); // ok to use v[0] after the erase(v[1]) because v[0] is by construction before v[1]

							}
						}
					}
				}

				if (merge)
					v[0] = vertices->begin() - 1;

			}
<<<<<<< HEAD

			if (investigate_merged_vertices && histos_output1) {
				const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());
                                
				for (size_t i = 0, ie = potential_merged_vertices.size(); i < ie; ++i) {
                    reco::Vertex v = potential_merged_vertices[i];
                    const int ntracks = v.nTracks();
                                        //std::cout << "ntrack in output1: " << ntracks << std::endl;
					const double vchi2 = v.normalizedChi2();
					Measurement1D dBV_Meas1D = vertex_dist_2d.distance(v, fake_bs_vtx);
					double dBV = dBV_Meas1D.value();
					double bs2derr = dBV_Meas1D.error();
                                        
					if (ntracks >= 5 && dBV > 0.01 && bs2derr < 0.0025) {
						h_output1_after_merged_criteria_vertex_chi2->Fill(vchi2);
					}
					if (vchi2 < 8 && dBV > 0.01 && bs2derr < 0.0025) {
						h_output1_after_merged_criteria_vertex_ntracks->Fill(ntracks);
					}
					if (vchi2 < 8 && ntracks >= 5 && bs2derr < 0.0025) {
						h_output1_after_merged_criteria_vertex_dBV->Fill(dBV);
					}
					if (vchi2 < 8 && ntracks >= 5 && dBV > 0.01) {
						h_output1_after_merged_criteria_vertex_bs2derr->Fill(bs2derr);
					}

				}
			}

=======
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
		}

	if (histos_output1) {
		std::map<reco::TrackRef, int> track_use;
		int count_5trk_vertices = 0;
<<<<<<< HEAD
          
=======

>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
		const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

		for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
			reco::Vertex& v = vertices->at(i);
			const int ntracks = v.nTracks();
			const double vchi2 = v.normalizedChi2();
			const double vndof = v.ndof();
			const double vx = v.position().x() - bsx;
			const double vy = v.position().y() - bsy;
			const double vz = v.position().z() - bsz;
			const double rho = mag(vx, vy);
			const double phi = atan2(vy, vx);
			const double r = mag(vx, vy, vz);
			for (const auto& r : vertex_track_set(v)) {
				if (track_use.find(r) != track_use.end())
					track_use[r] += 1;
				else
					track_use[r] = 1;
			}

			h_output1_vertex_ntracks->Fill(ntracks);
			if (ntracks >= 5) {
				count_5trk_vertices++;
				Measurement1D dBV_Meas1D = vertex_dist_2d.distance(v, fake_bs_vtx);
				double dBV = dBV_Meas1D.value();
				double bs2derr = dBV_Meas1D.error();
				h_at_least_5trk_output1_vertex_dBV->Fill(dBV);
				h_at_least_5trk_output1_vertex_bs2derr->Fill(bs2derr);

			}

			for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
				h_output1_vertex_track_weights->Fill(v.trackWeight(*it));

				reco::TransientTrack seed_track;
				seed_track = tt_builder->build(*it.operator*());
				std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v);
				h_output1_vertex_tkvtxdist->Fill(tk_vtx_dist.second.value());
				h_output1_vertex_tkvtxdisterr->Fill(tk_vtx_dist.second.error());
				h_output1_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
			}

			h_output1_vertex_chi2->Fill(vchi2);
			h_output1_vertex_ndof->Fill(vndof);
			h_output1_vertex_x->Fill(vx);
			h_output1_vertex_y->Fill(vy);
			h_output1_vertex_rho->Fill(rho);
			h_output1_vertex_phi->Fill(phi);
			h_output1_vertex_z->Fill(vz);
			h_output1_vertex_r->Fill(r);

			for (size_t j = i + 1, je = vertices->size(); j < je; ++j) {
				const reco::Vertex& vj = vertices->at(j);
				const double vjx = vj.position().x() - bsx;
				const double vjy = vj.position().y() - bsy;
				const double phij = atan2(vjy, vjx);
				Measurement1D v_dist = vertex_dist(vj, v);
				h_output1_vertex_paird2d->Fill(mag(vx - vjx, vy - vjy));
				h_output1_vertex_paird2dsig->Fill(v_dist.significance());
				h_output1_vertex_pairdphi->Fill(fabs(reco::deltaPhi(phi, phij)));
			}

		}

		h_n_at_least_5trk_output1_vertices->Fill(count_5trk_vertices);

	}

	//////////////////////////////////////////////////////////////////////
	// Shared-jet mitigation with the following procedure:
	//   - 	 work in progress 
	//   - 
	//   -  
	//   - 
	// Note that 
	//////////////////////////////////////////////////////////////////////

	if (resolve_shared_jets) {
<<<<<<< HEAD
                //std::cout << "yes resolve shared-jet" << std::endl;
		edm::Handle<pat::JetCollection> jets;
		event.getByToken(shared_jet_token, jets);

		std::vector<std::vector<int> > sv_total_track_which_idx;

		std::vector<std::vector<int> > sv_match_track_which_idx;
		std::vector<std::vector<int> > sv_match_track_which_jet;

=======
		edm::Handle<pat::JetCollection> jets;
		event.getByToken(shared_jet_token, jets);

		std::vector<std::vector<int> > sv_track_which_idx;
		std::vector<std::vector<int> > sv_track_which_jet;
		
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
		typedef std::vector<reco::TrackRef> track_vec;
		const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

		std::vector<size_t> vertex_ntracks;
<<<<<<< HEAD

		for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
			std::vector<int> track_idx;
			std::vector<int> track_which_idx;
			std::vector<int> track_which_jet;
			track_vec tks = vertex_track_vec(*v[0]);
                        const int ntracks = v[0]->nTracks();
                        vertex_ntracks.push_back(ntracks);
                        //std::cout << "before ntrack/vtx: " << ntracks << std::endl;
			int i = 0;
			for (const reco::TrackRef& itk : tks) {
				i++;
				track_idx.push_back(i);
				for (size_t j = 0; j < jets->size(); ++j) {
					int jet_index = static_cast<int>(j);
					if (match_track_jet(*itk, (*jets)[j], *jets, jet_index)) {
						track_which_idx.push_back(i);
						track_which_jet.push_back(j);
						if (verbose)
							printf(" track %u matched with a jet %lu \n", tks[i].key(), j);
					}

				}
			}
                        //std::cout << "after ntrack/vtx: " << track_which_idx.size() << std::endl;
						//std::cout << "(corrected)after ntrack/vtx: " << track_idx.size() << std::endl;
			sv_total_track_which_idx.push_back(track_idx);
			sv_match_track_which_idx.push_back(track_which_idx);
			sv_match_track_which_jet.push_back(track_which_jet);


		}
                //std::cout << vertex_ntracks.size() << std::endl;
		if (vertex_ntracks.size() >= 2) {

			int first_ntracks_vtxidx = std::distance(vertex_ntracks.begin(), std::max_element(vertex_ntracks.begin(), vertex_ntracks.end()));
			reco::Vertex& v0 = vertices->at(first_ntracks_vtxidx);
			vertex_ntracks[first_ntracks_vtxidx] = 0;
			int second_ntracks_vtxidx = std::distance(vertex_ntracks.begin(), std::max_element(vertex_ntracks.begin(), vertex_ntracks.end()));
			reco::Vertex& v1 = vertices->at(second_ntracks_vtxidx);

			Measurement1D v_dist = vertex_dist_2d.distance(v0, v1);
			Measurement1D dBV0_Meas1D = vertex_dist_2d.distance(v0, fake_bs_vtx);
			double dBV0 = dBV0_Meas1D.value();
			double bs2derr0 = dBV0_Meas1D.error();

			Measurement1D dBV1_Meas1D = vertex_dist_2d.distance(v1, fake_bs_vtx);
			double dBV1 = dBV1_Meas1D.value();
			double bs2derr1 = dBV1_Meas1D.error();

			double v0x = v0.x() - bsx;
			double v0y = v0.y() - bsy;

			double phi0 = atan2(v0y, v0x);

			double v1x = v1.x() - bsx;
			double v1y = v1.y() - bsy;

			double phi1 = atan2(v1y, v1x);

			bool shared_jet = std::find_first_of(sv_match_track_which_jet[first_ntracks_vtxidx].begin(), sv_match_track_which_jet[first_ntracks_vtxidx].end(), sv_match_track_which_jet[second_ntracks_vtxidx].begin(), sv_match_track_which_jet[second_ntracks_vtxidx].end()) != sv_match_track_which_jet[first_ntracks_vtxidx].end();

			h_output1_most_track_vertices_shared_jets_or_not->Fill(shared_jet);

		
			if (shared_jet) {

				//std::cout << "shared-jet event id: " << " run: " << event.id().run() << " lumi: " << event.luminosityBlock() << " event: " << event.id().event() << std::endl;
                                //std::cout << "yes shared-jet" << std::endl;
				int nsharedjets = 0;

				std::vector<size_t> nsharedjet_jet_index;
				std::vector<std::vector<int>> sv_match_track_which_jet_copy = sv_match_track_which_jet;

				std::vector<int> nsharedjet_tracks_sv0;
				std::vector<int> nsharedjet_tracks_sv1;
				std::vector<std::vector<int> >sv0_sharedjet_which_idx;
				std::vector<std::vector<int> >sv1_sharedjet_which_idx;

				std::vector<int> sv0_total_track_which_idx = sv_total_track_which_idx[first_ntracks_vtxidx];
				std::vector<int> sv0_match_track_which_jet = sv_match_track_which_jet[first_ntracks_vtxidx];
				std::vector<int> sv0_match_track_which_idx = sv_match_track_which_idx[first_ntracks_vtxidx];
				std::vector<int> sv0_match_track_which_temp_idx;

				std::vector<int> sv1_total_track_which_idx = sv_total_track_which_idx[second_ntracks_vtxidx];
				std::vector<int> sv1_match_track_which_jet = sv_match_track_which_jet[second_ntracks_vtxidx];
				std::vector<int> sv1_match_track_which_idx = sv_match_track_which_idx[second_ntracks_vtxidx];
				std::vector<int> sv1_track_which_temp_idx;

				//std::cout << "vtx0 ntracks: " << sv0_total_track_which_idx.size() << std::endl;
				//std::cout << "vtx1 ntracks: " << sv1_total_track_which_idx.size() << std::endl;


				while (std::find_first_of(sv_match_track_which_jet_copy[first_ntracks_vtxidx].begin(), sv_match_track_which_jet_copy[first_ntracks_vtxidx].end(), sv_match_track_which_jet_copy[second_ntracks_vtxidx].begin(), sv_match_track_which_jet_copy[second_ntracks_vtxidx].end()) != sv_match_track_which_jet_copy[first_ntracks_vtxidx].end()) {
					nsharedjets++;
					std::vector<int> sv0_non_shared_track_which_idx = sv0_total_track_which_idx;
					std::vector<int> sv1_non_shared_track_which_idx = sv1_total_track_which_idx;
					std::vector<int>::iterator it = std::find_first_of(sv_match_track_which_jet_copy[first_ntracks_vtxidx].begin(), sv_match_track_which_jet_copy[first_ntracks_vtxidx].end(), sv_match_track_which_jet_copy[second_ntracks_vtxidx].begin(), sv_match_track_which_jet_copy[second_ntracks_vtxidx].end());
					int idx = std::distance(sv_match_track_which_jet_copy[first_ntracks_vtxidx].begin(), it);
					int jet_index = sv_match_track_which_jet_copy[first_ntracks_vtxidx].at(idx);
					nsharedjet_jet_index.push_back(sv_match_track_which_jet_copy[first_ntracks_vtxidx].at(idx));
					sv_match_track_which_jet_copy[first_ntracks_vtxidx].erase(std::remove(sv_match_track_which_jet_copy[first_ntracks_vtxidx].begin(), sv_match_track_which_jet_copy[first_ntracks_vtxidx].end(), jet_index), sv_match_track_which_jet_copy[first_ntracks_vtxidx].end());
					sv_match_track_which_jet_copy[second_ntracks_vtxidx].erase(std::remove(sv_match_track_which_jet_copy[second_ntracks_vtxidx].begin(), sv_match_track_which_jet_copy[second_ntracks_vtxidx].end(), jet_index), sv_match_track_which_jet_copy[second_ntracks_vtxidx].end());

					// start counting shared tracks of sv0 for each shared jet
					nsharedjet_tracks_sv0.push_back(std::count(sv0_match_track_which_jet.begin(), sv0_match_track_which_jet.end(), jet_index));
					std::multimap<int, size_t> sv0_m;
					for (size_t k = 0; k < sv0_match_track_which_jet.size(); k++) if (sv0_match_track_which_jet[k] == jet_index) { sv0_m.insert({ sv0_match_track_which_jet[k], k }); }

					for (auto it = sv0_m.begin(); it != sv0_m.end(); )
					{
						auto p = sv0_m.equal_range(it->first);

						while (p.first != p.second)
						{

							sv0_match_track_which_temp_idx.push_back(sv0_match_track_which_idx[p.first++->second]);
							//std::cout << "with jet index: " << jet_index << "idx is appended to a sv0 temp list: " << sv0_track_which_temp_idx.back() << std::endl;
						}
						it = p.second;

					}

					sv0_sharedjet_which_idx.push_back(sv0_match_track_which_temp_idx);
					for (size_t k = 0; k < sv0_match_track_which_temp_idx.size(); k++) {
						int track_index = sv0_match_track_which_temp_idx[k];
						 //std::cout << "sv0 w/ shared track's idx: " << track_index << std::endl;
						sv0_non_shared_track_which_idx.erase(std::remove(sv0_non_shared_track_which_idx.begin(), sv0_non_shared_track_which_idx.end(), track_index), sv0_non_shared_track_which_idx.end());

					}


					sv0_match_track_which_temp_idx = {};


					// start counting shared tracks of sv1 for each shared jet
					nsharedjet_tracks_sv1.push_back(std::count(sv1_match_track_which_jet.begin(), sv1_match_track_which_jet.end(), jet_index));
					std::multimap<int, size_t> sv1_m;
					for (size_t k = 0; k < sv1_match_track_which_jet.size(); k++) if (sv1_match_track_which_jet[k] == jet_index) { sv1_m.insert({ sv1_match_track_which_jet[k], k }); }

					for (auto it = sv1_m.begin(); it != sv1_m.end(); )
					{
						auto p = sv1_m.equal_range(it->first);

						while (p.first != p.second)
						{
							sv1_track_which_temp_idx.push_back(sv1_match_track_which_idx[p.first++->second]);
							//std::cout << "with jet index: " << jet_index << "idx is appended to a sv1 temp list: " << sv1_track_which_temp_idx.back() << std::endl;
						}
						it = p.second;

					}

					sv1_sharedjet_which_idx.push_back(sv1_track_which_temp_idx);
					for (size_t k = 0; k < sv1_track_which_temp_idx.size(); k++) {
						int track_index = sv1_track_which_temp_idx[k];
                                                //std::cout << "sv1 w/ shared track's idx: " << track_index << std::endl;
						sv1_non_shared_track_which_idx.erase(std::remove(sv1_non_shared_track_which_idx.begin(), sv1_non_shared_track_which_idx.end(), track_index), sv1_non_shared_track_which_idx.end());

					}

					sv1_track_which_temp_idx = {};



				}

				std::vector<int> sv0_sum_pt_track_which_idx = sv0_total_track_which_idx;
				std::vector<int> sv0_sum_pt_only_dR_track_which_idx = sv0_total_track_which_idx;
				//std::vector<int> sv0_median_tk_vtx_dist_track_which_idx = sv0_total_track_which_idx;
				//std::vector<int> sv0_median_tk_vtx_dist_only_dR_track_which_idx = sv0_total_track_which_idx;
				std::vector<int> sv0_only_X_track_which_idx = sv0_total_track_which_idx;
				std::vector<int> sv0_sum_pT_only_Y_track_which_idx = sv0_total_track_which_idx;
				std::vector<int> sv0_shared_ntrack_only_Y_track_which_idx = sv0_total_track_which_idx;
				std::vector<int> sv0_median_tk_vtx_dist_sig_track_which_idx = sv0_total_track_which_idx;
				std::vector<int> sv0_median_tk_vtx_dist_sig_only_dR_track_which_idx = sv0_total_track_which_idx;
				std::vector<int> sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx = sv0_total_track_which_idx;		
				std::vector<int> sv0_no_shared_track_which_idx;
				track_vec tks_v0 = vertex_track_vec(v0);
				std::vector<int> sv1_sum_pt_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_sum_pt_only_dR_track_which_idx = sv1_total_track_which_idx;
				//std::vector<int> sv1_median_tk_vtx_dist_track_which_idx = sv1_total_track_which_idx;
				//std::vector<int> sv1_median_tk_vtx_dist_only_dR_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_only_X_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_sum_pT_only_Y_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_shared_ntrack_only_Y_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_median_tk_vtx_dist_sig_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_median_tk_vtx_dist_sig_only_dR_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx = sv1_total_track_which_idx;
				std::vector<int> sv1_no_shared_track_which_idx;
				track_vec tks_v1 = vertex_track_vec(v1);


				//std::cout << "the number of shared-jets is " << nsharedjets << std::endl;
				//std::cout << "sv0's phi = " << phi0 << " and " << "sv1's phi = " << phi1 << std::endl;                                  
                                //std::cout << "|dphi(sv0,jet)|: " << fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)) << std::endl;
                                //std::cout << "|dphi(sv1,jet)|: " << fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1)) << std::endl;
                                double vtx_sum_pt_i_sv0 = 0;
				for (unsigned int j = 0; j < sv0_total_track_which_idx.size(); j++) {
					int idx = sv0_total_track_which_idx[j] - 1;
					vtx_sum_pt_i_sv0 = vtx_sum_pt_i_sv0 + tks_v0[idx]->pt();
				}
				double vtx_sum_pt_i_sv1 = 0;
				for (unsigned int j = 0; j < sv1_total_track_which_idx.size(); j++) {
					int idx = sv1_total_track_which_idx[j] - 1;
					vtx_sum_pt_i_sv1 = vtx_sum_pt_i_sv1 + tks_v1[idx]->pt();
				}
				
				int nsv_onlyX = -1;
				int nsv_sumpT_onlyY = -1;
				int nsv_lonetrk_onlyY = -1;
				int nsv_sumpT = -1;
				int nsv_lonetrk = -1;
				int nsv_sumpTandX = -1;
				int nsv_lonetrkandX = -1;
				int sv0_sumpTandX = -1;
				int sv0_lonetrkandX = -1;
				int sv1_sumpTandX = -1;
				int sv1_lonetrkandX = -1;
				int X_nsharedjets = 0;
				int Xa_nsharedjets = 0;
				int Xb_nsharedjets = 0;
				int Xc_nsharedjets = 0;
				int Y_nsharedjets = 0;
				
				std::vector<double> X_i_sharedjet_lone_tk_vtx0_dist;
				std::vector<double> X_i_sharedjet_lone_tk_vtx0_dist_sig;
				std::vector<double> X_i_sharedjet_lone_tk_vtx0_dist_err;

				std::vector<double> X_i_sharedjet_lone_tk_vtx1_dist;
				std::vector<double> X_i_sharedjet_lone_tk_vtx1_dist_sig;
				std::vector<double> X_i_sharedjet_lone_tk_vtx1_dist_err;
				

				for (int i = 0; i < nsharedjets; i++) {

					size_t jet_index = nsharedjet_jet_index[i];
                                        //std::cout << "|dphi(sv0,jet)|: " << fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)) << std::endl;                                                                              //std::cout << "|dphi(sv1,jet)|: " << fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1)) << std::endl;

					std::vector<int> sv0_i_sharedjet_which_idx = sv0_sharedjet_which_idx[i];
					std::vector<double> sv0_i_sharedjet_tk_vtx_dist_copy;
					std::vector<double> sv0_i_sharedjet_tk_vtx_dist;
					std::vector<double> sv0_i_sharedjet_tk_vtx_dist_sig_copy;
					std::vector<double> sv0_i_sharedjet_tk_vtx_dist_sig;
					std::vector<double> sv0_i_sharedjet_tk_vtx_dist_err;
					std::vector<double> sv0_i_sharedjet_tk_pT;
					std::vector<double> sv0_i_sharedjet_tk_eta;
					std::vector<double> sv0_i_sharedjet_tk_phi;

					double sum_dR_i_sv0 = 0;
					double sum_eta_i_sv0 = 0;
					double sum_x_i_sv0 = 0;
					double sum_y_i_sv0 = 0;
					double sum_pt_i_sv0 = 0;
					


					//std::cout << " shared-jet index: " << jet_index << std::endl;
					for (unsigned int j = 0; j < sv0_i_sharedjet_which_idx.size(); j++) {
						int idx = sv0_i_sharedjet_which_idx[j] - 1;
						//std::cout << "vtx0's only shared tracks w/ idx: " << idx << std::endl;
						sum_pt_i_sv0 = sum_pt_i_sv0 + tks_v0[idx]->pt();
						reco::TransientTrack v0_track;
						v0_track = tt_builder->build(tks_v0[idx]);
						std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(v0_track, v0);
						sv0_i_sharedjet_tk_vtx_dist.push_back(tk_vtx_dist.second.value());
                                                //std::cout << "check MD" << std::endl;
                                                //std::cout << "tkvtx dist: " << tk_vtx_dist.second.value() << std::endl;
						sv0_i_sharedjet_tk_vtx_dist_sig.push_back(tk_vtx_dist.second.significance());
						sv0_i_sharedjet_tk_vtx_dist_err.push_back(tk_vtx_dist.second.error());
						sv0_i_sharedjet_tk_pT.push_back(tks_v0[idx]->pt());
						sv0_i_sharedjet_tk_eta.push_back(tks_v0[idx]->eta());
						sv0_i_sharedjet_tk_phi.push_back(tks_v0[idx]->phi());

						double dR = reco::deltaR((*jets)[jet_index].eta(), (*jets)[jet_index].phi(), tks_v0[idx]->eta(), tks_v0[idx]->phi());
						sum_dR_i_sv0 = sum_dR_i_sv0 + dR;
						sum_eta_i_sv0 = sum_eta_i_sv0 + tks_v0[idx]->eta();
						sum_x_i_sv0 = sum_x_i_sv0 + cos(tks_v0[idx]->phi());
						sum_y_i_sv0 = sum_y_i_sv0 + sin(tks_v0[idx]->phi());
                                                //std::cout << "  " << j + 1 << " shared track's phi: " << tks_v0[idx]->phi() << " shared track's eta: " << tks_v0[idx]->eta() << " shared track's pt: " << tks_v0[idx]->pt() << " shared track's sig_dxy: " << tk_vtx_dist.second.significance() << std::endl; 
					}

					/*
					double median_tk_vtx_dist_sv0;
					
					
					sv0_i_sharedjet_tk_vtx_dist_copy = sv0_i_sharedjet_tk_vtx_dist;
					std::sort(sv0_i_sharedjet_tk_vtx_dist.begin(), sv0_i_sharedjet_tk_vtx_dist.end());
					
                                        //std::cout << "division by 2 of a set: " << sv0_i_sharedjet_tk_vtx_dist.size() / 2 << std::endl;

					if (fmod(sv0_i_sharedjet_tk_vtx_dist.size(), 2) == 1.0) {
						median_tk_vtx_dist_sv0 = sv0_i_sharedjet_tk_vtx_dist[sv0_i_sharedjet_tk_vtx_dist.size() / 2];
						}
					else {
						median_tk_vtx_dist_sv0 = (sv0_i_sharedjet_tk_vtx_dist[sv0_i_sharedjet_tk_vtx_dist.size() / 2] + sv0_i_sharedjet_tk_vtx_dist[(sv0_i_sharedjet_tk_vtx_dist.size() / 2) - 1]) / 2;
					}
					*/
					

					double median_tk_vtx_dist_sig_sv0;
					
					
                                        //double median_tk_vtx_dist_sig_its_value_sv0;
					sv0_i_sharedjet_tk_vtx_dist_sig_copy = sv0_i_sharedjet_tk_vtx_dist_sig;
					std::sort(sv0_i_sharedjet_tk_vtx_dist_sig.begin(), sv0_i_sharedjet_tk_vtx_dist_sig.end());
					
					if (fmod(sv0_i_sharedjet_tk_vtx_dist_sig.size(), 2) == 1.0) {
						median_tk_vtx_dist_sig_sv0 = sv0_i_sharedjet_tk_vtx_dist_sig[sv0_i_sharedjet_tk_vtx_dist_sig.size() / 2];
                                                //std::cout << "MDS index: " << pT_idx0_odd << std::endl;
                                                //std::cout << "correct MDS: " << median_tk_vtx_dist_sig_sv0 << std::endl;
                                                //std::cout << "MDS index to MDS: " << sv0_i_sharedjet_tk_vtx_dist_sig_copy[pT_idx0_odd] << std::endl;

						
						}
					else {
						median_tk_vtx_dist_sig_sv0 = (sv0_i_sharedjet_tk_vtx_dist_sig[sv0_i_sharedjet_tk_vtx_dist_sig.size() / 2] + sv0_i_sharedjet_tk_vtx_dist_sig[(sv0_i_sharedjet_tk_vtx_dist_sig.size() / 2) - 1]) / 2;
						
					}

					
				
					//.....................................................

					std::vector<int> sv1_i_sharedjet_which_idx = sv1_sharedjet_which_idx[i];
					std::vector<double> sv1_i_sharedjet_tk_pT;
					std::vector<double> sv1_i_sharedjet_tk_vtx_dist_copy;
					std::vector<double> sv1_i_sharedjet_tk_vtx_dist;
					std::vector<double> sv1_i_sharedjet_tk_vtx_dist_sig_copy;
					std::vector<double> sv1_i_sharedjet_tk_vtx_dist_sig;
					std::vector<double> sv1_i_sharedjet_tk_vtx_dist_err;
					std::vector<double> sv1_i_sharedjet_tk_eta;
					std::vector<double> sv1_i_sharedjet_tk_phi;

					double sum_dR_i_sv1 = 0;
					double sum_eta_i_sv1 = 0;
					double sum_x_i_sv1 = 0;
					double sum_y_i_sv1 = 0;
					double sum_pt_i_sv1 = 0;
					

					for (unsigned int j = 0; j < sv1_i_sharedjet_which_idx.size(); j++) {
						int idx = sv1_i_sharedjet_which_idx[j] - 1;
						sum_pt_i_sv1 = sum_pt_i_sv1 + tks_v1[idx]->pt();
						reco::TransientTrack v1_track;
						v1_track = tt_builder->build(tks_v1[idx]);
						std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(v1_track, v1);
						sv1_i_sharedjet_tk_vtx_dist_sig.push_back(tk_vtx_dist.second.significance());
						sv1_i_sharedjet_tk_vtx_dist.push_back(tk_vtx_dist.second.value());
						sv1_i_sharedjet_tk_vtx_dist_err.push_back(tk_vtx_dist.second.error());
						sv1_i_sharedjet_tk_pT.push_back(tks_v1[idx]->pt());
						sv1_i_sharedjet_tk_eta.push_back(tks_v1[idx]->eta());
						sv1_i_sharedjet_tk_phi.push_back(tks_v1[idx]->phi());

						double dR = reco::deltaR((*jets)[jet_index].eta(), (*jets)[jet_index].phi(), tks_v1[idx]->eta(), tks_v1[idx]->phi());
						sum_dR_i_sv1 = sum_dR_i_sv1 + dR;
						sum_eta_i_sv1 = sum_eta_i_sv1 + tks_v1[idx]->eta();
						sum_x_i_sv1 = sum_x_i_sv1 + cos(tks_v1[idx]->phi());
						sum_y_i_sv1 = sum_y_i_sv1 + sin(tks_v1[idx]->phi());
                                                //std::cout << "  " << j + 1 << " shared track's phi: " << tks_v1[idx]->phi() << " shared track's eta: " << tks_v1[idx]->eta() << " shared track's pt: " << tks_v1[idx]->pt() << " shared track's sig_dxy: " << tk_vtx_dist.second.significance() << std::endl; 
					}

					/*
					double median_tk_vtx_dist_sv1;
					
					sv1_i_sharedjet_tk_vtx_dist_copy = sv1_i_sharedjet_tk_vtx_dist;
					std::sort(sv1_i_sharedjet_tk_vtx_dist.begin(), sv1_i_sharedjet_tk_vtx_dist.end());
					std::vector<double>::iterator it1_odd = find(sv1_i_sharedjet_tk_vtx_dist_copy.begin(), sv1_i_sharedjet_tk_vtx_dist_copy.end(), sv1_i_sharedjet_tk_vtx_dist[sv1_i_sharedjet_tk_vtx_dist.size() / 2]);
                                        //std::cout << "division by 2 of a set: " << sv1_i_sharedjet_tk_vtx_dist.size() / 2 << std::endl; 
					
					if (fmod(sv1_i_sharedjet_tk_vtx_dist.size(), 2) == 1.0) {
						median_tk_vtx_dist_sv1 = sv1_i_sharedjet_tk_vtx_dist[sv1_i_sharedjet_tk_vtx_dist.size() / 2];
						}
					else {
						median_tk_vtx_dist_sv1 = (sv1_i_sharedjet_tk_vtx_dist[sv1_i_sharedjet_tk_vtx_dist.size() / 2] + sv1_i_sharedjet_tk_vtx_dist[(sv1_i_sharedjet_tk_vtx_dist.size() / 2) - 1]) / 2;
					}
					*/

					double median_tk_vtx_dist_sig_sv1;
					
                                        //double median_tk_vtx_dist_sig_its_value_sv1;

					sv1_i_sharedjet_tk_vtx_dist_sig_copy = sv1_i_sharedjet_tk_vtx_dist_sig;
					std::sort(sv1_i_sharedjet_tk_vtx_dist_sig.begin(), sv1_i_sharedjet_tk_vtx_dist_sig.end());
					
					if (fmod(sv1_i_sharedjet_tk_vtx_dist_sig.size(), 2) == 1.0) {
						median_tk_vtx_dist_sig_sv1 = sv1_i_sharedjet_tk_vtx_dist_sig[sv1_i_sharedjet_tk_vtx_dist_sig.size() / 2];
                                                //std::cout << "MDS index: " << pT_idx1_odd << std::endl;                                                                                                                             std::cout << "correct MDS: " << median_tk_vtx_dist_sig_sv1 << std::endl;                                                                                                            std::cout << "MDS index to MDS: " << sv1_i_sharedjet_tk_vtx_dist_sig_copy[pT_idx1_odd] << std::endl; 
						}
					else {
						median_tk_vtx_dist_sig_sv1 = (sv1_i_sharedjet_tk_vtx_dist_sig[sv1_i_sharedjet_tk_vtx_dist_sig.size() / 2] + sv1_i_sharedjet_tk_vtx_dist_sig[(sv1_i_sharedjet_tk_vtx_dist_sig.size() / 2) - 1]) / 2;
						
					}

					
					//......................................................

					double mean_x_sv0 = sum_x_i_sv0 / sv0_i_sharedjet_which_idx.size();
					double mean_y_sv0 = sum_y_i_sv0 / sv0_i_sharedjet_which_idx.size();
					double mean_x_sv1 = sum_x_i_sv1 / sv1_i_sharedjet_which_idx.size();
					double mean_y_sv1 = sum_y_i_sv1 / sv1_i_sharedjet_which_idx.size();

					double mean_eta_sv0 = sum_eta_i_sv0 / sv0_i_sharedjet_which_idx.size();
					double mean_phi_sv0 = atan2(mean_y_sv0, mean_x_sv0);
					double mean_eta_sv1 = sum_eta_i_sv1 / sv1_i_sharedjet_which_idx.size();
					double mean_phi_sv1 = atan2(mean_y_sv1, mean_x_sv1);

					double avg_dR_track_pair = reco::deltaR(mean_eta_sv0, mean_phi_sv0, mean_eta_sv1, mean_phi_sv1);
					//std::cout << "mean eta sv0: " << mean_eta_sv0 << std::endl;
					//std::cout << "mean phi sv0: " << mean_phi_sv0 << std::endl;
					//std::cout << "mean eta sv1: " << mean_eta_sv1 << std::endl;
					//std::cout << "mean phi sv1: " << mean_phi_sv1 << std::endl;
                                         

					double sum_pow2_dR_spread_i_sv0 = 0;
					for (unsigned int j = 0; j < sv0_i_sharedjet_which_idx.size(); j++) {
						if (sv0_i_sharedjet_which_idx.size() == 1) {
							sum_pow2_dR_spread_i_sv0 = pow(0.1, 2);
						}
						else {
							sum_pow2_dR_spread_i_sv0 = sum_pow2_dR_spread_i_sv0 + pow(reco::deltaR(mean_eta_sv0, mean_phi_sv0, sv0_i_sharedjet_tk_eta[j], sv0_i_sharedjet_tk_phi[j]), 2);
						}
					}

					double sum_pow2_dR_spread_i_sv1 = 0;
					for (unsigned int j = 0; j < sv1_i_sharedjet_which_idx.size(); j++) {
						if (sv1_i_sharedjet_which_idx.size() == 1) {
							sum_pow2_dR_spread_i_sv1 = pow(0.1, 2);
						}
						else {
							sum_pow2_dR_spread_i_sv1 = sum_pow2_dR_spread_i_sv1 + pow(reco::deltaR(mean_eta_sv1, mean_phi_sv1, sv1_i_sharedjet_tk_eta[j], sv1_i_sharedjet_tk_phi[j]), 2);
						}
					}

					double avg_dR_spread_track_pair = sqrt((sum_pow2_dR_spread_i_sv0 / sv0_i_sharedjet_which_idx.size()) + (sum_pow2_dR_spread_i_sv1 / sv1_i_sharedjet_which_idx.size()));	// is this the correct rms of the two track spreads combined? need a division by 2? 
                    //{1,1}
					if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv0_i_sharedjet_which_idx.size() == 1 && sv1_i_sharedjet_which_idx.size() == 1) {
						//case X

						if (sv0_total_track_which_idx.size() >= 5 && sv1_total_track_which_idx.size() >= 5) {
							//PK: tbs<->bkg
							X_nsharedjets++;  
							h_at_least_5trk_output1_shared_tracks_pair_dPhi_X->Fill(fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], sv1_i_sharedjet_tk_phi[0])));
							h_2D_at_least_5trk_output1_shared_track_vtx0_shared_track_vtx1_dPhi_X->Fill(fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], phi0)), fabs(reco::deltaPhi(sv1_i_sharedjet_tk_phi[0], phi1)));
							if (fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0))> fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1))) {
								h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_X->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1)));
							}
							else {
								h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_X->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)));
							}
							//PK
							h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_X->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_X->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							}
							h_at_least_5trk_output1_shared_tracks_pair_dR_sig_X->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
							h_at_least_5trk_output1_shared_tracks_pair_dR_X->Fill(avg_dR_track_pair);
							
							h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
							
							
							if (avg_dR_track_pair < 0.2) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								}
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								
							}
							else {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_XdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								}
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								
							}
							
							
							// case Xa
							if (sv0_total_track_which_idx.size() == 5 && sv1_total_track_which_idx.size() == 5) {
								Xa_nsharedjets++;
								h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xa->Fill(fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], sv1_i_sharedjet_tk_phi[0])));
								if (fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)) > fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1))) {
									h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xa->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1)));
								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xa->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)));
								}

							}
							//case Xc
							else if (sv0_total_track_which_idx.size() > 5 && sv1_total_track_which_idx.size() > 5) {
								Xc_nsharedjets++;
								h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xc->Fill(fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], sv1_i_sharedjet_tk_phi[0])));
								if (fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)) > fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1))) {
									h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xc->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1)));
								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xc->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)));
								}

							}
							//case Xb
							else {
								Xb_nsharedjets++;
								h_at_least_5trk_output1_shared_tracks_pair_dPhi_Xb->Fill(fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], sv1_i_sharedjet_tk_phi[0])));
								if (fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)) > fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1))) {
									h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xb->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1)));
								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_Xb->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)));
								}

							}
							
						}

						if (sv0_total_track_which_idx.size() >= 3 && sv1_total_track_which_idx.size() >= 3) {

							//PK: tbs<->bkg
							//X_nsharedjets++;  
							//h_at_least_5trk_output1_shared_tracks_pair_dPhi_X->Fill(fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], sv1_i_sharedjet_tk_phi[0])));
							//h_2D_at_least_5trk_output1_shared_track_vtx0_shared_track_vtx1_dPhi_X->Fill(fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], phi0)), fabs(reco::deltaPhi(sv1_i_sharedjet_tk_phi[0], phi1)));
							//if (fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)) > fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1))) {
							//	h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_X->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi1)));
							//}
							//else {
							//	h_at_least_5trk_output1_shared_tracks_pair_closevtxjet_dPhi_X->Fill(fabs(reco::deltaPhi((*jets)[jet_index].phi(), phi0)));
							//}
							//PK
							h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_X->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							h_at_least_3trk_output1_shared_tracks_pair_dR_sig_X->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
							h_at_least_3trk_output1_shared_tracks_pair_dR_X->Fill(avg_dR_track_pair);
							
							h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_X->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
							
							if (avg_dR_track_pair < 0.2) {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								
							}
							else {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_XdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_XdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								
							}
						}
					}
					//{n>1,1}
					if ((dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv0_i_sharedjet_which_idx.size() > 1 && sv1_i_sharedjet_which_idx.size() == 1) || (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv1_i_sharedjet_which_idx.size() > 1 && sv0_i_sharedjet_which_idx.size() == 1)) {
						//case Y 

						if (sv0_total_track_which_idx.size() >= 5 && sv1_total_track_which_idx.size() >= 5) {
							Y_nsharedjets++;  //PK: tbs<->bkg
							if (int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()) >= 4) {
                                                               //std::cout << __LINE__ << std::endl; 
								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}

							}
                                                        //std::cout << __LINE__ << std::endl; 
							if (int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()) >= 4) {
                                                                //std::cout << __LINE__ << std::endl; 
								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRinjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0 < -4.0 ) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRinjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRinjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRinjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YAdRoutjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0 < -4.0) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YAdRoutjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YAdRoutjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YAdRoutjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

								}

							}
                                                        //std::cout << __LINE__ << std::endl; 
							if (0 < int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()) && int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()) <= 3) {

                                                                //std::cout << __LINE__ << std::endl; 
								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}

							}
                                                        //std::cout << __LINE__ << std::endl; 
							if (0 < int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()) && int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()) <= 3) {

                                                                //std::cout << __LINE__ << std::endl; 
								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRinjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0 < -4.0) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRinjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRinjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRinjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

								}
                                                              
								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YBdRoutjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									if (median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0 < -4.0) {
										h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YBdRoutjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									}
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YBdRoutjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YBdRoutjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

								}

							}

                                                        //std::cout << __LINE__ << std::endl;
							h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_Y->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_Y->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							}
							h_at_least_5trk_output1_shared_tracks_pair_dR_sig_Y->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
							if (sv1_i_sharedjet_which_idx.size() == 1) {
								h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, sv0_i_sharedjet_which_idx.size());
								h_2D_at_least_5trk_output1_shared_tracks_pair_dR_shared_tracks_Y->Fill(avg_dR_track_pair, sv0_i_sharedjet_which_idx.size());
								h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y->Fill(sqrt(pow(avg_dR_spread_track_pair, 2) - pow(0.1, 2)), sv0_i_sharedjet_which_idx.size());
							}
							else {
								h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, sv1_i_sharedjet_which_idx.size());
								h_2D_at_least_5trk_output1_shared_tracks_pair_dR_shared_tracks_Y->Fill(avg_dR_track_pair, sv1_i_sharedjet_which_idx.size());
								h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y->Fill(sqrt(pow(avg_dR_spread_track_pair, 2) - pow(0.1, 2)), sv1_i_sharedjet_which_idx.size());

							}
							
							h_at_least_5trk_output1_shared_tracks_pair_dR_Y->Fill(avg_dR_track_pair);
							h_at_least_5trk_output1_shared_tracks_pair_dR_err_Y->Fill(sqrt(pow(avg_dR_spread_track_pair, 2) - pow(0.1, 2)));
							h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
							h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_Y->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
							
							

							if (avg_dR_track_pair < 0.2) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								}
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

							}
							else {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_YdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								}
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

							}
						}

						if (sv0_total_track_which_idx.size() >= 3 && sv1_total_track_which_idx.size() >= 3) {

							//Y_nsharedjets++;  //PK: tbs<->bkg
							h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_Y->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							h_at_least_3trk_output1_shared_tracks_pair_dR_sig_Y->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
							if (sv1_i_sharedjet_which_idx.size() == 1) {
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, sv0_i_sharedjet_which_idx.size());
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_Y->Fill(avg_dR_track_pair, sv0_i_sharedjet_which_idx.size());
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y->Fill(sqrt(pow(avg_dR_spread_track_pair, 2) - pow(0.1, 2)), sv0_i_sharedjet_which_idx.size());
							}
							else {
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_Y->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, sv1_i_sharedjet_which_idx.size());
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_Y->Fill(avg_dR_track_pair, sv1_i_sharedjet_which_idx.size());
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_Y->Fill(sqrt(pow(avg_dR_spread_track_pair, 2) - pow(0.1, 2)), sv1_i_sharedjet_which_idx.size());

							}
							h_at_least_3trk_output1_shared_tracks_pair_dR_Y->Fill(avg_dR_track_pair);
							h_at_least_3trk_output1_shared_tracks_pair_dR_err_Y->Fill(sqrt(pow(avg_dR_spread_track_pair, 2) - pow(0.1, 2)));
							h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_Y->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
							h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_Y->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
							

							if (avg_dR_track_pair < 0.2) {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

							}
							else {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_YdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_YdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_YdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

							}
						}
					}
					//{n>1,m>1} 
					if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv0_i_sharedjet_which_idx.size() > 1 && sv1_i_sharedjet_which_idx.size() > 1) {
						if (sv0_total_track_which_idx.size() >= 5 && sv1_total_track_which_idx.size() >= 5) {
                                                        //std::cout << __LINE__ << std::endl;
							//case ZA: tight SVa/b
							if (int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()) >= 4) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZA->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZA->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_ZA->Fill(avg_dR_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZA->Fill(avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZA->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZA->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
								h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZA->Fill(int(sv0_i_sharedjet_which_idx.size()), int(sv1_i_sharedjet_which_idx.size()));
                                                                //std::cout << __LINE__ << std::endl;
								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}

								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}
							        //std::cout << __LINE__ << std::endl;	


							}

							if (int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()) >= 4) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZA->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
								h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZA->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_ZA->Fill(avg_dR_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZA->Fill(avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZA->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZA->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));
								h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZA->Fill(int(sv1_i_sharedjet_which_idx.size()), int(sv0_i_sharedjet_which_idx.size()));
                                                                //std::cout << __LINE__ << std::endl;
								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRinjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRinjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRinjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

								}
								else  {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZAdRoutjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZAdRoutjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZAdRoutjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

								}
                                                                //std::cout << __LINE__ << std::endl;

							}

							//case ZB: loose SVa/b 
							if (0 < int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()) && int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()) <= 3) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZB->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZB->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_ZB->Fill(avg_dR_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZB->Fill(avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZB->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZB->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
								h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZB->Fill(int(sv0_i_sharedjet_which_idx.size()), int(sv1_i_sharedjet_which_idx.size()));

								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

									

								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}

							}

							if (0 < int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()) && int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()) <= 3) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZB->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
								h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZB->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_ZB->Fill(avg_dR_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZB->Fill(avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZB->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZB->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));
								h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZB->Fill(int(sv1_i_sharedjet_which_idx.size()), int(sv0_i_sharedjet_which_idx.size()));

								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRinjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRinjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRinjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

									
								}
								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZBdRoutjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZBdRoutjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZBdRoutjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

									
								}

							}

							//case ZC: equal SVa/b 	 (SV0 - SV1)
							if (int(sv0_i_sharedjet_which_idx.size()) == int(sv1_i_sharedjet_which_idx.size())) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZC->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZC->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_ZC->Fill(avg_dR_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZC->Fill(avg_dR_spread_track_pair);
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZC->Fill(int(sv0_i_sharedjet_which_idx.size()));
								
								if (avg_dR_track_pair < 0.2) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);

								}
								
								else {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);

								}

							}

							//case ZO: every shared-jets	 (SV0 - SV1)
							h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZO->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZO->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							}
							h_at_least_5trk_output1_shared_tracks_pair_dR_sig_ZO->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
							h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()));
							h_2D_at_least_5trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, int(sv1_i_sharedjet_which_idx.size()));
							h_at_least_5trk_output1_shared_tracks_pair_dR_ZO->Fill(avg_dR_track_pair);
							h_2D_at_least_5trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO->Fill(avg_dR_track_pair, int(sv0_i_sharedjet_which_idx.size()));
							h_2D_at_least_5trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO->Fill(avg_dR_track_pair, int(sv1_i_sharedjet_which_idx.size()));
							h_at_least_5trk_output1_shared_tracks_pair_dR_err_ZO->Fill(avg_dR_spread_track_pair);
							h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO->Fill(avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()));
							h_2D_at_least_5trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO->Fill(avg_dR_spread_track_pair, int(sv1_i_sharedjet_which_idx.size()));
							h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
							h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZO->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
							h_2D_at_least_5trk_output1_shared_tracks_pair_shared_tracks_ZO->Fill(int(sv0_i_sharedjet_which_idx.size()), int(sv1_i_sharedjet_which_idx.size()));

                                                        //std::cout << __LINE__ << std::endl;
							if (avg_dR_track_pair < 0.2) {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
								if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								}
							
							}
							
							else {
								h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_5trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_5trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
								if (median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 < -4.0 || median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1 > 4.0) {
									h_at_least_5trk_output1_shared_tracks_pair_asym_sum_pT_of_large_MDS_ZOdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								}
							}

						        //std::cout << __LINE__ << std::endl; 	
						}
						                                 
						if (sv0_total_track_which_idx.size() >= 3 && sv1_total_track_which_idx.size() >= 3) {
							//case Znon-C: SVa/b
                                                  //std::cout << __LINE__ << std::endl;
							if (0 < int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size())) {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonC->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZnonC->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_diff_shared_tracks_ZnonC->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_dR_ZnonC->Fill(avg_dR_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_diff_shared_tracks_ZnonC->Fill(avg_dR_track_pair, int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZnonC->Fill(avg_dR_spread_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_diff_shared_tracks_ZnonC->Fill(avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonC->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonC->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
					                       // std::cout << __LINE__ << std::endl; 			
								if (avg_dR_track_pair < 0.2) {
									h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}
								
								else {
									h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
									h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

								}
                                                               // std::cout << __LINE__ << std::endl; 

							}
                                                        //std::cout << __LINE__ << std::endl;
							if (0 < int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size())) {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonC->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
								h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZnonC->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_diff_shared_tracks_ZnonC->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_dR_ZnonC->Fill(avg_dR_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_diff_shared_tracks_ZnonC->Fill(avg_dR_track_pair, int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZnonC->Fill(avg_dR_spread_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_diff_shared_tracks_ZnonC->Fill( avg_dR_spread_track_pair, int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonC->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
								h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonC->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));
								
								if (avg_dR_track_pair < 0.2) {
									h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRinjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
									h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRinjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRinjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));


								}
								
								else {
									h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZnonCdRoutjet->Fill((sum_pt_i_sv1 - sum_pt_i_sv0) / (sum_pt_i_sv1 + sum_pt_i_sv0));
									h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZnonCdRoutjet->Fill(median_tk_vtx_dist_sig_sv1 - median_tk_vtx_dist_sig_sv0);
									h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZnonCdRoutjet->Fill(int(sv1_i_sharedjet_which_idx.size()) - int(sv0_i_sharedjet_which_idx.size()));

								}

							}
                                                        //std::cout << __LINE__ << std::endl; 
							//case ZC: equal SVa/b 	 (SV0 - SV1)
							if (int(sv0_i_sharedjet_which_idx.size()) == int(sv1_i_sharedjet_which_idx.size())) {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZC->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZC->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_shared_tracks_ZC->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_dR_ZC->Fill(avg_dR_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_shared_tracks_ZC->Fill(avg_dR_track_pair, int(sv0_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZC->Fill(avg_dR_spread_track_pair);
								h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_shared_tracks_ZC->Fill(avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZC->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZC->Fill(int(sv0_i_sharedjet_which_idx.size()));

								if (avg_dR_track_pair < 0.2) {
									h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);

								}
								else {
									h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZCdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
									h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZCdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								}

							}
                                                        //std::cout << __LINE__ << std::endl; 

							//case ZO: every shared-jets	 (SV0 - SV1)
							h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZO->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
							h_at_least_3trk_output1_shared_tracks_pair_dR_sig_ZO->Fill(avg_dR_track_pair / avg_dR_spread_track_pair);
							h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()));
							h_2D_at_least_3trk_output1_shared_tracks_pair_dR_sig_2x_shared_tracks_ZO->Fill(avg_dR_track_pair / avg_dR_spread_track_pair, int(sv1_i_sharedjet_which_idx.size()));
							h_at_least_3trk_output1_shared_tracks_pair_dR_ZO->Fill(avg_dR_track_pair);
							h_2D_at_least_3trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO->Fill(avg_dR_track_pair, int(sv0_i_sharedjet_which_idx.size()));
							h_2D_at_least_3trk_output1_shared_tracks_pair_dR_2x_shared_tracks_ZO->Fill(avg_dR_track_pair, int(sv1_i_sharedjet_which_idx.size()));
							h_at_least_3trk_output1_shared_tracks_pair_dR_err_ZO->Fill(avg_dR_spread_track_pair);
							h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO->Fill(avg_dR_spread_track_pair, int(sv0_i_sharedjet_which_idx.size()));
							h_2D_at_least_3trk_output1_shared_tracks_pair_dR_err_2x_shared_tracks_ZO->Fill(avg_dR_spread_track_pair, int(sv1_i_sharedjet_which_idx.size()));

							h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZO->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
							h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZO->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));
							h_2D_at_least_3trk_output1_shared_tracks_pair_shared_tracks_ZO->Fill(int(sv0_i_sharedjet_which_idx.size()), int(sv1_i_sharedjet_which_idx.size()));

							if (avg_dR_track_pair < 0.2) {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRinjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRinjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRinjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

							}
							
							else {
								h_at_least_3trk_output1_shared_tracks_pair_asym_sum_pT_ZOdRoutjet->Fill((sum_pt_i_sv0 - sum_pt_i_sv1) / (sum_pt_i_sv0 + sum_pt_i_sv1));
								h_at_least_3trk_output1_shared_tracks_pair_diff_median_tkvtxdistsig_ZOdRoutjet->Fill(median_tk_vtx_dist_sig_sv0 - median_tk_vtx_dist_sig_sv1);
								h_at_least_3trk_output1_shared_tracks_pair_diff_shared_tracks_ZOdRoutjet->Fill(int(sv0_i_sharedjet_which_idx.size()) - int(sv1_i_sharedjet_which_idx.size()));

							}



						}
					}

				

					std::vector<int> sv1_diff;
					std::vector<int> sv0_diff;


					if (sum_pt_i_sv0 >= sum_pt_i_sv1) {
						//std::cout << " sv0 is selected " << std::endl;
						std::set_difference(sv1_sum_pt_track_which_idx.begin(), sv1_sum_pt_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
						std::inserter(sv1_diff, sv1_diff.begin()));
						sv1_sum_pt_track_which_idx = sv1_diff;
						if (avg_dR_track_pair / avg_dR_spread_track_pair < 1)
							sv1_sum_pt_only_dR_track_which_idx = sv1_diff;
					}
					else {
						//std::cout << " sv1 is selected " << std::endl;
						std::set_difference(sv0_sum_pt_track_which_idx.begin(), sv0_sum_pt_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
						std::inserter(sv0_diff, sv0_diff.begin()));
						sv0_sum_pt_track_which_idx = sv0_diff;
						if (avg_dR_track_pair / avg_dR_spread_track_pair < 1)
							sv0_sum_pt_only_dR_track_which_idx = sv0_diff;
					}

					/*
					sv1_diff = {};
					sv0_diff = {};


					if (median_tk_vtx_dist_sv1 >= median_tk_vtx_dist_sv0) {
						//std::cout << " sv0 is selected " << std::endl;
						std::set_difference(sv1_median_tk_vtx_dist_track_which_idx.begin(), sv1_median_tk_vtx_dist_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
							std::inserter(sv1_diff, sv1_diff.begin()));
						sv1_median_tk_vtx_dist_track_which_idx = sv1_diff;
						if (avg_dR_track_pair / avg_dR_spread_track_pair < 1)
							sv1_median_tk_vtx_dist_only_dR_track_which_idx = sv1_diff;
					}
					else {
						//std::cout << " sv1 is selected " << std::endl;
						std::set_difference(sv0_median_tk_vtx_dist_track_which_idx.begin(), sv0_median_tk_vtx_dist_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
							std::inserter(sv0_diff, sv0_diff.begin()));
						sv0_median_tk_vtx_dist_track_which_idx = sv0_diff;
						if (avg_dR_track_pair / avg_dR_spread_track_pair < 1)
							sv0_median_tk_vtx_dist_only_dR_track_which_idx = sv0_diff;
					}
					*/

					// if X case only
					sv1_diff = {};
					sv0_diff = {};

					if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv0_i_sharedjet_which_idx.size() == 1 && sv1_i_sharedjet_which_idx.size() == 1) {

						if (sv0_total_track_which_idx.size() >= 5 && sv1_total_track_which_idx.size() >= 5) { //PK: tbs<->bkg
							nsv_onlyX = 2;
							reco::TransientTrack lonesv0_track;
							int lonesv0_idx = sv0_i_sharedjet_which_idx[0] - 1;
							lonesv0_track = tt_builder->build(tks_v0[lonesv0_idx]);
							std::pair<bool, Measurement1D> lone_tk_vtx0_dist = track_dist(lonesv0_track, v0);
							X_i_sharedjet_lone_tk_vtx0_dist_sig.push_back(lone_tk_vtx0_dist.second.significance());
							X_i_sharedjet_lone_tk_vtx0_dist.push_back(lone_tk_vtx0_dist.second.value());
							X_i_sharedjet_lone_tk_vtx0_dist_err.push_back(lone_tk_vtx0_dist.second.error());

							reco::TransientTrack lonesv1_track;
							int lonesv1_idx = sv1_i_sharedjet_which_idx[0] - 1;
							lonesv1_track = tt_builder->build(tks_v1[lonesv1_idx]);
							std::pair<bool, Measurement1D> lone_tk_vtx1_dist = track_dist(lonesv1_track, v1);
							X_i_sharedjet_lone_tk_vtx1_dist_sig.push_back(lone_tk_vtx1_dist.second.significance());
							X_i_sharedjet_lone_tk_vtx1_dist.push_back(lone_tk_vtx1_dist.second.value());
							X_i_sharedjet_lone_tk_vtx1_dist_err.push_back(lone_tk_vtx1_dist.second.error());
							
							if (fabs(reco::deltaPhi(sv0_i_sharedjet_tk_phi[0], sv1_i_sharedjet_tk_phi[0])) < 1.5) {
								std::set_difference(sv1_only_X_track_which_idx.begin(), sv1_only_X_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
									std::inserter(sv1_diff, sv1_diff.begin()));
								sv1_only_X_track_which_idx = sv1_diff;

								std::set_difference(sv0_only_X_track_which_idx.begin(), sv0_only_X_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
									std::inserter(sv0_diff, sv0_diff.begin()));
								sv0_only_X_track_which_idx = sv0_diff;
							}

							
						}
					}
					// end X case only 

					// if Y case only
					sv1_diff = {};
					sv0_diff = {};
					
					if ((dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv0_i_sharedjet_which_idx.size() > 1 && sv1_i_sharedjet_which_idx.size() == 1) || (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv1_i_sharedjet_which_idx.size() > 1 && sv0_i_sharedjet_which_idx.size() == 1)) {
						
						if (sv0_total_track_which_idx.size() >= 5 && sv1_total_track_which_idx.size() >= 5) { //PK: tbs<->bkg
							nsv_sumpT_onlyY = 2;
							if (sum_pt_i_sv0 >= sum_pt_i_sv1) {
								//std::cout << " sv0 is selected " << std::endl;
								std::set_difference(sv1_sum_pT_only_Y_track_which_idx.begin(), sv1_sum_pT_only_Y_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
									std::inserter(sv1_diff, sv1_diff.begin()));
								sv1_sum_pT_only_Y_track_which_idx = sv1_diff;

							}
							else {
								//std::cout << " sv1 is selected " << std::endl;
								std::set_difference(sv0_sum_pT_only_Y_track_which_idx.begin(), sv0_sum_pT_only_Y_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
									std::inserter(sv0_diff, sv0_diff.begin()));
								sv0_sum_pT_only_Y_track_which_idx = sv0_diff;

							}
						}
					}

					sv1_diff = {};
					sv0_diff = {};

					if ((dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv0_i_sharedjet_which_idx.size() > 1 && sv1_i_sharedjet_which_idx.size() == 1) || (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && sv1_i_sharedjet_which_idx.size() > 1 && sv0_i_sharedjet_which_idx.size() == 1)) {

						if (sv0_total_track_which_idx.size() >= 5 && sv1_total_track_which_idx.size() >= 5) {  //PK: tbs<->bkg
							nsv_lonetrk_onlyY = 2; 
							if (sv0_i_sharedjet_which_idx.size() > sv1_i_sharedjet_which_idx.size()) {
								//std::cout << " sv0 is selected " << std::endl;
								std::set_difference(sv1_shared_ntrack_only_Y_track_which_idx.begin(), sv1_shared_ntrack_only_Y_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
									std::inserter(sv1_diff, sv1_diff.begin()));
								sv1_shared_ntrack_only_Y_track_which_idx = sv1_diff;

							}
							else {
								//std::cout << " sv1 is selected " << std::endl;
								std::set_difference(sv0_shared_ntrack_only_Y_track_which_idx.begin(), sv0_shared_ntrack_only_Y_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
									std::inserter(sv0_diff, sv0_diff.begin()));
								sv0_shared_ntrack_only_Y_track_which_idx = sv0_diff;

							}
						}
					}

					//end Y case only 
					sv1_diff = {};
					sv0_diff = {};

					
					if (median_tk_vtx_dist_sig_sv1 >= median_tk_vtx_dist_sig_sv0) {
						//std::cout << " sv0 is selected " << std::endl;
						std::set_difference(sv1_median_tk_vtx_dist_sig_track_which_idx.begin(), sv1_median_tk_vtx_dist_sig_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
							std::inserter(sv1_diff, sv1_diff.begin()));
						sv1_median_tk_vtx_dist_sig_track_which_idx = sv1_diff;
						if (avg_dR_track_pair / avg_dR_spread_track_pair < 1) 
							sv1_median_tk_vtx_dist_sig_only_dR_track_which_idx = sv1_diff;
							
					}
					else {
						//std::cout << " sv1 is selected " << std::endl;
						std::set_difference(sv0_median_tk_vtx_dist_sig_track_which_idx.begin(), sv0_median_tk_vtx_dist_sig_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
							std::inserter(sv0_diff, sv0_diff.begin()));
						sv0_median_tk_vtx_dist_sig_track_which_idx = sv0_diff;
						if (avg_dR_track_pair / avg_dR_spread_track_pair < 1)
							sv0_median_tk_vtx_dist_sig_only_dR_track_which_idx = sv0_diff;
					}

                                        sv1_diff = {};
                                        sv0_diff = {};

					if (avg_dR_track_pair / avg_dR_spread_track_pair < 1) {
						if (median_tk_vtx_dist_sig_sv1 > 2 && median_tk_vtx_dist_sig_sv0 > 2) {
							if (median_tk_vtx_dist_sig_sv1 >= median_tk_vtx_dist_sig_sv0) {
								//std::cout << " sv0 is selected " << std::endl;
								std::set_difference(sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx.begin(), sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
									std::inserter(sv1_diff, sv1_diff.begin()));
								sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx = sv1_diff;
								
							}
							else {
								//std::cout << " sv1 is selected " << std::endl;
								std::set_difference(sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx.begin(), sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
									std::inserter(sv0_diff, sv0_diff.begin()));
								sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx = sv0_diff;
								
							}

						}
						if (median_tk_vtx_dist_sig_sv1 > 2 && median_tk_vtx_dist_sig_sv0 <= 2) {
							std::set_difference(sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx.begin(), sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx.end(), sv1_i_sharedjet_which_idx.begin(), sv1_i_sharedjet_which_idx.end(),
								std::inserter(sv1_diff, sv1_diff.begin()));
							sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx = sv1_diff;
						}
						if (median_tk_vtx_dist_sig_sv0 > 2 && median_tk_vtx_dist_sig_sv1 <= 2) {
							std::set_difference(sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx.begin(), sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx.end(), sv0_i_sharedjet_which_idx.begin(), sv0_i_sharedjet_which_idx.end(),
								std::inserter(sv0_diff, sv0_diff.begin()));
							sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx = sv0_diff;
						}
					}
					

				}

				
			

				if (X_nsharedjets > 0 && Y_nsharedjets > 0) {
					h_2D_qualify_most_track_vertices_XandY_nsharedjet->Fill(X_nsharedjets, Y_nsharedjets);
				}

				Measurement1D dBV0_Meas1D = vertex_dist_2d.distance(v0, fake_bs_vtx);
				double dBV0 = dBV0_Meas1D.value();
				double bs2derr0 = dBV0_Meas1D.error();

				Measurement1D dBV1_Meas1D = vertex_dist_2d.distance(v1, fake_bs_vtx);
				double dBV1 = dBV1_Meas1D.value();
				double bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist = vertex_dist(v0, v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && v0.nTracks() >= 5 && v1.nTracks() >= 5) {	 //PK: tbs<->bkg
					nsv_sumpT = 2;
					nsv_lonetrk = 2;
					nsv_sumpTandX = 2;
					nsv_lonetrkandX = 2;
					sv0_sumpTandX = 1;
					sv0_lonetrkandX = 1;
					sv1_sumpTandX = 1;
					sv1_lonetrkandX = 1;
					h_qualify_svdist2d_three_bins->Fill(v_dist.value());
					h_qualify_most_track_vertices_nsharedjet->Fill(nsharedjets);
				}
					

				//--------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_v0_ttks;
				for (unsigned int i = 0, ie = sv0_sum_pt_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_sum_pt_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_v0;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_v0_ttks))
					nosharedjets_v0 = reco::Vertex(tv);

				/*
				if (nosharedjets_v0.nTracks() > 0) {
					for (unsigned int i = 0, ie = sv0_sum_pt_track_which_idx.size(); i < ie; ++i) {
						reco::TransientTrack v0_track;
						int idx = sv0_sum_pt_track_which_idx[i] - 1;
						v0_track = tt_builder->build(tks_v0[idx]);
						std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(v0_track, nosharedjets_v0);
						//std::cout << "  " << i + 1 << " shared track's phi: " << tks_v0[idx]->phi() << " shared track's pt: " << tks_v0[idx]->pt() << " shared track's sig_dxy: " << tk_vtx_dist.second.significance() << std::endl;
					}
				}
				*/




				std::vector<reco::TransientTrack> nosharedjets_v1_ttks;
				for (unsigned int i = 0, ie = sv1_sum_pt_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_sum_pt_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_v1;
				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_v1_ttks))
					nosharedjets_v1 = reco::Vertex(tv);

				/*
				if (nosharedjets_v1.nTracks() > 0) {
					for (unsigned int i = 0, ie = sv1_sum_pt_track_which_idx.size(); i < ie; ++i) {
						reco::TransientTrack v1_track;
						int idx = sv1_sum_pt_track_which_idx[i] - 1;
						v1_track = tt_builder->build(tks_v1[idx]);
						std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(v1_track, nosharedjets_v1);
						//std::cout << "  " << i + 1 << " shared track's phi: " << tks_v1[idx]->phi() << " shared track's pt: " << tks_v1[idx]->pt() << " shared track's sig_dxy: " << tk_vtx_dist.second.significance() << std::endl;
					}
				}
				*/

				dBV0_Meas1D = vertex_dist_2d.distance(nosharedjets_v0, fake_bs_vtx);
				dBV0 = dBV0_Meas1D.value();
			    bs2derr0 = dBV0_Meas1D.error();

				dBV1_Meas1D = vertex_dist_2d.distance(nosharedjets_v1, fake_bs_vtx);
				dBV1 = dBV1_Meas1D.value();
				bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist_noshare_sum_pT = vertex_dist(nosharedjets_v0, nosharedjets_v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && nosharedjets_v0.nTracks() >= 5 && nosharedjets_v1.nTracks() >= 5)
					h_qualify_by_sum_pT_svdist2d_three_bins->Fill(v_dist_noshare_sum_pT.value());


				//--------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_only_dR_v0_ttks;
				for (unsigned int i = 0, ie = sv0_sum_pt_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_sum_pt_only_dR_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_only_dR_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_only_dR_v0;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_only_dR_v0_ttks))
					nosharedjets_only_dR_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_only_dR_v1_ttks;
				for (unsigned int i = 0, ie = sv1_sum_pt_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_sum_pt_only_dR_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_only_dR_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_only_dR_v1;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_only_dR_v1_ttks))
					nosharedjets_only_dR_v1 = reco::Vertex(tv);

				dBV0_Meas1D = vertex_dist_2d.distance(nosharedjets_only_dR_v0, fake_bs_vtx);
				dBV0 = dBV0_Meas1D.value();
				bs2derr0 = dBV0_Meas1D.error();

				dBV1_Meas1D = vertex_dist_2d.distance(nosharedjets_only_dR_v1, fake_bs_vtx);
				dBV1 = dBV1_Meas1D.value();
				bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist_noshare_sum_pT_only_dR = vertex_dist(nosharedjets_only_dR_v0, nosharedjets_only_dR_v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && nosharedjets_only_dR_v0.nTracks() >= 5 && nosharedjets_only_dR_v1.nTracks() >= 5)
					h_qualify_only_small_dR_by_sum_pT_svdist2d_three_bins->Fill(v_dist_noshare_sum_pT_only_dR.value());
				
				//------------------------------------------------------------

				/*
				
				std::vector<reco::TransientTrack> nosharedjets_med_dist_v0_ttks;
				for (unsigned int i = 0, ie = sv0_median_tk_vtx_dist_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_median_tk_vtx_dist_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_med_dist_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_med_dist_v0;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_v0_ttks))
					nosharedjets_med_dist_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_med_dist_v1_ttks;
				for (unsigned int i = 0, ie = sv1_median_tk_vtx_dist_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_median_tk_vtx_dist_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_med_dist_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_med_dist_v1;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_v1_ttks))
					nosharedjets_med_dist_v1 = reco::Vertex(tv);

				dBV0_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_v0, fake_bs_vtx);
				dBV0 = dBV0_Meas1D.value();
				bs2derr0 = dBV0_Meas1D.error();

				dBV1_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_v1, fake_bs_vtx);
				dBV1 = dBV1_Meas1D.value();
				bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist_noshare_med_dist = vertex_dist(nosharedjets_med_dist_v0, nosharedjets_med_dist_v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && nosharedjets_med_dist_v0.nTracks() >= 5 && nosharedjets_med_dist_v1.nTracks() >= 5)
					h_qualify_by_median_tkvtxdist_svdist2d_three_bins->Fill(v_dist_noshare_med_dist.value());
				
				//------------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_med_dist_only_dR_v0_ttks;
				for (unsigned int i = 0, ie = sv0_median_tk_vtx_dist_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_median_tk_vtx_dist_only_dR_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_med_dist_only_dR_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_med_dist_only_dR_v0;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_only_dR_v0_ttks))
					nosharedjets_med_dist_only_dR_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_med_dist_only_dR_v1_ttks;
				for (unsigned int i = 0, ie = sv1_median_tk_vtx_dist_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_median_tk_vtx_dist_only_dR_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_med_dist_only_dR_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_med_dist_only_dR_v1;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_only_dR_v1_ttks))
					nosharedjets_med_dist_only_dR_v1 = reco::Vertex(tv);

				dBV0_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_only_dR_v0, fake_bs_vtx);
				dBV0 = dBV0_Meas1D.value();
				bs2derr0 = dBV0_Meas1D.error();

				dBV1_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_only_dR_v1, fake_bs_vtx);
				dBV1 = dBV1_Meas1D.value();
				bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist_only_dR_noshare_med_dist = vertex_dist(nosharedjets_med_dist_only_dR_v0, nosharedjets_med_dist_only_dR_v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && nosharedjets_med_dist_only_dR_v0.nTracks() >= 5 && nosharedjets_med_dist_only_dR_v1.nTracks() >= 5)
					h_qualify_only_small_dR_by_median_tkvtxdist_svdist2d_three_bins->Fill(v_dist_only_dR_noshare_med_dist.value());

				*/
				//------------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_onlyX_v0_ttks;
				for (unsigned int i = 0, ie = sv0_only_X_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_only_X_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_onlyX_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_onlyX_v0;

				for (const TransientVertex& tv : kv_reco_dropin_nocut(nosharedjets_onlyX_v0_ttks))
					nosharedjets_onlyX_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_onlyX_v1_ttks;
				for (unsigned int i = 0, ie = sv1_only_X_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_only_X_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_onlyX_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_onlyX_v1;

				for (const TransientVertex& tv : kv_reco_dropin_nocut(nosharedjets_onlyX_v1_ttks))
					nosharedjets_onlyX_v1 = reco::Vertex(tv);

				double v0_chi2 = v0.normalizedChi2();
				double v0_ndof = v0.ndof();

				double v1_chi2 = v1.normalizedChi2();
				double v1_ndof = v1.ndof();

				double nosharedjets_onlyX_v0_chi2 = nosharedjets_onlyX_v0.normalizedChi2();
				double nosharedjets_onlyX_v0_ndof = nosharedjets_onlyX_v0.ndof();

				double nosharedjets_onlyX_v1_chi2 = nosharedjets_onlyX_v1.normalizedChi2();
				double nosharedjets_onlyX_v1_ndof = nosharedjets_onlyX_v1.ndof();

				double shift_unnorm_chi2_v0 = (nosharedjets_onlyX_v0_chi2 * nosharedjets_onlyX_v0_ndof) - (v0_chi2 * v0_ndof);
				double shift_unnorm_chi2_v1 = (nosharedjets_onlyX_v1_chi2 * nosharedjets_onlyX_v1_ndof) - (v1_chi2 * v1_ndof);

				



				if (sv0_only_X_track_which_idx.size() < sv0_total_track_which_idx.size() && shift_unnorm_chi2_v0 > shift_unnorm_chi2_v1 ) {  

					h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_X->Fill(shift_unnorm_chi2_v0);
					h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_X->Fill(v0_chi2 * v0_ndof);
					h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_X->Fill(nosharedjets_onlyX_v0_chi2 * nosharedjets_onlyX_v0_ndof);

					if (nosharedjets_onlyX_v0.nTracks() < 5 || nosharedjets_onlyX_v0_chi2  > 5) {  //PK: tbs<->bkg
						
						nsv_onlyX -= 1;
						sv0_sumpTandX -=-1;
						sv0_lonetrkandX -=1;
					}



				}

				if (sv1_only_X_track_which_idx.size() < sv1_total_track_which_idx.size() && shift_unnorm_chi2_v1 > shift_unnorm_chi2_v0 ) {

					h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_X->Fill(shift_unnorm_chi2_v1);
					h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_X->Fill(v1_chi2* v1_ndof);
					h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_X->Fill(nosharedjets_onlyX_v1_chi2* nosharedjets_onlyX_v1_ndof);

					if (nosharedjets_onlyX_v1.nTracks() < 5 || nosharedjets_onlyX_v1_chi2  > 5) {  //PK: tbs<->bkg
						
						nsv_onlyX -= 1;
						sv1_sumpTandX -= -1;
						sv1_lonetrkandX -= 1;
					}
				}

				
				if (nsv_onlyX >= 0) {
					h_qualify_most_track_vertices_X_nsharedjet->Fill(X_nsharedjets);
					h_at_least_5trk_output1_shared_tracks_pair_X_nsv_X->Fill(nsv_onlyX);
					h_2D_most_5trk_track_vertices_X_Deltachi2_SV0_SV1->Fill(shift_unnorm_chi2_v0, shift_unnorm_chi2_v1);
					h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_X->Fill(fabs(reco::deltaPhi(phi0, phi1)));

					if ((shift_unnorm_chi2_v0 >= 0 || shift_unnorm_chi2_v1 >= 0) && (nosharedjets_onlyX_v0.nTracks() > 0) && (nosharedjets_onlyX_v1.nTracks() > 0)) {
						std::cout << "MFVVertexer " << module_label << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << std::endl;
						std::cout << "shift in v0: " << shift_unnorm_chi2_v0 << std::endl;
						std::cout << "chi2 of v0: " << v0_chi2 * v0_ndof << std::endl;
						std::cout << "ndof of v0: " << v0_ndof << std::endl;
						
						for (unsigned int i = 0, ie = X_i_sharedjet_lone_tk_vtx0_dist.size(); i < ie; ++i) {
							std::cout << "sv0's " << i << "{1,1} shared jet" << std::endl;
							std::cout << "miss_dist_sig of lone trk to v0: " << X_i_sharedjet_lone_tk_vtx0_dist_sig[i] << std::endl;
							std::cout << "miss_dist_value of lone trk to v0: " << X_i_sharedjet_lone_tk_vtx0_dist[i] << std::endl;
							std::cout << "miss_dist_error of lone trk to v0: " << X_i_sharedjet_lone_tk_vtx0_dist_err[i] << std::endl;
						}
						
						std::cout << "shift in v1: " << shift_unnorm_chi2_v1 << std::endl;
						std::cout << "chi2 of v1: " << v1_chi2 * v1_ndof << std::endl;
						std::cout << "ndof of v1: " << v1_ndof << std::endl;
						for (unsigned int i = 0, ie = X_i_sharedjet_lone_tk_vtx1_dist.size(); i < ie; ++i) {
							std::cout << "sv1's " << i << "{1,1} shared jet" << std::endl;
							std::cout << "miss_dist_sig of lone trk to v1: " << X_i_sharedjet_lone_tk_vtx1_dist_sig[i] << std::endl;
							std::cout << "miss_dist_value of lone trk to v1: " << X_i_sharedjet_lone_tk_vtx1_dist[i] << std::endl;
							std::cout << "miss_dist_error of lone trk to v1: " << X_i_sharedjet_lone_tk_vtx1_dist_err[i] << std::endl;
						}
					}

					if ((shift_unnorm_chi2_v0 < -50 || shift_unnorm_chi2_v1 < -50) && (nosharedjets_onlyX_v0.nTracks() > 0) && (nosharedjets_onlyX_v1.nTracks() > 0)) {
						std::cout << "MFVVertexer " << module_label << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << std::endl;
						std::cout << "shift in v0: " << shift_unnorm_chi2_v0 << std::endl;
						std::cout << "chi2 of v0: " << v0_chi2 * v0_ndof << std::endl;
						std::cout << "ndof of v0: " << v0_ndof << std::endl;
						for (unsigned int i = 0, ie = X_i_sharedjet_lone_tk_vtx0_dist.size(); i < ie; ++i) {
							std::cout << "sv0's " << i << "{1,1} shared jet" << std::endl;
							std::cout << "miss_dist_sig of lone trk to v0: " << X_i_sharedjet_lone_tk_vtx0_dist_sig[i] << std::endl;
							std::cout << "miss_dist_value of lone trk to v0: " << X_i_sharedjet_lone_tk_vtx0_dist[i] << std::endl;
							std::cout << "miss_dist_error of lone trk to v0: " << X_i_sharedjet_lone_tk_vtx0_dist_err[i] << std::endl;
						}
						std::cout << "shift in v1: " << shift_unnorm_chi2_v1 << std::endl;
						std::cout << "chi2 of v1: " << v1_chi2 * v1_ndof << std::endl;
						std::cout << "ndof of v1: " << v1_ndof << std::endl;
						for (unsigned int i = 0, ie = X_i_sharedjet_lone_tk_vtx1_dist.size(); i < ie; ++i) {
							std::cout << "sv1's " << i << "{1,1} shared jet" << std::endl;
							std::cout << "miss_dist_sig of lone trk to v1: " << X_i_sharedjet_lone_tk_vtx1_dist_sig[i] << std::endl;
							std::cout << "miss_dist_value of lone trk to v1: " << X_i_sharedjet_lone_tk_vtx1_dist[i] << std::endl;
							std::cout << "miss_dist_error of lone trk to v1: " << X_i_sharedjet_lone_tk_vtx1_dist_err[i] << std::endl;
						}
					}
					

					// case Xa
					if (sv0_total_track_which_idx.size() == 5 && sv1_total_track_which_idx.size() == 5) {
						h_qualify_most_5trk_track_vertices_Xa_nsharedjet->Fill(Xa_nsharedjets);
						h_2D_most_5trk_track_vertices_Xa_Deltachi2_SV0_SV1->Fill(shift_unnorm_chi2_v0, shift_unnorm_chi2_v1);
						h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xa->Fill(fabs(reco::deltaPhi(phi0, phi1)));
					}
					//case Xc
					else if (sv0_total_track_which_idx.size() > 5 && sv1_total_track_which_idx.size() > 5) {
						h_qualify_most_5trk_track_vertices_Xc_nsharedjet->Fill(Xc_nsharedjets);
						h_2D_most_5trk_track_vertices_Xc_Deltachi2_SV0_SV1->Fill(shift_unnorm_chi2_v0, shift_unnorm_chi2_v1);
						h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xc->Fill(fabs(reco::deltaPhi(phi0, phi1)));
					}
					//case Xb
					else {
						h_qualify_most_5trk_track_vertices_Xb_nsharedjet->Fill(Xb_nsharedjets);
						h_2D_most_5trk_track_vertices_Xb_Deltachi2_SV0_SV1->Fill(shift_unnorm_chi2_v0, shift_unnorm_chi2_v1);
						h_at_least_5trk_output1_shared_tracks_pair_vtx01_dPhi_Xb->Fill(fabs(reco::deltaPhi(phi0, phi1)));
					}

				}

				

				//------------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_sumpT_onlyY_v0_ttks;
				for (unsigned int i = 0, ie = sv0_sum_pT_only_Y_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_sum_pT_only_Y_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_sumpT_onlyY_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_sumpT_onlyY_v0;

				for (const TransientVertex& tv : kv_reco_dropin_nocut(nosharedjets_sumpT_onlyY_v0_ttks))
					nosharedjets_sumpT_onlyY_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_sumpT_onlyY_v1_ttks;
				for (unsigned int i = 0, ie = sv1_sum_pT_only_Y_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_sum_pT_only_Y_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_sumpT_onlyY_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_sumpT_onlyY_v1;

				for (const TransientVertex& tv : kv_reco_dropin_nocut(nosharedjets_sumpT_onlyY_v1_ttks))
					nosharedjets_sumpT_onlyY_v1 = reco::Vertex(tv);


				double nosharedjets_sumpT_onlyY_v0_chi2 = nosharedjets_sumpT_onlyY_v0.normalizedChi2();
				double nosharedjets_sumpT_onlyY_v0_ndof = nosharedjets_sumpT_onlyY_v0.ndof();

				double nosharedjets_sumpT_onlyY_v1_chi2 = nosharedjets_sumpT_onlyY_v1.normalizedChi2();
				double nosharedjets_sumpT_onlyY_v1_ndof = nosharedjets_sumpT_onlyY_v1.ndof();

				shift_unnorm_chi2_v0 = (nosharedjets_sumpT_onlyY_v0_chi2 * nosharedjets_sumpT_onlyY_v0_ndof) - (v0_chi2 * v0_ndof);
				shift_unnorm_chi2_v1 = (nosharedjets_sumpT_onlyY_v1_chi2 * nosharedjets_sumpT_onlyY_v1_ndof) - (v1_chi2 * v1_ndof);
				
				
				
				if (sv0_sum_pT_only_Y_track_which_idx.size() < sv0_total_track_which_idx.size()) {
					
					//std::cout << "{SUM PT}" << std::endl;
					//std::cout << "v0 ntrack: " << sv0_total_track_which_idx.size() << " # of shared jet: " << nsharedjets << " norm-chi2: " << v0_chi2 << " ndof: " << v0_ndof << std::endl;
					//std::cout << "after removing only {1,n>1} shared jets by sum pY" << std::endl;
					//std::cout << "new v0 ntrack: " << sv0_sum_pT_only_Y_track_which_idx.size() << " new v1 ntrack: " << sv1_sum_pT_only_Y_track_which_idx.size() << " new norm-chi2: " << nosharedjets_sumpT_onlyY_v0_chi2 << " new ndof: " << nosharedjets_sumpT_onlyY_v0_ndof << std::endl;
					//std::cout << "new v0 non-norm chi2 ( " << nosharedjets_sumpT_onlyY_v0_chi2 * nosharedjets_sumpT_onlyY_v0_ndof << " ) - v0 non-norm chi2 ( " << v0_chi2 * v0_ndof << " ) = " << shift_unnorm_chi2_v0 << std::endl;
					h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_sumpT_Y->Fill(shift_unnorm_chi2_v0);
					h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_sumpT_Y->Fill(v0_chi2* v0_ndof);
					h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_sumpT_Y->Fill(nosharedjets_sumpT_onlyY_v0_chi2* nosharedjets_sumpT_onlyY_v0_ndof);

					if (nosharedjets_sumpT_onlyY_v0.nTracks() < 5 || nosharedjets_sumpT_onlyY_v0_chi2 > 5) {	 //PK: tbs<->bkg
						nsv_sumpT -= 1;
						nsv_sumpT_onlyY -= 1;
						sv0_sumpTandX -= 1;
					}

					

				}

				if (sv1_sum_pT_only_Y_track_which_idx.size() < sv1_total_track_which_idx.size()) {
	
					h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_sumpT_Y->Fill(shift_unnorm_chi2_v1);
					h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_sumpT_Y->Fill(v1_chi2* v1_ndof);
					h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_sumpT_Y->Fill(nosharedjets_sumpT_onlyY_v1_chi2* nosharedjets_sumpT_onlyY_v1_ndof);

					if (nosharedjets_sumpT_onlyY_v1.nTracks() < 5 || nosharedjets_sumpT_onlyY_v1_chi2 > 5) {	//PK: tbs<->bkg
						nsv_sumpT -= 1;
						nsv_sumpT_onlyY -= 1;
						sv1_sumpTandX -= 1;
					}
				}

				sv0_sumpTandX = 1 - (sv0_sumpTandX <= 0);
				sv1_sumpTandX = 1 - (sv1_sumpTandX <= 0);
				if (nsv_sumpTandX == 2) {
					h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_YandX->Fill(sv0_sumpTandX + sv1_sumpTandX);
				}
				if (nsv_sumpT >= 0) {  
					h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_sumpT_Y->Fill(nsv_sumpT);
				}
				if (nsv_sumpT_onlyY >= 0) {
					h_qualify_most_track_vertices_Y_nsharedjet->Fill(Y_nsharedjets);
					h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_sumpT_Y->Fill(nsv_sumpT_onlyY);
				}

				//------------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_shared_ntrack_onlyY_v0_ttks;
				for (unsigned int i = 0, ie = sv0_shared_ntrack_only_Y_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_shared_ntrack_only_Y_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_shared_ntrack_onlyY_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_shared_ntrack_onlyY_v0;

				for (const TransientVertex& tv : kv_reco_dropin_nocut(nosharedjets_shared_ntrack_onlyY_v0_ttks))
					nosharedjets_shared_ntrack_onlyY_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_shared_ntrack_onlyY_v1_ttks;
				for (unsigned int i = 0, ie = sv1_shared_ntrack_only_Y_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_shared_ntrack_only_Y_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_shared_ntrack_onlyY_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_shared_ntrack_onlyY_v1;

				for (const TransientVertex& tv : kv_reco_dropin_nocut(nosharedjets_shared_ntrack_onlyY_v1_ttks))
					nosharedjets_shared_ntrack_onlyY_v1 = reco::Vertex(tv);


				double nosharedjets_shared_ntrack_onlyY_v0_chi2 = nosharedjets_shared_ntrack_onlyY_v0.normalizedChi2();
				double nosharedjets_shared_ntrack_onlyY_v0_ndof = nosharedjets_shared_ntrack_onlyY_v0.ndof();

				double nosharedjets_shared_ntrack_onlyY_v1_chi2 = nosharedjets_shared_ntrack_onlyY_v1.normalizedChi2();
				double nosharedjets_shared_ntrack_onlyY_v1_ndof = nosharedjets_shared_ntrack_onlyY_v1.ndof();

				shift_unnorm_chi2_v0 = (nosharedjets_shared_ntrack_onlyY_v0_chi2 * nosharedjets_shared_ntrack_onlyY_v0_ndof) - (v0_chi2 * v0_ndof);
				shift_unnorm_chi2_v1 = (nosharedjets_shared_ntrack_onlyY_v1_chi2 * nosharedjets_shared_ntrack_onlyY_v1_ndof) - (v1_chi2 * v1_ndof);

				
				
				if (sv0_shared_ntrack_only_Y_track_which_idx.size() < sv0_total_track_which_idx.size()) {
                                        //std::cout << "{SHARED NTRACK}" << std::endl;
					//std::cout << "v0 ntrack: " << sv0_total_track_which_idx.size() << " # of shared jet: " << nsharedjets << " norm-chi2: " << v0_chi2 << " ndof: " << v0_ndof << std::endl;
					//std::cout << "after removing only {1,n>1} shared jets by one shared ntrack" << std::endl;
					//std::cout << "new v0 ntrack: " << sv0_shared_ntrack_only_Y_track_which_idx.size() << " new v1 ntrack: " << sv1_shared_ntrack_only_Y_track_which_idx.size() << " new norm-chi2: " << nosharedjets_shared_ntrack_onlyY_v0_chi2 << " new ndof: " << nosharedjets_shared_ntrack_onlyY_v0_ndof << std::endl;
					//std::cout << "new v0 non-norm chi2 ( " << nosharedjets_shared_ntrack_onlyY_v0_chi2 * nosharedjets_shared_ntrack_onlyY_v0_ndof << " ) - v0 non-norm chi2 ( " << v0_chi2 * v0_ndof << " ) = " << shift_unnorm_chi2_v0 << std::endl;
					h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_shared_ntrack_Y->Fill(shift_unnorm_chi2_v0);
					h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_shared_ntrack_Y->Fill(v0_chi2*v0_ndof);
					h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_shared_ntrack_Y->Fill(nosharedjets_shared_ntrack_onlyY_v0_chi2* nosharedjets_shared_ntrack_onlyY_v0_ndof);

					if (nosharedjets_shared_ntrack_onlyY_v0.nTracks() < 5 || nosharedjets_shared_ntrack_onlyY_v0_chi2 > 5) {	 //PK: tbs<->bkg 
						nsv_lonetrk -= 1;
						nsv_lonetrk_onlyY -= 1;
						sv0_lonetrkandX -= 1;
					}
					
				}

				if (sv1_shared_ntrack_only_Y_track_which_idx.size() < sv1_total_track_which_idx.size()) {
					h_at_least_5trk_output1_shared_tracks_pair_shift_unnorm_chi2_by_shared_ntrack_Y->Fill(shift_unnorm_chi2_v1);
					h_at_least_5trk_output1_shared_tracks_pair_old_unnorm_chi2_by_shared_ntrack_Y->Fill(v1_chi2*v1_ndof);
					h_at_least_5trk_output1_shared_tracks_pair_new_unnorm_chi2_by_shared_ntrack_Y->Fill(nosharedjets_shared_ntrack_onlyY_v1_chi2* nosharedjets_shared_ntrack_onlyY_v1_ndof);

					if (nosharedjets_shared_ntrack_onlyY_v1.nTracks() < 5 || nosharedjets_shared_ntrack_onlyY_v1_chi2 > 5) {	 //PK: tbs<->bkg
						nsv_lonetrk -= 1;
						nsv_lonetrk_onlyY -= 1;
						sv1_lonetrkandX -= 1;
					}

				}

				sv0_lonetrkandX = 1 - (sv0_lonetrkandX <= 0);
				sv1_lonetrkandX = 1 - (sv1_lonetrkandX <= 0);
				if (nsv_lonetrkandX == 2) {
					h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_YandX->Fill(sv0_lonetrkandX + sv1_lonetrkandX);
				}
				if (nsv_lonetrk >= 0) {	
					h_at_least_5trk_output1_shared_tracks_pair_XYZ_nsv_by_shared_ntrack_Y->Fill(nsv_lonetrk);
				}
				if (nsv_lonetrk_onlyY >= 0) {
					h_at_least_5trk_output1_shared_tracks_pair_Y_nsv_by_shared_ntrack_Y->Fill(nsv_lonetrk_onlyY);
				}

				//------------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_med_dist_sig_v0_ttks;
				for (unsigned int i = 0, ie = sv0_median_tk_vtx_dist_sig_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_median_tk_vtx_dist_sig_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_med_dist_sig_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_med_dist_sig_v0;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_sig_v0_ttks))
					nosharedjets_med_dist_sig_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_med_dist_sig_v1_ttks;
				for (unsigned int i = 0, ie = sv1_median_tk_vtx_dist_sig_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_median_tk_vtx_dist_sig_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_med_dist_sig_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_med_dist_sig_v1;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_sig_v1_ttks))
					nosharedjets_med_dist_sig_v1 = reco::Vertex(tv);

				dBV0_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_sig_v0, fake_bs_vtx);
				dBV0 = dBV0_Meas1D.value();
				bs2derr0 = dBV0_Meas1D.error();

				dBV1_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_sig_v1, fake_bs_vtx);
				dBV1 = dBV1_Meas1D.value();
				bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist_sig_noshare_med_dist = vertex_dist(nosharedjets_med_dist_sig_v0, nosharedjets_med_dist_sig_v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && nosharedjets_med_dist_sig_v0.nTracks() >= 5 && nosharedjets_med_dist_sig_v1.nTracks() >= 5)
					h_qualify_by_median_tkvtxdistsig_svdist2d_three_bins->Fill(v_dist_sig_noshare_med_dist.value());

				//------------------------------------------------------------

				std::vector<reco::TransientTrack> nosharedjets_med_dist_sig_only_dR_v0_ttks;
				for (unsigned int i = 0, ie = sv0_median_tk_vtx_dist_sig_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_median_tk_vtx_dist_sig_only_dR_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_med_dist_sig_only_dR_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_med_dist_sig_only_dR_v0;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_sig_only_dR_v0_ttks))
					nosharedjets_med_dist_sig_only_dR_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_med_dist_sig_only_dR_v1_ttks;
				for (unsigned int i = 0, ie = sv1_median_tk_vtx_dist_sig_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_median_tk_vtx_dist_sig_only_dR_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_med_dist_sig_only_dR_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_med_dist_sig_only_dR_v1;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_sig_only_dR_v1_ttks))
					nosharedjets_med_dist_sig_only_dR_v1 = reco::Vertex(tv);

				dBV0_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_sig_only_dR_v0, fake_bs_vtx);
				dBV0 = dBV0_Meas1D.value();
				bs2derr0 = dBV0_Meas1D.error();

				dBV1_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_sig_only_dR_v1, fake_bs_vtx);
				dBV1 = dBV1_Meas1D.value();
				bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist_sig_only_dR_noshare_med_dist = vertex_dist(nosharedjets_med_dist_sig_only_dR_v0, nosharedjets_med_dist_sig_only_dR_v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && nosharedjets_med_dist_sig_only_dR_v0.nTracks() >= 5 && nosharedjets_med_dist_sig_only_dR_v1.nTracks() >= 5)
					h_qualify_only_small_dR_by_median_tkvtxdistsig_svdist2d_three_bins->Fill(v_dist_sig_only_dR_noshare_med_dist.value());

				//---------------------------------------------------------------


				std::vector<reco::TransientTrack> nosharedjets_med_dist_2sig_only_dR_v0_ttks;
				for (unsigned int i = 0, ie = sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_median_tk_vtx_dist_2sig_only_dR_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					nosharedjets_med_dist_2sig_only_dR_v0_ttks.push_back(v0_track);
				}

				reco::Vertex nosharedjets_med_dist_2sig_only_dR_v0;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_2sig_only_dR_v0_ttks))
					nosharedjets_med_dist_2sig_only_dR_v0 = reco::Vertex(tv);

				std::vector<reco::TransientTrack> nosharedjets_med_dist_2sig_only_dR_v1_ttks;
				for (unsigned int i = 0, ie = sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_median_tk_vtx_dist_2sig_only_dR_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					nosharedjets_med_dist_2sig_only_dR_v1_ttks.push_back(v1_track);
				}

				reco::Vertex nosharedjets_med_dist_2sig_only_dR_v1;

				for (const TransientVertex& tv : kv_reco_dropin(nosharedjets_med_dist_2sig_only_dR_v1_ttks))
					nosharedjets_med_dist_2sig_only_dR_v1 = reco::Vertex(tv);

				dBV0_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_2sig_only_dR_v0, fake_bs_vtx);
				dBV0 = dBV0_Meas1D.value();
				bs2derr0 = dBV0_Meas1D.error();

				dBV1_Meas1D = vertex_dist_2d.distance(nosharedjets_med_dist_2sig_only_dR_v1, fake_bs_vtx);
				dBV1 = dBV1_Meas1D.value();
				bs2derr1 = dBV1_Meas1D.error();
				Measurement1D v_dist_2sig_only_dR_noshare_med_dist = vertex_dist(nosharedjets_med_dist_2sig_only_dR_v0, nosharedjets_med_dist_2sig_only_dR_v1);

				if (dBV1 > 0.0100 && dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && nosharedjets_med_dist_2sig_only_dR_v0.nTracks() >= 5 && nosharedjets_med_dist_2sig_only_dR_v1.nTracks() >= 5)
					h_qualify_only_small_dR_by_2sigma_median_tkvtxdistsig_svdist2d_three_bins->Fill(v_dist_2sig_only_dR_noshare_med_dist.value());



	


				
                                //v0 = nosharedjets_med_dist_2sig_only_dR_v0;
				                //v1 = nosharedjets_med_dist_2sig_only_dR_v1;
                                //v0 = nosharedjets_v0;
                                //v1 = nosharedjets_v1;
                                //v0 = nosharedjets_only_dR_v0;
                                //v1 = nosharedjets_only_dR_v1;
                                //std::cout << "after shared-jet mitigation opt3shj7chi5: " << std::endl;
                                //std::cout << "vtx0 ntracks: " << v0.nTracks() << std::endl;
                                //std::cout << "vtx1 ntracks: " << v1.nTracks() << std::endl;

			}

			else {
				if (dBV1 > 0.0100&& dBV0 > 0.0100 && bs2derr0 < 0.0025 && bs2derr1 < 0.0025 && v0.nTracks() >= 5 && v1.nTracks() >= 5){
				track_vec tks_v0 = vertex_track_vec(v0);
				std::vector<int> sv0_total_track_which_idx = sv_total_track_which_idx[first_ntracks_vtxidx];
				std::vector<reco::TransientTrack> good_v0_ttks;
				for (unsigned int i = 1, ie = sv0_total_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v0_track;
					int idx = sv0_total_track_which_idx[i] - 1;
					v0_track = tt_builder->build(tks_v0[idx]);
					good_v0_ttks.push_back(v0_track);
				}

				reco::Vertex good_v0;

				for (const TransientVertex& tv : kv_reco_dropin(good_v0_ttks))
					good_v0 = reco::Vertex(tv);

				track_vec tks_v1 = vertex_track_vec(v1);
				std::vector<int> sv1_total_track_which_idx = sv_total_track_which_idx[second_ntracks_vtxidx];
				std::vector<reco::TransientTrack> good_v1_ttks;
				for (unsigned int i = 0, ie = sv1_total_track_which_idx.size(); i < ie; ++i) {
					reco::TransientTrack v1_track;
					int idx = sv1_total_track_which_idx[i] - 1;
					v1_track = tt_builder->build(tks_v1[idx]);
					good_v1_ttks.push_back(v1_track);
				}

				reco::Vertex good_v1;

				for (const TransientVertex& tv : kv_reco_dropin(good_v1_ttks))
					good_v1 = reco::Vertex(tv);

				double v0_chi2 = v0.normalizedChi2();
				double v0_ndof = v0.ndof();

				double v1_chi2 = v1.normalizedChi2();
				double v1_ndof = v1.ndof();

				double good_v0_chi2 = good_v0.normalizedChi2();
				double good_v0_ndof = good_v0.ndof();

				double good_v1_chi2 = good_v1.normalizedChi2();
				double good_v1_ndof = good_v1.ndof();

				double shift_unnorm_chi2_v0 = (good_v0_chi2 * good_v0_ndof) - (v0_chi2 * v0_ndof);
				double shift_unnorm_chi2_v1 = (good_v1_chi2 * good_v1_ndof) - (v1_chi2 * v1_ndof);

				h_at_least_5trk_output1_no_shared_tracks_pair_shift_unnorm_chi2->Fill(shift_unnorm_chi2_v0);
				h_at_least_5trk_output1_no_shared_tracks_pair_shift_unnorm_chi2->Fill(shift_unnorm_chi2_v1);
				h_2D_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2->Fill(v0.nTracks(), v0_chi2* v0_ndof);
				h_2D_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2->Fill(v1.nTracks(), v1_chi2* v1_ndof);
				//h_2Dpfx_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2->Fill(v0.nTracks(), v0_chi2* v0_ndof);
				//h_2Dpfx_at_least_5trk_output1_no_shared_tracks_pair_ntrack_unnorm_chi2->Fill(v1.nTracks(), v1_chi2* v1_ndof);
			}

            }

		}
	}

	if (histos_output2) {
		std::map<reco::TrackRef, int> track_use;
		int count_5trk_vertices = 0;
                //std::cout << "yes histos_output2" << std::endl;
		const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

		for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
			reco::Vertex& v = vertices->at(i);
			const int ntracks = v.nTracks();
			const double vchi2 = v.normalizedChi2();
			const double vndof = v.ndof();
			const double vx = v.position().x() - bsx;
			const double vy = v.position().y() - bsy;
			const double vz = v.position().z() - bsz;
			const double rho = mag(vx, vy);
			const double phi = atan2(vy, vx);
			const double r = mag(vx, vy, vz);
			for (const auto& r : vertex_track_set(v)) {
				if (track_use.find(r) != track_use.end())
					track_use[r] += 1;
				else
					track_use[r] = 1;
			}

			h_output2_vertex_ntracks->Fill(ntracks);
			if (ntracks >= 5) {
				count_5trk_vertices++;
				Measurement1D dBV_Meas1D = vertex_dist_2d.distance(v, fake_bs_vtx);
				double dBV = dBV_Meas1D.value();
				double bs2derr = dBV_Meas1D.error();
				h_at_least_5trk_output2_vertex_dBV->Fill(dBV);
				h_at_least_5trk_output2_vertex_bs2derr->Fill(bs2derr);

			}

			for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
				h_output1_vertex_track_weights->Fill(v.trackWeight(*it));

				reco::TransientTrack seed_track;
				seed_track = tt_builder->build(*it.operator*());
				std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v);
				h_output2_vertex_tkvtxdist->Fill(tk_vtx_dist.second.value());
				h_output2_vertex_tkvtxdisterr->Fill(tk_vtx_dist.second.error());
				h_output2_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
			}

			h_output2_vertex_chi2->Fill(vchi2);
			h_output2_vertex_ndof->Fill(vndof);
			h_output2_vertex_x->Fill(vx);
			h_output2_vertex_y->Fill(vy);
			h_output2_vertex_rho->Fill(rho);
			h_output2_vertex_phi->Fill(phi);
			h_output2_vertex_z->Fill(vz);
			h_output2_vertex_r->Fill(r);

			for (size_t j = i + 1, je = vertices->size(); j < je; ++j) {
				const reco::Vertex& vj = vertices->at(j);
				const double vjx = vj.position().x() - bsx;
				const double vjy = vj.position().y() - bsy;
				const double phij = atan2(vjy, vjx);
				Measurement1D v_dist = vertex_dist(vj, v);
				h_output2_vertex_paird2d->Fill(mag(vx - vjx, vy - vjy));
				h_output2_vertex_paird2dsig->Fill(v_dist.significance());
				h_output2_vertex_pairdphi->Fill(fabs(reco::deltaPhi(phi, phij)));
			}

		}

		h_n_at_least_5trk_output2_vertices->Fill(count_5trk_vertices);

=======
		for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
			track_vec tks = vertex_track_vec(*v[0]);
			size_t ntks = tks.size();
			vertex_ntracks.push_back(ntks);
		}
        
		for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
			std::vector<int> track_which_idx;
			std::vector<int> track_which_jet;
			track_vec tks = vertex_track_vec(*v[0]);
			
			int i = 0;
			for (const reco::TrackRef& itk : tks) {
				i++;
				for (size_t j = 0; j < jets->size(); ++j) {
				       int jet_index = static_cast<int>(j);	
                       if (match_track_jet(*itk, (*jets)[j], *jets,jet_index)) {
							track_which_idx.push_back(i);  
							track_which_jet.push_back(j);
					   if (verbose)
						   printf(" track %u matched with a jet %lu \n", tks[i].key(), j);
					   }

				}
            }
			sv_track_which_idx.push_back(track_which_idx);
			sv_track_which_jet.push_back(track_which_jet);

		              
	}
	
	// end of shared-jet track removal 
       

	
>>>>>>> 11c82df9b2453b3eb467a0cb9809afa6aa5b7806
	}

  //////////////////////////////////////////////////////////////////////
  // Put the output.
  //////////////////////////////////////////////////////////////////////

  finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
}
bool MFVVertexer::match_track_jet(const reco::Track& tk, const pat::Jet& matchjet, const pat::JetCollection& jets, const int& idx) {
	//if (reco::deltaR2(tk, jet)>0.16) return false;
	
        if (verbose) {
		std::cout << "jet track matching..." << std::endl;
		std::cout << "  target track pt " << tk.pt() << " eta " << tk.eta() << " phi " << tk.phi() << std::endl;
	}
	
	
		double match_thres = 1.3;                                                                                                                                                           int jet_index = 255;                                                                                                                                                                for (size_t j = 0; j < jets.size(); ++j) {
                   for (size_t idau = 0, idaue = jets[j].numberOfDaughters(); idau < idaue; ++idau) {               	        	
                        const reco::Candidate* dau = jets[j].daughter(idau);
			if (dau->charge() == 0)
				continue;
			const reco::Track * jtk = 0;
			const reco::PFCandidate * pf = dynamic_cast<const reco::PFCandidate*>(dau);
			if (pf) {
				const reco::TrackRef& r = pf->trackRef();
				if (r.isNonnull())
					jtk = &*r;
			}
			else {
				const pat::PackedCandidate* pk = dynamic_cast<const pat::PackedCandidate*>(dau);
				if (pk && pk->charge() && pk->hasTrackDetails())
					jtk = &pk->pseudoTrack();
			}
			if (jtk) {
			     double a = fabs(tk.pt() - fabs(jtk->charge() * jtk->pt())) + 1;
			     double b = fabs(tk.eta() - jtk->eta()) + 1;
			     double c = fabs(tk.phi() - jtk->phi()) + 1;
			     if (verbose)
				std::cout << "  jet track pt " << jtk->pt() << " eta " << jtk->eta() << " phi " << jtk->phi() << " match abc " << a * b * c << std::endl;
			     if (a * b * c < match_thres) {
				match_thres = a * b * c;
			        jet_index = j; 
			     }
                        }
                    }
                 }
                 if (jet_index == idx){
                   return true;
                 }
	

	return false;
}

DEFINE_FWK_MODULE(MFVVertexer);
