/*
 * This program constructs the background template from one-vertex events.
 * Set the input parameters at the top of the method construct_dvvc().
 * Set which combinations of input parameters to run in main().
 * To run: compile with the Makefile (make); execute (./2v_from_jets.exe); delete the .exe (make clean).
 *
 * Here are details on each of the input parameters:
 * which filepath?
 *  - Provide the filepath to the MiniTree directory.
 *
 * which samples?
 *  - The MC and data samples and weights are set in static arrays; edit nbkg if necessary.
 *  - For the 2017 MC samples the weights calculated assume an integrated luminosity of 41.53 fb^-1 and the number of events run on for each sample:
samples -i <<EOF
for sample in qcd_samples_2017 + ttbar_samples_2017:
    nevents = sample.nevents('/uscms_data/d2/tucker/crab_dirs/MiniTreeV22m/%s.root' % sample.name)
    print '%20s %6.1f %9d %10.3g' % (sample.name, sample.xsec, nevents, 41530.*sample.xsec/nevents)
EOF
 *  - For the background template only the relative weights are relevant because we only construct the shape; the normalization comes from the fit.
 *  - Todo: MC weights and data samples for 2018.
 *  - If the samples array is modified, ibkg_begin and ibkg_end should also be modified.
 *
 * which ntracks?
 *  - This sets the treepath and shouldn't need to be modified.  (For Ntk3or4 two-vertex event is considered to be 4-track x 3-track if ntk0==4 and ntk1==3.)
 *
 * deltaphi input
 *  - Run fit_jetpairdphi.py to get the values of dphi_pdf_c, dphi_pdf_a.
 *  - Todo: update for 2017 (the current values are from 2015+2016 data).
 *
 * efficiency input
 *  - Run vertexer_eff.py to get the .root file with the efficiency curve.
 *  - vpeffs_version refers to the version of VertexerPairEffs.
 */

#include <cstdlib>
#include <math.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <string>
//#include <Python.h>
#include "TCanvas.h"
#include "TF1.h"
#include "TFile.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TLegend.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TRatioPlot.h"
#include "TStyle.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h" //Alec added from here
#include "TH2.h"
#include "TMath.h"
#include <math.h>
#include "JMTucker/MFVNeutralino/interface/NtupleFiller.h" //fails without lboost added to the Makefile
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"
#include "TrackingTools/GeomPropagators/interface/AnalyticalTrajectoryExtrapolatorToLine.h"
#include "TrackingTools/GeomPropagators/interface/AnalyticalImpactPointExtrapolator.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h" //fails without lboost added to the Makefile
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/UniformEngine/interface/UniformMagneticField.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexerPairEff.h"
#include "JMTucker/MFVNeutralino/interface/VertexerParams.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include <TRandom3.h> //Alec added to here

int dvv_nbins = 100;
double dvv_bin_width = 0.01;
std::vector<TString> cb_cbbar_vector = {};
const std::string ulversion = "ULV30Lepm"; //Use for Lepton triggered samples
//const std::string ulversion = "ULV30BvetoLHTm"; //Use for bjet triggered samples
bool use_signal = false;
bool use_dvv3D = true;
bool c1v_vertexer = true;

struct ConstructDvvcParameters {
  int ibkg_begin_;
  int ibkg_end_;
  bool is_mc_;
  bool only_20pc_;
  bool inject_signal_;
  std::string year_;
  int ntracks_;
  int bquarks_;
  int btags_;
  bool vary_dphi_;
  bool clearing_from_eff_;
  bool vary_eff_;
  int min_npu_;
  int max_npu_;

  ConstructDvvcParameters()
    : ibkg_begin_(-999),
      ibkg_end_(-999),
      is_mc_(false),
      only_20pc_(true),
      inject_signal_(false),
      year_("run2"), //change depending on year run
      ntracks_(5),
      bquarks_(-1),
      btags_(-1),
      vary_dphi_(false),
      clearing_from_eff_(true),
      //clearing_from_eff_(true),
      vary_eff_(false),
      min_npu_(0),
      max_npu_(255)
  {
  }

  int ibkg_begin() const { return ibkg_begin_; }
  int ibkg_end() const { return ibkg_end_; }
  bool is_mc() const { return is_mc_; }
  bool only_20pc() const { return only_20pc_; }
  bool inject_signal() const { return inject_signal_; }
  std::string year() const { return year_; }
  int ntracks() const { return ntracks_; }
  int bquarks() const { return bquarks_; }
  int btags() const { return btags_; }
  bool vary_dphi() const { return vary_dphi_; }
  bool clearing_from_eff() const { return clearing_from_eff_; }
  bool vary_eff() const { return vary_eff_; }
  int min_npu() const { return min_npu_; }
  int max_npu() const { return max_npu_; }

  ConstructDvvcParameters ibkg_begin(bool x)        { ConstructDvvcParameters y(*this); y.ibkg_begin_        = x; return y; }
  ConstructDvvcParameters ibkg_end(bool x)          { ConstructDvvcParameters y(*this); y.ibkg_end_          = x; return y; }
  ConstructDvvcParameters is_mc(bool x)             { ConstructDvvcParameters y(*this); y.is_mc_             = x; return y; }
  ConstructDvvcParameters only_20pc(bool x)         { ConstructDvvcParameters y(*this); y.only_20pc_         = x; return y; }
  ConstructDvvcParameters inject_signal(bool x)     { ConstructDvvcParameters y(*this); y.inject_signal_     = x; return y; }
  ConstructDvvcParameters year(std::string x)       { ConstructDvvcParameters y(*this); y.year_              = x; return y; }
  ConstructDvvcParameters ntracks(int x)            { ConstructDvvcParameters y(*this); y.ntracks_           = x; return y; }
  ConstructDvvcParameters bquarks(int x)            { ConstructDvvcParameters y(*this); y.bquarks_           = x; return y; }
  ConstructDvvcParameters btags(int x)              { ConstructDvvcParameters y(*this); y.btags_             = x; return y; }
  ConstructDvvcParameters vary_dphi(bool x)         { ConstructDvvcParameters y(*this); y.vary_dphi_         = x; return y; }
  ConstructDvvcParameters clearing_from_eff(bool x) { ConstructDvvcParameters y(*this); y.clearing_from_eff_ = x; return y; }
  ConstructDvvcParameters vary_eff(bool x)          { ConstructDvvcParameters y(*this); y.vary_eff_          = x; return y; }
  ConstructDvvcParameters min_npu(int x)            { ConstructDvvcParameters y(*this); y.min_npu_           = x; return y; }
  ConstructDvvcParameters max_npu(int x)            { ConstructDvvcParameters y(*this); y.max_npu_           = x; return y; }

  void print() const {
     printf("ibkg_begin-end = %d-%d, is_mc = %d, only_20pc = %d, inject_signal = %d, year = %s, ntracks = %d, bquarks = %d, btags = %d, vary_dphi = %d, clearing_from_eff = %d, vary_eff = %d, min_npu = %d, max_npu = %d", ibkg_begin(), ibkg_end(), is_mc(), only_20pc(), inject_signal(), year_.c_str(), ntracks(), bquarks(), btags(), vary_dphi(), clearing_from_eff(), vary_eff(), min_npu(), max_npu());
  }

  //This is a coarse parameterization of the vertex pair reconstruction efficiency after vertex refinement step, this needs to be used in conjunction with vertexer_eff.py outputs
  float extra_eff_2d(float dvv) {
    if (dvv < 0.08) return 0.60;
    if (dvv > 0.20) return 0.84;
    else return (0.213 + 6.00*dvv - 14.4*dvv*dvv);
  }

};

std::string callPythonAndGetOutput(const std::string& argument) { //Alec added this command to call python commands that find the sample scale factor
  //std::string command = "python /uscms/homes/a/alecduqu/mfv_ScaleFactors/src/JMTucker/MFVNeutralino/test/One2Two/2v_from_jets_new.py " + argument + " " + ulversion;
  std::string command = "python 2v_from_jets_new.py " + argument + " " + ulversion;
  //std::cout << command << std::endl;
  std::array<char, 128> buffer;
  std::string result;
  // Open a pipe to the command
  FILE* pipe = popen(command.c_str(), "r");
  if (!pipe) throw std::runtime_error("popen() failed!");
  try {
    // Read the output line by line
    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
      result += buffer.data();
    }
  } catch (...) {
    pclose(pipe);
    throw;
  }
  pclose(pipe);
  return result;
}

//functions for the revertexing of constructed events, only used if c1v_vertexer = true
typedef std::set<reco::TrackRef> track_set;
typedef std::vector<reco::TrackRef> track_vec;
const int n_tracks_per_seed_vertex = 2; //This is what is defined in Vertexer_cfi.py
const double max_seed_vertex_chi2 = 5;
const bool order_seed_vertex = false;
const double merge_shared_dist = -1;
const double max_track_vertex_dist = -1;
const double max_track_vertex_sig = 5;
const double min_track_vertex_sig_to_remove = 1.5;
const bool remove_one_track_at_a_time = true;
const bool resolve_split_vertices_tight = true;
const bool investigate_merged_vertices = false;
const bool use_2d_vertex_dist = false;
const bool use_2d_track_dist = false;
const double merge_shared_sig = 4;

VertexDistanceXY vertex_dist_2d;
VertexDistance3D vertex_dist_3d;
std::unique_ptr<KalmanVertexFitter> kv_reco;


//bool is_track_subset(const track_set & a, const track_set & b) const { //Alec had to remove const here
bool is_track_subset(const track_set & a, const track_set & b) {
  bool is_subset = true;
  const track_set& smaller = a.size() <= b.size() ? a : b;
  const track_set& bigger = a.size() <= b.size() ? b : a;

  for (auto t : smaller)
    if (bigger.count(t) < 1) {
      is_subset = false;
      break;
    }

  return is_subset;
}

//track_set vertex_track_set(const reco::Vertex & v, const double min_weight = mfv::track_vertex_weight_min) const { //Alec had to remove const here
track_set vertex_track_set(const reco::Vertex & v, const double min_weight = mfv::track_vertex_weight_min) {
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

//track_vec vertex_track_vec(const reco::Vertex & v, const double min_weight = mfv::track_vertex_weight_min) const { //Alec had to remove const here
track_vec vertex_track_vec(const reco::Vertex & v, const double min_weight = mfv::track_vertex_weight_min) {
  track_set s = vertex_track_set(v, min_weight);
  return track_vec(s.begin(), s.end());
}

//Measurement1D vertex_dist(const reco::Vertex & v0, const reco::Vertex & v1) const { //Alec had to remove const here 
Measurement1D vertex_dist(const reco::Vertex & v0, const reco::Vertex & v1) {
  if (use_2d_vertex_dist)
    return vertex_dist_2d.distance(v0, v1);
  else
    return vertex_dist_3d.distance(v0, v1);
}

//std::pair<bool, Measurement1D> track_dist(const reco::TransientTrack & t, const reco::Vertex & v) const { //Alec had to remove const here
std::pair<bool, Measurement1D> track_dist(const reco::TransientTrack & t, const reco::Vertex & v) {
  if (use_2d_track_dist)
    return IPTools::absoluteTransverseImpactParameter(t, v);
  else
    return IPTools::absoluteImpactParameter3D(t, v);
}


//std::pair<bool, Measurement1D> track_dist2d(const reco::TransientTrack & t, const reco::Vertex & v) const { //Alec had to remove const here 
std::pair<bool, Measurement1D> track_dist2d(const reco::TransientTrack & t, const reco::Vertex & v) { 
  return IPTools::absoluteTransverseImpactParameter(t, v);
}

//VertexDistanceXY vertex_dist_2d;
//VertexDistance3D vertex_dist_3d;
//std::unique_ptr<KalmanVertexFitter> kv_reco;

std::vector<TransientVertex> kv_reco_dropin(std::vector<reco::TransientTrack>& ttks, double chi2=5) {
  if (ttks.size() < 2)
    return std::vector<TransientVertex>();
  std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
  //std::cout << "fitted vertex chi2/dof: " << v[0].normalisedChiSquared() << std::endl;
  if (v[0].normalisedChiSquared() > chi2) //15
    return std::vector<TransientVertex>();
  return v;
}

std::vector<TransientVertex> kv_reco_dropin_nocut(std::vector<reco::TransientTrack> & ttks) {
  if (ttks.size() < 2)
    return std::vector<TransientVertex>();
  std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
  return v;
}

struct order_seed_vtx_pt {
  int operator()(const reco::Vertex& a, const reco::Vertex& b) {
    return a.p4().pt() > b.p4().pt();
  };
};

void finish(reco::Vertex::Point bs_pos, double bssigma_x, double bssigma_y, double bssigma_z, const std::vector<reco::TransientTrack>& seed_tracks, std::unique_ptr<reco::VertexCollection> vertices, std::unique_ptr<VertexerPairEffs> vpeffs, const std::vector<std::pair<track_set, track_set>>& vpeffs_tracks) { //only used if we are revertexing the constructed events
  std::unique_ptr<reco::TrackCollection> tracks_seed      (new reco::TrackCollection);
  std::unique_ptr<reco::TrackCollection> tracks_missseed (new reco::TrackCollection);
  std::unique_ptr<reco::TrackCollection> tracks_all(new reco::TrackCollection);
  std::unique_ptr<reco::TrackCollection> tracks_inVertices(new reco::TrackCollection);

  std::map<std::pair<unsigned, unsigned>, unsigned char> seed_track_ref_map;
  unsigned char itk = 0;
  for (const reco::TransientTrack& ttk : seed_tracks) {
    tracks_seed->push_back(ttk.track());
    const reco::TrackBaseRef& tk(ttk.trackBaseRef());
    seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())] = uint2uchar_clamp(itk++);
  }

  //edm::Handle<reco::BeamSpot> beamspot;       //these lines are in Vertexer.cc but it is not used in finish(), so I do not know why this is here
  //event.getByToken(beamspot_token, beamspot);

  assert(vpeffs->size() == vpeffs_tracks.size());
  for (size_t i = 0, ie = vpeffs->size(); i < ie; ++i) {
    for (auto tk : vpeffs_tracks[i].first)  (*vpeffs)[i].tracks_push_back(0, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
    for (auto tk : vpeffs_tracks[i].second) (*vpeffs)[i].tracks_push_back(1, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
  }

  int count_3trk_vertices = 0;
  int count_5trk_vertices = 0;
  for (const reco::Vertex& v : *vertices) {
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      reco::TrackRef tk = it->castTo<reco::TrackRef>();
      tracks_inVertices->push_back(*tk);
    }
    if (v.nTracks() >= 3)
      ++count_3trk_vertices;
    if (v.nTracks() >= 5)
      ++count_5trk_vertices;
  }

  /*event.put(std::move(vertices));     //FIGURE OUT HOW TO TRANSLATE THIS INTO HISTOGRAM OUTPUTS AS AFUNCTION OF 3D DVV!!!
  event.put(std::move(vpeffs));
  event.put(std::move(tracks_seed),       "seed");
  event.put(std::move(tracks_missseed),       "seed");
  event.put(std::move(tracks_all),        "all");
  event.put(std::move(tracks_inVertices), "inVertices");*/
  std::cout << "check if 0.5: " << bssigma_x << std::endl;
  std::cout << "pt of first track of first vertex after revertexing: " << seed_tracks[0].track().pt() << std::endl;
}

void produce(std::vector<double> bs_pos, double bssigma_x, double bssigma_y, double bssigma_z, std::vector<reco::TransientTrack> seed_tracks, reco::TrackCollection track_collection) { //only used if we are revertexing the constructed events, CHECK IF THESE INPUTS ARE CORRECT WHEN BUGS ARE GONE
  const double bsx = bs_pos[0];
  const double bsy = bs_pos[1];
  const double bsz = bs_pos[2];
  reco::Vertex::Point bsposition(bsx, bsy, bsz);
  reco::Vertex::Error bscovariance; //reco::Vertex::Error or CovarianceMatrix, either should work
  bscovariance(0, 0) = bssigma_x * bssigma_x; //this information is currently not stored in the minitrees
  bscovariance(1, 1) = bssigma_y * bssigma_y; //we may need to rerun them to properly define
  bscovariance(2, 2) = bssigma_z * bssigma_z; //these variables
  const reco::Vertex fake_bs_vtx(bsposition, bscovariance);
  std::cout << "beamspot variables reformatted" << std::endl;

  //edm::ESHandle<TransientTrackBuilder> tt_builder;                              //THIS IS USED A LOT LATER FIND OUT WHY!!!!
  //setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  //edm::Handle<std::vector<reco::TrackRef>> quality_track_refs;
  //if (track_attachment)
  //  event.getByToken(quality_tracks_token, quality_track_refs);

  //reco::TrackCollection track_collection;
  //for (int i = 0; i < seed_tracks.size(); ++i) {
    //track_collection.push_back(seed_tracks[i]); //reco::Tracks must fill a reco::TrackCollection
  //}
  std::map<reco::TrackRef, size_t> seed_track_ref_map;
  for (int i = 0; i < seed_tracks.size(); ++i) {
    reco::TrackRef tk(&track_collection, i);
    seed_track_ref_map[tk] = seed_tracks.size() - 1;
  }  

  const size_t ntk = seed_tracks.size();
  std::cout << "track variables defined" << std::endl;

  //////////////////////////////////////////////////////////////////////
  // Form seed vertices from all pairs of tracks whose vertex fit
  // passes cuts.
  //////////////////////////////////////////////////////////////////////

  std::unique_ptr<reco::VertexCollection> vertices(new reco::VertexCollection);
  std::unique_ptr<VertexerPairEffs> vpeffs(new VertexerPairEffs);
  std::vector<std::pair<track_set, track_set>> vpeffs_tracks;

  if (ntk == 0) {
    //finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks); //original Vertexer.cc finish() inputs
    finish(bsposition, bssigma_x, bssigma_y, bssigma_z, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
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
    }
  };
  std::cout << "after first use of the seed_tracks variable" << std::endl;
  
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

  int count_3trk_vertices = 0;

  //if (histos) {
  //  for (std::vector<reco::Vertex>::const_iterator v0 = vertices->begin(); v0 != vertices->end(); ++v0) {
  //    const double v0x = v0->position().x() - bsx;
  //    const double v0y = v0->position().y() - bsy;
  //    const double phi0 = atan2(v0y, v0x);
  //    const int ntracks = v0->nTracks();
  //    if (ntracks >= 3)
  //      count_3trk_vertices++;
  //    for (std::vector<reco::Vertex>::const_iterator v1 = v0 + 1; v1 != vertices->end(); ++v1) {
  //      const double v1x = v1->position().x() - bsx;
  //      const double v1y = v1->position().y() - bsy;
  //      const double phi1 = atan2(v1y, v1x);
  //      //h_seed_vertex_paird2d->Fill(mag(v0x - v1x, v0y - v1y));
  //      //h_seed_vertex_pairdphi->Fill(reco::deltaPhi(phi0, phi1));
  //    }
  //  }
  //}

  //if (histos){
  //  h_n_at_least_3trk_seed_vertices->Fill(count_3trk_vertices);
  //  h_n_seed_vertices->Fill(vertices->size());
  //}

  if (order_seed_vertex){
    //order vertices by pt 
    std::sort(vertices->begin(), vertices->end(), order_seed_vtx_pt());
  }
  std::cout << "before start of vertex shared track mitigation" << std::endl;
  
  //////////////////////////////////////////////////////////////////////
  // Take care of track sharing. If a track is in two vertices, and
  // the vertices are "close", refit the tracks from the two together
  // as one vertex. If the vertices are not close, keep the track in
  // the vertex to which it is "closer".
  //////////////////////////////////////////////////////////////////////
  track_set discarded_tracks;
  int n_resets = 0;
  int n_onetracks = 0;
  std::vector<reco::Vertex>::iterator v[2];
  size_t ivtx[2];  

  for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
    track_set tracks[2];
    ivtx[0] = v[0] - vertices->begin();
    tracks[0] = vertex_track_set(*v[0]);

    if (tracks[0].size() < 2) {
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
        v[1] = vertices->erase(v[1]) - 1;
        ++n_onetracks;
        continue;
      }

      if (is_track_subset(tracks[0], tracks[1])) {
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

      if (shared_tracks.size() > 0) {
        if (vpeff)
          vpeff->kind(VertexerPairEff::share);

        Measurement1D v_dist = vertex_dist(*v[0], *v[1]);

        if (v_dist.value() < merge_shared_dist || v_dist.significance() < merge_shared_sig) {
          merge = true;
        }
        else
          refit = true;

        for (auto tk : shared_tracks) {
          const reco::TransientTrack& ttk = seed_tracks[seed_track_ref_map[tk]];
          std::pair<bool, Measurement1D> t_dist_0 = track_dist(ttk, *v[0]);
          std::pair<bool, Measurement1D> t_dist_1 = track_dist(ttk, *v[1]);

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

          if (remove_from_0) tracks_to_remove_in_refit[0].insert(tk);
          if (remove_from_1) tracks_to_remove_in_refit[1].insert(tk);

          if (remove_one_track_at_a_time) {
            break;
          }
        }
        break;
      }
    }

    if (duplicate) {
      vertices->erase(v[1]);
    }
    else if (merge) {
      track_set tracks_to_fit;
      for (int i = 0; i < 2; ++i)
        for (auto tk : tracks[i])
          tracks_to_fit.insert(tk);

      std::vector<reco::TransientTrack> ttks;
      for (auto tk : tracks_to_fit)
        ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);

      reco::VertexCollection new_vertices;

      for (const TransientVertex& tv : kv_reco_dropin(ttks))
        new_vertices.push_back(reco::Vertex(tv));

      // If we got two new vertices, maybe it took A B and A C D and made a better one from B C D, and left a broken one A B! C! D!.
      // If we get one that is truly the merger of the track lists, great. If it is just something like A B , A C -> A B C!, or we get nothing, then default to arbitration.
      if (new_vertices.size() > 1) {
        assert(new_vertices.size() == 2);
        *v[1] = reco::Vertex(new_vertices[1]);
        *v[0] = reco::Vertex(new_vertices[0]);
      }
      else if (new_vertices.size() == 1 && vertex_track_set(new_vertices[0], 0) == tracks_to_fit) {
        if (vpeff)
          vpeff->kind(VertexerPairEff::merge);

        vertices->erase(v[1]);
        *v[0] = reco::Vertex(new_vertices[0]); // ok to use v[0] after the erase(v[1]) because v[0] is by construction before v[1]
      }
      else {
        refit = true;
      }
    }

    if (refit) {
      bool erase[2] = { false };
      reco::Vertex vsave[2] = { *v[0], *v[1] };

      for (int i = 0; i < 2; ++i) {
        if (tracks_to_remove_in_refit[i].empty())
          continue;

        std::vector<reco::TransientTrack> ttks;
        for (auto tk : tracks[i])
          if (tracks_to_remove_in_refit[i].count(tk) == 0)
            ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);

        reco::VertexCollection new_vertices;
        for (const TransientVertex& tv : kv_reco_dropin(ttks))
          new_vertices.push_back(reco::Vertex(tv));
        if (new_vertices.size() == 1)
          * v[i] = new_vertices[0];
        else
          erase[i] = true;
      }

      if (vpeff && (erase[0] || erase[1]))
        vpeff->kind(VertexerPairEff::erase);

      if (erase[1]) vertices->erase(v[1]);
      if (erase[0]) vertices->erase(v[0]);
    }

    // If we changed the vertices at all, start loop over completely.
    if (duplicate || merge || refit) {
      v[0] = vertices->begin() - 1;  // -1 because about to ++sv
      ++n_resets;
      //if (n_resets == 3000)
      //  throw "I'm dumb";
    }
  }

  // Debugging plots for track refinement and noshare histos: 
  // These steps are sequential within the loop, but nested in their own `if` statements below.
  // (useful e.g. if one wants to look at the noshare plots during the track refinement)
  /*
  if (do_track_refinement || histos_noshare) {  //Alec found, we have not been using this which remove tracks + trim out tracks with IP significance larger than trackrefine_sigmacut and trackrefine_trimmax, respectively 
    std::map<reco::TrackRef, int> track_use;
    for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
      reco::Vertex& v_trf = vertices->at(i);
      const int ntracks = v_trf.nTracks();
      const double vmass = v_trf.p4().mass();
      const double vchi2 = v_trf.normalizedChi2();
      const double vndof = v_trf.ndof();
      const double vx = v_trf.position().x() - bsx;
      const double vy = v_trf.position().y() - bsy;
      const double vz = v_trf.position().z() - bsz;
      const double rho = mag(vx, vy);
      const double phi = atan2(vy, vx);
      const double r = mag(vx, vy, vz);
      for (const auto& tk : vertex_track_set(v_trf)) {
        if (track_use.find(tk) != track_use.end())
          track_use[tk] += 1;
        else
          track_use[tk] = 1;
      }

      if (do_track_refinement) {

        track_set set_trackrefine_sigmacut_tks;
        std::vector<reco::TransientTrack> trackrefine_sigmacut_ttks;
        track_set set_trackrefine_trimmax_tks;
        std::vector<reco::TransientTrack> trackrefine_trimmax_ttks;
        std::vector<double> trackrefine_trim_ttks_missdist_sig;
        for (auto it = v_trf.tracks_begin(), ite = v_trf.tracks_end(); it != ite; ++it) {

          reco::TransientTrack seed_track;
          seed_track = tt_builder->build(*it.operator*());
          std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v_trf);

          //h_noshare_vertex_tkvtxdist_before_do_track_refinement->Fill(tk_vtx_dist.second.value());
          //h_noshare_vertex_tkvtxdisterr_before_do_track_refinement->Fill(tk_vtx_dist.second.error());
          //h_noshare_vertex_tkvtxdistsig_before_do_track_refinement->Fill(tk_vtx_dist.second.significance());

          if (tk_vtx_dist.second.significance() < trackrefine_sigmacut) {
            set_trackrefine_sigmacut_tks.insert(it->castTo<reco::TrackRef>());
          }
        }

        for (auto tk : set_trackrefine_sigmacut_tks) {
          trackrefine_sigmacut_ttks.push_back(tt_builder->build(tk));
        }

        // if tracks's miss distance significance is larger than trackrefine_sigmacut, we first remove all those tracks and refit a new vertex
        double trackrefine_sigmacut_v0x = v_trf.position().x() - bsx;
        double trackrefine_sigmacut_v0y = v_trf.position().y() - bsy;
        double trackrefine_sigmacut_v0r = mag(trackrefine_sigmacut_v0x, trackrefine_sigmacut_v0y);

        reco::Vertex trackrefine_sigmacut_v;
        for (const TransientVertex& tv : kv_reco_dropin(trackrefine_sigmacut_ttks))
          trackrefine_sigmacut_v = reco::Vertex(tv);
        double trackrefine_sigmacut_vchi2 = trackrefine_sigmacut_v.normalizedChi2();
        //h_noshare_trackrefine_sigmacut_vertex_chi2->Fill(trackrefine_sigmacut_vchi2);

        double trackrefine_sigmacut_v1x = trackrefine_sigmacut_v.position().x() - bsx;
        double trackrefine_sigmacut_v1y = trackrefine_sigmacut_v.position().y() - bsy;
        double trackrefine_sigmacut_v1r = mag(trackrefine_sigmacut_v1x, trackrefine_sigmacut_v1y);

        // just to check how the new vertex is shifted by removing tracks by trackrefine_sigmacut
        double sigmacut_vertex_distr = trackrefine_sigmacut_v1r - trackrefine_sigmacut_v0r;
        //h_noshare_trackrefine_sigmacut_vertex_distr_shift->Fill(sigmacut_vertex_distr);

        for (auto it = trackrefine_sigmacut_v.tracks_begin(), ite = trackrefine_sigmacut_v.tracks_end(); it != ite; ++it) {
          reco::TransientTrack trackrefine_sigmacut_track;
          trackrefine_sigmacut_track = tt_builder->build(*it.operator*());
          std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(trackrefine_sigmacut_track, trackrefine_sigmacut_v);
          //h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
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
          //h_noshare_trackrefine_trimmax_vertex_distr_shift->Fill(trimmax_vertex_distr);

          trackrefine_trim_ttks_missdist_sig.clear();

          for (auto it = trackrefine_trimmax_v.tracks_begin(), ite = trackrefine_trimmax_v.tracks_end(); it != ite; ++it) {
            reco::TransientTrack trackrefine_trimmax_track;
            trackrefine_trimmax_track = tt_builder->build(*it.operator*());
            std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(trackrefine_trimmax_track, trackrefine_trimmax_v);
            trackrefine_trim_ttks_missdist_sig.push_back(tk_vtx_dist.second.significance());
          }

        }

        double trackrefine_trimmax_vchi2 = trackrefine_trimmax_v.normalizedChi2();
        //h_noshare_trackrefine_trimmax_vertex_chi2->Fill(trackrefine_trimmax_vchi2);

        //for (unsigned int j = 0, je = trackrefine_trim_ttks_missdist_sig.size(); j < je; ++j) {
        //  h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig->Fill(trackrefine_trim_ttks_missdist_sig[j]);
        //}

        // the end of track refinement in two steps -- (1) sigmacut and (2) trimmax
        // we replace the noshare vertex by the vertex after the track refinement
        v_trf = trackrefine_trimmax_v;
      }

    }

    int max_noshare_track_multiplicity = 0;
    for (const auto& p : track_use) {
      if (p.second > max_noshare_track_multiplicity)
        max_noshare_track_multiplicity = p.second;
    }
  }
  */


  //////////////////////////////////////////////////////////////////////////////////////////////
  // Merge vertices that are still "close" in 2D, aka "loose" merging (typically off by default)
  //////////////////////////////////////////////////////////////////////////////////////////////
  //Alec found that we do not use this, instead we have been using resolve_split_vertices_tight which is a merging routine based on vtx dphi and dVV instead of merging vertices within a given dist or significance
  /*
  if (resolve_split_vertices_loose) {

    if (merge_anyway_sig > 0 || merge_anyway_dist > 0) {
      double v0x;
      double v0y;
      double phi0;

      for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
        ivtx[0] = v[0] - vertices->begin();

        double v1x;
        double v1y;
        double phi1;

        for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {

          ivtx[1] = v[1] - vertices->begin();

          Measurement1D v_dist = vertex_dist(*v[0], *v[1]);
          v0x = v[0]->x() - bsx;
          v0y = v[0]->y() - bsy;
          phi0 = atan2(v0y, v0x);
          v1x = v[1]->x() - bsx;
          v1y = v[1]->y() - bsy;
          phi1 = atan2(v1y, v1x);

          if (v_dist.value() < merge_anyway_dist || v_dist.significance() < merge_anyway_sig) {
            std::vector<reco::TransientTrack> ttks;

            for (int i = 0; i < 2; ++i) {
              for (auto tk : vertex_track_set(*v[i])) {
                ttks.push_back(tt_builder->build(tk));
              }
            }

            reco::VertexCollection merged_vertices;
            for (const TransientVertex& tv : kv_reco_dropin(ttks)) {
              merged_vertices.push_back(reco::Vertex(tv));

              for (auto it = merged_vertices[0].tracks_begin(), ite = merged_vertices[0].tracks_end(); it != ite; ++it) {
                reco::TransientTrack seed_track;
                seed_track = tt_builder->build(*it.operator*());
                std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, merged_vertices[0]);
              }
            }

            if (merged_vertices.size() == 1) {
              *v[0] = merged_vertices[0];

              v[1] = vertices->erase(v[1]) - 1;
            }
          }
        }
      }

      // Printouts of new vertex distance when using verbose mode
      //if (verbose) {
      //  std::vector<reco::Vertex>::iterator nv[2];
      //  for (nv[0] = vertices->begin(); nv[0] != vertices->end(); ++nv[0]) {
      //    for (nv[1] = nv[0] + 1; nv[1] != vertices->end(); ++nv[1]) {

      //      Measurement1D nv_dist = vertex_dist(*nv[0], *nv[1]);
      //      printf("  new vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, nv_dist.value(), nv_dist.significance());
      //    }
      //  }
      //}
    }
  }

  if (histos_output_beforedzfit){
    fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::beforedzfit);
  }
  */
  //////////////////////////////////////////////////////////////////////
  // Drop tracks that "move" the vertex too much by refitting without each track.
  //////////////////////////////////////////////////////////////////////
  //Alec we do not need to apply the delta z refitting if we are looking at pairs of vertices, this is a 1-vertex quantity that should be already passed by vertices we are using
  /*
  if (max_nm1_refit_dist3 > 0 || max_nm1_refit_distz > 0 || max_nm1_refit_distz_sig > 0) { 
    std::vector<int> refit_count(vertices->size(), 0);
    int iv = 0;
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0], ++iv) {
      if (max_nm1_refit_count > 0 && refit_count[iv] >= max_nm1_refit_count)
        continue;

      const track_vec tks = vertex_track_vec(*v[0]);
      const size_t ntks = tks.size();
      if (ntks < 3)
        continue;

      std::vector<reco::TransientTrack> ttks(ntks - 1);
      for (size_t i = 0; i < ntks; ++i) {
        float tkpt_todrop = tks[i]->pt();
        float tkphi_todrop = tks[i]->phi();

        std::vector<float> track_dphis;
        for (size_t j = 0; j < ntks; ++j) {
          if (j != i) { 
            ttks[j - (j >= i)] = tt_builder->build(tks[j]);
            track_dphis.push_back(fabs(tkphi_todrop - tks[j]->phi()));
          }
        }
        double sum_dphi = std::accumulate(track_dphis.begin(), track_dphis.end(), 0.0);
        double dphi_avg = sum_dphi / track_dphis.size();

        reco::Vertex vnm1(TransientVertex(kv_reco->vertex(ttks)));
        const double dist3_2 = mag2(vnm1.x() - v[0]->x(), vnm1.y() - v[0]->y(), vnm1.z() - v[0]->z());
        const double distz = vnm1.z() - v[0]->z();
	const double tkv_distz = (tks[i]->vz() - v[0]->z()) - ((tks[i]->vx() -  v[0]->x()) * tks[i]->px() + (tks[i]->vy() -  v[0]->y()) * tks[i]->py()) / tks[i]->pt() * tks[i]->pz() / tks[i]->pt();
        const double err_tkv_distz = sqrt(tks[i]->covariance(4,4) * (tks[i]->p()*tks[i]->p())) / tks[i]->pt(); //same as dzErr() 
        std::pair<bool, Measurement1D> tkbs_dist_2d = track_dist2d(tt_builder->build(tks[i]), *v[0]);
        const double vchi2 = v[0]->normalizedChi2();
        Measurement1D dBV_Meas1D = vertex_dist_2d.distance(*v[0], fake_bs_vtx);
        double dBV = dBV_Meas1D.value();
        double bs2derr = dBV_Meas1D.error();
        reco::TrackRef tk = tks[i];
        std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(tt_builder->build(tks[i]), vnm1);

        const double distz_sig = distz/sqrt(mag(vnm1.covariance(2,2) - v[0]->covariance(2,2)));  

        if (vnm1.chi2() < 0 ||
            (max_nm1_refit_dist3 > 0 && mag2(vnm1.x() - v[0]->x(), vnm1.y() - v[0]->y(), vnm1.z() - v[0]->z()) > pow(max_nm1_refit_dist3, 2)) || (max_nm1_refit_distz_sig > 0 && fabs(distz_sig) > max_nm1_refit_distz_sig) 
  || (max_nm1_refit_distz > 0 && fabs(distz) > max_nm1_refit_distz)) 
        { 
          
          *v[0] = vnm1;
          ++refit_count[iv];
          --v[0], --iv;
          break;
        }
      }
    }
    iv = 0; //some vertices after dz refiting have normalized chi2 > 5
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0], ++iv) {
      h_dz_vertex_chi2->Fill((*v[0]).normalizedChi2());
      if ((*v[0]).normalizedChi2() > 5) {
         v[0] = vertices->erase(v[0]) - 1;
         continue;
       }
    }
  
  }
  */
  //if (histos_output_afterdzfit){
  //  fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::afterdzfit);
  //}
  /////////////////////////////////////////////////////////////////////////////////////////////////////
  // Merge every pair of output vertices that satisfy the following criteria to resolve split-vertices:
  //   - >=2trk/vtx
  //   - dBV > 100 um
  //   - |dPhi(vtx0,vtx1)| < 0.5 
  //   - svdist2d < 300 um
  // Note that the merged vertex must pass chi2/dof < 5
  ////////////////////////////////////////////////////////////////////////////////////////////////////
  if (resolve_split_vertices_tight) {
    reco::VertexCollection potential_merged_vertices;

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

            if (investigate_merged_vertices) {
              std::vector<TransientVertex> tv(1, kv_reco->vertex(ttks));
              potential_merged_vertices.push_back(reco::Vertex(tv[0]));
              //std::cout << "ntrack in potental merged: " << potential_merged_vertices.back().nTracks() << std::endl;
            }

            reco::VertexCollection merged_vertices;
            for (const TransientVertex& tv : kv_reco_dropin(ttks)) {
              merged_vertices.push_back(reco::Vertex(tv));
            }

            if (merged_vertices.size() == 1 && vertex_track_set(merged_vertices[0], 0) == tracks_to_fit) {

              merge = true;

              v[1] = vertices->erase(v[1]) - 1; // (1) erase and point the iterator at the previous entry
              *v[0] = reco::Vertex(merged_vertices[0]); // (2) updated v[0] (ok to use v[0] after the erase(v[1]) because v[0] is by construction before v[1])
            }
          }
        }
      }
	  // going through all the pairs of of v[1] and a fixed v[0] for merging, if merge happens (1) each v[1] is erased (2) v[0] is updated (recurring until exit loop) (3) reset the combination again
	  if (merge)
		  v[0] = vertices->begin() - 1; // (3) reset the combination if a valid merge happens 
    }

    if (investigate_merged_vertices) {
      for (size_t i = 0, ie = potential_merged_vertices.size(); i < ie; ++i) {
        reco::Vertex vpm = potential_merged_vertices[i];
        const int ntracks = vpm.nTracks();
        const double vchi2 = vpm.normalizedChi2();
        Measurement1D dBV_Meas1D = vertex_dist_2d.distance(vpm, fake_bs_vtx);
        double dBV = dBV_Meas1D.value();
        double bs2derr = dBV_Meas1D.error();

        // n-1 plots of the various cuts used (ntk, dBV, bs2derr, chi2)
        //if (ntracks >= 5 && dBV > 0.01 && bs2derr < 0.0050) {
        //  h_output_aftermerge_potential_merged_vertex_nm1_chi2->Fill(vchi2);
        //}
        //if (vchi2 < 5 && dBV > 0.01 && bs2derr < 0.0050) {
        //  h_output_aftermerge_potential_merged_vertex_nm1_ntracks->Fill(ntracks);
        //}
        //if (vchi2 < 5 && ntracks >= 5 && bs2derr < 0.0050) {
        //  h_output_aftermerge_potential_merged_vertex_nm1_bsbs2ddist->Fill(dBV);
        //}
        //if (vchi2 < 5 && ntracks >= 5 && dBV > 0.01) {
        //  h_output_aftermerge_potential_merged_vertex_nm1_bs2derr->Fill(bs2derr);
        //}
      }
    }
  }

  //if (histos_output_aftermerge) {
  //  fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::aftermerge);
  //}

  //////////////////////////////////////////////////////////////////////
  // Shared-jet mitigation with the following procedure:
  //   -   make a set of vertices that have been sorted by ascending number of tracks per vertex
  //   -   loop thru a pair of >=3trk vertices and check whether they share {1,1} and {1,n} shared jets or not 
  //   -   In the double loop: check one vertex at a time (sv0) and remove a lone track to the jet if it is pointing backward from its vertex (apply dphi < pi/2)
  //   -   In the double loop: assign a new fitted vertex to the one resolving shared jets
  //   -   loop thru a set of vertices after the mitigation to clean up a vertex with just one track
  // Note that:
  //   - {1,1} shared jets have exactly one track to the jet from both vertices
  //   - {1,n} shared jets have one of the two vertices contributing exactly one track to the jet
  //////////////////////////////////////////////////////////////////////
  /*if (resolve_shared_jets) {
    edm::Handle<pat::JetCollection> jets;
    event.getByToken(shared_jet_token, jets);

    std::vector<std::vector<size_t> > sv_total_track_which_trkidx; // a vector of each sv's track indx
    // we need ascending vectors of vertices based on their total tracks in order to speed up the shared-jet algorithm because the less-track vertex is more likely to be removed first after a single shared-jet track is removed, reducing the size of vertices to loop thru.  
    std::vector<unsigned int> sv_ascending_total_ntrack; // a vector of ascending number of total tracks per vertex 
    std::vector<size_t> sv_ascending_vtxidx; // a vector of vertex index corresponding to the order of ascending total tracks in sv_ascending_total_ntrack 


    std::vector<std::vector<size_t> > sv_match_trkidx; // a vector of each sv's track indx to keep a record of a track matching with a jet  
    std::vector<std::vector<size_t> > sv_match_jetidx; // a vector of each sv's jet indx to keep a record of a jet that matches with a track at the same iterator  

    std::vector<track_vec> sv_total_track_which_trk_vec; // a vector of each sv's track_vec object 

    int n_output_aftersharedjets_onetracks = 0;

    size_t vtxidx = 0;
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
      std::vector<size_t> track_idx;
      std::vector<size_t> tracktojet_which_trkidx;
      std::vector<size_t> tracktojet_which_jetidx;
      track_vec tks = vertex_track_vec(*v[0]);
      sv_total_track_which_trk_vec.push_back(tks);
      for (size_t i = 0; i < tks.size(); ++i) {
        const reco::TrackRef& itk = tks[i];
        track_idx.push_back(i);
        for (size_t j = 0; j < jets->size(); ++j) {
          if (match_track_jet(*itk, (*jets)[j], *jets, j)) {
            tracktojet_which_trkidx.push_back(i);
            tracktojet_which_jetidx.push_back(j);
            if (verbose)
              printf(" track %u matched with a jet %lu \n", tks[i].key(), j);
          }
        }
      }

      unsigned int ntracks = track_idx.size();

      if (vtxidx == 0) { // start creating the ascening vector of sorted number of total tracks and its corresponding vertex index
        sv_ascending_total_ntrack.push_back(ntracks);
        sv_ascending_vtxidx.push_back(vtxidx);
      }
      else { // the algorithm continues after the first vertex is added to the vector 

        std::vector<unsigned int>::iterator it_ntracks = sv_ascending_total_ntrack.end();
        std::vector<size_t>::iterator it_vtx = sv_ascending_vtxidx.end();
        // finding an iterator that points to a position that ntrack is just less than or equal to itself from the back to the front
        while (it_ntracks != sv_ascending_total_ntrack.begin() && ntracks <= sv_ascending_total_ntrack[std::distance(sv_ascending_total_ntrack.begin(), it_ntracks)-1])
        {
          --it_ntracks;
          --it_vtx;
        }
        // adding a vertex at the end if it has higher ntrack. otherwise, insert it before an iterator pointing to a position that this ntrack is smaller than itself 
        if (it_ntracks == sv_ascending_total_ntrack.end() && ntracks > sv_ascending_total_ntrack[std::distance(sv_ascending_total_ntrack.begin(), it_ntracks)]) {
          sv_ascending_total_ntrack.push_back(ntracks);
          sv_ascending_vtxidx.push_back(vtxidx);
        }

        else {
          sv_ascending_total_ntrack.insert(it_ntracks, ntracks);
          sv_ascending_vtxidx.insert(it_vtx, vtxidx);
        }
      }

      sv_total_track_which_trkidx.push_back(track_idx);
      sv_match_trkidx.push_back(tracktojet_which_trkidx);
      sv_match_jetidx.push_back(tracktojet_which_jetidx);
      vtxidx++;
    }


    if (vertices->size() >= 2) {
      // double for loops to double counts the sv0 and sv1 pairing. The code always remove 'lone shared tracks' from (multiple) special shared jets to sv0 in each round as long as they are not compatible to sv0. Otherwise, the sv1 from the earlier round will be considered again (double count) to have the tracks being removed or not. 
      for (size_t vtxi = 0; vtxi < sv_ascending_vtxidx.size(); vtxi++) {
        const size_t vtxidx0 = sv_ascending_vtxidx[vtxi];
        reco::Vertex& sv0 = vertices->at(vtxidx0);
        double sv0x = sv0.x() - bsx;
        double sv0y = sv0.y() - bsy;
        double phi0 = atan2(sv0y, sv0x);
        for (size_t vtxj = 0; vtxj < sv_ascending_vtxidx.size(); vtxj++) {
          if (vtxi == vtxj) continue;
          const size_t vtxidx1 = sv_ascending_vtxidx[vtxj];
          reco::Vertex& sv1 = vertices->at(vtxidx1);

          // only consider a pair with at least 3 tracks per vertex
          if (sv0.nTracks() > 2 && sv1.nTracks() > 2) {

            std::pair<bool, std::vector<std::vector<size_t>>> sharedjet_tool = sharedjets(vtxidx0, vtxidx1, sv_match_jetidx, sv_match_trkidx);

            // loop thru {1,1}+{1,n} nsharedjets and remove just one shared track from v0 if a |dPhi(v0,one shared track)| > pi/2
            if (sharedjet_tool.first) {
              std::vector<std::vector<size_t>> sv_lonesharedtrack_trkidx = sharedjet_tool.second;
              std::vector<size_t> sv0_lonesharedtrack_trkidx = sv_lonesharedtrack_trkidx[0];
              std::vector<size_t> sv1_lonesharedtrack_trkidx = sv_lonesharedtrack_trkidx[1];
              for (size_t k = 0; k < sv0_lonesharedtrack_trkidx.size(); k++) {
                track_vec tks_sv0 = sv_total_track_which_trk_vec[vtxidx0];
                size_t idx = sv0_lonesharedtrack_trkidx[k];
                h_resolve_shared_jets_lonetrkvtx_dphi->Fill(fabs(reco::deltaPhi(tks_sv0[idx]->phi(), phi0)));

                // drop the lone track pointing backwards from the vertex direction!
                if (fabs(reco::deltaPhi(tks_sv0[idx]->phi(), phi0)) > M_PI / 2) {
                  eraseElement(sv_total_track_which_trkidx[vtxidx0], idx);
                }
              }
              track_set  sv0_resolved_sharedtracks_trkset;
              for (unsigned int trk0_i = 0; trk0_i < sv_total_track_which_trkidx[vtxidx0].size(); ++trk0_i) {
                size_t idx = sv_total_track_which_trkidx[vtxidx0][trk0_i];
                track_vec tks_sv0 = sv_total_track_which_trk_vec[vtxidx0];
                sv0_resolved_sharedtracks_trkset.insert(tks_sv0[idx]);

              }
              std::vector<reco::TransientTrack> sv0_resolved_sharedtracks_ttks;
              for (auto tk : sv0_resolved_sharedtracks_trkset)
                sv0_resolved_sharedtracks_ttks.push_back(tt_builder->build(tk));

              reco::Vertex sv0_resolved_sharedtracks;

              for (const TransientVertex& tv : kv_reco_dropin(sv0_resolved_sharedtracks_ttks))
                sv0_resolved_sharedtracks = reco::Vertex(tv);

              sv0 = sv0_resolved_sharedtracks; // update sv0 after non-compatible 'lone shared tracks' from some special shared jets are removed 
            }
          }
        }
      }
    }

    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
      track_set tracks[2];
      ivtx[0] = v[0] - vertices->begin();
      tracks[0] = vertex_track_set(*v[0]);

      if (tracks[0].size() < 2) {
        if (verbose)
          throw cms::Exception("1-trk vtx in Vertexer") << "at vertex index: " << ivtx[0];
        v[0] = vertices->erase(v[0]) - 1;
        ++n_output_aftersharedjets_onetracks;
        continue;
      }

      if (tracks[0].size() < v[0]->nTracks()) {
        throw cms::Exception("inconsistent total tracks per vertex in Vertexer") << "please check for duplicated tracks ";
        std::vector<reco::TransientTrack> sv_nonduplicate_ttks;
        for (const reco::TrackRef& itk : vertex_track_set(*v[0])) {
          if (itk.isNonnull())
            sv_nonduplicate_ttks.push_back(tt_builder->build(itk));
        }

        for (const TransientVertex& tv : kv_reco_dropin(sv_nonduplicate_ttks))
          *v[0] = reco::Vertex(tv);
      }
    }

    if (histos_output_aftersharedjets) {
      fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::aftersharedjets);
      h_output_aftersharedjets_n_onetracks->Fill(n_output_aftersharedjets_onetracks);
    }
    }*/ //ADD THIS BACK IN FOR SHARED JET MITIGATION!!!!!!
																					  
  // track attachment
  /* Alec not sure what this is, but it is not used in Vertexer_cfi.py
  if (track_attachment) {
	  // build transient tracks from quality tracks (not included in seed tracks)
	  std::vector<reco::TransientTrack> quality_tracks;
	  std::map<reco::TrackRef, size_t> quality_track_ref_map;
	  track_set all_quality_tracks;
	  for (const reco::TrackRef& tk : *quality_track_refs) {
		  all_quality_tracks.insert(tk);
		  quality_tracks.push_back(tt_builder->build(tk));
		  quality_track_ref_map[tk] = quality_tracks.size() - 1;
	  }
	  //start track attachment, attach tracks to vertices if dist(track, vertex)<5 sigma, if a track is close to more than one vertices, attach to the closer one, if a tracks has distance with more than one vertices <=1.5 sigma, attach it to the vertex with more tracks
	  bool refit = true;
	  while (refit) {
		  refit = false;
		  for (const reco::TrackRef& itk : all_quality_tracks) {
			  const reco::TransientTrack& ttk = quality_tracks[quality_track_ref_map[itk]];
			  int v_assign = -1;
			  double v_assign_dist_sig = 999;
			  unsigned int v_assign_ntk = 0;

			  for (size_t i = 0; i < vertices->size(); ++i) {
				  const reco::Vertex& v = vertices->at(i);
				  std::pair<bool, Measurement1D> t_dist = track_dist(ttk, v);
				  t_dist.first = t_dist.first && (t_dist.second.value() < max_track_vertex_dist || t_dist.second.significance() < max_track_vertex_sig); // whether it is too far away from the vtx
				  if (t_dist.first) {
					  if ((t_dist.second.significance() < min_track_vertex_sig_to_remove) && (v_assign_dist_sig < min_track_vertex_sig_to_remove)) {
						  if (v_assign_ntk < v.nTracks()) {
							  v_assign = i;
							  v_assign_dist_sig = t_dist.second.significance();
							  v_assign_ntk = v.nTracks();
						  }
					  }
					  else if (t_dist.second.significance() < v_assign_dist_sig) {
						  v_assign = i;
						  v_assign_dist_sig = t_dist.second.significance();
						  v_assign_ntk = v.nTracks();
					  }
				  }

			  }
			  if (v_assign >= 0) {
				  refit = true;
				  all_quality_tracks.erase(itk);
				  std::vector<reco::TransientTrack> ttks;
				  for (auto tk : vertex_track_set((*vertices)[v_assign])) {
					  ttks.push_back(tt_builder->build(tk));
				  }
				  ttks.push_back(ttk);
				  reco::VertexCollection new_vertices;
				  for (const TransientVertex& tv : kv_reco_dropin(ttks))
					  new_vertices.push_back(reco::Vertex(tv));
				  if (new_vertices.size() == 1)
					  (*vertices)[v_assign] = new_vertices[0];
				  break;
			  }
		  }
	  }

	  if (histos_output_aftertrackattach) {
		  fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::aftertrackattach);
	  }
  }
  */
  //finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks); //original Vertexer.cc inputs
  finish(bsposition, bssigma_x, bssigma_y, bssigma_z, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
}



//constructs the background template
void construct_dvvc(ConstructDvvcParameters p, const char* out_fn) {

  //p.print(); printf(", out_fn = %s\n", out_fn);
  //std::string print_output = callPythonAndGetOutput("qcdht0700_2017");
  //std::cout << "C++ received from Python: " << print_output << std::endl;

  const char* file_path; //which filepath?
  const char* file_path_20161;
  const char* file_path_20162;
  const char* file_path_2017;
  const char* file_path_2018;
  if (p.is_mc()) {
    if (ulversion == "ULV30BvetoLHTm") {
      //file_path = "/eos/user/p/pekotamn/MiniTree_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm";
      //file_path = "/uscms_data/d3/shogan/crab_dirs/MiniTree_FixWP_ULV11Bm"; //Shaun's MiniTrees
      //file_path_20161 = "/uscms_data/d3/shogan/crab_dirs/MiniTree_FixWP_ULV11Bm";
      //file_path_20162 = "/uscms_data/d3/shogan/crab_dirs/MiniTree_FixWP_ULV11Bm";
      //file_path_2017 = "/uscms_data/d3/shogan/crab_dirs/MiniTree_FixWP_ULV11Bm";
      //file_path_2018 = "/uscms_data/d3/shogan/crab_dirs/MiniTree_FixWP_ULV11Bm";
      //file_path_20161 = "/uscms/home/joeyr/crabdirs/MiniTree__tagTestFixTrigThresholdsBvetoLHTm";
      //file_path_20162 = "/uscms/home/joeyr/crabdirs/MiniTree__tagTestFixTrigThresholdsBvetoLHTm";
      //file_path_2017 = "/uscms/home/joeyr/crabdirs/MiniTree__tagTestFixTrigThresholdsBvetoLHTm";
      //file_path_2018 = "/uscms/home/joeyr/crabdirs/MiniTree__tagTestFixTrigThresholdsBvetoLHTm";
      file_path_20161 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
      file_path_20162 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
      file_path_2017 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
      file_path_2018 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
    }
    else { 
      //file_path = "/eos/user/p/pekotamn/MiniTree_LepIPCut_OnnormdzULV30Lepm";
      //file_path_20161 = "/uscms/home/alecduqu/crab_dirs/MiniTree_LepIPCut_Lepton_SF_20161correctionsLepm_noef"; //20161
      //file_path_20162 = "/uscms/home/alecduqu/crab_dirs/MiniTree_LepIPCut_Lepton_SF_20162correctionsLepm_noef"; //20162
      //file_path_2017 = "/uscms/home/alecduqu/crab_dirs/MiniTree_LepIPCut_Lepton_SF_correctionsLepm_noef"; //2017 //Alec's MiniTrees
      //file_path_2018 = "/uscms/home/alecduqu/crab_dirs/MiniTree_LepIPCut_eventweights_Lepton_SF_2018correctionsLepm_noef"; //2018
      //file_path_20161 = "root://cmsxrootd.fnal.gov//store/group/lpclonglived/alecduqu/MiniTree_LepIPCut_Lepton_SF_20161correctionsLepm_noef/"; //20161 moved to eos
      //file_path_20162 = "root://cmsxrootd.fnal.gov//store/group/lpclonglived/alecduqu/MiniTree_LepIPCut_Lepton_SF_20162correctionsLepm_noef/"; //20162 moved to eos
      //file_path_2017 = "root://cmsxrootd.fnal.gov//store/group/lpclonglived/alecduqu/MiniTree_LepIPCut_Lepton_SF_correctionsLepm_noef/"; //2017 moved to eos
      //file_path_2018 = "root://cmsxrootd.fnal.gov//store/group/lpclonglived/alecduqu/MiniTree_LepIPCut_Lepton_SF_2018correctionsLepm_noef/"; //2018 moved to eos
      file_path_20161 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
      file_path_20162 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
      file_path_2017 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
      file_path_2018 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
    }
  } else if (p.only_20pc()) {
    if (ulversion == "ULV30BvetoLHTm") {
      file_path_20161 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
      file_path_20162 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
      file_path_2017 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
      file_path_2018 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001BvetoLHTm";
    }
    else { 
      file_path_20161 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
      file_path_20162 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
      file_path_2017 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
      file_path_2018 = "/uscms/home/joeyr/crabdirs/MiniTree_tag001Lepm";
    }
  } else {
    if (ulversion == "ULV30BvetoLHTm") {
      file_path = "/eos/user/p/pekotamn/MiniTree_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm";
    }
    else { 
      file_path = "/eos/user/p/pekotamn/MiniTree_LepIPCut_OnnormdzULV30Lepm";
    }
  }

  std::vector<const char*>  samples;
  std::vector<float>  weights;

  std::cout << "The year is: " << p.year() << std::endl;

  bool use_20161 = p.year() == "20161" or p.year() == "20161"   or p.year() == "run2";
  bool use_20162 = p.year() == "20162" or p.year() == "20162"   or p.year() == "run2";
  bool  use_2017 = p.year() == "2017"  or p.year() == "2017p8" or p.year() == "run2";
  bool  use_2018 = p.year() == "2018"  or p.year() == "2017p8" or p.year() == "run2";
  // FIXME these weights are based off of the number of finished ntuples (which is
  // close to, but not necessarily 100% of ntuples). When it comes time to do the
  // final studies, we'll need to make sure ALL ntuples/minitrees finish, and then
  // update some of the weights             std::string command = "python " + filepath + "ttbar_20161.root"; system(command.c_str());
  //Py_Initialize();
  //PyRun_SimpleString('sys.path.append("path/to/my/module/")');
  if (ulversion == "ULV30BvetoLHTm"){
    if (p.is_mc()) {
      if (use_20161) {
	if (use_signal) {
	  //samples.push_back("ggHToSSTodddd_tau100mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau100mm_M55_20161")));
	  //samples.push_back("ggHToSSTodddd_tau10mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau10mm_M55_20161")));
	  //samples.push_back("ggHToSSTodddd_tau1mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau1mm_M55_20161")));

	  /*samples.push_back("mfv_neu_tau000100um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0200_20161")));
	  samples.push_back("mfv_neu_tau000100um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0300_20161")));
	  samples.push_back("mfv_neu_tau000100um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0400_20161")));
	  samples.push_back("mfv_neu_tau000100um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0600_20161")));
	  samples.push_back("mfv_neu_tau000100um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0800_20161")));
	  samples.push_back("mfv_neu_tau000100um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1200_20161")));
	  samples.push_back("mfv_neu_tau000100um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1600_20161")));
	  samples.push_back("mfv_neu_tau000100um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M3000_20161")));
	  samples.push_back("mfv_neu_tau000300um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0200_20161")));
	  samples.push_back("mfv_neu_tau000300um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0300_20161")));
	  samples.push_back("mfv_neu_tau000300um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0400_20161")));
	  samples.push_back("mfv_neu_tau000300um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0600_20161")));
	  samples.push_back("mfv_neu_tau000300um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0800_20161")));
	  samples.push_back("mfv_neu_tau000300um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1200_20161")));
	  samples.push_back("mfv_neu_tau000300um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1600_20161")));
	  samples.push_back("mfv_neu_tau001000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0200_20161")));
	  samples.push_back("mfv_neu_tau001000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0300_20161")));
	  samples.push_back("mfv_neu_tau001000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0400_20161")));
	  samples.push_back("mfv_neu_tau001000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0600_20161")));
	  samples.push_back("mfv_neu_tau001000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0800_20161")));
	  samples.push_back("mfv_neu_tau001000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1200_20161")));
	  samples.push_back("mfv_neu_tau001000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1600_20161")));
	  samples.push_back("mfv_neu_tau001000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M3000_20161")));
	  samples.push_back("mfv_neu_tau010000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0200_20161")));
	  samples.push_back("mfv_neu_tau010000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0300_20161")));
	  samples.push_back("mfv_neu_tau010000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0400_20161")));
	  samples.push_back("mfv_neu_tau010000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0600_20161")));
	  samples.push_back("mfv_neu_tau010000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0800_20161")));
	  samples.push_back("mfv_neu_tau010000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1200_20161")));
	  samples.push_back("mfv_neu_tau010000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1600_20161")));
	  samples.push_back("mfv_neu_tau010000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M3000_20161")));
	  samples.push_back("mfv_neu_tau030000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0200_20161")));
	  samples.push_back("mfv_neu_tau030000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0300_20161")));
	  samples.push_back("mfv_neu_tau030000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0400_20161")));
	  samples.push_back("mfv_neu_tau030000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0600_20161")));
	  samples.push_back("mfv_neu_tau030000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0800_20161")));
	  samples.push_back("mfv_neu_tau030000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M1600_20161")));
	  samples.push_back("mfv_neu_tau030000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M3000_20161")));*/

	  /*samples.push_back("mfv_stopbbarbbar_tau000100um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0300_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0400_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0800_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M1200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M1600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M3000_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0300_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0400_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0800_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M1200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M1600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M3000_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0300_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0400_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0800_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M3000_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0300_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0400_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0800_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M3000_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0200_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0300_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0400_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0600_2016AP1));*/
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0800_20161")));
	  /*samples.push_back("mfv_stopbbarbbar_tau030000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1200_2016")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1600_20161")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M3000_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0300_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0400_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0800_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M3000_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0300_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0400_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0800_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M1200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M1600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M3000_20161")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0300_20161")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0800_20161")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M3000_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0300_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0400_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0800_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M3000_20161")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0300_20161")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0400_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0400_20161")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0600_2016AP1));*/
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0800_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0800_20161")));
	  /*samples.push_back("mfv_stopdbardbar_tau030000um_M1200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1200_20161")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M1600_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1600_20161")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M3000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M3000_20161")));*/
	}
	else {
	  samples.push_back("qcdht0100_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0100_20161")));
	  samples.push_back("qcdht0200_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0200_20161")));
	  samples.push_back("qcdht0300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0300_20161")));
	  samples.push_back("qcdht0500_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0500_20161")));
	  samples.push_back("qcdht0700_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0700_20161")));
	  samples.push_back("qcdht1000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht1000_20161")));
	  samples.push_back("qcdht1500_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht1500_20161")));
	  samples.push_back("qcdht2000_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht2000_20161")));
	  samples.push_back("ttbar_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ttbar_20161")));
	  //samples.push_back("ttbar_20161");    weights.push_back(0.35);
	  //samples.push_back("qcdht0100_20161");    weights.push_back(12658.82);
	  //samples.push_back("qcdht0200_20161");    weights.push_back(1408.45);
	  //samples.push_back("qcdht0300_20161");    weights.push_back(277.09);
	  //samples.push_back("qcdht0500_20161");    weights.push_back(22.53);
	  //samples.push_back("qcdht0700_20161");    weights.push_back(5.84);
	  //samples.push_back("qcdht1000_20161");    weights.push_back(3.47);
	  //samples.push_back("qcdht1500_20161");    weights.push_back(0.48);
	  //samples.push_back("qcdht2000_20161");    weights.push_back(0.19);
	}
      }

      if (use_20162) {
	if (use_signal) {
	  //samples.push_back("ggHToSSTodddd_tau100mm_M55_2016"); weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau100mm_M55_2016")));
	  //samples.push_back("ggHToSSTodddd_tau10mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau10mm_M55_20162")));
	  //samples.push_back("ggHToSSTodddd_tau1mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau1mm_M55_20162")));

	  /*samples.push_back("mfv_neu_tau000100um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0200_20162")));
	  samples.push_back("mfv_neu_tau000100um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0300_20162")));
	  samples.push_back("mfv_neu_tau000100um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0400_20162")));
	  samples.push_back("mfv_neu_tau000100um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0600_20162")));
	  samples.push_back("mfv_neu_tau000100um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0800_20162")));
	  samples.push_back("mfv_neu_tau000100um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1200_20162")));
	  samples.push_back("mfv_neu_tau000100um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1600_20162")));
	  samples.push_back("mfv_neu_tau000100um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M3000_20162")));
	  samples.push_back("mfv_neu_tau000300um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0200_20162")));
	  samples.push_back("mfv_neu_tau000300um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0300_20162")));
	  samples.push_back("mfv_neu_tau000300um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0400_20162")));
	  samples.push_back("mfv_neu_tau000300um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0600_20162")));
	  samples.push_back("mfv_neu_tau000300um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0800_20162")));
	  samples.push_back("mfv_neu_tau000300um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1200_20162")));
	  samples.push_back("mfv_neu_tau000300um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1600_20162")));
	  samples.push_back("mfv_neu_tau000300um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M3000_20162")));
	  samples.push_back("mfv_neu_tau001000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0200_20162")));
	  samples.push_back("mfv_neu_tau001000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0300_20162")));
	  samples.push_back("mfv_neu_tau001000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0400_20162")));
	  samples.push_back("mfv_neu_tau001000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0600_20162")));
	  samples.push_back("mfv_neu_tau001000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0800_20162")));
	  samples.push_back("mfv_neu_tau001000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1200_20162")));
	  samples.push_back("mfv_neu_tau001000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1600_20162")));
	  samples.push_back("mfv_neu_tau001000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M3000_20162")));
	  samples.push_back("mfv_neu_tau010000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0200_20162")));
	  samples.push_back("mfv_neu_tau010000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0300_20162")));
	  samples.push_back("mfv_neu_tau010000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0400_20162")));
	  samples.push_back("mfv_neu_tau010000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0600_20162")));
	  samples.push_back("mfv_neu_tau010000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0800_20162")));
	  samples.push_back("mfv_neu_tau010000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1200_20162")));
	  samples.push_back("mfv_neu_tau010000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1600_20162")));
	  samples.push_back("mfv_neu_tau010000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M3000_20162")));
	  samples.push_back("mfv_neu_tau030000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0200_20162")));
	  samples.push_back("mfv_neu_tau030000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0300_20162")));
	  samples.push_back("mfv_neu_tau030000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0400_20162")));
	  samples.push_back("mfv_neu_tau030000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0600_20162")));
	  samples.push_back("mfv_neu_tau030000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0800_20162")));
	  samples.push_back("mfv_neu_tau030000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M1200_20162")));
	  samples.push_back("mfv_neu_tau030000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M1600_20162")));
	  samples.push_back("mfv_neu_tau030000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M3000_20162")));*/

	  /*samples.push_back("mfv_stopbbarbbar_tau000100um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0300_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0400_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0800_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M1200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M1600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000100um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M3000_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0300_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0400_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0800_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M1600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau000300um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M3000_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0300_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0400_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0800_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau001000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M3000_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0300_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0400_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0800_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau010000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M3000_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0300_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0400_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0600_20162")));*/
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0800_20162")));
	  /*samples.push_back("mfv_stopbbarbbar_tau030000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1200_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1600_20162")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M3000_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0300_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0400_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0800_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000100um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M3000_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0300_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0400_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0800_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M1200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M1600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau000300um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M3000_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0300_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0400_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0800_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau001000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M3000_20162")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0300_20162")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0400_20162")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0800_20162")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau010000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0300_20162")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0400_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0400_20162")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0600_20162")));*/
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0800_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0800_20162")));
	  /*samples.push_back("mfv_stopdbardbar_tau030000um_M1200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1200_20162")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M1600_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1600_20162")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M3000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M3000_20162")));*/
	}
	else {
	  samples.push_back("qcdht0100_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0100_20162")));
	  samples.push_back("qcdht0200_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0200_20162")));
	  samples.push_back("qcdht0300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0300_20162")));
	  samples.push_back("qcdht0500_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0500_20162")));
	  samples.push_back("qcdht0700_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht0700_20162")));
	  samples.push_back("qcdht1000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht1000_20162")));
	  samples.push_back("qcdht1500_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht1500_20162")));
	  samples.push_back("qcdht2000_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdht2000_20162")));
	  samples.push_back("ttbar_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ttbar_20162")));
	  //samples.push_back("ttbar_20162");    weights.push_back(0.31);
	  //samples.push_back("qcdht0100_20162");    weights.push_back(11914.23);
	  //samples.push_back("qcdht0200_20162");    weights.push_back(1048.92);
	  //samples.push_back("qcdht0300_20162");    weights.push_back(246.00);
	  //samples.push_back("qcdht0500_20162");    weights.push_back(18.50);
	  //samples.push_back("qcdht0700_20162");    weights.push_back(5.58);
	  //samples.push_back("qcdht1000_20162");    weights.push_back(2.75);
	  //samples.push_back("qcdht1500_20162");    weights.push_back(0.37);
	  //samples.push_back("qcdht2000_20162");    weights.push_back(0.15);
	}
      }

      if (use_2017) {
	if (use_signal) {
	  //samples.push_back("ggHToSSTodddd_tau1mm_M55_2017");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau1mm_M55_2017")));
	  //samples.push_back("ggHToSSTodddd_tau10mm_M55_2017");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau10mm_M55_2017")));
	  //samples.push_back("ggHToSSTodddd_tau100mm_M55_2017");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau100mm_M55_2017")));

	  //samples.push_back("mfv_neu_tau000100um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0200_2017")));
	  //samples.push_back("mfv_neu_tau000100um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0300_2017")));
	  //samples.push_back("mfv_neu_tau000100um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0400_2017")));
	  //samples.push_back("mfv_neu_tau000100um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0600_2017")));
	  //samples.push_back("mfv_neu_tau000100um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1200_2017")));
	  //samples.push_back("mfv_neu_tau000100um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1600_2017")));
	  //samples.push_back("mfv_neu_tau000100um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M3000_2017")));
	  //samples.push_back("mfv_neu_tau000300um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0200_2017")));
	  //samples.push_back("mfv_neu_tau000300um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0300_2017")));
	  //samples.push_back("mfv_neu_tau000300um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0600_2017")));
	  //samples.push_back("mfv_neu_tau000300um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0800_2017")));
	  //samples.push_back("mfv_neu_tau000300um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1200_2017")));
	  //samples.push_back("mfv_neu_tau000300um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1600_2017")));
	  //samples.push_back("mfv_neu_tau000300um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M3000_2017")));
	  //not done samples.push_back("mfv_neu_tau001000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0200_2017")));
	  //samples.push_back("mfv_neu_tau001000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0300_2017")));
	  //samples.push_back("mfv_neu_tau001000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0400_2017")));
	  //samples.push_back("mfv_neu_tau001000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0600_2017")));
	  //samples.push_back("mfv_neu_tau001000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0800_2017")));
	  //samples.push_back("mfv_neu_tau001000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1200_2017")));
	  //samples.push_back("mfv_neu_tau001000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1600_2017")));
	  //samples.push_back("mfv_neu_tau001000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M3000_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0200_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0300_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0400_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0600_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0800_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1200_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1600_2017")));
	  //samples.push_back("mfv_neu_tau010000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M3000_2017")));
	  //samples.push_back("mfv_neu_tau030000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0200_2017")));
	  //samples.push_back("mfv_neu_tau030000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0300_2017")));
	  //samples.push_back("mfv_neu_tau030000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0400_2017")));
	  //samples.push_back("mfv_neu_tau030000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0600_2017")));
	  //samples.push_back("mfv_neu_tau030000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0800_2017")));
	  //samples.push_back("mfv_neu_tau030000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M1600_2017")));
	  //samples.push_back("mfv_neu_tau030000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M3000_2017")));

	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0300_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0400_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0800_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M1200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M3000_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0300_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0400_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0800_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M1200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M1600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M3000_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0300_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0400_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0800_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M3000_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0300_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0400_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0800_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M3000_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0300_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0400_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0600_2017")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0800_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1200_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1600_2017")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M3000_2017")));
	  ///samples.push_back("mfv_stopdbardbar_tau000100um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0300_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0400_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0600_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0800_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1600_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M3000_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0300_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0400_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0600_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0800_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M1200_2017")));
	  //not done samples.push_back("mfv_stopdbardbar_tau000300um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M3000_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0300_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0400_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0800_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1600_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M3000_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0300_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0400_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0600_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0800_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1600_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M3000_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0300_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M0400_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0400_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M0600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0600_2017")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0800_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0800_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M1200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1200_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M1600_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1600_2017")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M3000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M3000_2017")));
	}
	else {  
	  samples.push_back("ttbar_2017");      weights.push_back(std::stof(callPythonAndGetOutput("ttbar_2017")));
	  samples.push_back("qcdht0200_2017");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0200_2017"))); //No difference if removed
	  samples.push_back("qcdht0300_2017");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0300_2017"))); //little difference
	  samples.push_back("qcdht0500_2017");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0500_2017"))); //major culprit
	  samples.push_back("qcdht0700_2017");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0700_2017"))); //the major culprit
	  samples.push_back("qcdht1000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht1000_2017")));
	  samples.push_back("qcdht1500_2017");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht1500_2017")));
	  samples.push_back("qcdht2000_2017");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht2000_2017")));
	  //samples.push_back("ttbar_2017"); weights.push_back(0.27);
	  //samples.push_back("qcdht0200_2017"); weights.push_back(2954.88);
	  //samples.push_back("qcdht0300_2017"); weights.push_back(601.09);
	  //samples.push_back("qcdht0500_2017"); weights.push_back(67.95);
	  //samples.push_back("qcdht0700_2017"); weights.push_back(15.25);
	  //samples.push_back("qcdht1000_2017"); weights.push_back(8.68);
	  //samples.push_back("qcdht1500_2017"); weights.push_back(1.04);
	  //samples.push_back("qcdht2000_2017"); weights.push_back(0.43);
	}
      }

      if (use_2018) {
	if (use_signal) {
	  //samples.push_back("ggHToSSTodddd_tau1mm_M40_2018");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau1mm_M55_2018")));
          //samples.push_back("ggHToSSTodddd_tau10mm_M40_2018");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau10mm_M55_2018")));
          //samples.push_back("ggHToSSTodddd_tau100mm_M40_2018");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau100mm_M55_2018")));
	  //samples.push_back("ggHToSSTodddd_tau1mm_M55_2018");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau1mm_M55_2018")));
	  //samples.push_back("ggHToSSTodddd_tau10mm_M55_2018");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau10mm_M55_2018")));
	  //samples.push_back("ggHToSSTodddd_tau100mm_M55_2018");  weights.push_back(std::stof(callPythonAndGetOutput("ggHToSSTodddd_tau100mm_M55_2018")));

	  //samples.push_back("mfv_neu_tau000100um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0200_2018")));
	  //samples.push_back("mfv_neu_tau000100um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0300_2018")));
	  //samples.push_back("mfv_neu_tau000100um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0400_2018")));
	  //samples.push_back("mfv_neu_tau000100um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0600_2018")));
	  //samples.push_back("mfv_neu_tau000100um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M0800_2018")));
	  //samples.push_back("mfv_neu_tau000100um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1200_2018")));
	  //samples.push_back("mfv_neu_tau000100um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M1600_2018")));
	  //samples.push_back("mfv_neu_tau000100um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000100um_M3000_2018")));
	  //samples.push_back("mfv_neu_tau000300um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0200_2018")));
	  //samples.push_back("mfv_neu_tau000300um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0300_2018")));
	  //samples.push_back("mfv_neu_tau000300um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0400_2018")));
	  //samples.push_back("mfv_neu_tau000300um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M0800_2018")));
	  //samples.push_back("mfv_neu_tau000300um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1200_2018")));
	  //samples.push_back("mfv_neu_tau000300um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M1600_2018")));
	  //samples.push_back("mfv_neu_tau000300um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau000300um_M3000_2018")));
	  //samples.push_back("mfv_neu_tau001000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0300_2018")));
	  //samples.push_back("mfv_neu_tau001000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0400_2018"))); //tester
	  //samples.push_back("mfv_neu_tau001000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0600_2018")));
	  //samples.push_back("mfv_neu_tau001000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M0800_2018"))); //tester
	  //samples.push_back("mfv_neu_tau001000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1200_2018")));
	  //samples.push_back("mfv_neu_tau001000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M1600_2018")));
	  //samples.push_back("mfv_neu_tau001000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau001000um_M3000_2018")));
	  //samples.push_back("mfv_neu_tau010000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0200_2018")));
	  //samples.push_back("mfv_neu_tau010000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0300_2018")));
	  //samples.push_back("mfv_neu_tau010000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0400_2018"))); //tester
	  //samples.push_back("mfv_neu_tau010000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0600_2018")));
	  //samples.push_back("mfv_neu_tau010000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M0800_2018"))); //tester
	  //samples.push_back("mfv_neu_tau010000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1200_2018")));
	  //samples.push_back("mfv_neu_tau010000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau010000um_M1600_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0200_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0300_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0400_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0600_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M0800_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M1200_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M1600_2018")));
	  //samples.push_back("mfv_neu_tau030000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_neu_tau030000um_M3000_2018")));

	  // samples.push_back("mfv_stopbbarbbar_tau000100um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0300_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0400_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M0800_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M1200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M1600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000100um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000100um_M3000_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0300_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0400_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M0800_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M1200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M1600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau000300um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau000300um_M3000_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0300_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0400_2018"))); //tester
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M0800_2018"))); //tester
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M1600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau001000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau001000um_M3000_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0300_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0400_2018"))); //tester
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M0800_2018"))); //tester
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M1600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau010000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau010000um_M3000_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0300_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0400_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0600_2018")));
	  samples.push_back("mfv_stopbbarbbar_tau030000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M0800_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1200_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M1600_2018")));
	  //samples.push_back("mfv_stopbbarbbar_tau030000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopbbarbbar_tau030000um_M3000_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0300_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0400_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M0800_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M1600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000100um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000100um_M3000_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0300_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0400_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M0800_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M1200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M1600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau000300um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau000300um_M3000_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0300_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0400_2018"))); //tester
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M0800_2018"))); //tester
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M1600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau001000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau001000um_M3000_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0300_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0400_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0400_2018"))); //tester
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M0800_2018"))); //tester
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M1600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau010000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau010000um_M3000_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M0200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M0300_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0300_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M0600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0600_2018")));
	  samples.push_back("mfv_stopdbardbar_tau030000um_M0800_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M0800_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M1200_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1200_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M1600_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M1600_2018")));
	  //samples.push_back("mfv_stopdbardbar_tau030000um_M3000_2018"); weights.push_back(std::stof(callPythonAndGetOutput("mfv_stopdbardbar_tau030000um_M3000_2018")));
	}
	else {
	  samples.push_back("ttbar_2018");      weights.push_back(std::stof(callPythonAndGetOutput("ttbar_2018"))); //weights.push_back(0.30);
	  samples.push_back("qcdht0200_2018");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0200_2018"))); //weights.push_back(3235.19);
	  samples.push_back("qcdht0300_2018");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0300_2018"))); //weights.push_back(624.06);
	  samples.push_back("qcdht0500_2018");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0500_2018"))); //weights.push_back(73.49);
	  samples.push_back("qcdht0700_2018");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht0700_2018"))); //weights.push_back(15.73);
	  samples.push_back("qcdht1000_2018");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht1000_2018"))); //weights.push_back(9.01);
	  samples.push_back("qcdht1500_2018");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht1500_2018"))); //weights.push_back(1.00);
	  samples.push_back("qcdht2000_2018");  weights.push_back(std::stof(callPythonAndGetOutput("qcdht2000_2018"))); //weights.push_back(1.00);
	}
      }
    }
    else { //ADDING 20pc SAMPLES HERE!!!!
      if (use_2017) {
	//samples.push_back("JetHT2017B");                      weights.push_back(1);
	//samples.push_back("JetHT2017C");                      weights.push_back(1);
	//samples.push_back("JetHT2017D");                      weights.push_back(1);
	//samples.push_back("JetHT2017E");                      weights.push_back(1);
	//samples.push_back("JetHT2017F");                      weights.push_back(1);
      }
      if (use_2018) {  
	//samples.push_back("JetHT2018A");                      weights.push_back(1);
	//samples.push_back("JetHT2018B");                      weights.push_back(1);
	//samples.push_back("JetHT2018C");                      weights.push_back(1);
	//samples.push_back("JetHT2018D");                      weights.push_back(1);
      }
    }

  }
  else {
    if (p.is_mc()) {
      if (use_20161) {
	if (use_signal) {
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M40_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M40_20161")));
	  //samples.push_back("WminusHToSSTodddd_tau10mm_M40_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M40_20161")));
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M40_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M40_20161")));
	  //samples.push_back("WplusHToSSTodddd_tau10mm_M40_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M40_20161")));
	  //samples.push_back("ZHToSSTodddd_tau1mm_M40_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M40_20161")));
	  //samples.push_back("ZHToSSTodddd_tau10mm_M40_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M40_20161")));
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M55_20161")));
	  samples.push_back("WminusHToSSTodddd_tau10mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M55_20161")));
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M55_20161")));
	  samples.push_back("WplusHToSSTodddd_tau10mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M55_20161")));
	  //samples.push_back("ZHToSSTodddd_tau1mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M55_20161")));
	  samples.push_back("ZHToSSTodddd_tau10mm_M55_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M55_20161")));
	}
	else {
	  samples.push_back("dyjetstollM10_20161"); weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM10_20161"))); //weights.push_back(18.10);
	  samples.push_back("dyjetstollM50_20161"); weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM50_20161"))); //weights.push_back(1.10);
	  samples.push_back("qcdbctoept020_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept020_20161"))); //weights.push_back(831.25);
	  samples.push_back("qcdbctoept030_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept030_20161"))); //weights.push_back(906.11);
	  samples.push_back("qcdbctoept080_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept080_20161"))); //weights.push_back(99.62);
	  samples.push_back("qcdbctoept170_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept170_20161"))); //weights.push_back(6.15);
	  samples.push_back("qcdbctoept250_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept250_20161"))); //weights.push_back(1.62);
	  samples.push_back("qcdempt015_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt015_20161"))); //weights.push_back(6408.17);
	  samples.push_back("qcdempt020_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt020_20161"))); //weights.push_back(13452.91);
	  samples.push_back("qcdempt030_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt030_20161"))); //weights.push_back(34786.25);
	  samples.push_back("qcdempt050_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt050_20161"))); //weights.push_back(650179.33);
	  samples.push_back("qcdempt080_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt080_20161"))); //weights.push_back(1490.82);
	  samples.push_back("qcdempt120_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt120_20161"))); //weights.push_back(270.35);
	  samples.push_back("qcdempt170_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt170_20161"))); //weights.push_back(3411.90);
	  samples.push_back("qcdempt300_20161"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt300_20161"))); //weights.push_back(19.00);
	  samples.push_back("qcdmupt15_20161");  weights.push_back(std::stof(callPythonAndGetOutput("qcdmupt15_20161"))); //weights.push_back(541.11);
	  samples.push_back("ttbar_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ttbar_20161"))); //weights.push_back(0.17);
	  samples.push_back("wjetstolnu_0j_20161"); weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_0j_20161"))); //weights.push_back(6.82);
	  samples.push_back("wjetstolnu_1j_20161"); weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_1j_20161"))); //weights.push_back(1.05);
	  samples.push_back("wjetstolnu_2j_20161"); weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_2j_20161"))); //weights.push_back(0.74);
	  samples.push_back("ww_20161"); weights.push_back(std::stof(callPythonAndGetOutput("ww_20161"))); //weights.push_back(0.09);
	  samples.push_back("wz_20161"); weights.push_back(std::stof(callPythonAndGetOutput("wz_20161"))); //weights.push_back(0.07);
	  samples.push_back("zz_20161"); weights.push_back(std::stof(callPythonAndGetOutput("zz_20161"))); //weights.push_back(0.19);
	}
      }
            
      if (use_20162) { 
	if (use_signal) {
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M40_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M40_20162")));
	  //samples.push_back("WminusHToSSTodddd_tau10mm_M40_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M40_20162")));
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M40_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M40_20162")));
	  //samples.push_back("WplusHToSSTodddd_tau10mm_M40_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M40_20162")));
	  //samples.push_back("ZHToSSTodddd_tau1mm_M40_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M40_20162")));
	  //samples.push_back("ZHToSSTodddd_tau10mm_M40_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M40_20162")));
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M55_20162")));
	  samples.push_back("WminusHToSSTodddd_tau10mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M55_20162")));
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M55_20162")));
	  samples.push_back("WplusHToSSTodddd_tau10mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M55_20162")));
	  //samples.push_back("ZHToSSTodddd_tau1mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M55_20162")));
	  samples.push_back("ZHToSSTodddd_tau10mm_M55_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M55_20162")));
	}
	else {
	  samples.push_back("dyjetstollM10_20162"); weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM10_20162"))); //weights.push_back(11.32);
	  samples.push_back("dyjetstollM50_20162"); weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM50_20162"))); //weights.push_back(1.10);
	  samples.push_back("qcdbctoept020_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept020_20162"))); //weights.push_back(705.76);
	  samples.push_back("qcdbctoept030_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept030_20162"))); //weights.push_back(797.35);
	  samples.push_back("qcdbctoept080_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept080_20162"))); //weights.push_back(72.58);
	  samples.push_back("qcdbctoept170_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept170_20162"))); //weights.push_back(4.60);
	  samples.push_back("qcdbctoept250_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept250_20162"))); //weights.push_back(1.17);
	  samples.push_back("qcdempt015_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt015_20162"))); //weights.push_back(5582.99);
	  samples.push_back("qcdempt020_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt020_20162"))); //weights.push_back(11650.56);
	  samples.push_back("qcdempt030_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt030_20162"))); //weights.push_back(25156.70);
	  samples.push_back("qcdempt050_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt050_20162"))); //weights.push_back(6199.98);
	  samples.push_back("qcdempt080_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt080_20162"))); //weights.push_back(1298.58);
	  samples.push_back("qcdempt120_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt120_20162"))); //weights.push_back(225.78);
	  samples.push_back("qcdempt170_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt170_20162"))); //weights.push_back(151.61);
	  samples.push_back("qcdempt300_20162"); weights.push_back(std::stof(callPythonAndGetOutput("qcdempt300_20162"))); //weights.push_back(16.46);
	  samples.push_back("qcdmupt15_20162");  weights.push_back(std::stof(callPythonAndGetOutput("qcdmupt15_20162"))); //weights.push_back(456.73);
	  samples.push_back("ttbar_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ttbar_20162"))); //weights.push_back(0.16);
	  samples.push_back("wjetstolnu_0j_20162"); weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_0j_20162"))); //weights.push_back(5.60);
	  samples.push_back("wjetstolnu_1j_20162"); weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_1j_20162"))); //weights.push_back(0.89);
	  samples.push_back("wjetstolnu_2j_20162"); weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_2j_20162"))); //weights.push_back(0.66);
	  samples.push_back("ww_20162"); weights.push_back(std::stof(callPythonAndGetOutput("ww_20162"))); //weights.push_back(0.08);
	  samples.push_back("wz_20162"); weights.push_back(std::stof(callPythonAndGetOutput("wz_20162"))); //weights.push_back(0.06);
	  samples.push_back("zz_20162"); weights.push_back(std::stof(callPythonAndGetOutput("zz_20162"))); //weights.push_back(0.18);
	}
      }

      if (use_2017) {
	if (use_signal) {
	  //samples.push_back("WminusHToSSTodddd_tau100um_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau100um_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau300um_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau300um_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau3mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau3mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau10mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau30mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau30mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau100um_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau100um_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau300um_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau300um_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau3mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau3mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau10mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau30mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau30mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau100um_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau100um_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau300um_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau300um_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau3mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau3mm_M55_2017"))); //weights.push_back(1);
	  samples.push_back("WminusHToSSTodddd_tau10mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WminusHToSSTodddd_tau30mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau30mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau100um_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau100um_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau300um_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau300um_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau3mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau3mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau10mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau30mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau30mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau100um_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau100um_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau300um_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau300um_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau3mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau3mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau10mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau30mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau30mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau100um_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau100um_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau300um_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau300um_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau3mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau3mm_M55_2017"))); //weights.push_back(1);
	  samples.push_back("WplusHToSSTodddd_tau10mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("WplusHToSSTodddd_tau30mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau30mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau100um_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau100um_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau300um_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau300um_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau1mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau3mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau3mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau10mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau30mm_M15_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau30mm_M15_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau100um_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau100um_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau300um_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau300um_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau1mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau3mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau3mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau10mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau30mm_M40_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau30mm_M40_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau100um_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau100um_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau300um_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau300um_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau1mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau3mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau3mm_M55_2017"))); //weights.push_back(1);
	  samples.push_back("ZHToSSTodddd_tau10mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M55_2017"))); //weights.push_back(1);
	  //samples.push_back("ZHToSSTodddd_tau30mm_M55_2017"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau30mm_M55_2017"))); //weights.push_back(1);
	}
	else {
	  samples.push_back("dyjetstollM10_2017"); weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM10_2017")));//weights.push_back(15.45);
          samples.push_back("dyjetstollM50_2017"); weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM50_2017")));//weights.push_back(2.18);
	  samples.push_back("qcdbctoept015_2017"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept015_2017")));//weights.push_back(589.79);
	  samples.push_back("qcdbctoept020_2017"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept020_2017")));//weights.push_back(1142.48);
	  samples.push_back("qcdbctoept030_2017"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept030_2017")));//weights.push_back(1058.97);
	  samples.push_back("qcdbctoept080_2017"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept080_2017")));//weights.push_back(101.06);
	  samples.push_back("qcdbctoept170_2017"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept170_2017")));//weights.push_back(5.57);
	  samples.push_back("qcdbctoept250_2017"); weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept250_2017")));//weights.push_back(1.47);
	  samples.push_back("qcdempt020_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdempt020_2017")));//weights.push_back(14035.33);
	  samples.push_back("qcdempt030_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdempt030_2017")));//weights.push_back(29803.79);
	  samples.push_back("qcdempt050_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdempt050_2017")));//weights.push_back(7906.91);
	  samples.push_back("qcdempt080_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdempt080_2017")));//weights.push_back(4664.42);
	  samples.push_back("qcdempt120_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdempt120_2017")));//weights.push_back(300.25);
	  samples.push_back("qcdempt170_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdempt170_2017")));//weights.push_back(183.50);
	  samples.push_back("qcdempt300_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdempt300_2017")));//weights.push_back(20.24);
	  samples.push_back("qcdpt15mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt15mupt5_2017")));//weights.push_back(18680.12);
          samples.push_back("qcdpt20mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt20mupt5_2017")));//weights.push_back(1827.01);
          samples.push_back("qcdpt30mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt30mupt5_2017")));//weights.push_back(1347.09);
          samples.push_back("qcdpt50mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt50mupt5_2017")));//weights.push_back(412.17);
          samples.push_back("qcdpt80mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt80mupt5_2017")));//weights.push_back(84.36);
          samples.push_back("qcdpt120mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt120mupt5_2017")));//weights.push_back(33.29);
          samples.push_back("qcdpt170mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt170mupt5_2017")));//weights.push_back(6.18);
          samples.push_back("qcdpt300mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt300mupt5_2017")));//weights.push_back(0.43);
          samples.push_back("qcdpt470mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt470mupt5_2017")));//weights.push_back(0.06);
          samples.push_back("qcdpt600mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt600mupt5_2017")));//weights.push_back(0.02);
          samples.push_back("qcdpt800mupt5_2017");    weights.push_back(std::stof(callPythonAndGetOutput("qcdpt800mupt5_2017")));//weights.push_back(0.00);
          samples.push_back("qcdpt1000mupt5_2017");   weights.push_back(std::stof(callPythonAndGetOutput("qcdpt1000mupt5_2017")));//weights.push_back(0.00);
	  samples.push_back("ttbar_2017");         weights.push_back(std::stof(callPythonAndGetOutput("ttbar_2017")));//weights.push_back(0.14);
	  samples.push_back("wjetstolnu_0j_2017");    weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_0j_2017")));//weights.push_back(12.65);
	  samples.push_back("wjetstolnu_1j_2017");    weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_1j_2017")));//weights.push_back(2.00);
	  samples.push_back("wjetstolnu_2j_2017");    weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_2j_2017")));//weights.push_back(1.41);
	  samples.push_back("ww_2017");    weights.push_back(std::stof(callPythonAndGetOutput("ww_2017")));//weights.push_back(0.21);
	  samples.push_back("wz_2017");    weights.push_back(std::stof(callPythonAndGetOutput("wz_2017")));//weights.push_back(0.16);
	  samples.push_back("zz_2017");    weights.push_back(std::stof(callPythonAndGetOutput("zz_2017")));//weights.push_back(0.18);
	}
      }
      if (use_2018) {
	if (use_signal) {
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M40_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M40_2018")));
	  //samples.push_back("WminusHToSSTodddd_tau10mm_M40_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M40_2018")));
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M40_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M40_2018")));
	  //samples.push_back("WplusHToSSTodddd_tau10mm_M40_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M40_2018")));
	  //samples.push_back("ZHToSSTodddd_tau1mm_M40_2018"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M40_2018")));
	  //samples.push_back("ZHToSSTodddd_tau10mm_M40_2018"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M40_2018")));
	  //samples.push_back("WminusHToSSTodddd_tau1mm_M55_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau1mm_M55_2018")));
	  samples.push_back("WminusHToSSTodddd_tau10mm_M55_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WminusHToSSTodddd_tau10mm_M55_2018")));
	  //samples.push_back("WplusHToSSTodddd_tau1mm_M55_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau1mm_M55_2018")));
	  samples.push_back("WplusHToSSTodddd_tau10mm_M55_2018"); weights.push_back(std::stof(callPythonAndGetOutput("WplusHToSSTodddd_tau10mm_M55_2018")));
	  //samples.push_back("ZHToSSTodddd_tau1mm_M55_2018"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau1mm_M55_2018")));
	  samples.push_back("ZHToSSTodddd_tau10mm_M55_2018"); weights.push_back(std::stof(callPythonAndGetOutput("ZHToSSTodddd_tau10mm_M55_2018")));
	}
	else {
	  samples.push_back("dyjetstollM10_2018");   weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM10_2018"))); //weights.push_back(11.84);
          samples.push_back("dyjetstollM50_2018");   weights.push_back(std::stof(callPythonAndGetOutput("dyjetstollM50_2018"))); //weights.push_back(3.56);
	  samples.push_back("qcdbctoept015_2018");   weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept015_2018"))); //weights.push_back(671.48);
	  samples.push_back("qcdbctoept020_2018");   weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept020_2018"))); //weights.push_back(1709.18);
	  samples.push_back("qcdbctoept030_2018");   weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept030_2018"))); //weights.push_back(1912.59);
	  samples.push_back("qcdbctoept080_2018");   weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept080_2018"))); //weights.push_back(141.47);
	  samples.push_back("qcdbctoept170_2018");   weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept170_2018"))); //weights.push_back(9.93);
	  samples.push_back("qcdbctoept250_2018");   weights.push_back(std::stof(callPythonAndGetOutput("qcdbctoept250_2018"))); //weights.push_back(7.42);
	  samples.push_back("qcdempt015_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt015_2018"))); //weights.push_back(13836.45);
	  samples.push_back("qcdempt020_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt020_2018"))); //weights.push_back(20392.99);
	  samples.push_back("qcdempt030_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt030_2018"))); //weights.push_back(46444.82);
	  samples.push_back("qcdempt050_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt050_2018"))); //weights.push_back(11273.78);
	  samples.push_back("qcdempt080_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt080_2018"))); //weights.push_back(2316.50);
	  samples.push_back("qcdempt120_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt120_2018"))); //weights.push_back(410.66);
	  samples.push_back("qcdempt170_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt170_2018"))); //weights.push_back(267.03);
	  samples.push_back("qcdempt300_2018");      weights.push_back(std::stof(callPythonAndGetOutput("qcdempt300_2018"))); //weights.push_back(29.73);
	  samples.push_back("qcdmupt15_2018");   weights.push_back(std::stof(callPythonAndGetOutput("qcdmupt15_2018"))); //weights.push_back(1089.56);
	  samples.push_back("ttbar_2018");           weights.push_back(std::stof(callPythonAndGetOutput("ttbar_2018"))); //weights.push_back(0.16);
	  samples.push_back("wjetstolnu_0j_2018");   weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_0j_2018"))); //weights.push_back(20.75);
	  samples.push_back("wjetstolnu_1j_2018");   weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_1j_2018"))); //weights.push_back(4.62);
	  samples.push_back("wjetstolnu_2j_2018");   weights.push_back(std::stof(callPythonAndGetOutput("wjetstolnu_2j_2018"))); //weights.push_back(2.07);
	  samples.push_back("ww_2018");              weights.push_back(std::stof(callPythonAndGetOutput("ww_2018"))); //weights.push_back(0.54);
	  samples.push_back("wz_2018");              weights.push_back(std::stof(callPythonAndGetOutput("wz_2018"))); //weights.push_back(1.35);
	  samples.push_back("zz_2018");              weights.push_back(std::stof(callPythonAndGetOutput("zz_2018"))); //weights.push_back(0.21);
	}
      }  
    }
    else {
      if (use_20161) {
	//samples.push_back("Lepton_data_20161_20pc");   weights.push_back(1);
	samples.push_back("SingleMuon20161B_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon20161C_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon20161D_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon20161E_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon20161F_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20161B_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20161C_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20161D_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20161E_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20161F_20pc");    weights.push_back(1);
      }
      if (use_20162) {
	//samples.push_back("Lepton_data_20162_20pc");   weights.push_back(1);
	samples.push_back("SingleMuon20162F_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon20162G_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon20162H_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20162F_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20162G_20pc");    weights.push_back(1);
        samples.push_back("SingleElectron20162H_20pc");    weights.push_back(1);
      }
      if (use_2017) {
	//samples.push_back("Lepton_data_2017_20pc");    weights.push_back(1);
	samples.push_back("SingleElectron2017B_20pc");    weights.push_back(1);
	samples.push_back("SingleElectron2017D_20pc");    weights.push_back(1);
	samples.push_back("SingleElectron2017F_20pc");    weights.push_back(1);
	samples.push_back("SingleMuon2017D_20pc");        weights.push_back(1);
	samples.push_back("SingleMuon2017F_20pc");        weights.push_back(1);
	samples.push_back("SingleElectron2017C_20pc");    weights.push_back(1);
	samples.push_back("SingleElectron2017E_20pc");    weights.push_back(1);
	samples.push_back("SingleMuon2017C_20pc");        weights.push_back(1);
	samples.push_back("SingleMuon2017E_20pc");        weights.push_back(1);
      }
      if (use_2018) {
	//samples.push_back("Lepton_data_2018_20pc");    weights.push_back(1);
	samples.push_back("SingleMuon2018A_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon2018B_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon2018C_20pc");    weights.push_back(1);
        samples.push_back("SingleMuon2018D_20pc");    weights.push_back(1);
        samples.push_back("EGamma2018A_20pc");    weights.push_back(1);
        samples.push_back("EGamma2018B_20pc");    weights.push_back(1);
        samples.push_back("EGamma2018C_20pc");    weights.push_back(1);
        samples.push_back("EGamma2018D_20pc");    weights.push_back(1);
      }
    }

  }
  //end of adding sample weights to samples vector

  //Only uses vertices with the number of tracks defined by ntracks by taking data from the appropriate MiniTree
  const char* tree_path; int min_ntracks0 = 0; int max_ntracks0 = 1000000; int min_ntracks1 = 0; int max_ntracks1 = 1000000;
  if (p.ntracks() == 3)      { tree_path = "mfvMiniTreeNtk3/t"; }
  else if (p.ntracks() == 4) { tree_path = "mfvMiniTreeNtk4/t"; }
  else if (p.ntracks() == 5) { tree_path = "mfvMiniTree/t"; }
  else if (p.ntracks() == 7) { tree_path = "mfvMiniTreeNtk3or4/t"; min_ntracks0 = 4; max_ntracks0 = 4; min_ntracks1 = 3; max_ntracks1 = 3; }
  else if (p.ntracks() == 8) { tree_path = "mfvMiniTreeNtk3or5/t"; min_ntracks0 = 5; max_ntracks0 = 5; min_ntracks1 = 3; max_ntracks1 = 3; }
  else if (p.ntracks() == 9) { tree_path = "mfvMiniTreeNtk4or5/t"; min_ntracks0 = 5; max_ntracks0 = 5; min_ntracks1 = 4; max_ntracks1 = 4; }
  else { fprintf(stderr, "bad ntracks"); exit(1); }

  double dphi_pdf_c; double dphi_pdf_e = 2; double dphi_pdf_a; //deltaphi input
  /*if (p.is_mc()) {
    if      (p.year() == "20161")        { dphi_pdf_c = 1.22; dphi_pdf_a = 2.63; }
    else if (p.year() == "20162")        { dphi_pdf_c = 1.22; dphi_pdf_a = 2.54; }
    else if (p.year() == "20162")         { dphi_pdf_c = 1.22; dphi_pdf_a = 2.73; }
    else if (p.year() == "2017")         { dphi_pdf_c = 1.24; dphi_pdf_a = 4.86; }
    else if (p.year() == "2018")         { dphi_pdf_c = 1.38; dphi_pdf_a = 3.77; }
    else if (p.year() == "2017p8" or p.year() == "run2")  { dphi_pdf_c = 1.23; dphi_pdf_a = 4.18; }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else if (p.only_20pc()) {
    if (p.year() == "2017")         { dphi_pdf_c = 1.34; dphi_pdf_a = 5.44; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.25; dphi_pdf_a = 6.21; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.30; dphi_pdf_a = 5.78; }
    else if (p.year() == "2017B")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017C")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017D")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017E")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017F")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else {
    if (p.year() == "2017")         { dphi_pdf_c = 1.31; dphi_pdf_a = 5.91; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.30; dphi_pdf_a = 6.01; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.31; dphi_pdf_a = 5.96; }
    else { fprintf(stderr, "bad year"); exit(1); }
  }*/

  const char* vpeffs_version; //efficiency input
  if (p.only_20pc()) {
    vpeffs_version = "ULV11Bm";
  } else {
    vpeffs_version = "ULV11Bm";
  }
  //TString eff_file_name_2d = TString::Format("/afs/cern.ch/user/p/pekotamn/crabdirs/vpeffs%s_%s_%s%s.root", p.is_mc() ? "" : "_data", p.year().c_str(), vpeffs_version, p.vary_eff() ? "_ntkseeds" : "");
  //TString eff_file_name_2d = TString::Format("/uscms/home/alecduqu/mfv_ScaleFactors/src/JMTucker/MFVNeutralino/test/One2Two/vpeffs%s_%s_%s%s.root", p.is_mc() ? "" : "_data", p.year().c_str(), vpeffs_version, p.vary_eff() ? "_ntkseeds" : "");
  TString eff_file_name_2d = TString::Format("./vpeffsd2d%s_%s_%s%s.root", p.is_mc() ? "" : "_data", p.year().c_str(), vpeffs_version, p.vary_eff() ? "_ntkseeds" : "");
  TString eff_file_name_3d = TString::Format("./vpeffs%s_%s_%s%s.root", p.is_mc() ? "" : "_data", p.year().c_str(), vpeffs_version, p.vary_eff() ? "_ntkseeds" : "");
  TString jet_angle_fname = TString::Format("background_lw_2017.root"); //This is not ultimately used anywhere

  const char* eff_hist = "maxtk3";
  if (p.vary_eff()) {
    if (p.ntracks() == 3)      { eff_hist = "maxtk3"; }
    else if (p.ntracks() == 4) { eff_hist = "maxtk4"; }
    else if (p.ntracks() == 5) { eff_hist = "maxtk5"; }
    else                       { eff_hist = "maxtk3"; }
  }


  gRandom->SetSeed(12191982);

  //fill only-one-vertex dBV distribution
  TH1D* h_1v_dbv = new TH1D("h_1v_dbv", "only-one-vertex events;d_{BV} (cm);events", 200, 0, 2.0); //was 1250, 0, 2.5
  TH1D* h_1v_dbv_npult20 = new TH1D("h_1v_dbv_npult20", "only-one-vertex events;d_{BV} (cm);events", 200, 0, 2.0);
  TH1D* h_1v_dbv_npugt20lt30 = new TH1D("h_1v_dbv_npugt20lt30", "only-one-vertex events;d_{BV} (cm);events", 200, 0, 2.0);
  TH1D* h_1v_dbv_npugt30lt40 = new TH1D("h_1v_dbv_npugt30lt40", "only-one-vertex events;d_{BV} (cm);events", 200, 0, 2.0);
  TH1D* h_1v_dbv_npugt40 = new TH1D("h_1v_dbv_npugt40", "only-one-vertex events;d_{BV} (cm);events", 200, 0, 2.0);
  TH1D* h_1v_bs2derr = new TH1D("h_1v_bs2derr", "#sigma(dist2d(SV, beamspot)) (cm)", 100, 0, 0.005); //Alec added
  TH1D* h_1v_rescale_bs2derr = new TH1D("h_1v_rescale_bs2derr", "rescaled #sigma(dist2d(SV, beamspot)) (cm)", 100, 0, 0.005); //Alec added
  TH1D* h_1v_w = new TH1D("h_1v__w", ";event weight;events", 100, 0, 10); //Alec added
  TH2D* h_1v_xy  = new TH2D("h_1v_xy", "only-one-vertex events;x0 (cm);y0 (cm)", 250, -1.0, 1.0, 250, -1.0, 1.0);
  TH1D* h_1v_z = new TH1D("h_1v_z", ";z (cm);events", 250, -1, 1); //Alec added
  TH1D* h_1v_dz = new TH1D("h_1v_dz", ";z distance from pv to sv (cm);events", 250, -1, 1); //Alec added
  TH1D* h_1v_dbv0 = new TH1D("h_1v_dbv0", "only-one-vertex events;d_{BV}^{0} (cm);events", 1000, 0, 2.0);
  TH1D* h_1v_dbv1 = new TH1D("h_1v_dbv1", "only-one-vertex events;d_{BV}^{1} (cm);events", 1000, 0, 2.0);
  TH2D* h_1v_dbv_dz = new TH2D("h_1v_dbv_dz", "only-one-vertex events;d_{BV} (cm); d_{z} (cm)", 1000, 0, 2.0, 1000, 0, 2.0);
  TH2D* h_1v_dbv_bs2derr = new TH2D("h_1v_dbv_bs2derr", "only-one-vertex events;d_{BV} (cm); #sigma(dist2d(SV, beamspot)) (cm)", 1000, 0, 2.0, 100, 0, 0.005); //Alec added
  TH1F* h_1v_phiv = new TH1F("h_1v_phiv", "only-one-vertex events;vertex #phi;events", 50, -3.15, 3.15);
  TH1D* h_1v_npu = new TH1D("h_1v_npu", "only-one-vertex events;# PU interactions;events", 100, 0, 100);
  TH1F* h_1v_njets = new TH1F("h_1v_njets", "only-one-vertex events;number of jets;events", 20, 0, 20);
  TH1F* h_1v_ht40 = new TH1F("h_1v_ht40", "only-one-vertex events;H_{T} of jets with p_{T} > 40 GeV;events", 200, 0, 5000);
  TH1F* h_1v_phij = new TH1F("h_1v_phij", "only-one-vertex events;jets #phi;jets", 50, -3.15, 3.15);
  TH1F* h_1v_dphijj = new TH1F("h_1v_dphijj", "only-one-vertex events;#Delta#phi_{JJ};jet pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijv = new TH1F("h_1v_dphijv", "only-one-vertex events;#Delta#phi_{JV};jet-vertex pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijvpt = new TH1F("h_1v_dphijvpt", "only-one-vertex events;p_{T}-weighted #Delta#phi_{JV};jet-vertex pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijvmin = new TH1F("h_1v_dphijvmin", "only-one-vertex events;#Delta#phi_{JV}^{min};events", 50, 0, 3.1416);
  TH1F* h_1v_costh2_onlytks0 = new TH1F("h_1v_costh2_onlytks0", "only-one-vertex events;cos(angle2{flight,momentum}) (only tracks, no jets);events", 302, -1.001, 1.001); //Alec added
  TH1F* h_1v_costh20 = new TH1F("h_1v_costh20", "only-one-vertex events;cos(angle2{flight,momentum});events", 302, -1.001, 1.001); //Alec added, we don't want bins wider than 0.0075 due to granularity
  TH1F* h_2v_dbv = new TH1F("h_2v_dbv", "two-vertex events;d_{BV} (cm);vertices", 1250, 0, 2.5);
  TH2F* h_2v_dbv1_dbv0 = new TH2F("h_2v_dbv1_dbv0", "two-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 1250, 0, 2.5, 1250, 0, 2.5);
  TH1F* h_2v_dvv = new TH1F("h_2v_dvv", "two-vertex events;d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_2v_dvv3D = new TH1F("h_2v_dvv3D", "two-vertex events;3D d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_2v_sumdbv = new TH1F("h_2v_sumdbv", "two-vertex events; #Sigma(d_{BV})  (cm);events", 200, 0., 4.0); //was 100, 0, 4.0
  TH1F* h_2v_dphivv = new TH1F("h_2v_dphivv", "two-vertex events;#Delta#phi_{VV};events", 10, -3.15, 3.15);
  TH1F* h_2v_absdphivv = new TH1F("h_2v_absdphivv", "two-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1D* h_2v_npu = new TH1D("h_2v_npu", "two-vertex events;# PU interactions;events", 100, 0, 100);
  //checkpoint
  std::vector<double>  dbv_value_vector; //background template construction npu correction: define vectors for making a list of dbv values and errors
  std::vector<double>  z_value_vector;
  //std::vector<double>  dbv_value_vector_npult20;
  //std::vector<double>  dbv_value_vector_npugt20lt30;
  //std::vector<double>  dbv_value_vector_npugt30lt40;
  //std::vector<double>  dbv_value_vector_npugt40;
  std::vector<double>  dbv_weight_vector;
  //std::vector<double>  dbv_weight_vector_npult20;
  //std::vector<double>  dbv_weight_vector_npugt20lt30;
  //std::vector<double>  dbv_weight_vector_npugt30lt40;
  //std::vector<double>  dbv_weight_vector_npugt40;
  std::vector<int>  dbv_npubinid_vector;

  std::vector<double>  dbv_value_vector_btag_npult20;
  std::vector<double>  dbv_value_vector_btag_npugt20lt30;
  std::vector<double>  dbv_value_vector_btag_npugt30lt40;
  std::vector<double>  dbv_value_vector_btag_npugt40;
  std::vector<double>  dbv_value_vector_nobtag_npult20;
  std::vector<double>  dbv_value_vector_nobtag_npugt20lt30;
  std::vector<double>  dbv_value_vector_nobtag_npugt30lt40;
  std::vector<double>  dbv_value_vector_nobtag_npugt40;

  std::vector<double>  z_value_vector_btag_npult20;
  std::vector<double>  z_value_vector_btag_npugt20lt30;
  std::vector<double>  z_value_vector_btag_npugt30lt40;
  std::vector<double>  z_value_vector_btag_npugt40;
  std::vector<double>  z_value_vector_nobtag_npult20;
  std::vector<double>  z_value_vector_nobtag_npugt20lt30;
  std::vector<double>  z_value_vector_nobtag_npugt30lt40;
  std::vector<double>  z_value_vector_nobtag_npugt40;

  std::vector<double>  dbv_weight_vector_btag_npult20;
  std::vector<double>  dbv_weight_vector_btag_npugt20lt30;
  std::vector<double>  dbv_weight_vector_btag_npugt30lt40;
  std::vector<double>  dbv_weight_vector_btag_npugt40;
  std::vector<double>  dbv_weight_vector_nobtag_npult20;
  std::vector<double>  dbv_weight_vector_nobtag_npugt20lt30;
  std::vector<double>  dbv_weight_vector_nobtag_npugt30lt40;
  std::vector<double>  dbv_weight_vector_nobtag_npugt40;

  std::vector<std::vector<reco::TransientTrack>> reco_vertices;
  std::vector<int> reco_vertices_ntk;
  double bssigma_x = 0.5; //FIX THESE LATER                                                                                                                                  
  double bssigma_y = 0.5;
  double bssigma_z = 0.5;

  //loops over each sample defined above 
  int ns = (int)samples.size();
  for (int i = 0; i < ns; ++i) {
    mfv::MiniNtuple nt;
    TString iteration_sample_name = samples[i];
    TString fn;
    if (iteration_sample_name.Contains("20161")) {fn = TString::Format("%s/%s.root", file_path_20161, samples[i]);}
    if (iteration_sample_name.Contains("20162")) {fn = TString::Format("%s/%s.root", file_path_20162, samples[i]);}
    if (iteration_sample_name.Contains("2017")) {fn = TString::Format("%s/%s.root", file_path_2017, samples[i]);}
    if (iteration_sample_name.Contains("2018")) {fn = TString::Format("%s/%s.root", file_path_2018, samples[i]);}
    //TString fn = TString::Format("%s/%s.root", file_path, samples[i]);
    std::cout << fn.Data() << "\n";
    TFile* f = TFile::Open(fn);
    if (!f || !f->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }

    std::cout << tree_path << std::endl;
    TTree* t = (TTree*)f->Get(tree_path);
    if (!t) { fprintf(stderr, "bad tree"); exit(1); }

    // Tight WP of DeepJet
    float bdisc_cut_value = 0;

    std::string st_name = samples[i];

    // 20161 must come before 2016 in these conditionals, values from BTagging.cc
    if (st_name.find("20161") != std::string::npos) {
      //bdisc_cut_value = 0.0508; //loose
      //bdisc_cut_value = 0.2598; //medium
      bdisc_cut_value = 0.6502; //tight, originally used
    } 
    else if (st_name.find("20162") != std::string::npos) {
      //bdisc_cut_value = 0.0480; //loose
      //bdisc_cut_value = 0.2489;
      bdisc_cut_value = 0.6377; //tight, originally used
    } 
    else if (st_name.find("2017") != std::string::npos) {
      //bdisc_cut_value = 0.0532; //loose
      //bdisc_cut_value = 0.3040;
      bdisc_cut_value = 0.7476; //tight, originally used
    } 
    else if (st_name.find("2018") != std::string::npos) {
      //bdisc_cut_value = 0.0490; //loose
      //bdisc_cut_value = 0.2783;
      bdisc_cut_value = 0.7100; //tight, originally used
    } 
    //std::cout << "b discrimination value: " << bdisc_cut_value << std::endl;
    mfv::read_from_tree(t, nt);
    //std::cout << "read from minitree" << std::endl;
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;
      //if (nt.rescale_bs2derr0 > 0.0035) continue; //Alec added, bs2derr cut normally .005cm in MFVNeutralino/python/VertexSelector_cfi.py, but we can further constrain here
      //if (nt.rescale_bs2derr1 > 0.0035) continue; //Alec added
      if ((p.bquarks() == 0 && nt.gen_flavor_code == 2) || (p.bquarks() == 1 && nt.gen_flavor_code != 2)) continue;
      //if ((p.btags() == 0 && nt.nbtags(bdisc_cut_value,-1) >= 1) || (p.btags() == 1 && nt.nbtags(bdisc_cut_value,-1) < 1)) continue; //nbtags calls CSV we want DeepJet, see MiniNtuple.h
      if ((p.btags() == 0 && nt.nbtags_old(bdisc_cut_value,-1) >= 1) || (p.btags() == 1 && nt.nbtags_old(bdisc_cut_value,-1) < 1)) continue; //nbtags_old correctly calls DeepJet
      if (nt.npu < p.min_npu() || nt.npu > p.max_npu()) continue;
      //std::cout << "established cuts" << std::endl;
      const float w = weights[i] * nt.weight; //THIS IS WHERE THE WEIGHTS ARE APPLIED
      //std::cout << "sample weight: " << weights[i] << ", event weight: " << nt.weight << std::endl;

      double v0_track_sumpt = 0; //start of sumpt & m5 variables for cuts
      double v1_track_sumpt = 0;
      //double v0_track_sump = 0;
      double v0_track_sumpx = 0;
      double v0_track_sumpy = 0;
      double v0_track_sumpz = 0;
      double v0_track_sumE = 0;
      double v0_track_m5 = 0;
      //double v1_track_sump = 0;
      double v1_track_sumpx = 0;
      double v1_track_sumpy = 0;
      double v1_track_sumpz = 0;
      double v1_track_sumE = 0;
      double v1_track_m5 = 0; //end of sumpt & m5 variable for cuts
      if (nt.nvtx == 1) {
	//std::cout << "1-vertex event" << std::endl;
	//start of sumpt & m5 cut

	//std::cout << "before initializing reco variables" << std::endl;
	std::vector<reco::TransientTrack> seed_tracks;
	//std::map<reco::TrackRef, size_t> seed_track_ref_map;
	reco::TrackCollection track_collection;
	reco::Track reco_track;
	reco::TrackBase::Point referencePoint; //track's closest point of approach to the center of CMS
	math::XYZVector track_p_vector;
	//std::cout << "after initializing reco variables" << std::endl;
	int track_q;
	//std::vector<double> B_field(0,0,3.8);
	GlobalVector constantField(0.0, 0.0, 3.8);
	UniformMagneticField uniformField(constantField);
	const MagneticField* B_field = &uniformField;
	for (int k = 0; k < nt.ntk0; ++k) {
	  //std::cout << "beginning of loop for sumpt & m5 cut, " << nt.tk0_px[1] << std::endl;
	  v0_track_sumpt += sqrt(nt.p_tk0_px->at(k)*nt.p_tk0_px->at(k) + nt.p_tk0_py->at(k)*nt.p_tk0_py->at(k));
	  //std::cout << "added track pt to sumpt" << std::endl;
	  //v0_track_sump += sqrt(nt.p_tk0_px->at(k)*nt.p_tk0_px->at(k) + nt.p_tk0_py->at(k)*nt.p_tk0_py->at(k) + nt.p_tk0_pz->at(k)*nt.p_tk0_pz->at(k));
	  v0_track_sumpx += nt.p_tk0_px->at(k);
	  v0_track_sumpy += nt.p_tk0_py->at(k);
	  v0_track_sumpz += nt.p_tk0_pz->at(k);
	  v0_track_sumE += sqrt(nt.p_tk0_px->at(k)*nt.p_tk0_px->at(k) + nt.p_tk0_py->at(k)*nt.p_tk0_py->at(k) + nt.p_tk0_pz->at(k)*nt.p_tk0_pz->at(k) + 0.13957*0.13957); //0.13957 is pi+- mass
	  if (c1v_vertexer and j == 0) {
	    //FINISH HERE FOR THE VERTEXER ON CONSTRUCTED C1V EVENTS!!!!!!!!!
	    referencePoint = reco::TrackBase::Point(nt.p_tk0_vx->at(k),nt.p_tk0_vy->at(k),nt.p_tk0_vz->at(k));
	    track_p_vector = math::XYZVector(nt.p_tk0_px->at(k), nt.p_tk0_py->at(k), nt.p_tk0_pz->at(k));
	    reco_track = reco::Track(fabs(nt.p_tk0_qchi2->at(k)), nt.p_tk0_ndof->at(k), referencePoint, track_p_vector, sgn(nt.p_tk0_qchi2->at(k)), nt.p_tk0_cov->at(k));
	    track_collection.push_back(reco_track);
	    seed_tracks.push_back(reco::TransientTrack(reco_track, B_field));
	    //seed_track_ref_map[k] = seed_tracks.size() - 1;
	  }
	}
	if (c1v_vertexer and j == 0) std::cout << "finished looping through tracks" << std::endl;
	v0_track_m5 = sqrt(v0_track_sumE*v0_track_sumE - v0_track_sumpx*v0_track_sumpx - v0_track_sumpy*v0_track_sumpy - v0_track_sumpz*v0_track_sumpz);
	if (v0_track_sumpt < 10) continue;
	if (v0_track_m5 < 5.5) continue; //Alec added SUMPT & m5 CUT, this will not be needed once implemented in minitree step

	if (c1v_vertexer and j == 0) { //test of the revertexer
	  std::cout << "start of assigning track vectors that we will plug into produce()" << std::endl;
	  const size_t ntk = seed_tracks.size();
	  reco_vertices.push_back(seed_tracks);
	  reco_vertices_ntk.push_back(ntk);
	  std::cout << "finished assigning track vectors that we will plug into produce()" << std::endl;
	  double bsx = nt.bsx;
	  double bsy = nt.bsy;
	  double bsz = nt.bsz;
	  std::vector<double> bs_position = {bsx,bsy,bsz};
	  //double bssigma_x = 0.5; //FIX THESE LATER
	  //double bssigma_y = 0.5;
	  //double bssigma_z = 0.5;
	  std::cout << "pt of first track of first vertex before revertexing: " << seed_tracks[0].track().pt() << std::endl;
	  produce(bs_position, bssigma_x, bssigma_y, bssigma_z, seed_tracks, track_collection);
	}
	
	//std::cout << "finished sumpt and m5 cut" << std::endl;
        float temp_dbv      = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
        //float temp_dbv      = sqrt((nt.x0-nt.bsx)*(nt.x0-nt.bsx) + (nt.y0-nt.bsy)*(nt.y0-nt.bsy));
        float temp_dbv_pv   = sqrt((nt.x0-nt.pvx)*(nt.x0-nt.pvx) + (nt.y0-nt.pvy)*(nt.y0-nt.pvy));

	dbv_value_vector.push_back(temp_dbv);
	z_value_vector.push_back(nt.z0-nt.pvz);
	dbv_weight_vector.push_back(w);

	/*if (temp_dbv > 0.6 and tree_path == "mfvMiniTree/t") {
	  std::cout<< "dbv > 0.6 1-vertex event in btag=" << p.btags() << " category!" <<std::endl;
	  std::cout << "dbv: " << temp_dbv << ", run: " << nt.run << ", lumi: " << nt.lumi << ", event: " << nt.event << std::endl;
	}*/
	//std::cout << "starting npu and btag binning" << std::endl;
        h_1v_dbv->Fill(temp_dbv, w);
	//background template construction npu correction: assign dbv values to bins in npu for dbv pairing later
	/*if (nt.npu <= 20) {
	  h_1v_dbv_npult20->Fill(temp_dbv, w);
	  dbv_value_vector_npult20.push_back(temp_dbv);
	  dbv_weight_vector_npult20.push_back(w);
	  //dbv_npubinid_vector.push_back(1);
	}
	else if (nt.npu > 20 and nt.npu <= 30) {
	  h_1v_dbv_npugt20lt30->Fill(temp_dbv, w);
	  dbv_value_vector_npugt20lt30.push_back(temp_dbv);
          dbv_weight_vector_npugt20lt30.push_back(w);
	  //dbv_npubinid_vector.push_back(2);
	}
	else if (nt.npu > 30 and nt.npu <= 40) {
          h_1v_dbv_npugt30lt40->Fill(temp_dbv, w);
	  dbv_value_vector_npugt30lt40.push_back(temp_dbv);
          dbv_weight_vector_npugt30lt40.push_back(w);
	  //dbv_npubinid_vector.push_back(3);
        }
	else {
          h_1v_dbv_npugt40->Fill(temp_dbv, w);
	  dbv_value_vector_npugt40.push_back(temp_dbv);
          dbv_weight_vector_npugt40.push_back(w);
	  //dbv_npubinid_vector.push_back(4);
        }*/
	//background template construction npu correction: assign dbv values to bins in npu now also for with btagging
	//if (j<10) {
	//  std::cout << "npu: " << nt.npu << ", p.btags: " << p.btags() << std::endl;
	//}
	if (nt.npu <= 20 and nt.nbtags_old(bdisc_cut_value,-1) >= 1) { //originally used nt.nbtags but this calls CSV, we want DeepJet which is called by nt.nbtags_old
          dbv_value_vector_btag_npult20.push_back(temp_dbv);
	  z_value_vector_btag_npult20.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_btag_npult20.push_back(w);
          dbv_npubinid_vector.push_back(1);
        }
        else if (nt.npu > 20 and nt.npu <= 30 and nt.nbtags_old(bdisc_cut_value,-1) >= 1) {
          dbv_value_vector_btag_npugt20lt30.push_back(temp_dbv);
	  z_value_vector_btag_npugt20lt30.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_btag_npugt20lt30.push_back(w);
          dbv_npubinid_vector.push_back(2);
        }
        else if (nt.npu > 30 and nt.npu <= 40 and nt.nbtags_old(bdisc_cut_value,-1) >= 1) {
          dbv_value_vector_btag_npugt30lt40.push_back(temp_dbv);
	  z_value_vector_btag_npugt30lt40.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_btag_npugt30lt40.push_back(w);
          dbv_npubinid_vector.push_back(3);
        }
        else if (nt.npu > 40 and nt.nbtags_old(bdisc_cut_value,-1) >= 1) {
          dbv_value_vector_btag_npugt40.push_back(temp_dbv);
	  z_value_vector_btag_npugt40.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_btag_npugt40.push_back(w);
          dbv_npubinid_vector.push_back(4);
        }
	else if (nt.npu <= 20 and nt.nbtags_old(bdisc_cut_value,-1) < 1) {
          dbv_value_vector_nobtag_npult20.push_back(temp_dbv);
	  z_value_vector_nobtag_npult20.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_nobtag_npult20.push_back(w);
          dbv_npubinid_vector.push_back(5);
        }
        else if (nt.npu > 20 and nt.npu <= 30 and nt.nbtags_old(bdisc_cut_value,-1) < 1) {
          dbv_value_vector_nobtag_npugt20lt30.push_back(temp_dbv);
	  z_value_vector_nobtag_npugt20lt30.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_nobtag_npugt20lt30.push_back(w);
          dbv_npubinid_vector.push_back(6);
        }
        else if (nt.npu > 30 and nt.npu <= 40 and nt.nbtags_old(bdisc_cut_value,-1) < 1) {
          dbv_value_vector_nobtag_npugt30lt40.push_back(temp_dbv);
	  z_value_vector_nobtag_npugt30lt40.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_nobtag_npugt30lt40.push_back(w);
          dbv_npubinid_vector.push_back(7);
        }
        else if (nt.npu > 40 and nt.nbtags_old(bdisc_cut_value,-1) < 1) {
          dbv_value_vector_nobtag_npugt40.push_back(temp_dbv);
	  z_value_vector_nobtag_npugt40.push_back(nt.z0-nt.pvz);
          dbv_weight_vector_nobtag_npugt40.push_back(w);
          dbv_npubinid_vector.push_back(8);
        }

	h_1v_bs2derr->Fill(nt.bs2derr0, w);
	h_1v_rescale_bs2derr->Fill(nt.rescale_bs2derr0, w);
	h_1v_w->Fill(nt.weight);
	h_1v_z->Fill(nt.z0, w);
	h_1v_dz->Fill(nt.z0 - nt.pvz, w);
        h_1v_xy->Fill(nt.x0, nt.y0, w);
	h_1v_dbv_bs2derr->Fill(temp_dbv, nt.bs2derr0, w);

	//const TVector3 pv = nt.pvs().pos(0);
	//const TVector3 pos = nt.svs().pos(isv);
	//const TVector3 flight = pos - pv;
	//const TVector3 flight2(flight.X(), flight.Y(), 0);
	//edm::Handle<MFVVertexAuxCollection> vertices; //Alec work in progress
	//const MFVVertexAux& v0 = vertices->at(0);
	//const TVector3 flight2(nt.x0, nt.y0, 0);
	//const TLorentzVector p4 = nt.p4();
	//const TVector3 pperp(p4.X(), p4.Y(), 0);
	//const double costh2 = pperp.Unit().Dot(flight2.Unit());
	//float double costh2 = nt.costhtksjetsntkmombs0.push_back(v0.costhmombs(mfv::PTracksPlusJetsByNtracks));
	float costh2_onlytks0 = nt.costhtkonlymombs0;
	float costh20 = nt.costhtksjetsntkmombs0;
	//std::cout << "cos of the angle between displacement and momentum: " << costh20 << std::endl;
	h_1v_costh2_onlytks0->Fill(nt.costhtkonlymombs0, w);
	h_1v_costh20->Fill(nt.costhtksjetsntkmombs0, w);
        
	if (nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0) h_1v_dbv0->Fill(temp_dbv_pv, w);
	if (nt.ntk0 >= min_ntracks1 && nt.ntk0 <= max_ntracks1) h_1v_dbv1->Fill(temp_dbv_pv, w);
	h_1v_phiv->Fill(atan2(nt.y0,nt.x0), w);
	h_1v_npu->Fill(nt.npu, w);
	h_1v_njets->Fill(nt.njets, w);
	h_1v_ht40->Fill(nt.ht(40.), w);
        double dphijvmin = M_PI;
        for (int k = 0; k < nt.njets; ++k) {
          h_1v_phij->Fill(nt.jet_phi[k], w);
          h_1v_dphijv->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w);
          h_1v_dphijvpt->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w * (nt.jet_pt[k]/nt.ht(0.)));
          if (fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k])) < dphijvmin) dphijvmin = fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]));
          for (int l = k+1; l < nt.njets; ++l) {
            h_1v_dphijj->Fill(TVector2::Phi_mpi_pi(nt.jet_phi[k] - nt.jet_phi[l]), w);
          }
        }
        h_1v_dphijvmin->Fill(dphijvmin, w);
      }

      if (nt.nvtx >= 2 && nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0 && nt.ntk1 >= min_ntracks1 && nt.ntk1 <= max_ntracks1) {
	//std::cout << "2-vertex event" << std::endl;
	//start of sumpt & m5 cut
	
        for (int k = 0; k < nt.ntk0; ++k) {
          v0_track_sumpt += sqrt(nt.p_tk0_px->at(k)*nt.p_tk0_px->at(k) + nt.p_tk0_py->at(k)*nt.p_tk0_py->at(k));
	  //v0_track_sump += sqrt(nt.p_tk0_px->at(k)*nt.p_tk0_px->at(k) + nt.p_tk0_py->at(k)*nt.p_tk0_py->at(k) + nt.p_tk0_pz->at(k)*nt.p_tk0_pz->at(k));
	  v0_track_sumpx += nt.p_tk0_px->at(k);
          v0_track_sumpy += nt.p_tk0_py->at(k);
          v0_track_sumpz += nt.p_tk0_pz->at(k);
          v0_track_sumE += sqrt(nt.p_tk0_px->at(k)*nt.p_tk0_px->at(k) + nt.p_tk0_py->at(k)*nt.p_tk0_py->at(k) + nt.p_tk0_pz->at(k)*nt.p_tk0_pz->at(k) + 0.1396*0.1396);
        }
	for (int l = 0; l < nt.ntk1; ++l) {
          v1_track_sumpt += sqrt(nt.p_tk1_px->at(l)*nt.p_tk1_px->at(l) + nt.p_tk1_py->at(l)*nt.p_tk1_py->at(l));
	  //v1_track_sump += sqrt(nt.p_tk1_px->at(l)*nt.p_tk1_px->at(l) + nt.p_tk1_py->at(l)*nt.p_tk1_py->at(l) + nt.p_tk1_pz->at(l)*nt.p_tk1_pz->at(l));
	  v1_track_sumpx += nt.p_tk1_px->at(l);
          v1_track_sumpy += nt.p_tk1_py->at(l);
          v1_track_sumpz += nt.p_tk1_pz->at(l);
          v1_track_sumE += sqrt(nt.p_tk1_px->at(l)*nt.p_tk1_px->at(l) + nt.p_tk1_py->at(l)*nt.p_tk1_py->at(l) + nt.p_tk1_pz->at(l)*nt.p_tk1_pz->at(l) + 0.1396*0.1396);
        }
	v0_track_m5 = sqrt(v0_track_sumE*v0_track_sumE - v0_track_sumpx*v0_track_sumpx - v0_track_sumpy*v0_track_sumpy - v0_track_sumpz*v0_track_sumpz);
	v1_track_m5 = sqrt(v1_track_sumE*v1_track_sumE - v1_track_sumpx*v1_track_sumpx - v1_track_sumpy*v1_track_sumpy - v1_track_sumpz*v1_track_sumpz);
        if (v0_track_sumpt < 10 || v1_track_sumpt < 10) continue;
	if (v0_track_m5 < 5.5 || v1_track_m5 < 5.5) continue;  //Alec added SUMPT & m5 CUT, this will not be needed once implemented in minitree step
	
        double dbv0 = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
        double dbv1 = sqrt(nt.x1*nt.x1 + nt.y1*nt.y1);
        h_2v_dbv->Fill(dbv0, w);
        h_2v_dbv->Fill(dbv1, w);
        h_2v_dbv1_dbv0->Fill(dbv0, dbv1, w);
        double dvv = sqrt((nt.x0-nt.x1)*(nt.x0-nt.x1) + (nt.y0-nt.y1)*(nt.y0-nt.y1));
        if (dvv > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvv = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
        h_2v_dvv->Fill(dvv, w);
	double dvv3D = sqrt((nt.x0-nt.x1)*(nt.x0-nt.x1) + (nt.y0-nt.y1)*(nt.y0-nt.y1) + (nt.z0-nt.z1)*(nt.z0-nt.z1)); //Alec added
	if (dvv3D > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvv3D = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width; //Alec added
	h_2v_dvv3D->Fill(dvv3D, w); //Alec added
	
        h_2v_sumdbv->Fill(dbv0+dbv1, w);
        double dphi = TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0)-atan2(nt.y1,nt.x1));
        h_2v_dphivv->Fill(dphi, w);
        h_2v_absdphivv->Fill(fabs(dphi), w);
        h_2v_npu->Fill(nt.npu, w);
        //printf("ibkg %i %s 2v event j %i weight %f * %f = %f dbv %f %f dvv %f npu %i\n", i, samples[i], j, weights[i], nt.weight, w, dbv0, dbv1, dvv, nt.npu);
      }
    }
    //std::cout << "finished loop over 1 and 2 vertex events" << std::endl;
    f->Close();
    delete f;
  }

  // check for negative bins in dbv histograms that we throw from below--JMTBAD set zero, only wrong ~by a little
  for (TH1* h : { h_1v_dbv0, h_1v_dbv1})
    for (int ibin = 0; ibin <= h->GetNbinsX()+1; ++ibin)
      if (h->GetBinContent(ibin) < 0) {
        //printf("\e[1;31mdbv histogram %s has negative content %f in bin %i\e[0m\n", h->GetName(), h->GetBinContent(ibin), ibin);
        h->SetBinContent(ibin, 0);
      }

  //construct dvvc
  TH1F* h_c1v_dbv = new TH1F("h_c1v_dbv", "constructed from only-one-vertex events;d_{BV} (cm);vertices", 200, 0, 2.0); //was 1250, 0, 2.5
  TH1F* h_c1v_dvv = new TH1F("h_c1v_dvv", "constructed from only-one-vertex events;d_{VV} (cm);events", 100, 0, M_PI); //was (100, 0, 1.) changed during dphijj fit addition
  TH1F* h_c1v_sumdbv = new TH1F("h_c1v_sumdbv", "constructed from only-one-vertex events;#Sigma(d_{BV}) (cm);events", 200, 0, 4.0); //was 100, 0 ,4.0
  TH1F* h_c1v_sumdbv_w_errorbars = new TH1F("h_c1v_sumdbv_w_errorbars", "constructed from only-one-vertex events;#Sigma(d_{BV}) (cm);events", 200, 0, 4.0);
  TH1F* h_c1v_absdphivv = new TH1F("h_c1v_absdphivv", "constructed from only-one-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1F* h_c1v_dbv0 = new TH1F("h_c1v_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);events", 1250, 0, 2.5);
  TH1F* h_c1v_dbv1 = new TH1F("h_c1v_dbv1", "constructed from only-one-vertex events;d_{BV}^{1} (cm);events", 1250, 0, 2.5);
  TH2F* h_c1v_dbv1_dbv0 = new TH2F("h_c1v_dbv1_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 1250, 0, 2.5, 1250, 0, 2.5);


  //TF1* f_dphi = new TF1("f_dphi", "(abs(x)-[0])**[1] + [2]", 0, M_PI);
  //f_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);
  TF1* f_dphi = new TF1("f_dphi", "[1] + [2] + 1.0/[0]", 0, M_PI); //M_PI stands for the physical constant pi
  dphi_pdf_c = M_PI;
  f_dphi->SetParameters(dphi_pdf_c, 0.0, 0.0); //background template construction: define function of angular separation between displaced vertices, here it is always 1/pi
  
  TF1* i_dphi = 0;
  TF1* i_dphi2 = 0;
  TF1* fit_dphijj = 0;
  TF1* func_dphijj = 0;
  if (p.vary_dphi()) {
    //i_dphi = new TF1("i_dphi", "((1/([1]+1))*(x-[0])**([1]+1) + [2]*x - (1/([1]+1))*(-[0])**([1]+1)) / ((1/([1]+1))*(3.14159-[0])**([1]+1) + [2]*3.14159 - (1/([1]+1))*(-[0])**([1]+1))", 0, M_PI);
    //i_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);
    //i_dphi2 = new TF1("i_dphi2", "x/3.14159", 0, M_PI);
    //Alec added below
    fit_dphijj = new TF1("fit_dphijj", "(-3.14159<x && x<-0.6)*([2]*x**2+[1]*x+[0]) + (3.14159>x && x>0.6)*([2]*x**2-[1]*x+[0])", -M_PI, M_PI);
    fit_dphijj->SetParameters(10,10,5);
    h_1v_dphijj->Fit(fit_dphijj,"R");
    //func_dphijj = new TF1("fit_dphijj", "(-3.14159<x && x<0)*([2]*x**2+[1]*x+[0]) + (3.14159>x && x>=0)*([2]*x**2-[1]*x+[0])", -M_PI, M_PI);
    func_dphijj = new TF1("func_dphijj", "(3.14159>x && x>=0)*([2]*x**2-[1]*x+[0])", 0, M_PI);
    func_dphijj->SetParameters(fit_dphijj->GetParameter(0), fit_dphijj->GetParameter(1), fit_dphijj->GetParameter(2));
    //std::cout << fit_dphijj->GetParameter(0) <<  fit_dphijj->GetParameter(1) << fit_dphijj->GetParameter(2) << std::endl;
  }

  //TFile* jet_angle_file = TFile::Open(jet_angle_fname); //This is not used in this file

  TH1F* h_eff_3d = 0; //background template construction: create vertexing efficiency histogram from the vpeffs files based on number max number of tracks
  if (p.clearing_from_eff()) {
    TFile* eff_file = TFile::Open(eff_file_name_3d);
    if (!eff_file || !eff_file->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }
    h_eff_3d = (TH1F*)eff_file->Get(eff_hist);
    h_eff_3d->SetBinContent(h_eff_3d->GetNbinsX()+1, h_eff_3d->GetBinContent(h_eff_3d->GetNbinsX()));
  }

  TH1F* h_eff_2d = 0; //background template construction: create vertexing efficiency histogram from the vpeffs files based on number max number of tracks 
  if (p.clearing_from_eff()) {
    TFile* eff_file = TFile::Open(eff_file_name_2d);
    if (!eff_file || !eff_file->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }
    h_eff_2d = (TH1F*)eff_file->Get(eff_hist);
    h_eff_2d->SetBinContent(h_eff_2d->GetNbinsX()+1, h_eff_2d->GetBinContent(h_eff_2d->GetNbinsX()));
  }

  int bin1 = 0;
  int bin2 = 0;
  int bin3 = 0;
  int intobin1 = 0;
  int intobin2 = 0;
  int intobin3 = 0;
  int outofbin1 = 0;
  int outofbin2 = 0;
  int outofbin3 = 0;

  //random sampling for sumdbv background template
  const int nsamples = 1*int(h_1v_dbv->GetEntries());
  printf("sampling %i times (should be %i if no MC weights)\n", nsamples, 1*int(h_1v_dbv->Integral()));
  double events_after_eff = 0;

  //systematic sampling of each dbv entry with all others
  /*const int nsamples = dbv_value_vector.size();
  printf("sampling %i times\n", nsamples);
  double events_after_eff = 0;*/

  //signal contamination insertion
  /*if (p.ntracks() == 3 or p.ntracks() == 4 or p.ntracks() == 5) {
    TString ntracks_string = std::to_string(p.ntracks());
    TString contam_dir = "./ULV30BvetoLHTm_neuM400cT10mm_signonneg_p005bs2derrcut_run2/2v_from_jets_run2_"+ntracks_string+"track_default_ULV30BvetoLHTm.root";
    std::cout << "SIGNAL CONTAMINATION APPLIED!" << std::endl;
    std::cout << "Contaminating this background with signal from: " << contam_dir << std::endl;
    TString h_contam_name0 = "h_1v_dbv0";
    TString h_contam_name1 = "h_1v_dbv1";
    TFile * fcontam = TFile::Open(contam_dir);
    TH1D * h_contam0 = (TH1D*)fcontam->Get(h_contam_name0);
    TH1D * h_contam1 = (TH1D*)fcontam->Get(h_contam_name1);
    h_contam0->Scale(.01);
    h_contam1->Scale(.01);
    h_1v_dbv0->Add(h_contam0);
    h_1v_dbv1->Add(h_contam1);
  }*/
  //start loop with random seed
  //std::random_device rd;
  //std::mt19937 gen(rd());

  //always start with the same seed
  //std::mt19937 gen(42);
  std::mt19937 gen(73);
  //checkpoint
  std::uniform_int_distribution<> dist(0, dbv_value_vector.size() - 1);
  std::uniform_int_distribution<> dist1(0, dbv_value_vector_btag_npult20.size() - 1);
  std::uniform_int_distribution<> dist2(0, dbv_value_vector_btag_npugt20lt30.size() - 1);
  std::uniform_int_distribution<> dist3(0, dbv_value_vector_btag_npugt30lt40.size() - 1);
  std::uniform_int_distribution<> dist4(0, dbv_value_vector_btag_npugt40.size() - 1);
  std::uniform_int_distribution<> dist5(0, dbv_value_vector_nobtag_npult20.size() - 1);
  std::uniform_int_distribution<> dist6(0, dbv_value_vector_nobtag_npugt20lt30.size() - 1);
  std::uniform_int_distribution<> dist7(0, dbv_value_vector_nobtag_npugt30lt40.size() - 1);
  std::uniform_int_distribution<> dist8(0, dbv_value_vector_nobtag_npugt40.size() - 1);
  std::cout << "Start looping through samples" << std::endl;
  //std::vector<std::string>  dbv_check_vector(h_c1v_sumdbv_w_errorbars->GetNbinsX());
  std::vector<std::vector<int>> dbv_check_vector(h_c1v_sumdbv_w_errorbars->GetNbinsX());
  //double sumdbv_test = 0;
  for (int ij = 0; ij < nsamples; ++ij) {
    if (ij == 500000) {std::cout << "made it to 500,000th sample" << std::endl;}
    if (ij == 1000000) {std::cout << "made it to 1,000,000th sample" << std::endl;}
    double dbv0 = h_1v_dbv0->GetRandom();  //background template construction: get random entries in dbv histograms
    double dbv1 = h_1v_dbv1->GetRandom();
    /*int binx0 = -1;
    int binx1 = -1;
    double dbv0_error = 0;
    double dbv1_error = 0;
    double sumdbv_error_entry = 0;
    h_1v_dbv0->GetBinWithContent(dbv0,binx0);
    h_1v_dbv1->GetBinWithContent(dbv1,binx1);
    h_1v_dbv0->GetBinError(binx0);
    h_1v_dbv1->GetBinError(binx1);
    sumdbv_error_entry = sqrt(dbv0_error*dbv0_error + dbv1_error*dbv1_error);*/
    //
    //new for constructing background template
    //
    //random sampling for sumdbv background template
    int randomIndex0 = dist(gen);
    //int randomIndex1 = dist(gen);
    double dbv0_entry = dbv_value_vector[ij];
    double z0_entry = z_value_vector[ij];
    //double dbv1_entry = dbv_value_vector[randomIndex1];
    double dbv0_weight_entry = dbv_weight_vector[ij];
    //double dbv1_weight_entry = dbv_weight_vector[randomIndex1];

    //pileup study
    double dbv1_entry;
    double z1_entry;
    double dbv1_weight_entry;
    //std::cout << "Start of dbv1 assignment if statements." << std::endl;
    //std::cout << "npuid: " << dbv_npubinid_vector[ij] << std::endl;
    if (dbv_npubinid_vector[ij] == 1) {
      int randomIndex1 = dist1(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_btag_npult20[randomIndex1];
      z1_entry = z_value_vector_btag_npult20[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_btag_npult20[randomIndex1];
    }
    else if (dbv_npubinid_vector[ij] == 2) {
      int randomIndex1 = dist2(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_btag_npugt20lt30[randomIndex1];
      z1_entry = z_value_vector_btag_npugt20lt30[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_btag_npugt20lt30[randomIndex1];
    }
    else if (dbv_npubinid_vector[ij] == 3) {
      int randomIndex1 = dist3(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_btag_npugt30lt40[randomIndex1];
      z1_entry = z_value_vector_btag_npugt30lt40[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_btag_npugt30lt40[randomIndex1];
    }
    else if (dbv_npubinid_vector[ij] == 4) {
      int randomIndex1 = dist4(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_btag_npugt40[randomIndex1];
      z1_entry = z_value_vector_btag_npugt40[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_btag_npugt40[randomIndex1];
    }
    else if (dbv_npubinid_vector[ij] == 5) {
      int randomIndex1 = dist5(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_nobtag_npult20[randomIndex1];
      z1_entry = z_value_vector_nobtag_npult20[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_nobtag_npult20[randomIndex1];
    }
    else if (dbv_npubinid_vector[ij] == 6) {
      int randomIndex1 = dist6(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_nobtag_npugt20lt30[randomIndex1];
      z1_entry = z_value_vector_nobtag_npugt20lt30[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_nobtag_npugt20lt30[randomIndex1];
    }
    else if (dbv_npubinid_vector[ij] == 7) {
      int randomIndex1 = dist7(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_nobtag_npugt30lt40[randomIndex1];
      z1_entry = z_value_vector_nobtag_npugt30lt40[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_nobtag_npugt30lt40[randomIndex1];
    }
    else if (dbv_npubinid_vector[ij] == 8) {
      int randomIndex1 = dist8(gen);
      //std::cout << "randomIndex1 assigned with npuid " << dbv_npubinid_vector[ij] << ": " << randomIndex1 << std::endl;
      dbv1_entry = dbv_value_vector_nobtag_npugt40[randomIndex1];
      z1_entry = z_value_vector_nobtag_npugt40[randomIndex1];
      dbv1_weight_entry = dbv_weight_vector_nobtag_npugt40[randomIndex1];
    }

    double sumdbv_entry = dbv0_entry + dbv1_entry;
    double sumdbv_bin = h_c1v_sumdbv_w_errorbars->FindBin(sumdbv_entry);
    //double sumdbv_w_entry = sqrt(dbv0_weight_entry*dbv0_weight_entry + dbv1_weight_entry*dbv1_weight_entry); //we think this was wrong
    double sumdbv_w_entry = dbv0_weight_entry*dbv1_weight_entry;

    //std::cout << ", dbv1_entry: " << dbv1_entry << ", dbv1_weight_entry: " << dbv1_weight_entry << std::endl;
    /*if (ij < 10) {
      std::cout << "pair of dbv values: " << dbv0_entry << " and " << dbv1_entry << " sum to: " << sumdbv_entry <<std::endl;
      sumdbv_test += sumdbv_entry;
    }
    if (ij == 10) {
      std::cout << "sumdbv_test value: " << sumdbv_test/10 << std::endl;
      std::cout << "Should be about 0.1252 for default" << std::endl;
    }*/

    //systematic sampling of each dbv entry with all others
    /*double dbv0_entry = dbv_value_vector[ij];
    double dbv1_entry;
    double dbv0_weight_entry = dbv_weight_vector[ij];
    double dbv1_weight_entry;
    double sumdbv_entry;
    double sumdbv_w_entry;*/

    h_c1v_dbv->Fill(dbv0_entry);
    h_c1v_dbv->Fill(dbv1_entry);

    double dphi   = f_dphi->GetRandom(); //background template construction: get random angle (dphi) between the random dbv pair, always 1/pi (set above)

    double dvv_entry = sqrt(dbv0_entry*dbv0_entry + dbv1_entry*dbv1_entry - 2*dbv0_entry*dbv1_entry*cos(dphi));
    double dvv3D_entry = sqrt(dbv0_entry*dbv0_entry + dbv1_entry*dbv1_entry - 2*dbv0_entry*dbv1_entry*cos(dphi) + (z0_entry - z1_entry)*(z0_entry - z1_entry));
    double dvvc   = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(dphi)); //background template construction: compute 2D distance between 2 random dbv pair vertices with dphi angular separation (1/pi)
    double sumdbv = dbv0 + dbv1; //background template construction: sum random dbv pair to find sumdbv

    if (p.vary_dphi()) {
      //double dphi2 = i_dphi2->GetX(i_dphi->Eval(dphi), 0, M_PI);//Alec commented
      double dphi2 = func_dphijj->GetRandom(); //Alec added
      double dvvc2 = sqrt(dbv0_entry*dbv0_entry + dbv1_entry*dbv1_entry - 2*dbv0_entry*dbv1_entry*cos(dphi2));
      if (dvvc < 0.04) ++bin1;
      if (dvvc >= 0.04 && dvvc < 0.07) ++bin2;
      if (dvvc >= 0.07) ++bin3;
      if (!(dvvc < 0.04) && (dvvc2 < 0.04)) ++intobin1;
      if (!(dvvc >= 0.04 && dvvc < 0.07) && (dvvc2 >= 0.04 && dvvc2 < 0.07)) ++intobin2;
      if (!(dvvc >= 0.07) && (dvvc2 >= 0.07)) ++intobin3;
      if ((dvvc < 0.04) && !(dvvc2 < 0.04)) ++outofbin1;
      if ((dvvc >= 0.04 && dvvc < 0.07) && !(dvvc2 >= 0.04 && dvvc2 < 0.07)) ++outofbin2;
      if ((dvvc >= 0.07) && !(dvvc2 >= 0.07)) ++outofbin3;
      dphi = dphi2;
      dvvc = dvvc2;
      dvv_entry = dvvc2;
    }

    double prob  = 1; //background template construction: 
    if (p.clearing_from_eff()) {
      prob = h_eff_2d->GetBinContent(h_eff_2d->FindBin(dvvc));
      prob *= p.extra_eff_2d(dvvc);
    }
    double prob_sumdbv_w_errorbars  = 1; //background template construction:
    if (p.clearing_from_eff() and use_dvv3D) {
      prob_sumdbv_w_errorbars = h_eff_3d->GetBinContent(h_eff_3d->FindBin(dvv3D_entry));
      //prob_sumdbv_w_errorbars *= p.extra_eff_2d(dvv_entry);
    }
    else if (p.clearing_from_eff()) {
      prob_sumdbv_w_errorbars = h_eff_2d->GetBinContent(h_eff_2d->FindBin(dvv_entry));
      //prob_sumdbv_w_errorbars *= p.extra_eff_2d(dvv_entry);
    }

    double btag_weight = 1; //REMEMBER TO FINISH/ADJUST THIS!!!!!!!!!
    if (dbv_npubinid_vector[ij] < 5) {
      btag_weight = 99/80;
    }
    else {
      btag_weight = 1/20;
    }

    if (dvvc > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvvc = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
    h_c1v_dvv->Fill(dvv_entry, prob);  //errors not propagated properly just for dvv here
    h_c1v_sumdbv->Fill(sumdbv_entry, prob); //background template construction: fill histogram with constructed value and weight
    //h_c1v_sumdbv_w_errorbars->Fill(sumdbv_entry, sqrt(prob_sumdbv_w_errorbars*prob_sumdbv_w_errorbars + sumdbv_w_entry*sumdbv_w_entry));
    h_c1v_sumdbv_w_errorbars->Fill(sumdbv_entry, btag_weight*prob_sumdbv_w_errorbars*sumdbv_w_entry);
    //random sampling for sumdbv background template
    /*if (std::find(dbv_check_vector[sumdbv_bin].begin(), dbv_check_vector[sumdbv_bin].end(), randomIndex0) != dbv_check_vector[sumdbv_bin].end()) {
      h_c1v_sumdbv_w_errorbars->Fill(sumdbv_entry, prob_sumdbv_w_errorbars*pow(2*h_c1v_sumdbv_w_errorbars->GetBinError(sumdbv_bin)*sumdbv_w_entry+pow(sumdbv_w_entry,2),0.5));
    }
    else if (std::find(dbv_check_vector[sumdbv_bin].begin(), dbv_check_vector[sumdbv_bin].end(), randomIndex1) != dbv_check_vector[sumdbv_bin].end()) {
      h_c1v_sumdbv_w_errorbars->Fill(sumdbv_entry, prob_sumdbv_w_errorbars*pow(2*h_c1v_sumdbv_w_errorbars->GetBinError(sumdbv_bin)*sumdbv_w_entry+pow(sumdbv_w_entry,2),0.5));
    }
    else {
      h_c1v_sumdbv_w_errorbars->Fill(sumdbv_entry, prob_sumdbv_w_errorbars*sumdbv_w_entry);
    }
    dbv_check_vector[sumdbv_bin].push_back(randomIndex0);
    dbv_check_vector[sumdbv_bin].push_back(randomIndex1);*/

    //systematic sampling of each dbv entry with all others
    /*for (int k = ij; k < nsamples; ++k) {
      if (ij != k) {
	dbv1_entry = dbv_value_vector[k];
	dbv1_weight_entry = dbv_weight_vector[k];
	sumdbv_entry = dbv0_entry + dbv1_entry;
	sumdbv_w_entry = sqrt(dbv0_weight_entry*dbv0_weight_entry + dbv1_weight_entry*dbv1_weight_entry);
	h_c1v_sumdbv_w_errorbars->Fill(sumdbv_entry, prob_sumdbv_w_errorbars*sumdbv_w_entry);
      }
    }*/

    h_c1v_absdphivv->Fill(fabs(dphi), prob);
    h_c1v_dbv0->Fill(dbv0_entry, prob);
    h_c1v_dbv1->Fill(dbv1_entry, prob);
    h_c1v_dbv1_dbv0->Fill(dbv0_entry, dbv1_entry, prob);

    events_after_eff += prob;
  }
  //set bin errors for constructed sumdbv histogram
  std::cout << "End looping through samples" << std::endl;


  printf("events before efficiency correction = %d, events after efficiency correction = %f, integrated efficiency correction = %f\n", nsamples, events_after_eff, events_after_eff/nsamples);

  TString cb_cbbar = TString::Format("%s, %f", out_fn, events_after_eff/nsamples);
  cb_cbbar_vector.push_back(cb_cbbar);

  if (p.vary_dphi()) {
    printf("bin1 = %d, bin2 = %d, bin3 = %d, intobin1 = %d, intobin2 = %d, intobin3 = %d, outofbin1 = %d, outofbin2 = %d, outofbin3 = %d\n", bin1, bin2, bin3, intobin1, intobin2, intobin3, outofbin1, outofbin2, outofbin3);
    printf("uncorrelated variation / default (bin 1): %f +/- %f\n", 1 + (intobin1 - outofbin1) / (1.*bin1), sqrt(bin1 + bin1 + intobin1 - outofbin1) / bin1);
    printf("  correlated variation / default (bin 1): %f +/- %f\n", 1 + (intobin1 - outofbin1) / (1.*bin1), sqrt(intobin1 + outofbin1) / bin1);
    printf("uncertainty correlated / uncorrelated (bin 1): %f\n", sqrt(intobin1 + outofbin1) / sqrt(bin1 + bin1 + intobin1 - outofbin1));
    printf("uncorrelated variation / default (bin 2): %f +/- %f\n", 1 + (intobin2 - outofbin2) / (1.*bin2), sqrt(bin2 + bin2 + intobin2 - outofbin2) / bin2);
    printf("  correlated variation / default (bin 2): %f +/- %f\n", 1 + (intobin2 - outofbin2) / (1.*bin2), sqrt(intobin2 + outofbin2) / bin2);
    printf("uncertainty correlated / uncorrelated (bin 2): %f\n", sqrt(intobin2 + outofbin2) / sqrt(bin2 + bin2 + intobin2 - outofbin2));
    printf("uncorrelated variation / default (bin 3): %f +/- %f\n", 1 + (intobin3 - outofbin3) / (1.*bin3), sqrt(bin3 + bin3 + intobin3 - outofbin3) / bin3);
    printf("  correlated variation / default (bin 3): %f +/- %f\n", 1 + (intobin3 - outofbin3) / (1.*bin3), sqrt(intobin3 + outofbin3) / bin3);
    printf("uncertainty correlated / uncorrelated (bin 3): %f\n", sqrt(intobin3 + outofbin3) / sqrt(bin3 + bin3 + intobin3 - outofbin3));
  }

  TFile* fh = TFile::Open(out_fn, "recreate");

  h_1v_dbv->Write();
  h_1v_dbv_npult20->Write();
  h_1v_dbv_npugt20lt30->Write();
  h_1v_dbv_npugt30lt40->Write();
  h_1v_dbv_npugt40->Write();
  h_1v_costh2_onlytks0->Write(); //Alec added
  h_1v_costh20->Write(); //Alec added
  h_1v_bs2derr->Write(); //Alec added
  h_1v_rescale_bs2derr->Write(); //Alec added
  h_1v_w->Write(); //Alec added
  h_1v_z->Write();
  h_1v_dz->Write();
  h_1v_xy->Write();
  h_1v_dbv0->Write();
  h_1v_dbv1->Write();
  h_1v_dbv_dz->Write();
  h_1v_dbv_bs2derr->Write(); //Alec added
  h_1v_phiv->Write();
  h_1v_npu->Write();
  h_1v_njets->Write();
  h_1v_ht40->Write();
  h_1v_phij->Write();
  h_1v_dphijj->Write();
  h_1v_dphijv->Write();
  h_1v_dphijvpt->Write();
  h_1v_dphijvmin->Write();
  h_2v_dbv->Write();
  h_2v_dbv1_dbv0->Write();
  h_2v_dvv->Write();
  h_2v_dvv3D->Write(); //Alec added
  h_2v_sumdbv->Write();
  h_2v_dphivv->Write();
  h_2v_absdphivv->Write();
  h_2v_npu->Write();

  h_c1v_dbv->Write();
  //h_c1v_dvv->Scale(1./h_c1v_dvv->Integral());
  h_c1v_dvv->Write();
  //h_c1v_sumdbv->Scale(1./h_c1v_sumdbv->Integral());
  h_c1v_sumdbv->Write();
  h_c1v_sumdbv_w_errorbars->Write();
  h_c1v_absdphivv->Write();
  h_c1v_dbv0->Write();
  h_c1v_dbv1->Write();
  h_c1v_dbv1_dbv0->Write();

  TCanvas* c_dvv = new TCanvas("c_dvv", "c_dvv", 700, 700);
  TLegend* l_dvv = new TLegend(0.35,0.75,0.85,0.85);
  h_2v_dvv->SetTitle(";d_{VV} (cm);events");
  h_2v_dvv->SetLineColor(kBlue);
  h_2v_dvv->SetLineWidth(3);
  h_2v_dvv->Scale(1./h_2v_dvv->Integral());
  h_2v_dvv->SetStats(0);
  h_2v_dvv->Draw();
  l_dvv->AddEntry(h_2v_dvv, "two-vertex events");
  h_c1v_dvv->SetLineColor(kRed);
  h_c1v_dvv->SetLineWidth(3);
  h_c1v_dvv->Scale(1./h_c1v_dvv->Integral());
  h_c1v_dvv->SetStats(0);
  h_c1v_dvv->Draw("sames");
  l_dvv->AddEntry(h_c1v_dvv, "constructed from only-one-vertex events");
  l_dvv->SetFillColor(0);
  l_dvv->Draw();
  c_dvv->SetTickx();
  c_dvv->SetTicky();
  c_dvv->Write();

  TCanvas* c_sumdbv = new TCanvas("c_sumdbv", "c_sumdbv", 700, 700);
  TLegend* l_sumdbv = new TLegend(0.35,0.75,0.85,0.85);
  h_2v_sumdbv->SetTitle(";#Sigmad_{BV} (cm);events");
  h_2v_sumdbv->SetLineColor(kBlue);
  h_2v_sumdbv->SetLineWidth(3);
  h_2v_sumdbv->Scale(1./h_2v_sumdbv->Integral());
  h_2v_sumdbv->SetStats(0);
  h_2v_sumdbv->Draw();
  l_sumdbv->AddEntry(h_2v_sumdbv, "two-vertex events");
  h_c1v_sumdbv->SetLineColor(kRed);
  h_c1v_sumdbv->SetLineWidth(3);
  h_c1v_sumdbv->Scale(1./h_c1v_sumdbv->Integral());
  h_c1v_sumdbv->SetStats(0);
  h_c1v_sumdbv->Draw("sames");
  l_sumdbv->AddEntry(h_c1v_sumdbv, "constructed from only-one-vertex events");
  l_sumdbv->SetFillColor(0);
  l_sumdbv->Draw();
  c_sumdbv->SetTickx();
  c_sumdbv->SetTicky();
  c_sumdbv->Write();

  TCanvas* c_sumdbv_w_errorbars = new TCanvas("c_sumdbv_w_errorbars", "c_sumdbv_w_errorbars", 700, 700);
  TLegend* l_sumdbv_w_errorbars = new TLegend(0.35,0.75,0.85,0.85);
  h_2v_sumdbv->SetTitle(";#Sigmad_{BV} (cm);events");
  h_2v_sumdbv->SetLineColor(kBlue);
  h_2v_sumdbv->SetLineWidth(3);
  h_2v_sumdbv->Scale(1./h_2v_sumdbv->Integral());
  h_2v_sumdbv->SetStats(0);
  h_2v_sumdbv->Draw();
  l_sumdbv_w_errorbars->AddEntry(h_2v_sumdbv, "two-vertex events");
  h_c1v_sumdbv_w_errorbars->SetLineColor(kRed);
  h_c1v_sumdbv_w_errorbars->SetLineWidth(3);
  h_c1v_sumdbv_w_errorbars->Scale(1./h_c1v_sumdbv_w_errorbars->Integral());
  h_c1v_sumdbv_w_errorbars->SetStats(0);
  h_c1v_sumdbv_w_errorbars->Draw("sames");
  l_sumdbv_w_errorbars->AddEntry(h_c1v_sumdbv_w_errorbars, "constructed from only-one-vertex events");
  l_sumdbv_w_errorbars->SetFillColor(0);
  l_sumdbv_w_errorbars->Draw();
  c_sumdbv_w_errorbars->SetTickx();
  c_sumdbv_w_errorbars->SetTicky();
  c_sumdbv_w_errorbars->Write();

  TCanvas* c_absdphivv = new TCanvas("c_absdphivv", "c_absdphivv", 700, 700);
  TLegend* l_absdphivv = new TLegend(0.25,0.75,0.75,0.85);
  h_2v_absdphivv->SetTitle(";|#Delta#phi_{VV}|;events");
  h_2v_absdphivv->SetLineColor(kBlue);
  h_2v_absdphivv->SetLineWidth(3);
  h_2v_absdphivv->Scale(1./h_2v_absdphivv->Integral());
  h_2v_absdphivv->SetStats(0);
  h_2v_absdphivv->Draw();
  l_absdphivv->AddEntry(h_2v_absdphivv, "two-vertex events");
  h_c1v_absdphivv->SetLineColor(kRed);
  h_c1v_absdphivv->SetLineWidth(3);
  h_c1v_absdphivv->Scale(1./h_c1v_absdphivv->Integral());
  h_c1v_absdphivv->SetStats(0);
  h_c1v_absdphivv->Draw("sames");
  l_absdphivv->AddEntry(h_c1v_absdphivv, "constructed from only-one-vertex events");
  l_absdphivv->SetFillColor(0);
  l_absdphivv->Draw();
  c_absdphivv->SetTickx();
  c_absdphivv->SetTicky();
  c_absdphivv->Write();

  f_dphi->Write();
  if (p.clearing_from_eff()) {
    h_eff_2d->SetName("h_eff_2d");
    h_eff_2d->Write();
  }
  if (p.vary_dphi()) {
    //i_dphi->Write();
    //i_dphi2->Write();
    fit_dphijj->Write();
    func_dphijj->Write();
  }

  fh->Close();

  delete h_1v_dbv;
  delete h_1v_dbv_npult20;
  delete h_1v_dbv_npugt20lt30;
  delete h_1v_dbv_npugt30lt40;
  delete h_1v_dbv_npugt40;
  delete h_1v_costh2_onlytks0; //Alec added
  delete h_1v_costh20; //Alec added
  delete h_1v_bs2derr; //Alec added
  delete h_1v_rescale_bs2derr; //Alec added
  delete h_1v_w; //Alec added
  delete h_1v_z;
  delete h_1v_dz;
  delete h_1v_xy;
  delete h_1v_dbv0;
  delete h_1v_dbv1;
  delete h_1v_dbv_dz;
  delete h_1v_dbv_bs2derr; //Alec added
  delete h_1v_phiv;
  delete h_1v_npu;
  delete h_1v_njets;
  delete h_1v_ht40;
  delete h_1v_phij;
  delete h_1v_dphijj;
  delete h_1v_dphijv;
  delete h_1v_dphijvpt;
  delete h_1v_dphijvmin;
  delete h_2v_dbv;
  delete h_2v_dbv1_dbv0;
  delete h_2v_dvv;
  delete h_2v_dvv3D; //Alec added
  delete h_2v_sumdbv;
  delete h_2v_dphivv;
  delete h_2v_absdphivv;
  delete h_2v_npu;
  delete c_dvv;
  delete c_sumdbv;
  delete c_sumdbv_w_errorbars;
  delete c_absdphivv;
  delete h_c1v_dbv;
  delete h_c1v_dvv;
  delete h_c1v_sumdbv;
  delete h_c1v_sumdbv_w_errorbars;
  delete h_c1v_absdphivv;
  delete h_c1v_dbv0;
  delete h_c1v_dbv1;
  delete h_c1v_dbv1_dbv0;
}

int main(int argc, const char* argv[]) {
  TH1::SetDefaultSumw2();
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

  const bool only_default = argc >= 2 && strcmp(argv[1], "only_default") == 0;
  ConstructDvvcParameters pars;
  if (only_default) {
    const char* outfn  = "2v_from_jets.root";
    const char* drawfn = "2v_from_jets.png";
    const int ntracks  = argc >= 3 ? atoi(argv[2]) : 3;
    const char* year  = argc >= 4 ? argv[3] : "run2"; //change depending on year run
    const int ibkg  = argc >= 5 ? atoi(argv[4]) : -999;

    ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks);
    if (ibkg != -999) pars2 = pars2.ibkg_begin(ibkg).ibkg_end(ibkg);
    construct_dvvc(pars2, outfn);
    TCanvas c("c","",700,900);
    TFile* f = TFile::Open(outfn);
    TH1* h_2v_dvv  = (TH1*)f->Get("h_2v_dvv");
    TH1* h_c1v_dvv = (TH1*)f->Get("h_c1v_dvv");
    h_c1v_dvv->Scale(h_2v_dvv->Integral()/h_c1v_dvv->Integral());
    h_c1v_dvv->SetLineColor(kRed);
    h_2v_dvv->SetLineColor(kBlue);
    for (auto h : {h_c1v_dvv, h_2v_dvv}) {
      h->SetTitle(TString::Format("%i-track, 2-vertex events (%s);d_{VV} (cm);events", ntracks, year));
      h->SetLineWidth(2);
      h->SetStats(0);
    }
    TRatioPlot rat(h_2v_dvv, h_c1v_dvv);
    rat.SetH1DrawOpt("e");
    rat.SetH2DrawOpt("hist");
    rat.Draw();
    c.Update();
    rat.GetLowerPad()->SetLogy();
    double minr = 1e99, maxr = 0;
    for (int ibin = 1; ibin <= std::min(10,h_2v_dvv->GetNbinsX()); ++ibin) {
      const double r = h_2v_dvv->GetBinContent(ibin) / h_c1v_dvv->GetBinContent(ibin);
      minr = std::min(minr, r);
      maxr = std::max(maxr, r);
    }
    rat.GetLowerRefYaxis()->SetRangeUser(minr*0.5,maxr*2);
    rat.GetCalculationOutputGraph()->SetLineWidth(2);
    rat.GetCalculationOutputGraph()->SetLineColor(kBlue);
    rat.SetGridlines(std::vector<double>({1.}));

    c.SaveAs(drawfn);
    return 0;
  }

  // production version 
  char* version;
  if (ulversion == "ULV30BvetoLHTm") {
      version = "ULV30BvetoLHTm";
  }
  else{  
      version = "ULV30Lepm";
  }  
 
  // This for loop runs over simulated background 
  
  for (const char* year : { "run2",}) { //{"20161", "20162", "2017", "2018", "2017p8", "run2"}) { //change depending on year run
    for (int ntracks : { 3, 4, 5, 7}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks);

      construct_dvvc(pars2,                                     TString::Format("2v_from_jets_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(1),     TString::Format("2v_from_jets_%s_%dtrack_btags_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(0),     TString::Format("2v_from_jets_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.vary_dphi(true),          TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_default_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_dphi(true), TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_dphi(true), TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_eff(true), TString::Format("2v_from_jets_%s_%dtrack_vary_eff_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_eff(true), TString::Format("2v_from_jets_%s_%dtrack_vary_eff_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.              TString::Format("2v_from_jets_%s_%dtrack_bquark_uncorrected_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.bquarks(1),   TString::Format("2v_from_jets_%s_%dtrack_bquarks_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.bquarks(0),   TString::Format("2v_from_jets_%s_%dtrack_nobquarks_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).inject_signal(true),     TString::Format("2v_from_jets_%s_%dtrack_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).inject_signal(true),     TString::Format("2v_from_jets_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.clearing_from_eff(false),            TString::Format("2v_from_jets_%s_%dtrack_noclearing_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(0).max_npu(27),              TString::Format("2v_from_jets_%s_%dtrack_npu0to27_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(28).max_npu(36),             TString::Format("2v_from_jets_%s_%dtrack_npu28to36_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(37).max_npu(255),            TString::Format("2v_from_jets_%s_%dtrack_npu37to255_%s.root", year, ntracks, version));
    }
  }
    
  // This for loop runs over real data
  /*
  for (const char* year : {"2017",}){ // "2018", "2017p8"}) {
    for (int ntracks : {3, 4, 5, 7,}){ // 8, 9}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks).is_mc(false);
      construct_dvvc(pars2,                             TString::Format("2v_from_jets_data_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(1),                    TString::Format("2v_from_jets_data_%s_%dtrack_btags_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(0),                    TString::Format("2v_from_jets_data_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_nobtags_%s.root", year, ntracks, version));
    }
  }
  */
  // For use in bquark_fraction.py
  std::ofstream outfile;
  outfile.open("cb_vals/cb_vals.csv");
  outfile << "variant,cb_val" << std::endl;;

  for(TString cb_cbbar : cb_cbbar_vector){
    if(cb_cbbar.Contains("_btags_") || cb_cbbar.Contains("_nobtags_")){

      // format for our csv file
      cb_cbbar.ReplaceAll("2v_from_jets_","");
      cb_cbbar.ReplaceAll("_"+(TString)version+".root","");

      cb_cbbar.ReplaceAll("_btags","_cb");
      cb_cbbar.ReplaceAll("_nobtags","_cbbar");
      cb_cbbar.ReplaceAll("track","trk");
      cb_cbbar.ReplaceAll(" ","");
      outfile << cb_cbbar << std::endl;
    }
  }
  outfile.close();
}
