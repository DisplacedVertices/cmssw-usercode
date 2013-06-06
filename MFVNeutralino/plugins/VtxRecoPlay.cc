#include "TH1F.h"
#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
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
  const edm::InputTag tracks_src;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_src;
  const edm::InputTag vertex_src;
  const bool print_info;
  const bool is_mfv;
  const bool is_ttbar;
  const bool do_scatterplots;
  const double jet_pt_min;
  const double track_pt_min;

  const int min_sv_ntracks;
  const double max_sv_chi2dof;
  const double max_sv_err2d;
  const double min_sv_mass;
  const double min_sv_drmax;

  VertexDistanceXY distcalc_2d;
  VertexDistance3D distcalc_3d;

  float abs_error(const reco::Vertex& sv, bool use3d) {
    const double x = sv.x();
    const double y = sv.y();
    const double z = use3d ? sv.z() : 0;
    AlgebraicVector3 v(x,y,z);
    AlgebraicSymMatrix33 cov = sv.covariance();
    double dist = mag(x,y,z);
    double err2 = ROOT::Math::Similarity(v, cov);
    return dist != 0 ? sqrt(err2)/dist : 0;
  }

  struct vertex_tracks_distance {
    double drmin, drmax;
    double dravg, dravgw, dravgvw;
    double drrms, drrmsw, drrmsvw;

    vertex_tracks_distance(const reco::Vertex& sv) {
      drmin = 1e99;
      drmax = dravg = dravgw = drrms = drrmsw = 0;
      std::vector<double> drs;
      std::vector<double> ws;
      std::vector<double> vws;
      double sumw = 0, sumvw = 0;

      auto trkb = sv.tracks_begin();
      auto trke = sv.tracks_end();
      for (auto trki = trkb; trki != trke; ++trki) {
        for (auto trkj = trki + 1; trkj != trke; ++trkj) {
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
    return 
      int(vtx.tracksSize()) >= min_sv_ntracks &&
      vtx.normalizedChi2() < max_sv_chi2dof   &&
      abs_error(vtx, false) < max_sv_err2d    &&
      vtx.p4().mass() >= min_sv_mass          &&
      (min_sv_drmax == 0 || vertex_tracks_distance(vtx).drmax >= min_sv_drmax);
  }

  TH1F* h_sim_pileup_num_int[3];
  TH1F* h_sim_pileup_true_num_int[3];

  TH1F* h_gen_valid;
  TH1F* h_gen_pos_1d[2][3];
  TH2F* h_gen_pos_2d[2][3];

  TH1F* h_njets;
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
  TH1F* h_pv_phi[2];
  TH1F* h_pv_mass[2];
  TH1F* h_pv_sumpt2[2];
  
  TH1F* h_nsv;
  TH1F* h_nsvpass;
  TH2F* h_sv_max_trackicity;
  TH1F* h_sv_pos_1d[3][3]; // index 0: 0 = the highest mass SV (all),
                           // 1 = highest mass SV passing cuts, 
                           // 2 = second highest mass SV passing cuts,
                           // 2 = rest
  TH2F* h_sv_pos_2d[3][3];
  PairwiseHistos h_sv[3];

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
};

VtxRecoPlay::VtxRecoPlay(const edm::ParameterSet& cfg)
  : tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    print_info(cfg.getParameter<bool>("print_info")),
    is_mfv(cfg.getParameter<bool>("is_mfv")),
    is_ttbar(cfg.getParameter<bool>("is_ttbar")),
    do_scatterplots(cfg.getParameter<bool>("do_scatterplots")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    track_pt_min(cfg.getParameter<double>("track_pt_min")),
    min_sv_ntracks(cfg.getParameter<int>("min_sv_ntracks")),
    max_sv_chi2dof(cfg.getParameter<double>("max_sv_chi2dof")),
    max_sv_err2d(cfg.getParameter<double>("max_sv_err2d")),
    min_sv_mass(cfg.getParameter<double>("min_sv_mass")),
    min_sv_drmax(cfg.getParameter<double>("min_sv_drmax"))
{
  edm::Service<TFileService> fs;

  for (int i = 0; i < 3; ++i) {
    const char* ex = (i == 0 ? "m1" : (i == 1 ? "0" : "p1"));
    h_sim_pileup_num_int[i]      = fs->make<TH1F>(TString::Format("h_sim_pileup_num_int_bx%s",      ex), "", 65, 0, 65);
    h_sim_pileup_true_num_int[i] = fs->make<TH1F>(TString::Format("h_sim_pileup_true_num_int_bx%s", ex), "", 65, 0, 65);
  }

  h_gen_valid = fs->make<TH1F>("h_gen_valid", ";gen valid?;frac. events", 2, 0, 2);
  
  for (int j = 0; j < 2; ++j) {
    for (int i = 0; i < 3; ++i) {
      float l = i == 2 ? 25 : 1;
      h_gen_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_gen_pos_1d_%i%i", j, i), TString::Format(";gen #%i vtx pos[%i] (cm);arb. units", j, i), 100, -l, l);
    }
    h_gen_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_gen_pos_2d_%ixy", j), TString::Format(";gen #%i vtx x (cm);gen #%i vtx y (cm)", j, j), 100, -1, 1, 100, -1, 1);
    h_gen_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_gen_pos_2d_%ixz", j), TString::Format(";gen #%i vtx x (cm);gen #%i vtx z (cm)", j, j), 100, -1, 1, 100,-25,25);
    h_gen_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_gen_pos_2d_%iyz", j), TString::Format(";gen #%i vtx y (cm);gen #%i vtx z (cm)", j, j), 100, -1, 1, 100,-25,25);
  }

  h_njets = fs->make<TH1F>("h_njets", ";# of unclean PF jets;arb. units", 15, 0, 30);
  h_ntracks = fs->make<TH1F>("h_ntracks", ";# of general tracks;arb. units", 20, 0, 2000);
  h_ntracksptpass = fs->make<TH1F>("h_ntracksptpass", ";# of selected tracks;arb. units", 20, 0, 60);

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices;arb. units", 65, 0, 65);

  for (int j = 0; j < 2; ++j) {
    const char* ex = j == 0 ? "the" : "other";

    for (int i = 0; i < 3; ++i) {
      float l = i == 2 ? 25 : 1;
      h_pv_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_pv_pos_1d_%i%i", j, i), TString::Format(";%s PV pos[%i] (cm);arb. units", ex, i), 100, -l, l);
    }
    h_pv_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_pv_pos_2d_%ixy", j), TString::Format(";%s PV x (cm);%s PV y (cm)", ex, ex), 100, -1, 1, 100, -1, 1);
    h_pv_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_pv_pos_2d_%ixz", j), TString::Format(";%s PV x (cm);%s PV z (cm)", ex, ex), 100, -1, 1, 100,-25,25);
    h_pv_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_pv_pos_2d_%iyz", j), TString::Format(";%s PV y (cm);%s PV z (cm)", ex, ex), 100, -1, 1, 100,-25,25);
    
    h_pv_ntracks[j] = fs->make<TH1F>(TString::Format("h_pv_ntracks_%i", j), TString::Format(";# tracks for %s PV;arb.units", ex), 50, 0, 200);
    h_pv_ntracksptpass[j] = fs->make<TH1F>(TString::Format("h_pv_ntracksptpass_%i", j), TString::Format(";# selected tracks for %s PV;arb.units", ex), 50, 0, 50);
    h_pv_chi2dof[j] = fs->make<TH1F>(TString::Format("h_pv_chi2dof_%i", j), TString::Format(";#chi^{2}/dof for %s PV;arb.units", ex), 20, 0, 10);
    h_pv_chi2dofprob[j] = fs->make<TH1F>(TString::Format("h_pv_chi2dofprob_%i", j), TString::Format(";p(#chi^{2}/dof) for %s PV;arb.units", ex), 20, 0, 1);

    h_pv_pt[j] = fs->make<TH1F>(TString::Format("h_pv_pt_%i", j), TString::Format(";%s PV p_{T} (GeV);arb.units", ex), 25, 0, 500);
    h_pv_eta[j] = fs->make<TH1F>(TString::Format("h_pv_eta_%i", j), TString::Format(";%s PV #eta;arb.units", ex), 30, -5, 5);
    h_pv_phi[j] = fs->make<TH1F>(TString::Format("h_pv_phi_%i", j), TString::Format(";%s PV #phi;arb.units", ex), 30, -3.15, 3.15);
    h_pv_mass[j] = fs->make<TH1F>(TString::Format("h_pv_mass_%i", j), TString::Format(";%s PV mass (GeV);arb.units", ex), 50, 0, 1000);
    h_pv_sumpt2[j] = fs->make<TH1F>(TString::Format("h_pv_sumpt2_%i", j), TString::Format(";%s PV #Sigma p_{T}^{2} (GeV);arb.units", ex), 30, 0, 15000);
  }

  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices;arb. units", 100, 0, 100);
  h_nsvpass = fs->make<TH1F>("h_nsvpass", ";# of selected secondary vertices;arb. units", 100, 0, 100);
  h_sv_max_trackicity = fs->make<TH2F>("h_sv_max_trackicity", ";# of tracks in SV;highest trackicity", 40, 0, 40, 40, 0, 40);

  for (int j = 0; j < 3; ++j) {
    std::string ex;
    if (j == 0)
      ex = "mass0";
    else if (j == 1)
      ex = "mass1";
    else
      ex = "rest";
    const char* exc = ex.c_str();

    for (int i = 0; i < 3; ++i) {
      float l = i == 2 ? 10 : 1;
      h_sv_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_sv_pos_1d_%i%i", j, i), TString::Format(";%s SV pos[%i] (cm);arb. units", exc, i), 100, -l, l);
    }
    h_sv_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixy", j), TString::Format(";%s SV x (cm);%s SV y (cm)", exc, exc), 100, -1, 1, 100, -1, 1);
    h_sv_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixz", j), TString::Format(";%s SV x (cm);%s SV z (cm)", exc, exc), 100, -1, 1, 100,-25,25);
    h_sv_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%iyz", j), TString::Format(";%s SV y (cm);%s SV z (cm)", exc, exc), 100, -1, 1, 100,-25,25);

    PairwiseHistos::HistoDefs hs;
    hs.add("ntracks",        "# of tracks/SV",                              40,    0,      40);
    hs.add("ntracksptpass",  "# of selected tracks/SV",                     40,    0,      40);
    hs.add("trackminnhits",  "min number of hits on track per SV",          40,    0,      40);
    hs.add("chi2dof",        "SV #chi^2/dof",                               50,    0,      20);
    hs.add("chi2dofprob",    "SV p(#chi^2, dof)",                           50,    0,       1);
    hs.add("pt",             "SV p_{T} (GeV)",                             100,    0,     300);
    hs.add("eta",            "SV #eta",                                     50,   -4,       4);
    hs.add("phi",            "SV #phi",                                     50,   -3.15,    3.15);
    hs.add("mass",           "SV mass (GeV)",                              100,    0,     250);
    hs.add("sumpt2",         "SV #Sigma p_{T}^{2} (GeV^2)",                100,    0,   10000);
    hs.add("mintrackpt",     "SV min{trk_{i} p_{T}} (GeV)",                 50,    0,      50);
    hs.add("maxtrackpt",     "SV max{trk_{i} p_{T}} (GeV)",                100,    0,     150);
    hs.add("drmin",          "SV min{#Delta R(i,j)}",                      100,    0,       1);
    hs.add("drmax",          "SV max{#Delta R(i,j)}",                      100,    0,       4);
    hs.add("dravg",          "SV avg{#Delta R(i,j)}",                      100,    0,       2.5);
    hs.add("drrms",          "SV rms{#Delta R(i,j)}",                      100,    0,       2);
    hs.add("dravgw",         "SV wavg{#Delta R(i,j)}",                     100,    0,       3);
    hs.add("drrmsw",         "SV wrms{#Delta R(i,j)}",                     100,    0,       2);
    hs.add("gen2ddist",      "dist2d(SV, closest gen vtx) (cm)",           100,    0,       0.5);
    hs.add("gen2derr",       "#sigma(dist2d(SV, closest gen vtx)) (cm)",   100,    0,       0.5);
    hs.add("gen3ddist",      "dist3d(SV, closest gen vtx) (cm)",           100,    0,       0.5);
    hs.add("gen3derr",       "#sigma(dist3d(SV, closest gen vtx)) (cm)",   100,    0,       0.5);
    hs.add("bs2dcompatscss", "compat2d(SV, beamspot) success",               2,    0,       2);
    hs.add("bs2dcompat",     "compat2d(SV, beamspot)",                     100,    0,     500);
    hs.add("bs2ddist",       "dist2d(SV, beamspot) (cm)",                  100,    0,       0.5);
    hs.add("bs2derr",        "#sigma(dist2d(SV, beamspot)) (cm)",          100,    0,       0.1);
    hs.add("bs2dsig",        "N#sigma(dist2d(SV, beamspot))",              100,    0,     100);
    hs.add("pv2dcompatscss", "compat2d(SV, PV) success",                     2,    0,       2);
    hs.add("pv2dcompat",     "compat2d(SV, PV)",                           100,    0,     500);
    hs.add("pv2ddist",       "dist2d(SV, PV) (cm)",                        100,    0,       0.5);
    hs.add("pv2derr",        "#sigma(dist2d(SV, PV)) (cm)",                100,    0,       0.1);
    hs.add("pv2dsig",        "N#sigma(dist2d(SV, PV))",                    100,    0,     100);
    hs.add("pv3dcompatscss", "compat3d(SV, PV) success",                     2,    0,       2);
    hs.add("pv3dcompat",     "compat3d(SV, PV)",                           100,    0,     500);
    hs.add("pv3ddist",       "dist3d(SV, PV) (cm)",                        100,    0,       0.5);
    hs.add("pv3derr",        "#sigma(dist3d(SV, PV)) (cm)",                100,    0,       0.1);
    hs.add("pv3dsig",        "N#sigma(dist3d(SV, PV))",                    100,    0,     100);
    h_sv[j].Init("h_sv_" + ex, hs, true, do_scatterplots);
  }

  h_pair2dcompatscss = fs->make<TH1F>("h_pair2dcompatscss", ";pair compat2d success;arb. units",       2,    0,     2);
  h_pair2dcompat     = fs->make<TH1F>("h_pair2dcompat",     ";pair compat2d;arb. units",             100,    0,   100);
  h_pair2ddist       = fs->make<TH1F>("h_pair2ddist",       ";pair dist2d (cm);arb. units",          100,    0,     0.5);
  h_pair2derr        = fs->make<TH1F>("h_pair2derr",        ";pair #sigma(dist2d) (cm);arb. units",  100,    0,     0.1);
  h_pair2dsig        = fs->make<TH1F>("h_pair2dsig",        ";pair N#sigma(dist2d);arb. units",      100,    0,    50);
  h_pair3dcompatscss = fs->make<TH1F>("h_pair3dcompatscss", ";pair compat3d success;arb. units",       2,    0,     2);
  h_pair3dcompat     = fs->make<TH1F>("h_pair3dcompat",     ";pair compat3d;arb. units",             100,    0,   100);
  h_pair3ddist       = fs->make<TH1F>("h_pair3ddist",       ";pair dist3d (cm);arb. units",          100,    0,     0.5);
  h_pair3derr        = fs->make<TH1F>("h_pair3derr",        ";pair #sigma(dist3d) (cm);arb. units",  100,    0,     0.1);
  h_pair3dsig        = fs->make<TH1F>("h_pair3dsig",        ";pair N#sigma(dist3d);arb. units",      100,    0,    50);

  h_pairnsharedtracks = fs->make<TH1F>("h_pairnsharedtracks", "", 50, 0, 50);
  h_pairfsharedtracks = fs->make<TH2F>("h_pairfsharedtracks", "", 51, 0,  1.02, 51, 0,  1.02);
}

void VtxRecoPlay::analyze(const edm::Event& event, const edm::EventSetup& setup) {
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

  float gen_verts[2][3] = {{0}};
  bool gen_valid = false;

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

  edm::Handle<reco::PFJetCollection> jets;
  event.getByLabel("ak5PFJets", jets);
  
  int njets = 0;
  for (const reco::PFJet& jet : *jets) {
    if (jet.pt() > jet_pt_min && 
        fabs(jet.eta()) < 2.5 && 
        jet.numberOfDaughters() > 1 &&
        jet.neutralHadronEnergyFraction() < 0.99 && 
        jet.neutralEmEnergyFraction() < 0.99 && 
        (fabs(jet.eta()) >= 2.4 || (jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0. && jet.chargedMultiplicity() > 0)))
      njets += 1;
  }

  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(tracks_src, tracks);
  
  const int ntracks = int(tracks->size());
  int ntracksptpass = 0;
  for (const reco::Track& tk : *tracks)
    if (tk.pt() > track_pt_min)
      ++ntracksptpass;

  h_njets->Fill(njets);
  h_ntracks->Fill(ntracks);
  h_ntracksptpass->Fill(ntracksptpass);
  
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
    h_pv_phi          [pvndx]->Fill(pv.p4().phi());
    h_pv_mass         [pvndx]->Fill(pv.p4().mass());
    h_pv_sumpt2       [pvndx]->Fill(pv_sumpt2);
  }

  edm::Handle<reco::VertexCollection> original_secondary_vertices;
  event.getByLabel(vertex_src, original_secondary_vertices);

  reco::VertexCollection secondary_vertices(*original_secondary_vertices);
  std::sort(secondary_vertices.begin(), secondary_vertices.end(),
            [](const reco::Vertex& a, const reco::Vertex& b) { return a.p4().mass() > b.p4().mass(); });
  
  const int nsv = int(secondary_vertices.size());
  h_nsv->Fill(nsv);
  int nsvpass = 0;
  std::vector<std::map<int,int> > trackicities(nsv);
  for (int isv = 0; isv < nsv; ++isv) {
    const reco::Vertex& sv = secondary_vertices[isv];
    if (!use_vertex(sv))
      continue;
    ++nsvpass;

    const int svndx = isv >= 2 ? 2 : isv;

    for (int i = 0; i < 3; ++i)
      h_sv_pos_1d[svndx][i]->Fill(coord(sv.position(), i) - coord(beamspot->position(), i));
    h_sv_pos_2d[svndx][0]->Fill(sv.position().x() - bsx, sv.position().y() - bsy);
    h_sv_pos_2d[svndx][1]->Fill(sv.position().x() - bsx, sv.position().z() - bsz);
    h_sv_pos_2d[svndx][2]->Fill(sv.position().y() - bsy, sv.position().z() - bsz);

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();
    std::map<int,int>& trackicity_m = trackicities[isv];
    int ntracks = trke - trkb;
    int ntracksptpass = 0;
    int trackminnhits = 1000;
    double sumpt2 = 0;
    double mintrackpt = 1e99;
    double maxtrackpt = 0;

    for (auto trki = trkb; trki != trke; ++trki) {
      int key = trki->key();
      std::map<int,int>::iterator icity = trackicity_m.find(key);
      if (icity == trackicity_m.end())
        trackicity_m[key] = 1;
      else
        icity->second += 1;

      int nhits = (*trki)->numberOfValidHits();
      if (nhits < trackminnhits)
        trackminnhits = nhits;

      double pti = (*trki)->pt();
      if (pti > track_pt_min)
        ++ntracksptpass;
      if (pti > maxtrackpt)
        maxtrackpt = pti;
      if (pti < mintrackpt)
        mintrackpt = pti;
      sumpt2 += pti*pti;
    }

    std::vector<int> trackicity;
    for (auto i : trackicity_m) 
      trackicity.push_back(i.second);
    int max_trackicity = *std::max_element(trackicity.begin(), trackicity.end());
    h_sv_max_trackicity->Fill(ntracks, max_trackicity);

    vertex_tracks_distance vtx_tks_dist(sv);

    float gen2ddist = 1e99;
    float gen3ddist = 1e99;
    for (int i = 0; i < 2; ++i) {
      float gen2ddist_ = mag(sv.x() - gen_verts[i][0], sv.y() - gen_verts[i][1]);
      float gen3ddist_ = mag(sv.x() - gen_verts[i][0], sv.y() - gen_verts[i][1], sv.z() - gen_verts[i][2]);
      if (gen2ddist_ < gen2ddist) gen2ddist = gen2ddist_;
      if (gen3ddist_ < gen3ddist) gen3ddist = gen3ddist_;
    }
    
    float gen2derr = abs_error(sv, false);
    float gen3derr = abs_error(sv, true);

    std::pair<bool,float> bs2dcompat = compatibility(sv, fake_bs_vtx, false);
    Measurement1D bs2ddist = distcalc_2d.distance(sv, fake_bs_vtx);

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

    PairwiseHistos::ValueMap v = {
        {"ntracks",         ntracks},        
        {"ntracksptpass",   ntracksptpass},   
        {"trackminnhits",   trackminnhits},
        {"chi2dof",         sv.normalizedChi2()},        
        {"chi2dofprob",     TMath::Prob(sv.chi2(), sv.ndof())},
        {"pt",              sv.p4().pt()},
        {"eta",             sv.p4().eta()},
        {"phi",             sv.p4().phi()},
        {"mass",            sv.p4().mass()},
        {"sumpt2",          sumpt2},
        {"mintrackpt",      mintrackpt},
        {"maxtrackpt",      maxtrackpt},
        {"drmin",           vtx_tks_dist.drmin},
        {"drmax",           vtx_tks_dist.drmax},
        {"dravg",           vtx_tks_dist.dravg},
        {"drrms",           vtx_tks_dist.drrms},
        {"dravgw",          vtx_tks_dist.dravgw},
        {"drrmsw",          vtx_tks_dist.drrmsw},
        {"gen2ddist",       gen2ddist},
        {"gen2derr",        gen2derr},
        {"gen3ddist",       gen3ddist},
        {"gen3derr",        gen3derr},
        {"bs2dcompatscss",  bs2dcompat.first},
        {"bs2dcompat",      bs2dcompat.second},
        {"bs2ddist",        bs2ddist.value()},
        {"bs2derr",         bs2ddist.error()},
        {"bs2dsig",         bs2ddist.significance()},
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

  h_nsvpass->Fill(nsvpass);

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
