#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/CachingVertex.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/MCInteractionTops.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
//#include "JMTucker/Tools/interface/Framework.h"

namespace {
  template <typename T>
  T min(T x, T y) {
    return x < y ? x : y;
  }

  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }

  template <typename T>
  double mag(const T& v) {
    return mag(v.x(), v.y(), v.z());
  }

  template <typename T, typename T2>
  double dot2(const T& a, const T2& b) {
    return a.x() * b.x() + a.y() * b.y();
  }

  template <typename T, typename T2>
  double dot3(const T& a, const T2& b) {
    return a.x() * b.x() + a.y() * b.y() + a.z() * b.z();
  }

  template <typename T, typename T2>
  double costh2(const T& a, const T2& b) {
    return dot2(a,b) / mag(a.x(), a.y()) / mag(b.x(), b.y());
  }

  template <typename T, typename T2>
  double costh3(const T& a, const T2& b) {
    return dot3(a,b) / mag(a.x(), a.y(), a.z()) / mag(b.x(), b.y(), b.z());
  }

  template <typename V>
  double coord(const V& v, const int i) {
    if      (i == 0) return v.x();
    else if (i == 1) return v.y();
    else if (i == 2) return v.z();
    else
      throw cms::Exception("coord") << "no such coordinate " << i;
  }
}

class VtxRecoPlay : public edm::EDAnalyzer {
 public:
  explicit VtxRecoPlay(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag trigger_results_src;
  const edm::InputTag jets_src;
  const edm::InputTag tracks_src;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_src;
  const edm::InputTag vertex_src;
  const bool print_info;
  const bool is_mfv;
  const bool is_ttbar;
  const bool do_scatterplots;
  const bool do_ntuple;
  const double jet_pt_min;
  const double track_pt_min;
  const double track_vertex_weight_min;

  const int min_sv_ntracks;
  const double max_sv_chi2dof;
  const double max_sv_err2d;
  const double min_sv_mass;
  const double min_sv_drmax;
  const double min_sv_gen3dsig;
  const double max_sv_gen3dsig;

  VertexDistanceXY distcalc_2d;
  VertexDistance3D distcalc_3d;

  float gen_verts[2][3];
  bool gen_valid;

  float abs_error(const reco::Vertex& sv, bool use3d) const {
    const double x = sv.x();
    const double y = sv.y();
    const double z = use3d ? sv.z() : 0;
    AlgebraicVector3 v(x,y,z);
    AlgebraicSymMatrix33 cov = sv.covariance();
    double dist = mag(x,y,z);
    double err2 = ROOT::Math::Similarity(v, cov);
    return dist != 0 ? sqrt(err2)/dist : 0;
  }

  Measurement1D gen_dist(const reco::Vertex& sv, const bool use3d) const {
    float dist = 1e99;
    for (int i = 0; i < 2; ++i) {
      float dist_;
      if (use3d)
        dist_ = mag(sv.x() - gen_verts[i][0], sv.y() - gen_verts[i][1], sv.z() - gen_verts[i][2]);
      else
        dist_ = mag(sv.x() - gen_verts[i][0], sv.y() - gen_verts[i][1]);
      if (dist_ < dist) dist = dist_;
    }

    return Measurement1D(dist, abs_error(sv, use3d));
  }

  struct vertex_tracks_distance {
    double drmin, drmax;
    double dravg, dravgw, dravgvw;
    double drrms, drrmsw, drrmsvw;

    vertex_tracks_distance(const reco::Vertex& sv, const double track_vertex_weight_min) {
      drmin = 1e99;
      drmax = dravg = dravgw = drrms = drrmsw = 0;
      std::vector<double> drs;
      std::vector<double> ws;
      std::vector<double> vws;
      double sumw = 0, sumvw = 0;

      auto trkb = sv.tracks_begin();
      auto trke = sv.tracks_end();
      for (auto trki = trkb; trki != trke; ++trki) {
        if (sv.trackWeight(*trki) < track_vertex_weight_min)
          continue;

        for (auto trkj = trki + 1; trkj != trke; ++trkj) {
          if (sv.trackWeight(*trkj) < track_vertex_weight_min)
            continue;

          double dr = reco::deltaR(**trki, **trkj);
          drs.push_back(dr);

          double w  = 0.5*((*trki)->pt() + (*trkj)->pt());
          double vw = 0.5*(sv.trackWeight(*trki) + sv.trackWeight(*trkj));

          sumw  += w;
          sumvw += vw;
          ws .push_back(w);
          vws.push_back(vw);

          dravg   += dr;
          dravgw  += dr * w;
          dravgvw += dr * vw;

          if (dr < drmin)
            drmin = dr;
          if (dr > drmax)
            drmax = dr;
        }
      }

      dravg   /= drs.size();
      dravgw  /= sumw;
      dravgvw /= sumvw;

      for (int i = 0, ie = int(drs.size()); i < ie; ++i) {
        double dr = drs[i];
        drrms   += pow(dr - dravg,   2);
        drrmsw  += pow(dr - dravgw,  2) * ws [i];
        drrmsvw += pow(dr - dravgvw, 2) * vws[i];
      }

      drrms   = sqrt(drrms  /drs.size());
      drrmsw  = sqrt(drrmsw /sumw);
      drrmsvw = sqrt(drrmsvw/sumvw);
    }
  };

  std::pair<bool, float> compatibility(const reco::Vertex& x, const reco::Vertex& y, bool use3d) {
    bool success = false;
    float compat = 0;
    try {
      if (use3d)
        compat = distcalc_3d.compatibility(x, y);
      else
        compat = distcalc_2d.compatibility(x, y);
      success = true;
    }
    catch (cms::Exception& e) {
      if (e.category().find("matrix inversion problem") == std::string::npos)
        throw;
    }
    return std::make_pair(success, compat);
  }

  bool use_vertex(const reco::Vertex& vtx) {
    const bool use =
      int(vtx.tracksSize()) >= min_sv_ntracks &&
      vtx.normalizedChi2() < max_sv_chi2dof   &&
      abs_error(vtx, false) < max_sv_err2d    &&
      vtx.p4().mass() >= min_sv_mass          &&
      (min_sv_drmax == 0 || vertex_tracks_distance(vtx, track_vertex_weight_min).drmax >= min_sv_drmax);

    if (!use)
      return false;

    const float gd3sg = gen_dist(vtx, true).significance();
    return use && (!gen_valid || (gd3sg >= min_sv_gen3dsig && gd3sg < max_sv_gen3dsig));
  }

  TH1F* h_sim_pileup_num_int[3];
  TH1F* h_sim_pileup_true_num_int[3];

  TH1F* h_gen_valid;
  TH1F* h_gen_pos_1d[2][3];
  TH2F* h_gen_pos_2d[2][3];
  TH1F* h_lspdist2d;
  TH1F* h_lspdist3d;

  TH1F* h_pass_trigger;
  TH1F* h_njets;
  TH1F* h_ntightjets;
  TH1F* h_jetpt4;
  TH1F* h_tightjetpt4;
  TH1F* h_jetpt5;
  TH1F* h_tightjetpt5;
  TH1F* h_ntracks;
  TH1F* h_ntracksptpass;

  TH1F* h_npv;
  TH1F* h_pv_pos_1d[2][3]; // index 0: 0 = *the* PV, 1 = other PVs
  TH2F* h_pv_pos_2d[2][3];
  TH1F* h_pv_ntracks[2];
  TH1F* h_pv_ntracksptpass[2];
  TH1F* h_pv_chi2dof[2];
  TH1F* h_pv_chi2dofprob[2];
  TH1F* h_pv_pt[2];
  TH1F* h_pv_eta[2];
  TH1F* h_pv_rapidity[2];
  TH1F* h_pv_phi[2];
  TH1F* h_pv_mass[2];
  TH1F* h_pv_sumpt2[2];

  TH1F* h_nsv;
  TH1F* h_nsvpass;
  TH2F* h_nsvpass_v_minlspdist2d;
  TH2F* h_nsvpass_v_lspdist2d;
  TH2F* h_nsvpass_v_lspdist3d;

  TH2F* h_sv_max_trackicity;
  TH1F* h_sv_pos_1d[4][3]; // index 0: 0 = the highest mass SV, 1 = second highest, 2 = third highest, 3 = rest
  TH2F* h_sv_pos_2d[4][3];

  TH1F* h_sv_trackpt[4];
  TH1F* h_sv_tracketa[4];
  TH1F* h_sv_trackphi[4];
  TH1F* h_sv_trackdxy[4];
  TH1F* h_sv_trackdz[4];

  TH1F* h_sv_trackpaircosth[4];
  TH1F* h_sv_trackpairdr[4];
  TH1F* h_sv_trackpairmass[4];
  TH1F* h_sv_tracktriplemass[4];

  PairwiseHistos h_sv[4];

  TH1F* h_svdist2d;
  TH1F* h_svdist3d;
  TH2F* h_svdist2d_v_lspdist2d;
  TH2F* h_svdist3d_v_lspdist3d;
  TH2F* h_svdist2d_v_minlspdist2d;
  TH2F* h_svdist2d_v_minbsdist2d;

  TH1F* h_pair2dcompatscss;
  TH1F* h_pair2dcompat;
  TH1F* h_pair2ddist;
  TH1F* h_pair2derr;
  TH1F* h_pair2dsig;
  TH1F* h_pair3dcompatscss;
  TH1F* h_pair3dcompat;
  TH1F* h_pair3ddist;
  TH1F* h_pair3derr;
  TH1F* h_pair3dsig;

  TH1F* h_pairnsharedtracks;
  TH2F* h_pairfsharedtracks;

  struct ntuple_t {
    typedef unsigned short ushort;
    typedef unsigned int uint;
    uint run;
    uint lumi;
    uint event;
    float minlspdist2d;
    float lspdist2d;
    float lspdist3d;
    short pass_trigger;
    ushort njets;
    ushort ntightjets;
    float jetpt4;
    float jetpt5;
    float tightjetpt4;
    float tightjetpt5;
    ushort nsv;
    ushort nsvpass;

    short isv;
    ushort ntracks;
    ushort ntracksptgt10;
    ushort ntracksptgt20;
    ushort trackminnhits;
    ushort trackmaxnhits;
    float chi2dof;
    float chi2dofprob;
    float p;
    float pt;
    float eta;
    float rapidity;
    float phi;
    float mass;
    float costhmombs;
    float costhmompv2d;
    float costhmompv3d;
    float sumpt2;
    float mintrackpt;
    float maxtrackpt;
    float maxm1trackpt;
    float maxm2trackpt;
    float drmin;
    float drmax;
    float dravg;
    float drrms;
    float dravgw;
    float drrmsw;
    float gen2ddist;
    float gen2derr;
    float gen2dsig;
    float gen3ddist;
    float gen3derr;
    float gen3dsig;
    ushort bs2dcompatscss;
    float bs2dcompat;
    float bs2ddist;
    float bs2derr;
    float bs2dsig;
    float bs3ddist;
    ushort pv2dcompatscss;
    float pv2dcompat;
    float pv2ddist;
    float pv2derr;
    float pv2dsig;
    ushort pv3dcompatscss;
    float pv3dcompat;
    float pv3ddist;
    float pv3derr;
    float pv3dsig;

    void clear(bool all) {
      if (all) {
        run = -1; lumi = -1; event = -1; minlspdist2d = -1; lspdist2d = -1; lspdist3d = -1; pass_trigger = -1; njets = -1; ntightjets = -1; jetpt4 = -1; jetpt5 = -1; tightjetpt4 = -1; tightjetpt5 = -1; nsv = -1; nsvpass = -1;
      }
      isv = -1; ntracks = -1; ntracksptgt10 = -1; ntracksptgt20 = -1; trackminnhits = -1; trackmaxnhits = -1; chi2dof = -1; chi2dofprob = -1; p = -1; pt = -1; eta = -1; rapidity = -1; phi = -1; mass = -1; costhmombs = -1; costhmompv2d = -1; costhmompv3d = -1; sumpt2 = -1; mintrackpt = -1; maxtrackpt = -1; maxm1trackpt = -1; maxm2trackpt = -1; drmin = -1; drmax = -1; dravg = -1; drrms = -1; dravgw = -1; drrmsw = -1; gen2ddist = -1; gen2derr = -1; gen2dsig = -1; gen3ddist = -1; gen3derr = -1; gen3dsig = -1; bs2dcompatscss = -1; bs2dcompat = -1; bs2ddist = -1; bs2derr = -1; bs2dsig = -1; bs3ddist = -1; pv2dcompatscss = -1; pv2dcompat = -1; pv2ddist = -1; pv2derr = -1; pv2dsig = -1; pv3dcompatscss = -1; pv3dcompat = -1; pv3ddist = -1; pv3derr = -1; pv3dsig = -1;
    }
  };

  TTree* tree;
  ntuple_t nt;
};

VtxRecoPlay::VtxRecoPlay(const edm::ParameterSet& cfg)
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    print_info(cfg.getParameter<bool>("print_info")),
    is_mfv(cfg.getParameter<bool>("is_mfv")),
    is_ttbar(cfg.getParameter<bool>("is_ttbar")),
    do_scatterplots(cfg.getParameter<bool>("do_scatterplots")),
    do_ntuple(cfg.getParameter<bool>("do_ntuple")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    track_pt_min(cfg.getParameter<double>("track_pt_min")),
    track_vertex_weight_min(cfg.getParameter<double>("track_vertex_weight_min")),
    min_sv_ntracks(cfg.getParameter<int>("min_sv_ntracks")),
    max_sv_chi2dof(cfg.getParameter<double>("max_sv_chi2dof")),
    max_sv_err2d(cfg.getParameter<double>("max_sv_err2d")),
    min_sv_mass(cfg.getParameter<double>("min_sv_mass")),
    min_sv_drmax(cfg.getParameter<double>("min_sv_drmax")),
    min_sv_gen3dsig(cfg.getParameter<double>("min_sv_gen3dsig")),
    max_sv_gen3dsig(cfg.getParameter<double>("max_sv_gen3dsig"))
{
  edm::Service<TFileService> fs;

  if (!do_ntuple)
    tree = 0;
  else {
    tree = fs->make<TTree>("tree", "");
    tree->Branch("run", &nt.run, "run/i");
    tree->Branch("lumi", &nt.lumi, "lumi/i");
    tree->Branch("event", &nt.event, "event/i");
    tree->Branch("minlspdist2d", &nt.minlspdist2d, "minlspdist2d/F");
    tree->Branch("lspdist2d", &nt.lspdist2d, "lspdist2d/F");
    tree->Branch("lspdist3d", &nt.lspdist3d, "lspdist3d/F");
    tree->Branch("pass_trigger", &nt.pass_trigger, "pass_trigger/S");
    tree->Branch("njets", &nt.njets, "njets/s");
    tree->Branch("ntightjets", &nt.ntightjets, "ntightjets/s");
    tree->Branch("jetpt4", &nt.jetpt4, "jetpt4/F");
    tree->Branch("jetpt5", &nt.jetpt5, "jetpt5/F");
    tree->Branch("tightjetpt4", &nt.tightjetpt4, "tightjetpt4/F");
    tree->Branch("tightjetpt5", &nt.tightjetpt5, "tightjetpt5/F");
    tree->Branch("nsv", &nt.nsv, "nsv/s");
    tree->Branch("nsvpass", &nt.nsvpass, "nsvpass/s");
    tree->Branch("isv", &nt.isv, "isv/S");
    tree->Branch("ntracks", &nt.ntracks, "ntracks/s");
    tree->Branch("ntracksptgt10", &nt.ntracksptgt10, "ntracksptgt10/s");
    tree->Branch("ntracksptgt20", &nt.ntracksptgt20, "ntracksptgt20/s");
    tree->Branch("trackminnhits", &nt.trackminnhits, "trackminnhits/s");
    tree->Branch("trackmaxnhits", &nt.trackmaxnhits, "trackmaxnhits/s");
    tree->Branch("chi2dof", &nt.chi2dof, "chi2dof/F");
    tree->Branch("chi2dofprob", &nt.chi2dofprob, "chi2dofprob/F");
    tree->Branch("p", &nt.pt, "p/F");
    tree->Branch("pt", &nt.pt, "pt/F");
    tree->Branch("eta", &nt.eta, "eta/F");
    tree->Branch("rapidity", &nt.rapidity, "rapidity/F");
    tree->Branch("phi", &nt.phi, "phi/F");
    tree->Branch("mass", &nt.mass, "mass/F");
    tree->Branch("costhmombs", &nt.costhmombs, "costhmombs/F");
    tree->Branch("costhmompv2d", &nt.costhmompv2d, "costhmompv2d/F");
    tree->Branch("costhmompv3d", &nt.costhmompv3d, "costhmompv3d/F");
    tree->Branch("sumpt2", &nt.sumpt2, "sumpt2/F");
    tree->Branch("mintrackpt", &nt.mintrackpt, "mintrackpt/F");
    tree->Branch("maxtrackpt", &nt.maxtrackpt, "maxtrackpt/F");
    tree->Branch("maxm1trackpt", &nt.maxm1trackpt, "maxm1trackpt/F");
    tree->Branch("maxm2trackpt", &nt.maxm2trackpt, "maxm2trackpt/F");
    tree->Branch("drmin", &nt.drmin, "drmin/F");
    tree->Branch("drmax", &nt.drmax, "drmax/F");
    tree->Branch("dravg", &nt.dravg, "dravg/F");
    tree->Branch("drrms", &nt.drrms, "drrms/F");
    tree->Branch("dravgw", &nt.dravgw, "dravgw/F");
    tree->Branch("drrmsw", &nt.drrmsw, "drrmsw/F");
    tree->Branch("gen2ddist", &nt.gen2ddist, "gen2ddist/F");
    tree->Branch("gen2derr", &nt.gen2derr, "gen2derr/F");
    tree->Branch("gen2dsig", &nt.gen2dsig, "gen2dsig/F");
    tree->Branch("gen3ddist", &nt.gen3ddist, "gen3ddist/F");
    tree->Branch("gen3derr", &nt.gen3derr, "gen3derr/F");
    tree->Branch("gen3dsig", &nt.gen3dsig, "gen3dsig/F");
    tree->Branch("bs2dcompatscss", &nt.bs2dcompatscss, "bs2dcompatscss/s");
    tree->Branch("bs2dcompat", &nt.bs2dcompat, "bs2dcompat/F");
    tree->Branch("bs2ddist", &nt.bs2ddist, "bs2ddist/F");
    tree->Branch("bs2derr", &nt.bs2derr, "bs2derr/F");
    tree->Branch("bs2dsig", &nt.bs2dsig, "bs2dsig/F");
    tree->Branch("bs3ddist", &nt.bs3ddist, "bs3ddist/F");
    tree->Branch("pv2dcompatscss", &nt.pv2dcompatscss, "pv2dcompatscss/s");
    tree->Branch("pv2dcompat", &nt.pv2dcompat, "pv2dcompat/F");
    tree->Branch("pv2ddist", &nt.pv2ddist, "pv2ddist/F");
    tree->Branch("pv2derr", &nt.pv2derr, "pv2derr/F");
    tree->Branch("pv2dsig", &nt.pv2dsig, "pv2dsig/F");
    tree->Branch("pv3dcompatscss", &nt.pv3dcompatscss, "pv3dcompatscss/s");
    tree->Branch("pv3dcompat", &nt.pv3dcompat, "pv3dcompat/F");
    tree->Branch("pv3ddist", &nt.pv3ddist, "pv3ddist/F");
    tree->Branch("pv3derr", &nt.pv3derr, "pv3derr/F");
    tree->Branch("pv3dsig", &nt.pv3dsig, "pv3dsig/F");
  }

  for (int i = 0; i < 3; ++i) {
    const char* ex = (i == 0 ? "m1" : (i == 1 ? "0" : "p1"));
    h_sim_pileup_num_int[i]      = fs->make<TH1F>(TString::Format("h_sim_pileup_num_int_bx%s",      ex), "", 65, 0, 65);
    h_sim_pileup_true_num_int[i] = fs->make<TH1F>(TString::Format("h_sim_pileup_true_num_int_bx%s", ex), "", 65, 0, 65);
  }

  h_gen_valid = fs->make<TH1F>("h_gen_valid", ";gen valid?;frac. events", 2, 0, 2);

  for (int j = 0; j < 2; ++j) {
    for (int i = 0; i < 3; ++i) {
      float l = i == 2 ? 25 : 0.8;
      h_gen_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_gen_pos_1d_%i%i", j, i), TString::Format(";gen #%i vtx pos[%i] (cm);arb. units", j, i), 100, -l, l);
    }
    h_gen_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_gen_pos_2d_%ixy", j), TString::Format(";gen #%i vtx x (cm);gen #%i vtx y (cm)", j, j), 100, -1, 1, 100, -1, 1);
    h_gen_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_gen_pos_2d_%ixz", j), TString::Format(";gen #%i vtx x (cm);gen #%i vtx z (cm)", j, j), 100, -1, 1, 100,-25,25);
    h_gen_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_gen_pos_2d_%iyz", j), TString::Format(";gen #%i vtx y (cm);gen #%i vtx z (cm)", j, j), 100, -1, 1, 100,-25,25);
  }

  h_lspdist2d = fs->make<TH1F>("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);arb. units", 600, 0, 3);
  h_lspdist3d = fs->make<TH1F>("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);arb. units", 600, 0, 3);

  h_pass_trigger = fs->make<TH1F>("h_pass_trigger", ";pass-trigger code;arb. units", 3, -1, 2);
  h_njets = fs->make<TH1F>("h_njets", ";# of loose PF jets;arb. units", 30, 0, 30);
  h_ntightjets = fs->make<TH1F>("h_ntightjets", ";# of tight PF jets;arb. units", 30, 0, 30);
  h_jetpt4 = fs->make<TH1F>("h_jetpt4", ";p_{T} of 4th loose PF jet (GeV);arb. units", 100, 0, 500);
  h_tightjetpt4 = fs->make<TH1F>("h_tightjetpt4", ";p_{T} of 4th tight PF jet (GeV);arb. units", 100, 0, 500);
  h_jetpt5 = fs->make<TH1F>("h_jetpt5", ";p_{T} of 5th loose PF jet (GeV);arb. units", 100, 0, 500);
  h_tightjetpt5 = fs->make<TH1F>("h_tightjetpt5", ";p_{T} of 5th tight PF jet (GeV);arb. units", 100, 0, 500);
  h_ntracks = fs->make<TH1F>("h_ntracks", ";# of general tracks;arb. units", 20, 0, 2000);
  h_ntracksptpass = fs->make<TH1F>("h_ntracksptpass", ";# of selected tracks;arb. units", 20, 0, 60);

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices;arb. units", 65, 0, 65);

  for (int j = 0; j < 2; ++j) {
    const char* ex = j == 0 ? "the" : "other";

    for (int i = 0; i < 3; ++i) {
      float l = i == 2 ? 25 : 0.8;
      h_pv_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_pv_pos_1d_%i%i", j, i), TString::Format(";%s PV pos[%i] (cm);arb. units", ex, i), 100, -l, l);
    }
    h_pv_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_pv_pos_2d_%ixy", j), TString::Format(";%s PV x (cm);%s PV y (cm)", ex, ex), 100, -1, 1, 100, -1, 1);
    h_pv_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_pv_pos_2d_%ixz", j), TString::Format(";%s PV x (cm);%s PV z (cm)", ex, ex), 100, -1, 1, 100,-25,25);
    h_pv_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_pv_pos_2d_%iyz", j), TString::Format(";%s PV y (cm);%s PV z (cm)", ex, ex), 100, -1, 1, 100,-25,25);

    h_pv_ntracks[j] = fs->make<TH1F>(TString::Format("h_pv_ntracks_%i", j), TString::Format(";# tracks for %s PV;arb.units", ex), 50, 0, 200);
    h_pv_ntracksptpass[j] = fs->make<TH1F>(TString::Format("h_pv_ntracksptpass_%i", j), TString::Format(";# selected tracks for %s PV;arb.units", ex), 50, 0, 50);
    h_pv_chi2dof[j] = fs->make<TH1F>(TString::Format("h_pv_chi2dof_%i", j), TString::Format(";#chi^{2}/dof for %s PV;arb.units", ex), 20, 0, 5);
    h_pv_chi2dofprob[j] = fs->make<TH1F>(TString::Format("h_pv_chi2dofprob_%i", j), TString::Format(";p(#chi^{2}/dof) for %s PV;arb.units", ex), 24, 0, 1.2);

    h_pv_pt[j] = fs->make<TH1F>(TString::Format("h_pv_pt_%i", j), TString::Format(";%s PV p_{T} (GeV);arb.units", ex), 50, 0, 500);
    h_pv_eta[j] = fs->make<TH1F>(TString::Format("h_pv_eta_%i", j), TString::Format(";%s PV #eta;arb.units", ex), 30, -5, 5);
    h_pv_rapidity[j] = fs->make<TH1F>(TString::Format("h_pv_rapidity_%i", j), TString::Format(";%s PV rapidity;arb.units", ex), 30, -5, 5);
    h_pv_phi[j] = fs->make<TH1F>(TString::Format("h_pv_phi_%i", j), TString::Format(";%s PV #phi;arb.units", ex), 30, -3.15, 3.15);
    h_pv_mass[j] = fs->make<TH1F>(TString::Format("h_pv_mass_%i", j), TString::Format(";%s PV mass (GeV);arb.units", ex), 100, 0, 1000);
    h_pv_sumpt2[j] = fs->make<TH1F>(TString::Format("h_pv_sumpt2_%i", j), TString::Format(";%s PV #Sigma p_{T}^{2} (GeV);arb.units", ex), 200, 0, 20000);
  }

  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices;arb. units", 100, 0, 100);
  h_nsvpass = fs->make<TH1F>("h_nsvpass", ";# of selected secondary vertices;arb. units", 15, 0, 15);
  h_nsvpass_v_minlspdist2d = fs->make<TH2F>("h_nsvpass_v_lspdist2d", ";min dist2d(gen vtx #0, #1) (cm);# of selected secondary vertices", 600, 0, 3, 5, 0, 5);
  h_nsvpass_v_lspdist2d = fs->make<TH2F>("h_nsvpass_v_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);# of selected secondary vertices", 600, 0, 3, 5, 0, 5);
  h_nsvpass_v_lspdist3d = fs->make<TH2F>("h_nsvpass_v_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);# of selected secondary vertices", 600, 0, 3, 5, 0, 5);
  h_sv_max_trackicity = fs->make<TH2F>("h_sv_max_trackicity", ";# of tracks in SV;highest trackicity", 40, 0, 40, 40, 0, 40);

  for (int j = 0; j < 4; ++j) {
    std::string ex;
    if (j == 0)
      ex = "mass0";
    else if (j == 1)
      ex = "mass1";
    else if (j == 2)
      ex = "mass2";
    else
      ex = "rest";
    const char* exc = ex.c_str();

    for (int i = 0; i < 3; ++i) {
      float l = i == 2 ? 25 : 0.8;
      h_sv_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_sv_pos_1d_%i%i", j, i), TString::Format(";%s SV pos[%i] (cm);arb. units", exc, i), 100, -l, l);
    }
    h_sv_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixy", j), TString::Format(";%s SV x (cm);%s SV y (cm)", exc, exc), 100, -1, 1, 100, -1, 1);
    h_sv_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixz", j), TString::Format(";%s SV x (cm);%s SV z (cm)", exc, exc), 100, -1, 1, 100,-25,25);
    h_sv_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%iyz", j), TString::Format(";%s SV y (cm);%s SV z (cm)", exc, exc), 100, -1, 1, 100,-25,25);

    h_sv_trackpt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpt", exc), TString::Format(";SV %s track p_{T} (GeV);arb. units", exc), 100, 0, 200);
    h_sv_tracketa[j] = fs->make<TH1F>(TString::Format("h_sv_%s_tracketa", exc), TString::Format(";SV %s track #eta;arb. units", exc), 50, -2.7, 2.7);
    h_sv_trackphi[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackphi", exc), TString::Format(";SV %s track #phi;arb. units", exc), 50, -3.15, 3.15);
    h_sv_trackdxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackdxy", exc), TString::Format(";SV %s track dxy wrt bs (cm);arb. units", exc), 200, -1, 1);
    h_sv_trackdz[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackdz", exc), TString::Format(";SV %s track dz wrt bs (cm);arb. units", exc), 200, -20, 20);

    h_sv_trackpaircosth[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpaircosth", exc), TString::Format(";SV %s track pair cos(#theta);arb. units", exc), 100, -1, 1);
    h_sv_trackpairdr[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpairdr", exc), TString::Format(";SV %s track pair #Delta R;arb. units", exc), 100, 0, 7);
    h_sv_trackpairmass[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpairmass", exc), TString::Format(";SV %s track pair mass (GeV);arb. units", exc), 200, 0, 20);
    h_sv_tracktriplemass[j] = fs->make<TH1F>(TString::Format("h_sv_%s_tracktriplemass", exc), TString::Format(";SV %s track triple mass (GeV);arb. units", exc), 200, 0, 20);

    PairwiseHistos::HistoDefs hs;
    hs.add("ntracks",        "# of tracks/SV",                              40,    0,      40);
    hs.add("ntracksptgt10",  "# of tracks/SV w/ p_{T} > 10 GeV",            40,    0,      40);
    hs.add("ntracksptgt20",  "# of tracks/SV w/ p_{T} > 20 GeV",            40,    0,      40);
    hs.add("trackminnhits",  "min number of hits on track per SV",          40,    0,      40);
    hs.add("trackmaxnhits",  "max number of hits on track per SV",          40,    0,      40);
    hs.add("chi2dof",        "SV #chi^2/dof",                               50,    0,       7);
    hs.add("chi2dofprob",    "SV p(#chi^2, dof)",                           50,    0,       1.2);
    hs.add("p",              "SV p (GeV)",                                 100,    0,     300);
    hs.add("pt",             "SV p_{T} (GeV)",                             100,    0,     300);
    hs.add("eta",            "SV #eta",                                     50,   -4,       4);
    hs.add("rapidity",       "SV rapidity",                                 50,   -4,       4);
    hs.add("phi",            "SV #phi",                                     50,   -3.15,    3.15);
    hs.add("mass",           "SV mass (GeV)",                              100,    0,     250);
    hs.add("costhmombs",     "cos(angle(2-momentum, 2-dist to BS))",       100,   -1,       1);
    hs.add("costhmompv2d",   "cos(angle(2-momentum, 2-dist to PV))",       100,   -1,       1);
    hs.add("costhmompv3d",   "cos(angle(3-momentum, 3-dist to PV))",       100,   -1,       1);
    hs.add("sumpt2",         "SV #Sigma p_{T}^{2} (GeV^2)",                300,    0,    6000);
    hs.add("mintrackpt",     "SV min{trk_{i} p_{T}} (GeV)",                 50,    0,      10);
    hs.add("maxtrackpt",     "SV max{trk_{i} p_{T}} (GeV)",                100,    0,     150);
    hs.add("maxm1trackpt",   "SV max-1{trk_{i} p_{T}} (GeV)",              100,    0,     150);
    hs.add("maxm2trackpt",   "SV max-2{trk_{i} p_{T}} (GeV)",              100,    0,     150);
    hs.add("drmin",          "SV min{#Delta R(i,j)}",                      150,    0,       1.5);
    hs.add("drmax",          "SV max{#Delta R(i,j)}",                      150,    0,       7);
    hs.add("dravg",          "SV avg{#Delta R(i,j)}",                      150,    0,       5);
    hs.add("drrms",          "SV rms{#Delta R(i,j)}",                      150,    0,       3);
    hs.add("dravgw",         "SV wavg{#Delta R(i,j)}",                     150,    0,       5);
    hs.add("drrmsw",         "SV wrms{#Delta R(i,j)}",                     150,    0,       3);
    hs.add("gen2ddist",      "dist2d(SV, closest gen vtx) (cm)",           200,    0,       0.2);
    hs.add("gen2derr",       "#sigma(dist2d(SV, closest gen vtx)) (cm)",   200,    0,       0.2);
    hs.add("gen2dsig",       "N#sigma(dist2d(SV, closest gen vtx)) (cm)",  200,    0,     100);
    hs.add("gen3ddist",      "dist3d(SV, closest gen vtx) (cm)",           200,    0,       0.2);
    hs.add("gen3derr",       "#sigma(dist3d(SV, closest gen vtx)) (cm)",   200,    0,       0.2);
    hs.add("gen3dsig",       "N#sigma(dist3d(SV, closest gen vtx)) (cm)",  200,    0,     100);
    hs.add("bs2dcompatscss", "compat2d(SV, beamspot) success",               2,    0,       2);
    hs.add("bs2dcompat",     "compat2d(SV, beamspot)",                     100,    0,    1000);
    hs.add("bs2ddist",       "dist2d(SV, beamspot) (cm)",                  100,    0,       0.5);
    hs.add("bs2derr",        "#sigma(dist2d(SV, beamspot)) (cm)",          100,    0,       0.05);
    hs.add("bs2dsig",        "N#sigma(dist2d(SV, beamspot))",              100,    0,     100);
    hs.add("bs3ddist",       "dist2d(SV, beamspot) * sin(SV theta) (cm)",  100,    0,       0.5);
    hs.add("pv2dcompatscss", "compat2d(SV, PV) success",                     2,    0,       2);
    hs.add("pv2dcompat",     "compat2d(SV, PV)",                           100,    0,    1000);
    hs.add("pv2ddist",       "dist2d(SV, PV) (cm)",                        100,    0,       0.5);
    hs.add("pv2derr",        "#sigma(dist2d(SV, PV)) (cm)",                100,    0,       0.05);
    hs.add("pv2dsig",        "N#sigma(dist2d(SV, PV))",                    100,    0,     100);
    hs.add("pv3dcompatscss", "compat3d(SV, PV) success",                     2,    0,       2);
    hs.add("pv3dcompat",     "compat3d(SV, PV)",                           100,    0,    1000);
    hs.add("pv3ddist",       "dist3d(SV, PV) (cm)",                        100,    0,       0.5);
    hs.add("pv3derr",        "#sigma(dist3d(SV, PV)) (cm)",                100,    0,       0.1);
    hs.add("pv3dsig",        "N#sigma(dist3d(SV, PV))",                    100,    0,     100);
    h_sv[j].Init("h_sv_" + ex, hs, true, do_scatterplots);
  }

  h_svdist2d = fs->make<TH1F>("h_svdist2d", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist3d = fs->make<TH1F>("h_svdist3d", ";dist3d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist2d_v_lspdist2d = fs->make<TH2F>("h_svdist2d_v_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist3d_v_lspdist3d = fs->make<TH2F>("h_svdist3d_v_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);dist3d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist2d_v_minlspdist2d = fs->make<TH2F>("h_svdist2d_v_minlspdist2d", ";min dist2d(gen vtx #0, #1) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist2d_v_minbsdist2d = fs->make<TH2F>("h_svdist2d_v_mindist2d", ";min dist2d(sv, bs) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);

  h_pair2dcompatscss = fs->make<TH1F>("h_pair2dcompatscss", ";pair compat2d success;arb. units",       2,    0,     2);
  h_pair2dcompat     = fs->make<TH1F>("h_pair2dcompat",     ";pair compat2d;arb. units",             100,    0,  1000);
  h_pair2ddist       = fs->make<TH1F>("h_pair2ddist",       ";pair dist2d (cm);arb. units",          150,    0,     0.3);
  h_pair2derr        = fs->make<TH1F>("h_pair2derr",        ";pair #sigma(dist2d) (cm);arb. units",  100,    0,     0.05);
  h_pair2dsig        = fs->make<TH1F>("h_pair2dsig",        ";pair N#sigma(dist2d);arb. units",      100,    0,   100);
  h_pair3dcompatscss = fs->make<TH1F>("h_pair3dcompatscss", ";pair compat3d success;arb. units",       2,    0,     2);
  h_pair3dcompat     = fs->make<TH1F>("h_pair3dcompat",     ";pair compat3d;arb. units",             100,    0,  1000);
  h_pair3ddist       = fs->make<TH1F>("h_pair3ddist",       ";pair dist3d (cm);arb. units",          100,    0,     0.5);
  h_pair3derr        = fs->make<TH1F>("h_pair3derr",        ";pair #sigma(dist3d) (cm);arb. units",  100,    0,     0.07);
  h_pair3dsig        = fs->make<TH1F>("h_pair3dsig",        ";pair N#sigma(dist3d);arb. units",      100,    0,   100);

  h_pairnsharedtracks = fs->make<TH1F>("h_pairnsharedtracks", "", 50, 0, 50);
  h_pairfsharedtracks = fs->make<TH2F>("h_pairfsharedtracks", "", 51, 0,  1.02, 51, 0,  1.02);
}

void VtxRecoPlay::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  nt.clear(true);
  nt.run = event.id().run();
  nt.lumi = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<std::vector<PileupSummaryInfo> > pileup;
  event.getByLabel("addPileupInfo", pileup);
  for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi) {
    const int bx = psi->getBunchCrossing();
    if (bx < -1 || bx > 1)
      throw cms::Exception("SimPUInfo") << "pileup BX not -1, 0, or 1: " << bx << "\n";
    h_sim_pileup_num_int     [bx+1]->Fill(psi->getPU_NumInteractions());
    h_sim_pileup_true_num_int[bx+1]->Fill(psi->getTrueNumInteractions());
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);
  const float bsx = beamspot->x0();
  const float bsy = beamspot->y0();
  const float bsz = beamspot->z0();
  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);

  gen_valid = false;

  if (is_mfv) {
    MCInteractionMFV3j mci;
    mci.Init(*gen_particles);
    if ((gen_valid = mci.Valid())) {
      if (print_info)
        mci.Print(std::cout);
      for (int i = 0; i < 2; ++i) {
        const reco::GenParticle* daughter = mci.stranges[i];
        gen_verts[i][0] = daughter->vx();
        gen_verts[i][1] = daughter->vy();
        gen_verts[i][2] = daughter->vz();
      }
    }
  }
  else if (is_ttbar) {
    MCInteractionTops mci;
    mci.Init(*gen_particles);
    if ((gen_valid = mci.Valid())) {
      for (int i = 0; i < 2; ++i) {
        const reco::GenParticle* daughter = mci.tops[i];
        gen_verts[i][0] = daughter->vx();
        gen_verts[i][1] = daughter->vy();
        gen_verts[i][2] = daughter->vz();
      }
    }
  }
  else {
    for (int i = 0; i < 2; ++i) {
      gen_verts[i][0] = beamspot->x0();
      gen_verts[i][1] = beamspot->y0();
      gen_verts[i][2] = beamspot->z0();
    }
  }

  if (!gen_valid && (is_mfv || is_ttbar))
    edm::LogWarning("VtxRecoPlay") << "warning: is_mfv=" << is_mfv << ", is_ttbar=" << is_ttbar << " and neither MCI valid";

  h_gen_valid->Fill(gen_valid);
  for (int j = 0; j < 2; ++j) {
    for (int i = 0; i < 3; ++i)
      h_gen_pos_1d[j][i]->Fill(gen_verts[j][i] - coord(beamspot->position(), i));
    h_gen_pos_2d[j][0]->Fill(gen_verts[j][0] - bsx, gen_verts[j][1] - bsy);
    h_gen_pos_2d[j][1]->Fill(gen_verts[j][0] - bsx, gen_verts[j][2] - bsz);
    h_gen_pos_2d[j][2]->Fill(gen_verts[j][1] - bsy, gen_verts[j][2] - bsz);
  }

  nt.minlspdist2d = min(mag(gen_verts[0][0] - bsx, gen_verts[0][1] - bsy),
                        mag(gen_verts[1][0] - bsx, gen_verts[1][1] - bsy));
  nt.lspdist2d = mag(gen_verts[0][0] - gen_verts[1][0],
                     gen_verts[0][1] - gen_verts[1][1]);
  nt.lspdist3d = mag(gen_verts[0][0] - gen_verts[1][0],
                     gen_verts[0][1] - gen_verts[1][1],
                     gen_verts[0][2] - gen_verts[1][2]);

  h_lspdist2d->Fill(nt.lspdist2d);
  h_lspdist3d->Fill(nt.lspdist3d);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByLabel(trigger_results_src, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  const size_t npaths = trigger_names.size();
  const std::string trigger = "HLT_QuadJet50_v";
  for (size_t ipath = 0; ipath < npaths; ++ipath) {
    const std::string path = trigger_names.triggerName(ipath);
    if (path.substr(0, trigger.size()) == trigger) {
      nt.pass_trigger = trigger_results->accept(ipath);
      break;
    }
  }

  h_pass_trigger->Fill(nt.pass_trigger);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::PFJetCollection> jets;
  event.getByLabel(jets_src, jets);

  nt.njets = 0;
  nt.ntightjets = 0;
  for (const reco::PFJet& jet : *jets) {
    if (jet.pt() > jet_pt_min &&
        fabs(jet.eta()) < 2.5 &&
        jet.numberOfDaughters() > 1 &&
        (fabs(jet.eta()) >= 2.4 || (jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0. && jet.chargedMultiplicity() > 0))) {

      if (jet.neutralHadronEnergyFraction() < 0.99 && jet.neutralEmEnergyFraction() < 0.99)
        ++nt.njets;
      if (jet.neutralHadronEnergyFraction() < 0.90 && jet.neutralEmEnergyFraction() < 0.90)
        ++nt.ntightjets;

      if (nt.njets == 4)
        nt.jetpt4 = jet.pt();
      else if (nt.njets == 5)
        nt.jetpt5 = jet.pt();

      if (nt.ntightjets == 4)
        nt.tightjetpt4 = jet.pt();
      else if (nt.ntightjets == 5)
        nt.tightjetpt5 = jet.pt();
    }
  }

  h_njets->Fill(nt.njets);
  h_ntightjets->Fill(nt.ntightjets);
  h_jetpt4->Fill(nt.jetpt4);
  h_tightjetpt4->Fill(nt.tightjetpt4);
  h_jetpt5->Fill(nt.jetpt5);
  h_tightjetpt5->Fill(nt.tightjetpt5);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(tracks_src, tracks);

  const int ntracks = int(tracks->size());
  int ntracksptpass = 0;
  for (const reco::Track& tk : *tracks)
    if (tk.pt() > track_pt_min)
      ++ntracksptpass;

  h_ntracks->Fill(ntracks);
  h_ntracksptpass->Fill(ntracksptpass);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  const int npv = primary_vertices->size();
  h_npv->Fill(npv);

  for (int ipv = 0; ipv < npv; ++ipv) {
    const reco::Vertex& pv = primary_vertices->at(ipv);
    int pvndx = ipv > 0;
    for (int i = 0; i < 3; ++i)
      h_pv_pos_1d[pvndx][i]->Fill(coord(pv.position(), i) - coord(beamspot->position(), i));
    h_pv_pos_2d[pvndx][0]->Fill(pv.position().x() - bsx, pv.position().y() - bsy);
    h_pv_pos_2d[pvndx][1]->Fill(pv.position().x() - bsx, pv.position().z() - bsz);
    h_pv_pos_2d[pvndx][2]->Fill(pv.position().y() - bsy, pv.position().z() - bsz);

    auto trkb = pv.tracks_begin();
    auto trke = pv.tracks_end();
    int pv_ntracks = trke - trkb;
    int pv_ntracksptpass = 0;
    double pv_sumpt2 = 0;
    for (auto trki = trkb; trki != trke; ++trki) {
      double trkpt = (*trki)->pt();
      if (trkpt > track_pt_min)
        ++pv_ntracksptpass;
      pv_sumpt2 += trkpt * trkpt;
    }

    h_pv_ntracks      [pvndx]->Fill(pv_ntracks);
    h_pv_ntracksptpass[pvndx]->Fill(pv_ntracksptpass);
    h_pv_chi2dof      [pvndx]->Fill(pv.normalizedChi2());
    h_pv_chi2dofprob  [pvndx]->Fill(TMath::Prob(pv.chi2(), pv.ndof()));
    h_pv_pt           [pvndx]->Fill(pv.p4().pt());
    h_pv_eta          [pvndx]->Fill(pv.p4().eta());
    h_pv_rapidity     [pvndx]->Fill(pv.p4().Rapidity());
    h_pv_phi          [pvndx]->Fill(pv.p4().phi());
    h_pv_mass         [pvndx]->Fill(pv.p4().mass());
    h_pv_sumpt2       [pvndx]->Fill(pv_sumpt2);
  }

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> original_secondary_vertices;
  event.getByLabel(vertex_src, original_secondary_vertices);

  reco::VertexCollection secondary_vertices(*original_secondary_vertices);
  std::sort(secondary_vertices.begin(), secondary_vertices.end(),
            [](const reco::Vertex& a, const reco::Vertex& b) { return a.p4().mass() > b.p4().mass(); });

  const int nsv = int(secondary_vertices.size());
  h_nsv->Fill(nsv);
  int nsvpass = 0;
  const reco::Vertex* sv0 = 0;
  const reco::Vertex* sv1 = 0;
  std::vector<std::map<int,int> > trackicities(nsv);
  for (int isv = 0; isv < nsv; ++isv) {
    const reco::Vertex& sv = secondary_vertices[isv];
    if (!use_vertex(sv))
      continue;

    if (sv0 == 0)
      sv0 = &sv;
    else if (sv1 == 0)
      sv1 = &sv;

    const int svndx = nsvpass >= 3 ? 3 : nsvpass;

    nt.clear(false);
    nt.isv = nsvpass;

    ++nsvpass;

    for (int i = 0; i < 3; ++i)
      h_sv_pos_1d[svndx][i]->Fill(coord(sv.position(), i) - coord(beamspot->position(), i));
    h_sv_pos_2d[svndx][0]->Fill(sv.position().x() - bsx, sv.position().y() - bsy);
    h_sv_pos_2d[svndx][1]->Fill(sv.position().x() - bsx, sv.position().z() - bsz);
    h_sv_pos_2d[svndx][2]->Fill(sv.position().y() - bsy, sv.position().z() - bsz);

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();
    std::map<int,int>& trackicity_m = trackicities[isv];
    int ntracks = trke - trkb;
    int ntracksptgt10 = 0;
    int ntracksptgt20 = 0;
    int trackminnhits = 1000;
    int trackmaxnhits = 0;
    double sumpt2 = 0;
    std::vector<double> trackpts;

    for (auto trki = trkb; trki != trke; ++trki) {
      if (sv.trackWeight(*trki) < track_vertex_weight_min)
        continue;

      const reco::TrackBaseRef& tri = *trki;

      int key = tri.key();
      std::map<int,int>::iterator icity = trackicity_m.find(key);
      if (icity == trackicity_m.end())
        trackicity_m[key] = 1;
      else
        icity->second += 1;

      int nhits = tri->numberOfValidHits();
      if (nhits < trackminnhits)
        trackminnhits = nhits;
      if (nhits < trackmaxnhits)
        trackmaxnhits = nhits;

      double pti = tri->pt();
      trackpts.push_back(pti);
      if (pti > 10)
        ++ntracksptgt10;
      if (pti > 20)
        ++ntracksptgt20;
      sumpt2 += pti*pti;

      h_sv_trackpt[svndx]->Fill(pti);
      h_sv_tracketa[svndx]->Fill(tri->eta());
      h_sv_trackphi[svndx]->Fill(tri->phi());
      h_sv_trackdxy[svndx]->Fill(tri->dxy(beamspot->position()));
      h_sv_trackdz[svndx]->Fill(tri->dz(beamspot->position()));

      TLorentzVector p4_i, p4_j, p4_k;
      const double m = 0.135;
      p4_i.SetPtEtaPhiM(pti, tri->eta(), tri->phi(), m);
      for (auto trkj = trki + 1; trkj != trke; ++trkj) {
        if (sv.trackWeight(*trkj) < track_vertex_weight_min)
          continue;
        const reco::TrackBaseRef& trj = *trkj;
        p4_j.SetPtEtaPhiM(trj->pt(), trj->eta(), trj->phi(), m);

        h_sv_trackpaircosth[svndx]->Fill(tri->momentum().Dot(trj->momentum()) / tri->p() / trj->p());
        h_sv_trackpairdr[svndx]->Fill(reco::deltaR(*tri, *trj));
        TLorentzVector p4_ij = p4_i + p4_j;
        h_sv_trackpairmass[svndx]->Fill(p4_ij.M());

        for (auto trkk = trkj + 1; trkk != trke; ++trkk) {
          if (sv.trackWeight(*trkk) < track_vertex_weight_min)
            continue;

          const reco::TrackBaseRef& trk = *trkk;
          p4_k.SetPtEtaPhiM(trk->pt(), trk->eta(), trk->phi(), m);
          h_sv_tracktriplemass[svndx]->Fill((p4_ij + p4_k).M());
        }
      }
    }

    std::sort(trackpts.begin(), trackpts.end());
    const double mintrackpt = trackpts[0];
    const double maxtrackpt = trackpts[trackpts.size()-1];
    const double maxm1trackpt = trackpts[trackpts.size()-2];
    const double maxm2trackpt = trackpts[trackpts.size()-3];

    std::vector<int> trackicity;
    for (auto i : trackicity_m)
      trackicity.push_back(i.second);
    auto max_tcity = std::max_element(trackicity.begin(), trackicity.end());
    int max_trackicity = max_tcity != trackicity.end() ? *max_tcity : 0;
    h_sv_max_trackicity->Fill(ntracks, max_trackicity);

    const vertex_tracks_distance vtx_tks_dist(sv, track_vertex_weight_min);

    const Measurement1D gen2ddist = gen_dist(sv, false);
    const Measurement1D gen3ddist = gen_dist(sv, true);

    const std::pair<bool,float> bs2dcompat = compatibility(sv, fake_bs_vtx, false);
    const Measurement1D bs2ddist = distcalc_2d.distance(sv, fake_bs_vtx);

    std::pair<bool,float> pv2dcompat, pv3dcompat;
    float pv2ddist_val, pv3ddist_val;
    float pv2ddist_err, pv3ddist_err;
    float pv2ddist_sig, pv3ddist_sig;
    pv2dcompat = pv3dcompat = std::make_pair(false, -1.f);
    pv2ddist_val = pv3ddist_val = pv2ddist_err = pv3ddist_err = pv2ddist_sig = pv3ddist_sig = -1;

    if (primary_vertex != 0) {
      pv2dcompat = compatibility(sv, *primary_vertex, false);
      Measurement1D pv2ddist = distcalc_2d.distance(sv, *primary_vertex);
      pv2ddist_val = pv2ddist.value();
      pv2ddist_err = pv2ddist.error();
      pv2ddist_sig = pv2ddist.significance();

      pv3dcompat = compatibility(sv, *primary_vertex, true);
      Measurement1D pv3ddist = distcalc_3d.distance(sv, *primary_vertex);
      pv3ddist_val = pv3ddist.value();
      pv3ddist_err = pv3ddist.error();
      pv3ddist_sig = pv3ddist.significance();
    }

    const auto bs2sv = sv.position() - beamspot->position();
    const Measurement1D bs3ddist(mag(bs2sv.x(), bs2sv.y()) * sin(sv.p4().theta()));

    const float costhmombs = costh2(sv.p4(), bs2sv);
    float costhmompv2d = -2, costhmompv3d = -2;
    if (primary_vertex != 0) {
      const auto disp = sv.position() - primary_vertex->position();
      costhmompv2d = costh2(sv.p4(), disp);
      costhmompv3d = costh3(sv.p4(), disp);
    }

    if (do_ntuple) {
      nt.ntracks         = ntracks;
      nt.ntracksptgt10   = ntracksptgt10;
      nt.ntracksptgt20   = ntracksptgt20;
      nt.trackminnhits   = trackminnhits;
      nt.trackmaxnhits   = trackmaxnhits;
      nt.chi2dof         = sv.normalizedChi2();
      nt.chi2dofprob     = TMath::Prob(sv.chi2(), sv.ndof());
      nt.p               = sv.p4().P();
      nt.pt              = sv.p4().pt();
      nt.eta             = sv.p4().eta();
      nt.rapidity        = sv.p4().Rapidity();
      nt.phi             = sv.p4().phi();
      nt.mass            = sv.p4().mass();
      nt.costhmombs      = costhmombs;
      nt.costhmompv2d    = costhmompv2d;
      nt.costhmompv3d    = costhmompv3d;
      nt.sumpt2          = sumpt2;
      nt.mintrackpt      = mintrackpt;
      nt.maxtrackpt      = maxtrackpt;
      nt.maxm1trackpt    = maxm1trackpt;
      nt.maxm2trackpt    = maxm2trackpt;
      nt.drmin           = vtx_tks_dist.drmin;
      nt.drmax           = vtx_tks_dist.drmax;
      nt.dravg           = vtx_tks_dist.dravg;
      nt.drrms           = vtx_tks_dist.drrms;
      nt.dravgw          = vtx_tks_dist.dravgw;
      nt.drrmsw          = vtx_tks_dist.drrmsw;
      nt.gen2ddist       = gen2ddist.value();
      nt.gen2derr        = gen2ddist.error();
      nt.gen2dsig        = gen2ddist.significance();
      nt.gen3ddist       = gen3ddist.value();
      nt.gen3derr        = gen3ddist.error();
      nt.gen3dsig        = gen3ddist.significance();
      nt.bs2dcompatscss  = bs2dcompat.first;
      nt.bs2dcompat      = bs2dcompat.second;
      nt.bs2ddist        = bs2ddist.value();
      nt.bs2derr         = bs2ddist.error();
      nt.bs2dsig         = bs2ddist.significance();
      nt.bs3ddist        = bs3ddist.value();
      nt.pv2dcompatscss  = pv2dcompat.first;
      nt.pv2dcompat      = pv2dcompat.second;
      nt.pv2ddist        = pv2ddist_val;
      nt.pv2derr         = pv2ddist_err;
      nt.pv2dsig         = pv2ddist_sig;
      nt.pv3dcompatscss  = pv3dcompat.first;
      nt.pv3dcompat      = pv3dcompat.second;
      nt.pv3ddist        = pv3ddist_val;
      nt.pv3derr         = pv3ddist_err;
      nt.pv3dsig         = pv3ddist_sig;

      tree->Fill();
    }

    PairwiseHistos::ValueMap v = {
        {"ntracks",         ntracks},
        {"ntracksptgt10",   ntracksptgt10},
        {"ntracksptgt20",   ntracksptgt20},
        {"trackminnhits",   trackminnhits},
        {"trackmaxnhits",   trackmaxnhits},
        {"chi2dof",         sv.normalizedChi2()},
        {"chi2dofprob",     TMath::Prob(sv.chi2(), sv.ndof())},
        {"p",               sv.p4().P()},
        {"pt",              sv.p4().pt()},
        {"eta",             sv.p4().eta()},
        {"rapidity",        sv.p4().Rapidity()},
        {"phi",             sv.p4().phi()},
        {"mass",            sv.p4().mass()},
        {"costhmombs",      costhmombs},
        {"costhmompv2d",    costhmompv2d},
        {"costhmompv3d",    costhmompv3d},
        {"sumpt2",          sumpt2},
        {"mintrackpt",      mintrackpt},
        {"maxtrackpt",      maxtrackpt},
        {"maxm1trackpt",    maxm1trackpt},
        {"maxm2trackpt",    maxm2trackpt},
        {"drmin",           vtx_tks_dist.drmin},
        {"drmax",           vtx_tks_dist.drmax},
        {"dravg",           vtx_tks_dist.dravg},
        {"drrms",           vtx_tks_dist.drrms},
        {"dravgw",          vtx_tks_dist.dravgw},
        {"drrmsw",          vtx_tks_dist.drrmsw},
        {"gen2ddist",       gen2ddist.value()},
        {"gen2derr",        gen2ddist.error()},
        {"gen2dsig",        gen2ddist.significance()},
        {"gen3ddist",       gen3ddist.value()},
        {"gen3derr",        gen3ddist.error()},
        {"gen3dsig",        gen3ddist.significance()},
        {"bs2dcompatscss",  bs2dcompat.first},
        {"bs2dcompat",      bs2dcompat.second},
        {"bs2ddist",        bs2ddist.value()},
        {"bs2derr",         bs2ddist.error()},
        {"bs2dsig",         bs2ddist.significance()},
        {"bs3ddist",        bs3ddist.value()},
        {"pv2dcompatscss",  pv2dcompat.first},
        {"pv2dcompat",      pv2dcompat.second},
        {"pv2ddist",        pv2ddist_val},
        {"pv2derr",         pv2ddist_err},
        {"pv2dsig",         pv2ddist_sig},
        {"pv3dcompatscss",  pv3dcompat.first},
        {"pv3dcompat",      pv3dcompat.second},
        {"pv3ddist",        pv3ddist_val},
        {"pv3derr",         pv3ddist_err},
        {"pv3dsig",         pv3ddist_sig},
    };
    h_sv[svndx].Fill(v);
  }

  //////////////////////////////////////////////////////////////////////

  if (do_ntuple) {
    nt.clear(false);
    nt.nsv = nsv;
    nt.nsvpass = nsvpass;
    tree->Fill();
  }

  h_nsvpass->Fill(nsvpass);
  h_nsvpass_v_minlspdist2d->Fill(nt.minlspdist2d, nsvpass);
  h_nsvpass_v_lspdist2d->Fill(nt.lspdist2d, nsvpass);
  h_nsvpass_v_lspdist3d->Fill(nt.lspdist3d, nsvpass);

  if (sv0 && sv1) {
    double svdist2d = mag(sv0->position().x() - sv1->position().x(),
                          sv0->position().y() - sv1->position().y());
    double svdist3d = mag(sv0->position().x() - sv1->position().x(),
                          sv0->position().y() - sv1->position().y(),
                          sv0->position().z() - sv1->position().z());
    h_svdist2d->Fill(svdist2d);
    h_svdist3d->Fill(svdist3d);
    h_svdist2d_v_lspdist2d->Fill(nt.lspdist2d, svdist2d);
    h_svdist3d_v_lspdist3d->Fill(nt.lspdist3d, svdist3d);
    h_svdist2d_v_minlspdist2d->Fill(nt.minlspdist2d, svdist2d);
  }

  const int nvtx = secondary_vertices.size();
  for (int ivtx = 0; ivtx < nvtx; ++ivtx) {
    const reco::Vertex& vtxi = secondary_vertices[ivtx];
    if (!use_vertex(vtxi))
      continue;

    const std::map<int,int>& icityi = trackicities[ivtx];

    for (int jvtx = ivtx + 1; jvtx < nvtx; ++jvtx) {
      const reco::Vertex& vtxj = secondary_vertices[jvtx];
      if (!use_vertex(vtxj))
        continue;

      const std::map<int,int>& icityj = trackicities[jvtx];

      Measurement1D pair2ddist = distcalc_2d.distance(vtxi, vtxj);
      Measurement1D pair3ddist = distcalc_3d.distance(vtxi, vtxj);

      std::pair<bool, float> pair2dcompat = compatibility(vtxi, vtxj, false);
      std::pair<bool, float> pair3dcompat = compatibility(vtxi, vtxj, true);

      h_pair2dcompatscss->Fill(pair2dcompat.first);
      h_pair2dcompat->Fill(pair2dcompat.second);
      h_pair2ddist->Fill(pair2ddist.value());
      h_pair2derr->Fill(pair2ddist.error());
      h_pair2dsig->Fill(pair2ddist.significance());
      h_pair3dcompatscss->Fill(pair3dcompat.first);
      h_pair3dcompat->Fill(pair3dcompat.second);
      h_pair3ddist->Fill(pair3ddist.value());
      h_pair3derr->Fill(pair3ddist.error());
      h_pair3dsig->Fill(pair3ddist.significance());

      int nsharedtracks = 0;
      for (auto it : icityi)
        if (icityj.find(it.first) != icityj.end())
          ++nsharedtracks;

      h_pairnsharedtracks->Fill(nsharedtracks);
      h_pairfsharedtracks->Fill(float(nsharedtracks)/icityi.size(), float(nsharedtracks)/icityj.size());
    }
  }
}

DEFINE_FWK_MODULE(VtxRecoPlay);
