#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVResolutions : public edm::EDAnalyzer {
 public:
  explicit MFVResolutions(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const std::string mode;
  const bool doing_mfv3j;
  const bool doing_h2xqq;

  const edm::InputTag vertex_src;
  const edm::InputTag mevent_src;
  const int which_mom;
  const double max_dr;
  const double max_dist;

  const edm::InputTag gen_src;
  bool mci_warned;
  const edm::InputTag gen_jet_src;

  TH1F* h_dr;
  TH1F* h_dist;

  TH1F* h_lsp_nmatch[2];
  TH2F* h_lsp0nmatch_lsp1nmatch;
  TH2F* h_vtxmatch_vtxtotal;

  TH1F* h_dx;
  TH1F* h_dy;
  TH1F* h_dz;
  TH1F* h_dist2d;
  TH1F* h_dist3d;

  TH1F* h_cxx;
  TH1F* h_cyy;
  TH1F* h_czz;
  TH1F* h_bs2derr;

  TH1F* h_pull_dx;
  TH1F* h_pull_dy;
  TH1F* h_pull_dz;
  TH1F* h_pull_dist2d;

  TH1F* h_r_p;
  TH1F* h_r_pt;
  TH1F* h_r_eta;
  TH1F* h_r_phi;
  TH1F* h_r_mass;
  TH1F* h_r_msptm;
  TH1F* h_r_msptm_mass;
  TH1F* h_r_energy;
  TH1F* h_r_px;
  TH1F* h_r_py;
  TH1F* h_r_pz;
  TH1F* h_r_rapidity;
  TH1F* h_r_theta;
  TH1F* h_r_betagamma;
  TH1F* h_r_avgbetagammalab;
  TH1F* h_r_avgbetagammacmz;

  TH1F* h_f_p;
  TH1F* h_f_pt;
  TH1F* h_f_mass;
  TH1F* h_f_msptm;
  TH1F* h_f_msptm_mass;
  TH1F* h_f_energy;

  TH2F* h_rp_rmass;
  TH2F* h_fp_fmass;
  TH2F* h_s_p_mass;

  TH2F* h_rp_renergy;
  TH2F* h_fp_fenergy;
  TH2F* h_s_p_energy;

  TH2F* h_s_p;
  TH2F* h_s_pt;
  TH2F* h_s_eta;
  TH2F* h_s_phi;
  TH2F* h_s_mass;
  TH2F* h_s_msptm;
  TH2F* h_s_msptm_mass;
  TH2F* h_s_energy;
  TH2F* h_s_px;
  TH2F* h_s_py;
  TH2F* h_s_pz;
  TH2F* h_s_rapidity;
  TH2F* h_s_theta;
  TH2F* h_s_betagamma;
  TH2F* h_s_avgbetagammalab;
  TH2F* h_s_avgbetagammacmz;

  TH2F* h_s_genjets_njets;
  TH2F* h_s_genjets_ncalojets;
  TH2F* h_s_genjets_calojetpt4;
  TH2F* h_s_genjets_jetsumht;

  TH2F* h_s_partons_njets;
  TH2F* h_s_partons_ncalojets;
  TH2F* h_s_partons_calojetpt4;
  TH2F* h_s_partons_jetsumht;

  TH2F* h_s_drmin;
  TH2F* h_s_drmax;

  TH1F* h_dbv_nomatch;
  TH2F* h_s_dbv;
  TH2F* h_s_dvv;

  TH2F* h_s_dbv_gendvv;
  TH2F* h_s_dbv_betagamma;
  TH2F* h_s_drmax_betagamma;
  TH2F* h_s_drmax_dbv;
  TH2F* h_s_gendrmax_dbv;

  TH2F* h_s_dx_drmax;
  TH2F* h_s_dy_drmax;
  TH2F* h_s_dz_drmax;
  TH2F* h_s_dist2d_drmax;
  TH2F* h_s_dist3d_drmax;

  TH1F* h_partons_pt1;
  TH1F* h_partons_pt2;
  TH1F* h_partons_pt3;
  TH1F* h_partons_pt4;
  TH1F* h_partons_pt5;
  TH1F* h_partons_sumpt;

  TH1F* h_gen_dbv;
  TH1F* h_gen_dvv;
  TH1F* h_gen_dvv_matched;
};

MFVResolutions::MFVResolutions(const edm::ParameterSet& cfg)
  : mode(cfg.getParameter<std::string>("mode")),
    doing_mfv3j(mode == "mfv3j"),
    doing_h2xqq(mode == "h2xqq"),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    which_mom(cfg.getParameter<int>("which_mom")),
    max_dr(cfg.getParameter<double>("max_dr")),
    max_dist(cfg.getParameter<double>("max_dist")),
    gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src"))
{
  if (!(doing_mfv3j || doing_h2xqq))
    throw cms::Exception("Configuration") << "mode must be either mfv3j or h2xqq, got " << mode;

  die_if_not(which_mom >= 0 && which_mom < mfv::NMomenta, "invalid which_mom");

  edm::Service<TFileService> fs;

  h_dr = fs->make<TH1F>("h_dr", ";deltaR to closest lsp;number of vertices", 150, 0, 7);
  h_dist = fs->make<TH1F>("h_dist", ";distance to closest lsp;number of vertices", 100, 0, 0.02);

  for (int i = 0; i < 2; ++i) {
    h_lsp_nmatch[i] = fs->make<TH1F>(TString::Format("h_lsp%d_nmatch", i), TString::Format(";number of vertices that match lsp%d;events", i), 15, 0, 15);
  }
  h_lsp0nmatch_lsp1nmatch = fs->make<TH2F>("h_lsp0nmatch_lsp1nmatch", ";lsp1_nmatch;lsp0_nmatch", 15, 0, 15, 15, 0, 15);
  h_vtxmatch_vtxtotal = fs->make<TH2F>("h_vtxmatch_vtxtotal", ";total number of vertices in the event;number of vertices that match an lsp", 15, 0, 15, 15, 0, 15);

  h_dx = fs->make<TH1F>("h_dx", ";x resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dy = fs->make<TH1F>("h_dy", ";y resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dz = fs->make<TH1F>("h_dz", ";z resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dist2d = fs->make<TH1F>("h_dist2d", ";dist2d(lsp,vtx) (cm);number of vertices", 100, 0, 0.02);
  h_dist3d = fs->make<TH1F>("h_dist3d", ";dist3d(lsp,vtx) (cm);number of vertices", 100, 0, 0.02);

  h_cxx = fs->make<TH1F>("h_cxx", ";sqrt(cxx) (cm);number of vertices", 100, 0, 0.05);
  h_cyy = fs->make<TH1F>("h_cyy", ";sqrt(cyy) (cm);number of vertices", 100, 0, 0.05);
  h_czz = fs->make<TH1F>("h_czz", ";sqrt(czz) (cm);number of vertices", 100, 0, 0.05);
  h_bs2derr = fs->make<TH1F>("h_bs2derr", ";bs2derr (cm);number of vertices", 100, 0, 0.05);

  h_pull_dx = fs->make<TH1F>("h_pull_dx", ";pull on x resolution;number of vertices", 100, -5, 5);
  h_pull_dy = fs->make<TH1F>("h_pull_dy", ";pull on y resolution;number of vertices", 100, -5, 5);
  h_pull_dz = fs->make<TH1F>("h_pull_dz", ";pull on z resolution;number of vertices", 100, -5, 5);
  h_pull_dist2d = fs->make<TH1F>("h_pull_dist2d", ";pull on dist2d resolution;number of vertices", 100, 0, 5);

  h_r_p = fs->make<TH1F>("h_r_p", ";p resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_pt = fs->make<TH1F>("h_r_pt", ";p_{T} resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_eta = fs->make<TH1F>("h_r_eta", ";eta resolution;number of vertices", 50, -4, 4);
  h_r_phi = fs->make<TH1F>("h_r_phi", ";phi resolution;number of vertices", 50, -3.15, 3.15);
  h_r_mass = fs->make<TH1F>("h_r_mass", ";mass resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_msptm = fs->make<TH1F>("h_r_msptm", ";msptm resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_msptm_mass = fs->make<TH1F>("h_r_msptm_mass", ";msptm resolution w.r.t. mass (GeV);number of vertices", 300, -1500, 1500);
  h_r_energy = fs->make<TH1F>("h_r_energy", ";energy resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_px = fs->make<TH1F>("h_r_px", ";px resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_py = fs->make<TH1F>("h_r_py", ";py resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_pz = fs->make<TH1F>("h_r_pz", ";pz resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_rapidity = fs->make<TH1F>("h_r_rapidity", ";rapidity resolution;number of vertices", 50, -4, 4);
  h_r_theta = fs->make<TH1F>("h_r_theta", ";theta resolution;number of vertices", 50, -3.15, 3.15);
  h_r_betagamma = fs->make<TH1F>("h_r_betagamma", ";betagamma resolution;number of vertices", 200, -10, 10);
  h_r_avgbetagammalab = fs->make<TH1F>("h_r_avgbetagammalab", ";avgbetagammalab resolution;events", 200, -10, 10);
  h_r_avgbetagammacmz = fs->make<TH1F>("h_r_avgbetagammacmz", ";avgbetagammacmz resolution;events", 200, -10, 10);

  h_f_p = fs->make<TH1F>("h_f_p", ";fractional p resolution;number of vertices", 100, -1, 5);
  h_f_pt = fs->make<TH1F>("h_f_pt", ";fractional p_{T} resolution;number of vertices", 100, -1, 5);
  h_f_mass = fs->make<TH1F>("h_f_mass", ";fractional mass resolution;number of vertices", 100, -1, 5);
  h_f_msptm = fs->make<TH1F>("h_f_msptm", ";fractional msptm resolution;number of vertices", 100, -1, 5);
  h_f_msptm_mass = fs->make<TH1F>("h_f_msptm_mass", ";fractional msptm resolution w.r.t. mass;number of vertices", 100, -1, 5);
  h_f_energy = fs->make<TH1F>("h_f_energy", ";fractional energy resolution;number of vertices", 100, -1, 5);

  h_rp_rmass = fs->make<TH2F>("h_rp_rmass", ";mass resolution;p resolution", 300, -1500, 1500, 300, -1500, 1500);
  h_fp_fmass = fs->make<TH2F>("h_fp_fmass", ";fractional mass resolution;fractional p resolution", 300, -1, 2, 300, -1, 2);
  h_s_p_mass = fs->make<TH2F>("h_s_p_mass", ";reconstructed mass;reconstructed p", 150, 0, 1500, 150, 0, 1500);

  h_rp_renergy = fs->make<TH2F>("h_rp_renergy", ";energy resolution;p resolution", 300, -1500, 1500, 300, -1500, 1500);
  h_fp_fenergy = fs->make<TH2F>("h_fp_fenergy", ";fractional energy resolution;fractional p resolution", 300, -1, 2, 300, -1, 2);
  h_s_p_energy = fs->make<TH2F>("h_s_p_energy", ";reconstructed energy;reconstructed p", 150, 0, 1500, 150, 0, 1500);

  h_s_p = fs->make<TH2F>("h_s_p", ";generated p;reconstructed p", 150, 0, 1500, 150, 0, 1500);
  h_s_pt = fs->make<TH2F>("h_s_pt", ";generated pt;reconstructed pt", 150, 0, 1500, 150, 0, 1500);
  h_s_eta = fs->make<TH2F>("h_s_eta", ";generated eta;reconstructed eta", 50, -4, 4, 50, -4, 4);
  h_s_phi = fs->make<TH2F>("h_s_phi", ";generated phi;reconstructed phi", 50, -3.15, 3.15, 50, -3.15, 3.15);
  h_s_mass = fs->make<TH2F>("h_s_mass", ";generated mass;reconstructed mass", 150, 0, 1500, 150, 0, 1500);
  h_s_msptm = fs->make<TH2F>("h_s_msptm", ";generated msptm;reconstructed msptm", 150, 0, 1500, 150, 0, 1500);
  h_s_msptm_mass = fs->make<TH2F>("h_s_msptm_mass", ";generated mass;reconstructed msptm", 150, 0, 1500, 150, 0, 1500);
  h_s_energy = fs->make<TH2F>("h_s_energy", ";generated energy;reconstructed energy", 150, 0, 1500, 150, 0, 1500);
  h_s_px = fs->make<TH2F>("h_s_px", ";generated px;reconstructed px", 300, -1500, 1500, 300, -1500, 1500);
  h_s_py = fs->make<TH2F>("h_s_py", ";generated py;reconstructed py", 300, -1500, 1500, 300, -1500, 1500);
  h_s_pz = fs->make<TH2F>("h_s_pz", ";generated pz;reconstructed pz", 300, -1500, 1500, 300, -1500, 1500);
  h_s_rapidity = fs->make<TH2F>("h_s_rapidity", ";generated rapidity;reconstructed rapidity", 50, -4, 4, 50, -4, 4);
  h_s_theta = fs->make<TH2F>("h_s_theta", ";generated theta;reconstructed theta", 50, 0, 3.15, 50, 0, 3.15);
  h_s_betagamma = fs->make<TH2F>("h_s_betagamma", ";generated betagamma;reconstructed betagamma", 100, 0, 10, 100, 0, 10);
  h_s_avgbetagammalab = fs->make<TH2F>("h_s_avgbetagammalab", ";generated avgbetagammalab;reconstructed avgbetagammalab", 100, 0, 10, 100, 0, 10);
  h_s_avgbetagammacmz = fs->make<TH2F>("h_s_avgbetagammacmz", ";generated avgbetagammacmz;reconstructed avgbetagammacmz", 100, 0, 10, 100, 0, 10);

  h_s_genjets_njets = fs->make<TH2F>("h_s_genjets_njets", ";number of genJets;number of PF jets", 50, 0, 50, 50, 0, 50);
  h_s_genjets_ncalojets = fs->make<TH2F>("h_s_genjets_ncalojets", ";number of genJets;number of calojets", 50, 0, 50, 50, 0, 50);
  h_s_genjets_calojetpt4 = fs->make<TH2F>("h_s_genjets_calojetpt4", ";p_{T} of 4th genJet (GeV);p_{T} of 4th calojet (GeV)", 100, 0, 500, 100, 0, 500);
  h_s_genjets_jetsumht = fs->make<TH2F>("h_s_genjets_jetsumht", ";#SigmaH_{T} of genJets (GeV);#SigmaH_{T} of PF jets (GeV)", 200, 0, 5000, 200, 0, 5000);

  h_s_partons_njets = fs->make<TH2F>("h_s_partons_njets", ";number of partons;number of PF jets", 50, 0, 50, 50, 0, 50);
  h_s_partons_ncalojets = fs->make<TH2F>("h_s_partons_ncalojets", ";number of partons;number of calojets", 50, 0, 50, 50, 0, 50);
  h_s_partons_calojetpt4 = fs->make<TH2F>("h_s_partons_calojetpt4", ";p_{T} of 4th parton (GeV);p_{T} of 4th calojet (GeV)", 100, 0, 500, 100, 0, 500);
  h_s_partons_jetsumht = fs->make<TH2F>("h_s_partons_jetsumht", ";#SigmaH_{T} of partons (GeV);#SigmaH_{T} of PF jets (GeV)", 200, 0, 5000, 200, 0, 5000);

  h_s_drmin = fs->make<TH2F>("h_s_drmin", ";min #DeltaR between partons;min #DeltaR between tracks", 100, 0, 5, 100, 0, 5);
  h_s_drmax = fs->make<TH2F>("h_s_drmax", ";max #DeltaR between partons;max #DeltaR between tracks", 100, 0, 5, 100, 0, 5);

  h_dbv_nomatch = fs->make<TH1F>("h_dbv_nomatch", ";reconstructed d_{BV};reconstructed vertices without matched generated vertex", 500, 0, 2.5);
  h_s_dbv = fs->make<TH2F>("h_s_dbv", ";generated d_{BV};reconstructed d_{BV}", 500, 0, 2.5, 500, 0, 2.5);
  h_s_dvv = fs->make<TH2F>("h_s_dvv", ";generated d_{VV};reconstructed d_{VV}", 1000, 0, 5, 1000, 0, 5);

  h_s_dbv_gendvv = fs->make<TH2F>("h_s_dbv_gendvv", "d_{VV} > 300 #mum;generated d_{BV};reconstructed d_{BV}", 500, 0, 2.5, 500, 0, 2.5);
  h_s_dbv_betagamma = fs->make<TH2F>("h_s_dbv_betagamma", ";generated #beta#gamma;generated d_{BV}", 100, 0, 10, 100, 0, 0.5);
  h_s_drmax_betagamma = fs->make<TH2F>("h_s_drmax_betagamma", ";generated #beta#gamma;reconstructed drmax", 100, 0, 10, 100, 0, 5);
  h_s_drmax_dbv = fs->make<TH2F>("h_s_drmax_dbv", ";generated d_{BV};reconstructed drmax", 100, 0, 0.5, 100, 0, 5);
  h_s_gendrmax_dbv = fs->make<TH2F>("h_s_gendrmax_dbv", ";generated d_{BV};generated drmax", 100, 0, 0.5, 100, 0, 5);

  h_s_dx_drmax = fs->make<TH2F>("h_s_dx_drmax", ";max #DeltaR between tracks;x resolution (cm)", 100, 0, 5, 200, -0.02, 0.02);
  h_s_dy_drmax = fs->make<TH2F>("h_s_dy_drmax", ";max #DeltaR between tracks;y resolution (cm)", 100, 0, 5, 200, -0.02, 0.02);
  h_s_dz_drmax = fs->make<TH2F>("h_s_dz_drmax", ";max #DeltaR between tracks;z resolution (cm)", 100, 0, 5, 200, -0.02, 0.02);
  h_s_dist2d_drmax = fs->make<TH2F>("h_s_dist2d_drmax", ";max #DeltaR between tracks;dist2d(lsp,vtx) (cm)", 100, 0, 5, 100, 0, 0.02);
  h_s_dist3d_drmax = fs->make<TH2F>("h_s_dist3d_drmax", ";max #DeltaR between tracks;dist3d(lsp,vtx) (cm)", 100, 0, 5, 100, 0, 0.02);

  h_partons_pt1 = fs->make<TH1F>("h_partons_pt1", ";p_{T} of 1st accepted parton (GeV);generated LSPs", 100, 0, 1000);
  h_partons_pt2 = fs->make<TH1F>("h_partons_pt2", ";p_{T} of 2nd accepted parton (GeV);generated LSPs", 100, 0, 1000);
  h_partons_pt3 = fs->make<TH1F>("h_partons_pt3", ";p_{T} of 3rd accepted parton (GeV);generated LSPs", 100, 0, 1000);
  h_partons_pt4 = fs->make<TH1F>("h_partons_pt4", ";p_{T} of 4th accepted parton (GeV);generated LSPs", 100, 0, 1000);
  h_partons_pt5 = fs->make<TH1F>("h_partons_pt5", ";p_{T} of 5th accepted parton (GeV);generated LSPs", 100, 0, 1000);
  h_partons_sumpt = fs->make<TH1F>("h_partons_sumpt", ";#Sigmap_{T} of accepted partons (GeV);generated LSPs", 100, 0, 1000);

  h_gen_dbv = fs->make<TH1F>("h_gen_dbv", ";generated d_{BV};generated LSPs with a reconstructed vertex within 120 #mum", 100, 0, 0.5);
  h_gen_dvv = fs->make<TH1F>("h_gen_dvv", ";generated d_{VV};events", 200, 0, 1);
  h_gen_dvv_matched = fs->make<TH1F>("h_gen_dvv_matched", ";generated d_{VV};events with two matched vertices", 200, 0, 1);
}

namespace {
  float mag(float x, float y) {
    return sqrt(x*x + y*y);
  }
  
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
  
  float signed_mag(float x, float y) {
    float m = mag(x,y);
    if (y < 0) return -m;
    return m;
  }
}

void MFVResolutions::analyze(const edm::Event& event, const edm::EventSetup&) {
if (doing_h2xqq) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);
  const size_t ngen = gen_particles->size();

  double v[2][3] = {{0}};
  std::vector<const reco::GenParticle*> partons;

  for (size_t igen = 0; igen < ngen; ++igen) {
    const reco::GenParticle& gen = gen_particles->at(igen);
    if (gen.status() == 3 && abs(gen.pdgId()) == 35) {
      assert(gen.numberOfDaughters() >= 2);
      for (size_t idau = 0; idau < 2; ++idau) {
        const reco::Candidate* dau = gen.daughter(idau);
        int dauid = dau->pdgId();
        // https://espace.cern.ch/cms-exotica/long-lived/selection/MC2012.aspx
        // 600N114 = quarks where N is 1 2 or 3 for the lifetime selection
        assert(dauid/6000000 == 1);
        dauid %= 6000000;
        const int h2x = dauid / 1000;
        assert(h2x == 1 || h2x == 2 || h2x == 3);
        dauid %= h2x*1000;
        assert(dauid/100 == 1);
        dauid %= 100;
        assert(dauid/10 == 1);
        dauid %= 10;
        assert(dauid == 3 || dauid == 4);

        const size_t ngdau = dau->numberOfDaughters();
        assert(ngdau >= 2);
        for (size_t igdau = 0; igdau < 2; ++igdau) {
          const reco::Candidate* gdau = dau->daughter(igdau);
          const int id = gdau->pdgId();
          assert(abs(id) >= 1 && abs(id) <= 5);
          partons.push_back(dynamic_cast<const reco::GenParticle*>(gdau));
        }
      }
    }
  }

  assert(partons.size() == 4);
  for (int i = 0; i < 2; ++i) {
    assert(partons[i*2]->numberOfDaughters() > 0);
    v[i][0] = partons[i*2]->daughter(0)->vx(); // i*2 since first two partons are from first X, second two partons are from second X
    v[i][1] = partons[i*2]->daughter(0)->vy();
    v[i][2] = partons[i*2]->daughter(0)->vz();
  }
  const double dvv = mag(v[0][0] - v[1][0],
                         v[0][1] - v[1][1]);
  h_gen_dvv->Fill(dvv);
}

if (doing_mfv3j) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);

  die_if_not(mevent->gen_valid, "not running on signal sample");

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);

  if (!mci.Valid()) {
    if (!mci_warned)
      edm::LogWarning("Resolutions") << "MCInteractionMFV3j invalid; no further warnings!";
    mci_warned = true;
  }

  TLorentzVector lsp_p4s[2] = { mevent->gen_lsp_p4(0), mevent->gen_lsp_p4(1) };
  int lsp_nmatch[2] = {0,0};
  int nvtx_match = 0;
  bool lsp_matched[2] = {false,false};

  for (const MFVVertexAux& vtx : *vertices) {
    double dr = 1e99, dist = 1e99;

    int ilsp = -1;
    if (max_dr > 0) {
      double drs[2] = {
        reco::deltaR(lsp_p4s[0].Eta(), lsp_p4s[0].Phi(), vtx.eta[which_mom], vtx.phi[which_mom]),
        reco::deltaR(lsp_p4s[1].Eta(), lsp_p4s[1].Phi(), vtx.eta[which_mom], vtx.phi[which_mom])
      };
      
      for (int i = 0; i < 2; ++i) {
        if (drs[i] < max_dr) {
          ++lsp_nmatch[i];
          if (drs[i] < dr) {
            dr = drs[i];
            ilsp = i;
          }
        }
      }
    }
    else if (max_dist > 0) {
      double dists[2] = {
        mag(mevent->gen_lsp_decay[0*3+0] - vtx.x,
            mevent->gen_lsp_decay[0*3+1] - vtx.y,
            mevent->gen_lsp_decay[0*3+2] - vtx.z),
        mag(mevent->gen_lsp_decay[1*3+0] - vtx.x,
            mevent->gen_lsp_decay[1*3+1] - vtx.y,
            mevent->gen_lsp_decay[1*3+2] - vtx.z),
      };

      for (int i = 0; i < 2; ++i) {
        if (dists[i] < max_dist) {
          ++lsp_nmatch[i];
          if (dists[i] < dist) {
            dist = dists[i];
            ilsp = i;
          }
        }
      }
    }

    if (ilsp < 0) {
      h_dbv_nomatch->Fill(mevent->bs2ddist(vtx));
      continue;
    }

    ++nvtx_match;
    const TLorentzVector& lsp_p4 = lsp_p4s[ilsp];
    const TLorentzVector& vtx_p4 = vtx.p4(which_mom);

    // histogram dr, dist
    h_dr->Fill(dr);
    h_dist->Fill(dist);

    // histogram space resolutions: x, y, z, dist2d, dist3d
    h_dx->Fill(vtx.x - mevent->gen_lsp_decay[ilsp*3+0]);
    h_dy->Fill(vtx.y - mevent->gen_lsp_decay[ilsp*3+1]);
    h_dz->Fill(vtx.z - mevent->gen_lsp_decay[ilsp*3+2]);
    h_dist2d->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x,
                       mevent->gen_lsp_decay[ilsp*3+1] - vtx.y));
    h_dist3d->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x,
                       mevent->gen_lsp_decay[ilsp*3+1] - vtx.y,
                       mevent->gen_lsp_decay[ilsp*3+2] - vtx.z));

    // histogram space uncertainties: sqrt(cxx), sqrt(cyy), sqrt(czz), bs2derr
    h_cxx->Fill(sqrt(vtx.cxx));
    h_cyy->Fill(sqrt(vtx.cyy));
    h_czz->Fill(sqrt(vtx.czz));
    h_bs2derr->Fill(vtx.bs2derr);

    // histogram space pulls: x, y, z, dist2d
    h_pull_dx->Fill((vtx.x - mevent->gen_lsp_decay[ilsp*3+0]) / sqrt(vtx.cxx));
    h_pull_dy->Fill((vtx.y - mevent->gen_lsp_decay[ilsp*3+1]) / sqrt(vtx.cyy));
    h_pull_dz->Fill((vtx.z - mevent->gen_lsp_decay[ilsp*3+2]) / sqrt(vtx.czz));
    h_pull_dist2d->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x,
                            mevent->gen_lsp_decay[ilsp*3+1] - vtx.y) / vtx.bs2derr);

    // histogram momentum resolutions: p, pt, eta, phi, mass, energy, px, py, pz, rapidity, theta, betagamma
    double vtx_msptm = sqrt(vtx_p4.M() * vtx_p4.M() + vtx_p4.Pt() * vtx_p4.Pt())+ fabs(vtx_p4.Pt());
    double lsp_msptm = sqrt(lsp_p4.M() * lsp_p4.M() + lsp_p4.Pt() * lsp_p4.Pt())+ fabs(lsp_p4.Pt());

    h_r_p->Fill(vtx_p4.P() - lsp_p4.P());
    h_r_pt->Fill(vtx_p4.Pt() - lsp_p4.Pt());
    h_r_eta->Fill(vtx_p4.Eta() - lsp_p4.Eta());
    h_r_phi->Fill(reco::deltaPhi(vtx_p4.Phi(), lsp_p4.Phi()));
    h_r_mass->Fill(vtx_p4.M() - lsp_p4.M());
    h_r_msptm->Fill(vtx_msptm - lsp_msptm);
    h_r_msptm_mass->Fill(vtx_msptm - lsp_p4.M());
    h_r_energy->Fill(vtx_p4.E() - lsp_p4.E());
    h_r_px->Fill(vtx_p4.Px() - lsp_p4.Px());
    h_r_py->Fill(vtx_p4.Py() - lsp_p4.Py());
    h_r_pz->Fill(vtx_p4.Pz() - lsp_p4.Pz());
    h_r_rapidity->Fill(vtx_p4.Rapidity() - lsp_p4.Rapidity());
    h_r_theta->Fill(vtx_p4.Theta() - lsp_p4.Theta());
    h_r_betagamma->Fill(vtx_p4.Beta()*vtx_p4.Gamma() - lsp_p4.Beta()*lsp_p4.Gamma());

    h_f_p->Fill((vtx_p4.P() - lsp_p4.P()) / lsp_p4.P());
    h_f_pt->Fill((vtx_p4.Pt() - lsp_p4.Pt()) / lsp_p4.Pt());
    h_f_mass->Fill((vtx_p4.M() - lsp_p4.M()) / lsp_p4.M());
    h_f_msptm->Fill((vtx_msptm - lsp_msptm) / lsp_msptm);
    h_f_msptm_mass->Fill((vtx_msptm - lsp_p4.M()) / lsp_p4.M());
    h_f_energy->Fill((vtx_p4.E() - lsp_p4.E()) / lsp_p4.E());

    h_rp_rmass->Fill(vtx_p4.M() - lsp_p4.M(), vtx_p4.P() - lsp_p4.P());
    h_fp_fmass->Fill((vtx_p4.M() - lsp_p4.M()) / lsp_p4.M(), (vtx_p4.P() - lsp_p4.P()) / lsp_p4.P());
    h_s_p_mass->Fill(vtx_p4.M(), vtx_p4.P());

    h_rp_renergy->Fill(vtx_p4.M() - lsp_p4.M(), vtx_p4.E() - lsp_p4.E());
    h_fp_fenergy->Fill((vtx_p4.M() - lsp_p4.M()) / lsp_p4.M(), (vtx_p4.E() - lsp_p4.E()) / lsp_p4.E());
    h_s_p_energy->Fill(vtx_p4.M(), vtx_p4.E());

    h_s_p->Fill(lsp_p4.P(), vtx_p4.P());
    h_s_pt->Fill(lsp_p4.Pt(), vtx_p4.Pt());
    h_s_eta->Fill(lsp_p4.Eta(), vtx_p4.Eta());
    h_s_phi->Fill(lsp_p4.Phi(), vtx_p4.Phi());
    h_s_mass->Fill(lsp_p4.M(), vtx_p4.M());
    h_s_msptm->Fill(lsp_msptm, vtx_msptm);
    h_s_msptm_mass->Fill(lsp_p4.M(), vtx_msptm);
    h_s_energy->Fill(lsp_p4.E(), vtx_p4.E());
    h_s_px->Fill(lsp_p4.Px(), vtx_p4.Px());
    h_s_py->Fill(lsp_p4.Py(), vtx_p4.Py());
    h_s_pz->Fill(lsp_p4.Pz(), vtx_p4.Pz());
    h_s_rapidity->Fill(lsp_p4.Rapidity(), vtx_p4.Rapidity());
    h_s_theta->Fill(lsp_p4.Theta(), vtx_p4.Theta());
    h_s_betagamma->Fill(lsp_p4.Beta()*lsp_p4.Gamma(), vtx_p4.Beta()*vtx_p4.Gamma());

    // histogram drmin, drmax
    const int ndau = 5;
    const reco::GenParticle* daughters[ndau] = { mci.stranges[ilsp], mci.bottoms[ilsp], mci.bottoms_from_tops[ilsp], mci.W_daughters[ilsp][0], mci.W_daughters[ilsp][1] };

    float drmin =  1e99;
    float drmax = -1e99;
    for (int j = 0; j < ndau; ++j) {
      if (is_neutrino(daughters[j]) || fabs(daughters[j]->eta()) > 2.5) continue;
      for (int k = j+1; k < ndau; ++k) {
        if (is_neutrino(daughters[k]) || fabs(daughters[k]->eta()) > 2.5) continue;
        float dr = reco::deltaR(*daughters[j], *daughters[k]);
        if (dr < drmin)
          drmin = dr;
        if (dr > drmax)
          drmax = dr;
      }
    }

    h_s_drmin->Fill(drmin, vtx.drmin());
    h_s_drmax->Fill(drmax, vtx.drmax());

    // histogram pt1, pt2, pt3, pt4, pt5, sumpt of partons
    if (!lsp_matched[ilsp]) {
      lsp_matched[ilsp] = true;
      std::vector<float> parton_pt;
      float sumpt = 0;
      for (int j = 0; j < ndau; ++j) {
        if (is_lepton(daughters[j]) || is_neutrino(daughters[j]) || daughters[j]->pt() < 20 || fabs(daughters[j]->eta()) > 2.5 || fabs(mag(mci.stranges[ilsp]->vx() - mci.lsps[ilsp]->vx(), mci.stranges[ilsp]->vy() - mci.lsps[ilsp]->vy()) * sin(daughters[j]->phi() - atan2(mci.stranges[ilsp]->vy() - mci.lsps[ilsp]->vy(), mci.stranges[ilsp]->vx() - mci.lsps[ilsp]->vx()))) < 0.01) continue;
        parton_pt.push_back(daughters[j]->pt());
        sumpt += daughters[j]->pt();
      }
      std::sort(parton_pt.begin(), parton_pt.end(), [](float p1, float p2) { return p1 > p2; } );
      h_partons_pt1->Fill(int(parton_pt.size()) >= 1 ? parton_pt.at(0) : 0.f);
      h_partons_pt2->Fill(int(parton_pt.size()) >= 2 ? parton_pt.at(1) : 0.f);
      h_partons_pt3->Fill(int(parton_pt.size()) >= 3 ? parton_pt.at(2) : 0.f);
      h_partons_pt4->Fill(int(parton_pt.size()) >= 4 ? parton_pt.at(3) : 0.f);
      h_partons_pt5->Fill(int(parton_pt.size()) >= 5 ? parton_pt.at(4) : 0.f);
      h_partons_sumpt->Fill(sumpt);
    }

    // histogram dBV
    h_s_dbv->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - gen_particles->at(2).vx(), mevent->gen_lsp_decay[ilsp*3+1] - gen_particles->at(2).vy()), mevent->bs2ddist(vtx));
    if (mag(mevent->gen_lsp_decay[0*3+0] - mevent->gen_lsp_decay[1*3+0], mevent->gen_lsp_decay[0*3+1] - mevent->gen_lsp_decay[1*3+1]) > 0.03) {
      h_s_dbv_gendvv->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - gen_particles->at(2).vx(), mevent->gen_lsp_decay[ilsp*3+1] - gen_particles->at(2).vy()), mevent->bs2ddist(vtx));
    }

    h_s_dbv_betagamma->Fill(lsp_p4.Beta()*lsp_p4.Gamma(), mag(mevent->gen_lsp_decay[ilsp*3+0] - gen_particles->at(2).vx(), mevent->gen_lsp_decay[ilsp*3+1] - gen_particles->at(2).vy()));
    h_s_drmax_betagamma->Fill(lsp_p4.Beta()*lsp_p4.Gamma(), vtx.drmax());
    h_s_drmax_dbv->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - gen_particles->at(2).vx(), mevent->gen_lsp_decay[ilsp*3+1] - gen_particles->at(2).vy()), vtx.drmax());
    h_s_gendrmax_dbv->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - gen_particles->at(2).vx(), mevent->gen_lsp_decay[ilsp*3+1] - gen_particles->at(2).vy()), drmax);

    h_s_dx_drmax->Fill(vtx.drmax(), vtx.x - mevent->gen_lsp_decay[ilsp*3+0]);
    h_s_dy_drmax->Fill(vtx.drmax(), vtx.y - mevent->gen_lsp_decay[ilsp*3+1]);
    h_s_dz_drmax->Fill(vtx.drmax(), vtx.z - mevent->gen_lsp_decay[ilsp*3+2]);
    h_s_dist2d_drmax->Fill(vtx.drmax(), mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x, mevent->gen_lsp_decay[ilsp*3+1] - vtx.y));
    h_s_dist3d_drmax->Fill(vtx.drmax(), mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x, mevent->gen_lsp_decay[ilsp*3+1] - vtx.y, mevent->gen_lsp_decay[ilsp*3+2] - vtx.z));
  }

  for (int ilsp = 0; ilsp < 2; ++ilsp) {
    bool matched = false;
    for (const MFVVertexAux& vtx : *vertices) {
      double dist = mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x,
                        mevent->gen_lsp_decay[ilsp*3+1] - vtx.y,
                        mevent->gen_lsp_decay[ilsp*3+2] - vtx.z);
      if (dist < max_dist) {
        matched = true;
        break;
      }
    }
    if (matched) {
      h_gen_dbv->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - gen_particles->at(2).vx(), mevent->gen_lsp_decay[ilsp*3+1] - gen_particles->at(2).vy()));
    }
  }

  // histogram lsp_nmatch
  for (int i = 0; i < 2; ++i) {
    h_lsp_nmatch[i]->Fill(lsp_nmatch[i]);
  }
  h_lsp0nmatch_lsp1nmatch->Fill(lsp_nmatch[1], lsp_nmatch[0]);

  const int nsv = int(vertices->size());
  h_vtxmatch_vtxtotal->Fill(nsv, nvtx_match);

  if (nsv >= 2) {
    const MFVVertexAux& v0 = vertices->at(0);
    const MFVVertexAux& v1 = vertices->at(1);

    // histogram average betagamma resolutions
    TLorentzVector lsp0_p4 = lsp_p4s[0];
    TLorentzVector lsp1_p4 = lsp_p4s[1];
    double lsp_avgbetagammalab = (lsp0_p4.Beta()*lsp0_p4.Gamma() + lsp1_p4.Beta()*lsp1_p4.Gamma()) / 2;
    TVector3 lsp_betacmz = TVector3(0, 0, -(lsp0_p4.Pz() + lsp1_p4.Pz()) / (lsp0_p4.E() + lsp1_p4.E()));
    lsp0_p4.Boost(lsp_betacmz);
    lsp1_p4.Boost(lsp_betacmz);
    double lsp_avgbetagammacmz = (lsp0_p4.Beta()*lsp0_p4.Gamma() + lsp1_p4.Beta()*lsp1_p4.Gamma()) / 2;

    TLorentzVector vtx0_p4 = v0.p4(which_mom);
    TLorentzVector vtx1_p4 = v1.p4(which_mom);
    double vtx_avgbetagammalab = (vtx0_p4.Beta()*vtx0_p4.Gamma() + vtx1_p4.Beta()*vtx1_p4.Gamma()) / 2;
    TVector3 vtx_betacmz = TVector3(0, 0, -(vtx0_p4.Pz() + vtx1_p4.Pz()) / (vtx0_p4.E() + vtx1_p4.E()));
    vtx0_p4.Boost(vtx_betacmz);
    vtx1_p4.Boost(vtx_betacmz);
    double vtx_avgbetagammacmz = (vtx0_p4.Beta()*vtx0_p4.Gamma() + vtx1_p4.Beta()*vtx1_p4.Gamma()) / 2;

    h_r_avgbetagammalab->Fill(vtx_avgbetagammalab - lsp_avgbetagammalab);
    h_r_avgbetagammacmz->Fill(vtx_avgbetagammacmz - lsp_avgbetagammacmz);
    h_s_avgbetagammalab->Fill(lsp_avgbetagammalab, vtx_avgbetagammalab);
    h_s_avgbetagammacmz->Fill(lsp_avgbetagammacmz, vtx_avgbetagammacmz);

    // histogram dVV
    h_s_dvv->Fill(mag(mevent->gen_lsp_decay[0*3+0] - mevent->gen_lsp_decay[1*3+0], mevent->gen_lsp_decay[0*3+1] - mevent->gen_lsp_decay[1*3+1]), mag(v0.x - v1.x, v0.y - v1.y));

    bool matched[2] = {false, false};
    for (int ivtx = 0; ivtx < 2; ++ivtx) {
      for (int ilsp = 0; ilsp < 2; ++ilsp) {
        double dist = mag(mevent->gen_lsp_decay[ilsp*3+0] - vertices->at(ivtx).x,
                          mevent->gen_lsp_decay[ilsp*3+1] - vertices->at(ivtx).y,
                          mevent->gen_lsp_decay[ilsp*3+2] - vertices->at(ivtx).z);
        if (dist < max_dist) {
          matched[ivtx] = true;
          break;
        }
      }
    }
    if (matched[0] && matched[1]) {
      h_gen_dvv_matched->Fill(mag(mevent->gen_lsp_decay[0*3+0] - mevent->gen_lsp_decay[1*3+0], mevent->gen_lsp_decay[0*3+1] - mevent->gen_lsp_decay[1*3+1]));
    }
  }
  h_gen_dvv->Fill(mag(mevent->gen_lsp_decay[0*3+0] - mevent->gen_lsp_decay[1*3+0], mevent->gen_lsp_decay[0*3+1] - mevent->gen_lsp_decay[1*3+1]));

  // histogram njets, ncalojets, calojetpt4, jetsumht vs. genJets
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel(gen_jet_src, gen_jets);

  std::vector<float> gen_jet_pt;
  for (const reco::GenJet& jet : *gen_jets) {
    if (jet.pt() > 20 && fabs(jet.eta()) < 2.5)
      gen_jet_pt.push_back(jet.pt());
  }
  std::sort(gen_jet_pt.begin(), gen_jet_pt.end(), [](float p1, float p2) { return p1 > p2; });

  h_s_genjets_njets->Fill(int(gen_jet_pt.size()), mevent->njets());
  h_s_genjets_ncalojets->Fill(int(gen_jet_pt.size()), mevent->ncalojets());
  h_s_genjets_calojetpt4->Fill(int(gen_jet_pt.size()) >= 4 ? gen_jet_pt.at(3) : 0.f, mevent->calojetpt4());
  h_s_genjets_jetsumht->Fill(std::accumulate(gen_jet_pt.begin(), gen_jet_pt.end(), 0.f), mevent->jet_sum_ht());

  // histogram njets, ncalojets, calojetpt4, jetsumht vs. partons
  std::vector<const reco::GenParticle*> partons;
  for (int i = 0; i < 2; ++i) {
    partons.push_back(mci.stranges[i]);
    partons.push_back(mci.bottoms[i]);
    partons.push_back(mci.bottoms_from_tops[i]);
    if (mci.decay_type[i] == 3) {
      partons.push_back(mci.W_daughters[i][0]);
      partons.push_back(mci.W_daughters[i][1]);
    }
  }

  std::vector<std::vector<float> > parton_pt_eta_phi;
  float parton_sumht = 0;
  for (const reco::GenParticle* p : partons) {
    if (p->pt() > 20 && fabs(p->eta()) < 2.5) {
      std::vector<float> pt_eta_phi;
      pt_eta_phi.push_back(p->pt());
      pt_eta_phi.push_back(p->eta());
      pt_eta_phi.push_back(p->phi());
      parton_pt_eta_phi.push_back(pt_eta_phi);
      parton_sumht += p->pt();
    }
  }
  std::sort(parton_pt_eta_phi.begin(), parton_pt_eta_phi.end(), [](std::vector<float> p1, std::vector<float> p2) { return p1.at(0) > p2.at(0); } );

  bool unmerged = true;
  while (unmerged) {
    bool merged = false;
    for (int i = 0; i < int(parton_pt_eta_phi.size()); ++i) {
      std::vector<float> p1 = parton_pt_eta_phi.at(i);
      for (int j = i+1; j < int(parton_pt_eta_phi.size()); ++j) {
        std::vector<float> p2 = parton_pt_eta_phi.at(j);
        if (reco::deltaR(p1.at(1), p1.at(2), p2.at(1), p2.at(2)) < 0.6) {
          std::vector<float> pt_eta_phi;
          pt_eta_phi.push_back(p1.at(0) + p2.at(0));
          pt_eta_phi.push_back((p1.at(0) * p1.at(1) + p2.at(0) * p2.at(1)) / (p1.at(0) + p2.at(0)));
          pt_eta_phi.push_back((p1.at(0) * p1.at(2) + p2.at(0) * p2.at(2)) / (p1.at(0) + p2.at(0)));
          parton_pt_eta_phi.erase(parton_pt_eta_phi.begin() + j);
          parton_pt_eta_phi.erase(parton_pt_eta_phi.begin() + i);
          parton_pt_eta_phi.push_back(pt_eta_phi);
          std::sort(parton_pt_eta_phi.begin(), parton_pt_eta_phi.end(), [](std::vector<float> p1, std::vector<float> p2) { return p1.at(0) > p2.at(0); } );
          merged = true;
          break;
        }
      }
      if (merged) {
        break;
      }
    }
    if (merged) {
      continue;
    }
    unmerged = false;
  }

  h_s_partons_njets->Fill(int(parton_pt_eta_phi.size()), mevent->njets());
  h_s_partons_ncalojets->Fill(int(parton_pt_eta_phi.size()), mevent->ncalojets());
  h_s_partons_calojetpt4->Fill(int(parton_pt_eta_phi.size()) >= 4 ? parton_pt_eta_phi.at(3).at(0) : 0.f, mevent->calojetpt4());
  h_s_partons_jetsumht->Fill(parton_sumht, mevent->jet_sum_ht());
}
}

DEFINE_FWK_MODULE(MFVResolutions);
