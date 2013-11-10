#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"

class MFVVertexHistos : public edm::EDAnalyzer {
 public:
  explicit MFVVertexHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag mfv_event_src;
  const edm::InputTag vertex_aux_src;
  const edm::InputTag weight_src;
  const bool use_ref;
  const bool do_scatterplots;

  VertexDistanceXY distcalc_2d;
  VertexDistance3D distcalc_3d;

  TH1F* h_nsv;
  TH2F* h_nsv_v_minlspdist2d;
  TH2F* h_nsv_v_lspdist2d;
  TH2F* h_nsv_v_lspdist3d;

  // indices for h_sv below:
  enum sv_index { sv_best0, sv_best1, sv_best2, sv_rest, sv_top2, sv_all, sv_num_indices };
  static const char* sv_index_names[sv_num_indices];

  void fill_multi(TH1F** hs, const int isv, const double val, const double weight) const;
  void fill_multi(TH2F** hs, const int isv, const double val, const double val2, const double weight) const;
  void fill_multi(PairwiseHistos* hs, const int isv, const PairwiseHistos::ValueMap& val, const double weight) const;

  TH1F* h_sv_pos_1d[4][3];
  TH2F* h_sv_pos_2d[4][3];

  TH1F* h_sv_trackpt[sv_num_indices];
  TH1F* h_sv_trackfracpterr[sv_num_indices];
  TH1F* h_sv_tracketa[sv_num_indices];
  TH1F* h_sv_trackphi[sv_num_indices];
  TH1F* h_sv_trackdxy[sv_num_indices];
  TH1F* h_sv_trackdz[sv_num_indices];
  TH1F* h_sv_tracknhits[sv_num_indices];

  TH1F* h_sv_trackpaircosth[sv_num_indices];
  TH1F* h_sv_trackpairdr[sv_num_indices];
  TH1F* h_sv_trackpairmass[sv_num_indices];
  TH1F* h_sv_tracktriplemass[sv_num_indices];

  PairwiseHistos h_sv[sv_num_indices];
  PairwiseHistos h_sv_sums[3]; // top2, top3, all

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
};

const char* MFVVertexHistos::sv_index_names[MFVVertexHistos::sv_num_indices] = { "best0", "best1", "best2", "rest", "top2", "all" };

MFVVertexHistos::MFVVertexHistos(const edm::ParameterSet& cfg)
  : mfv_event_src(cfg.getParameter<edm::InputTag>("mfv_event_src")),
    vertex_aux_src(cfg.getParameter<edm::InputTag>("vertex_aux_src")),
    weight_src(cfg.getParameter<edm::InputTag>("weight_src")),
    use_ref(cfg.getParameter<bool>("use_ref")),
    do_scatterplots(cfg.getParameter<bool>("do_scatterplots"))
{
  edm::Service<TFileService> fs;

  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices;arb. units", 15, 0, 15);
  h_nsv_v_minlspdist2d = fs->make<TH2F>("h_nsv_v_minlspdist2d", ";min dist2d(gen vtx #0, #1) (cm);# of secondary vertices", 600, 0, 3, 5, 0, 5);
  h_nsv_v_lspdist2d = fs->make<TH2F>("h_nsv_v_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);# of secondary vertices", 600, 0, 3, 5, 0, 5);
  h_nsv_v_lspdist3d = fs->make<TH2F>("h_nsv_v_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);# of secondary vertices", 600, 0, 3, 5, 0, 5);

  PairwiseHistos::HistoDefs hs;
  hs.add("ntracks",                       "# of tracks/SV",                                                               40,    0,      40);
  hs.add("nbadtracks",                    "# of 'bad' tracks/SV",                                                         40,    0,      40);
  hs.add("ntracksptgt3",                  "# of tracks/SV w/ p_{T} > 3 GeV",                                              40,    0,      40);
  hs.add("ntracksptgt5",                  "# of tracks/SV w/ p_{T} > 5 GeV",                                              40,    0,      40);
  hs.add("ntracksptgt10",                 "# of tracks/SV w/ p_{T} > 10 GeV",                                             40,    0,      40);
  hs.add("trackminnhits",                 "min number of hits on track per SV",                                           40,    0,      40);
  hs.add("trackmaxnhits",                 "max number of hits on track per SV",                                           40,    0,      40);
  hs.add("njetsntks",                     "# of jets assoc. by tracks to SV",                                             10,    0,      10);
  hs.add("njetscomb",                     "# of jets assoc. by combination to SV",                                        10,    0,      10);
  hs.add("chi2dof",                       "SV #chi^2/dof",                                                                50,    0,       7);
  hs.add("chi2dofprob",                   "SV p(#chi^2, dof)",                                                            50,    0,       1.2);

  hs.add("tkonlyp",                       "SV tracks-only p (GeV)",                                                      100,    0,     300);
  hs.add("tkonlypt",                      "SV tracks-only p_{T} (GeV)",                                                  100,    0,     300);
  hs.add("tkonlyeta",                     "SV tracks-only #eta",                                                          50,   -4,       4);
  hs.add("tkonlyrapidity",                "SV tracks-only rapidity",                                                      50,   -4,       4);
  hs.add("tkonlyphi",                     "SV tracks-only #phi",                                                          50,   -3.15,    3.15);
  hs.add("tkonlymass",                    "SV tracks-only mass (GeV)",                                                   100,    0,     250);

  hs.add("jetsntkp",                      "SV jets-by-ntracks -only p (GeV)",                                            100,    0,     300);
  hs.add("jetsntkpt",                     "SV jets-by-ntracks -only p_{T} (GeV)",                                        100,    0,     300);
  hs.add("jetsntketa",                    "SV jets-by-ntracks -only #eta",                                                50,   -4,       4);
  hs.add("jetsntkrapidity",               "SV jets-by-ntracks -only rapidity",                                            50,   -4,       4);
  hs.add("jetsntkphi",                    "SV jets-by-ntracks -only #phi",                                                50,   -3.15,    3.15);
  hs.add("jetsntkmass",                   "SV jets-by-ntracks -only mass (GeV)",                                         100,    0,    1500);

  hs.add("jetscmbp",                      "SV jets-by-combination -only p (GeV)",                                        100,    0,     300);
  hs.add("jetscmbpt",                     "SV jets-by-combination -only p_{T} (GeV)",                                    100,    0,     300);
  hs.add("jetscmbeta",                    "SV jets-by-combination -only #eta",                                            50,   -4,       4);
  hs.add("jetscmbrapidity",               "SV jets-by-combination -only rapidity",                                        50,   -4,       4);
  hs.add("jetscmbphi",                    "SV jets-by-combination -only #phi",                                            50,   -3.15,    3.15);
  hs.add("jetscmbmass",                   "SV jets-by-combination -only mass (GeV)",                                     100,    0,    1500);
				     
  hs.add("tksjetsntkp",                   "SV tracks-plus-jets-by-ntracks p (GeV)",                                      100,    0,     300);
  hs.add("tksjetsntkpt",                  "SV tracks-plus-jets-by-ntracks p_{T} (GeV)",                                  100,    0,     300);
  hs.add("tksjetsntketa",                 "SV tracks-plus-jets-by-ntracks #eta",                                          50,   -4,       4);
  hs.add("tksjetsntkrapidity",            "SV tracks-plus-jets-by-ntracks rapidity",                                      50,   -4,       4);
  hs.add("tksjetsntkphi",                 "SV tracks-plus-jets-by-ntracks #phi",                                          50,   -3.15,    3.15);
  hs.add("tksjetsntkmass",                "SV tracks-plus-jets-by-ntracks mass (GeV)",                                   100,    0,    1500);
				        
  hs.add("tksjetscmbp",                  "SV tracks-plus-jets-by-combination p (GeV)",                                  100,    0,     300);
  hs.add("tksjetscmbpt",                 "SV tracks-plus-jets-by-combination p_{T} (GeV)",                              100,    0,     300);
  hs.add("tksjetscmbeta",                "SV tracks-plus-jets-by-combination #eta",                                      50,   -4,       4);
  hs.add("tksjetscmbrapidity",           "SV tracks-plus-jets-by-combination rapidity",                                  50,   -4,       4);
  hs.add("tksjetscmbphi",                "SV tracks-plus-jets-by-combination #phi",                                      50,   -3.15,    3.15);
  hs.add("tksjetscmbmass",               "SV tracks-plus-jets-by-combination mass (GeV)",                               100,    0,    1500);

  hs.add("costhtkonlymombs",              "cos(angle(2-momentum (tracks-only), 2-dist to BS))",                          101,   -1,       1.02);
  hs.add("costhtkonlymompv2d",            "cos(angle(2-momentum (tracks-only), 2-dist to PV))",                          101,   -1,       1.02);
  hs.add("costhtkonlymompv3d",            "cos(angle(3-momentum (tracks-only), 3-dist to PV))",                          101,   -1,       1.02);

  hs.add("costhjetsntkmombs",             "cos(angle(2-momentum (jets-by-ntracks -only), 2-dist to BS))",                101,   -1,       1.02);
  hs.add("costhjetsntkmompv2d",           "cos(angle(2-momentum (jets-by-ntracks -only), 2-dist to PV))",                101,   -1,       1.02);
  hs.add("costhjetsntkmompv3d",           "cos(angle(3-momentum (jets-by-ntracks -only), 3-dist to PV))",                101,   -1,       1.02);

  hs.add("costhjetscmbmombs",             "cos(angle(2-momentum (jets-by-combination -only), 2-dist to BS))",            101,   -1,       1.02);
  hs.add("costhjetscmbmompv2d",           "cos(angle(2-momentum (jets-by-combination -only), 2-dist to PV))",            101,   -1,       1.02);
  hs.add("costhjetscmbmompv3d",           "cos(angle(3-momentum (jets-by-combination -only), 3-dist to PV))",            101,   -1,       1.02);

  hs.add("costhtksjetsntkmombs",          "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to BS))",          101,   -1,       1.02);
  hs.add("costhtksjetsntkmompv2d",        "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to PV))",          101,   -1,       1.02);
  hs.add("costhtksjetsntkmompv3d",        "cos(angle(3-momentum (tracks-plus-jets-by-ntracks), 3-dist to PV))",          101,   -1,       1.02);

  hs.add("costhtksjetscmbmombs",          "cos(angle(2-momentum (tracks-plus-jets-by-combination), 2-dist to BS))",      101,   -1,       1.02);
  hs.add("costhtksjetscmbmompv2d",        "cos(angle(2-momentum (tracks-plus-jets-by-combination), 2-dist to PV))",      101,   -1,       1.02);
  hs.add("costhtksjetscmbmompv3d",        "cos(angle(3-momentum (tracks-plus-jets-by-combination), 3-dist to PV))",      101,   -1,       1.02);

  hs.add("missdisttkonlypv",              "miss dist. (tracks-only) of SV to PV (cm)",                                   100,    0,       2);
  hs.add("missdisttkonlypverr",           "#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                           100,    0,       0.05);
  hs.add("missdisttkonlypvsig",           "N#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                          100,    0,     100);

  hs.add("missdistjetsntkpv",             "miss dist. (jets-by-ntracks -only) of SV to PV (cm)",                         100,    0,       2);
  hs.add("missdistjetsntkpverr",          "#sigma(miss dist. (jets-by-ntracks -only) of SV to PV) (cm)",                 100,    0,       0.05);
  hs.add("missdistjetsntkpvsig",          "N#sigma(miss dist. (jets-by-ntracks -only) of SV to PV) (cm)",                100,    0,     100);

  hs.add("missdistjetscmbpv",             "miss dist. (jets-by-combination -only) of SV to PV (cm)",                     100,    0,       2);
  hs.add("missdistjetscmbpverr",          "#sigma(miss dist. (jets-by-combination -only) of SV to PV) (cm)",             100,    0,       0.05);
  hs.add("missdistjetscmbpvsig",          "N#sigma(miss dist. (jets-by-combination -only) of SV to PV) (cm)",            100,    0,     100);

  hs.add("missdisttksjetsntkpv",          "miss dist. (tracks-plus-jets-by-ntracks) of SV to PV (cm)",                   100,    0,       2);
  hs.add("missdisttksjetsntkpverr",       "#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",           100,    0,       0.05);
  hs.add("missdisttksjetsntkpvsig",       "N#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",          100,    0,     100);
					  
  hs.add("missdisttksjetscmbpv",          "miss dist. (tracks-plus-jets-by-combination) of SV to PV (cm)",               100,    0,       2);
  hs.add("missdisttksjetscmbpverr",       "#sigma(miss dist. (tracks-plus-jets-by-combination) of SV to PV) (cm)",       100,    0,       0.05);
  hs.add("missdisttksjetscmbpvsig",       "N#sigma(miss dist. (tracks-plus-jets-by-combination) of SV to PV) (cm)",      100,    0,     100);

  hs.add("sumpt2",                        "SV #Sigma p_{T}^{2} (GeV^2)",                                                 300,    0,    6000);
  hs.add("maxnhitsbehind",                "max number of hits behind SV",                                                 15,    0,      15);
  hs.add("sumnhitsbehind",                "sum number of hits behind SV",                                                100,    0,     100);
  hs.add("mintrackpt",                    "SV min{trk_{i} p_{T}} (GeV)",                                                  50,    0,      10);
  hs.add("maxtrackpt",                    "SV max{trk_{i} p_{T}} (GeV)",                                                 100,    0,     150);
  hs.add("maxm1trackpt",                  "SV max-1{trk_{i} p_{T}} (GeV)",                                               100,    0,     150);
  hs.add("maxm2trackpt",                  "SV max-2{trk_{i} p_{T}} (GeV)",                                               100,    0,     150);
  hs.add("drmin",                         "SV min{#Delta R(i,j)}",                                                       150,    0,       1.5);
  hs.add("drmax",                         "SV max{#Delta R(i,j)}",                                                       150,    0,       7);
  hs.add("dravg",                         "SV avg{#Delta R(i,j)}",                                                       150,    0,       5);
  hs.add("drrms",                         "SV rms{#Delta R(i,j)}",                                                       150,    0,       3);
  hs.add("dravgw",                        "SV wavg{#Delta R(i,j)}",                                                      150,    0,       5);
  hs.add("drrmsw",                        "SV wrms{#Delta R(i,j)}",                                                      150,    0,       3);
  hs.add("gen2ddist",                     "dist2d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  hs.add("gen2derr",                      "#sigma(dist2d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  hs.add("gen2dsig",                      "N#sigma(dist2d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  hs.add("gen3ddist",                     "dist3d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  hs.add("gen3derr",                      "#sigma(dist3d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  hs.add("gen3dsig",                      "N#sigma(dist3d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  hs.add("bs2dcompatscss",                "compat2d(SV, beamspot) success",                                                2,    0,       2);
  hs.add("bs2dcompat",                    "compat2d(SV, beamspot)",                                                      100,    0,    1000);
  hs.add("bs2ddist",                      "dist2d(SV, beamspot) (cm)",                                                   100,    0,       0.5);
  hs.add("bs2derr",                       "#sigma(dist2d(SV, beamspot)) (cm)",                                           100,    0,       0.05);
  hs.add("bs2dsig",                       "N#sigma(dist2d(SV, beamspot))",                                               100,    0,     100);
  hs.add("bs3ddist",                      "dist2d(SV, beamspot) * sin(SV theta) (cm)",                                   100,    0,       0.5);
  hs.add("pv2dcompatscss",                "compat2d(SV, PV) success",                                                      2,    0,       2);
  hs.add("pv2dcompat",                    "compat2d(SV, PV)",                                                            100,    0,    1000);
  hs.add("pv2ddist",                      "dist2d(SV, PV) (cm)",                                                         100,    0,       0.5);
  hs.add("pv2derr",                       "#sigma(dist2d(SV, PV)) (cm)",                                                 100,    0,       0.05);
  hs.add("pv2dsig",                       "N#sigma(dist2d(SV, PV))",                                                     100,    0,     100);
  hs.add("pv3dcompatscss",                "compat3d(SV, PV) success",                                                      2,    0,       2);
  hs.add("pv3dcompat",                    "compat3d(SV, PV)",                                                            100,    0,    1000);
  hs.add("pv3ddist",                      "dist3d(SV, PV) (cm)",                                                         100,    0,       0.5);
  hs.add("pv3derr",                       "#sigma(dist3d(SV, PV)) (cm)",                                                 100,    0,       0.1);
  hs.add("pv3dsig",                       "N#sigma(dist3d(SV, PV))",                                                     100,    0,     100);

  for (int j = 0; j < sv_num_indices; ++j) {
    const std::string ex = sv_index_names[j];
    const char* exc = ex.c_str();

    if (j < 4) {
      for (int i = 0; i < 3; ++i) {
        float l = i == 2 ? 25 : 0.8;
        h_sv_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_sv_pos_1d_%i%i", j, i), TString::Format(";%s SV pos[%i] (cm);arb. units", exc, i), 100, -l, l);
      }
      h_sv_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixy", j), TString::Format(";%s SV x (cm);%s SV y (cm)", exc, exc), 100, -1, 1, 100, -1, 1);
      h_sv_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixz", j), TString::Format(";%s SV x (cm);%s SV z (cm)", exc, exc), 100, -1, 1, 100,-25,25);
      h_sv_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%iyz", j), TString::Format(";%s SV y (cm);%s SV z (cm)", exc, exc), 100, -1, 1, 100,-25,25);
    }

    if (use_ref) {
      h_sv_trackpt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpt", exc), TString::Format(";SV %s track p_{T} (GeV);arb. units", exc), 100, 0, 200);
      h_sv_trackfracpterr[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackfracpterr", exc), TString::Format(";SV %s fractional track p_{T} uncertainty (GeV);arb. units", exc), 100, 0, 20);
      h_sv_tracketa[j] = fs->make<TH1F>(TString::Format("h_sv_%s_tracketa", exc), TString::Format(";SV %s track #eta;arb. units", exc), 50, -2.7, 2.7);
      h_sv_trackphi[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackphi", exc), TString::Format(";SV %s track #phi;arb. units", exc), 50, -3.15, 3.15);
      h_sv_trackdxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackdxy", exc), TString::Format(";SV %s track dxy wrt bs (cm);arb. units", exc), 200, -1, 1);
      h_sv_trackdz[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackdz", exc), TString::Format(";SV %s track dz wrt bs (cm);arb. units", exc), 200, -20, 20);
      h_sv_tracknhits[j] = fs->make<TH1F>(TString::Format("h_sv_%s_tracknhits", exc), TString::Format(";SV %s track nhits;arb. units", exc), 60, 0, 60);

      h_sv_trackpaircosth[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpaircosth", exc), TString::Format(";SV %s track pair cos(#theta);arb. units", exc), 100, -1, 1);
      h_sv_trackpairdr[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpairdr", exc), TString::Format(";SV %s track pair #Delta R;arb. units", exc), 100, 0, 7);
      h_sv_trackpairmass[j] = fs->make<TH1F>(TString::Format("h_sv_%s_trackpairmass", exc), TString::Format(";SV %s track pair mass (GeV);arb. units", exc), 200, 0, 20);
      h_sv_tracktriplemass[j] = fs->make<TH1F>(TString::Format("h_sv_%s_tracktriplemass", exc), TString::Format(";SV %s track triple mass (GeV);arb. units", exc), 200, 0, 20);
    }

    h_sv[j].Init("h_sv_" + ex, hs, true, do_scatterplots);
  }

  for (int j = 0; j < 3; ++j) {
    std::string ex;
    if (j == 0)
      ex = "sumtop2";
    else if (j == 1)
      ex = "sumtop3";
    else if (j == 2)
      ex = "sumtop4";

    h_sv_sums[j].Init("h_sv_" + ex, hs, true, do_scatterplots, j+2);
  }    

  h_svdist2d = fs->make<TH1F>("h_svdist2d", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist3d = fs->make<TH1F>("h_svdist3d", ";dist3d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist2d_v_lspdist2d = fs->make<TH2F>("h_svdist2d_v_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist3d_v_lspdist3d = fs->make<TH2F>("h_svdist3d_v_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);dist3d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist2d_v_minlspdist2d = fs->make<TH2F>("h_svdist2d_v_minlspdist2d", ";min dist2d(gen vtx #0, #1) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist2d_v_minbsdist2d = fs->make<TH2F>("h_svdist2d_v_mindist2d", ";min dist2d(sv, bs) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);

  if (use_ref) {
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
  }
}

// JMTBAD ugh
void MFVVertexHistos::fill_multi(TH1F** hs, const int isv, const double val, const double weight) const {
  hs[isv < 3 ? isv : sv_rest]->Fill(val, weight);
  if (isv < 2)
    hs[sv_top2]->Fill(val, weight);
  hs[sv_all]->Fill(val, weight);
}

void MFVVertexHistos::fill_multi(TH2F** hs, const int isv, const double val, const double val2, const double weight) const {
  hs[isv < 3 ? isv : sv_rest]->Fill(val, val2, weight);
  if (isv < 2)
    hs[sv_top2]->Fill(val, val2, weight);
  hs[sv_all]->Fill(val, val2, weight);
}

void MFVVertexHistos::fill_multi(PairwiseHistos* hs, const int isv, const PairwiseHistos::ValueMap& val, const double weight) const {
  hs[isv < 3 ? isv : sv_rest].Fill(val, -1, weight);
  if (isv < 2)
    hs[sv_top2].Fill(val, -1, weight);
  hs[sv_all].Fill(val, -1, weight);
}

void MFVVertexHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mfv_event_src, mevent);

  edm::Handle<double> weight;
  event.getByLabel(weight_src, weight);

  const float bsx = mevent->bsx;
  const float bsy = mevent->bsy;
  const float bsz = mevent->bsz;
  const math::XYZPoint bs(bsx, bsy, bsz);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByLabel(vertex_aux_src, auxes);

  const int nsv = int(auxes->size());

  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);

    const int svndx = isv >= 3 ? 3 : isv; // don't use fill_multi for the position plots
    h_sv_pos_1d[svndx][0]->Fill(aux.x - bsx, *weight);
    h_sv_pos_1d[svndx][1]->Fill(aux.y - bsy, *weight);
    h_sv_pos_1d[svndx][2]->Fill(aux.z - bsz, *weight);
    h_sv_pos_2d[svndx][0]->Fill(aux.x - bsx, aux.y - bsy, *weight);
    h_sv_pos_2d[svndx][1]->Fill(aux.x - bsx, aux.z - bsz, *weight);
    h_sv_pos_2d[svndx][2]->Fill(aux.y - bsy, aux.z - bsz, *weight);

    if (use_ref) {
      for (auto trki = aux.ref->tracks_begin(), trke = aux.ref->tracks_end(); trki != trke; ++trki) {
        if (aux.ref->trackWeight(*trki) < mfv::track_vertex_weight_min)
          continue;

        const reco::TrackBaseRef& tri = *trki;

        fill_multi(h_sv_trackpt,          isv, tri->pt(), *weight);
        fill_multi(h_sv_trackfracpterr,   isv, tri->ptError()/tri->pt(), *weight);
        fill_multi(h_sv_tracketa,         isv, tri->eta(), *weight);
        fill_multi(h_sv_trackphi,         isv, tri->phi(), *weight);
        fill_multi(h_sv_trackdxy,         isv, tri->dxy(bs), *weight);
        fill_multi(h_sv_trackdz,          isv, tri->dz (bs), *weight);
        fill_multi(h_sv_tracknhits,       isv, tri->numberOfValidHits(), *weight);

        TLorentzVector p4_i, p4_j, p4_k;
        const double m = 0.135;
        p4_i.SetPtEtaPhiM(tri->pt(), tri->eta(), tri->phi(), m);
        for (auto trkj = trki + 1; trkj != trke; ++trkj) {
          if (aux.ref->trackWeight(*trkj) < mfv::track_vertex_weight_min)
            continue;
          const reco::TrackBaseRef& trj = *trkj;
          p4_j.SetPtEtaPhiM(trj->pt(), trj->eta(), trj->phi(), m);

          const TLorentzVector p4_ij = p4_i + p4_j;
          fill_multi(h_sv_trackpaircosth, isv, tri->momentum().Dot(trj->momentum()) / tri->p() / trj->p(), *weight);
          fill_multi(h_sv_trackpairdr,    isv, reco::deltaR(*tri, *trj), *weight);
          fill_multi(h_sv_trackpairmass,  isv, p4_ij.M(), *weight);

          for (auto trkk = trkj + 1; trkk != trke; ++trkk) {
            if (aux.ref->trackWeight(*trkk) < mfv::track_vertex_weight_min)
              continue;

            const reco::TrackBaseRef& trk = *trkk;
            p4_k.SetPtEtaPhiM(trk->pt(), trk->eta(), trk->phi(), m);
            fill_multi(h_sv_tracktriplemass, isv, (p4_ij + p4_k).M(), *weight);
          }
        }
      }
    }

    PairwiseHistos::ValueMap v = {
        {"ntracks",                 aux.ntracks},
        {"nbadtracks",              aux.nbadtracks},
        {"ntracksptgt3",            aux.ntracksptgt3},
        {"ntracksptgt5",            aux.ntracksptgt5},
        {"ntracksptgt10",           aux.ntracksptgt10},
        {"trackminnhits",           aux.trackminnhits},
        {"trackmaxnhits",           aux.trackmaxnhits},
        {"njetsntks",               aux.njets[mfv::JByNtracks]},
        {"njetscomb",               aux.njets[mfv::JByCombination]},
        {"chi2dof",                 aux.chi2/aux.ndof},
        {"chi2dofprob",             TMath::Prob(aux.chi2, aux.ndof)},

        {"tkonlyp",             aux.p4(mfv::PTracksOnly).P()},
        {"tkonlypt",            aux.pt[mfv::PTracksOnly]},
        {"tkonlyeta",           aux.eta[mfv::PTracksOnly]},
        {"tkonlyrapidity",      aux.p4(mfv::PTracksOnly).Rapidity()},
        {"tkonlyphi",           aux.phi[mfv::PTracksOnly]},
        {"tkonlymass",          aux.mass[mfv::PTracksOnly]},

        {"jetsntkp",             aux.p4(mfv::PJetsByNtracks).P()},
        {"jetsntkpt",            aux.pt[mfv::PJetsByNtracks]},
        {"jetsntketa",           aux.eta[mfv::PJetsByNtracks]},
        {"jetsntkrapidity",      aux.p4(mfv::PJetsByNtracks).Rapidity()},
        {"jetsntkphi",           aux.phi[mfv::PJetsByNtracks]},
        {"jetsntkmass",          aux.mass[mfv::PJetsByNtracks]},

        {"jetscmbp",             aux.p4(mfv::PJetsByCombination).P()},
        {"jetscmbpt",            aux.pt[mfv::PJetsByCombination]},
        {"jetscmbeta",           aux.eta[mfv::PJetsByCombination]},
        {"jetscmbrapidity",      aux.p4(mfv::PJetsByCombination).Rapidity()},
        {"jetscmbphi",           aux.phi[mfv::PJetsByCombination]},
        {"jetscmbmass",          aux.mass[mfv::PJetsByCombination]},

        {"tksjetsntkp",             aux.p4(mfv::PTracksPlusJetsByNtracks).P()},
        {"tksjetsntkpt",            aux.pt[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntketa",           aux.eta[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkrapidity",      aux.p4(mfv::PTracksPlusJetsByNtracks).Rapidity()},
        {"tksjetsntkphi",           aux.phi[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkmass",          aux.mass[mfv::PTracksPlusJetsByNtracks]},

        {"tksjetscmbp",             aux.p4(mfv::PTracksPlusJetsByCombination).P()},
        {"tksjetscmbpt",            aux.pt[mfv::PTracksPlusJetsByCombination]},
        {"tksjetscmbeta",           aux.eta[mfv::PTracksPlusJetsByCombination]},
        {"tksjetscmbrapidity",      aux.p4(mfv::PTracksPlusJetsByCombination).Rapidity()},
        {"tksjetscmbphi",           aux.phi[mfv::PTracksPlusJetsByCombination]},
        {"tksjetscmbmass",          aux.mass[mfv::PTracksPlusJetsByCombination]},
        
        {"costhtkonlymombs",         aux.costhmombs  [mfv::PTracksOnly]},
        {"costhtkonlymompv2d",       aux.costhmompv2d[mfv::PTracksOnly]},
        {"costhtkonlymompv3d",       aux.costhmompv3d[mfv::PTracksOnly]},

        {"costhjetsntkmombs",        aux.costhmombs  [mfv::PJetsByNtracks]},
        {"costhjetsntkmompv2d",      aux.costhmompv2d[mfv::PJetsByNtracks]},
        {"costhjetsntkmompv3d",      aux.costhmompv3d[mfv::PJetsByNtracks]},

        {"costhjetscmbmombs",        aux.costhmombs  [mfv::PJetsByCombination]},
        {"costhjetscmbmompv2d",      aux.costhmompv2d[mfv::PJetsByCombination]},
        {"costhjetscmbmompv3d",      aux.costhmompv3d[mfv::PJetsByCombination]},

        {"costhtksjetsntkmombs",     aux.costhmombs  [mfv::PTracksPlusJetsByNtracks]},
        {"costhtksjetsntkmompv2d",   aux.costhmompv2d[mfv::PTracksPlusJetsByNtracks]},
        {"costhtksjetsntkmompv3d",   aux.costhmompv3d[mfv::PTracksPlusJetsByNtracks]},

        {"costhtksjetscmbmombs",     aux.costhmombs  [mfv::PTracksPlusJetsByCombination]},
        {"costhtksjetscmbmompv2d",   aux.costhmompv2d[mfv::PTracksPlusJetsByCombination]},
        {"costhtksjetscmbmompv3d",   aux.costhmompv3d[mfv::PTracksPlusJetsByCombination]},

        {"missdisttkonlypv",        aux.missdistpv   [mfv::PTracksOnly]},
        {"missdisttkonlypverr",     aux.missdistpverr[mfv::PTracksOnly]},
        {"missdisttkonlypvsig",     aux.missdistpvsig(mfv::PTracksOnly)},

        {"missdistjetsntkpv",        aux.missdistpv   [mfv::PJetsByNtracks]},
        {"missdistjetsntkpverr",     aux.missdistpverr[mfv::PJetsByNtracks]},
        {"missdistjetsntkpvsig",     aux.missdistpvsig(mfv::PJetsByNtracks)},

        {"missdistjetscmbpv",        aux.missdistpv   [mfv::PJetsByCombination]},
        {"missdistjetscmbpverr",     aux.missdistpverr[mfv::PJetsByCombination]},
        {"missdistjetscmbpvsig",     aux.missdistpvsig(mfv::PJetsByCombination)},

        {"missdisttksjetsntkpv",        aux.missdistpv   [mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpverr",     aux.missdistpverr[mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpvsig",     aux.missdistpvsig(mfv::PTracksPlusJetsByNtracks)},

        {"missdisttksjetscmbpv",        aux.missdistpv   [mfv::PTracksPlusJetsByCombination]},
        {"missdisttksjetscmbpverr",     aux.missdistpverr[mfv::PTracksPlusJetsByCombination]},
        {"missdisttksjetscmbpvsig",     aux.missdistpvsig(mfv::PTracksPlusJetsByCombination)},

        {"sumpt2",                  aux.sumpt2},
        {"sumnhitsbehind",          aux.sumnhitsbehind},
        {"maxnhitsbehind",          aux.maxnhitsbehind},
        {"mintrackpt",              aux.mintrackpt},
        {"maxtrackpt",              aux.maxtrackpt},
        {"maxm1trackpt",            aux.maxm1trackpt},
        {"maxm2trackpt",            aux.maxm2trackpt},
        {"drmin",                   aux.drmin},
        {"drmax",                   aux.drmax},
        {"dravg",                   aux.dravg},
        {"drrms",                   aux.drrms},
        {"dravgw",                  aux.dravgw},
        {"drrmsw",                  aux.drrmsw},
        {"gen2ddist",               aux.gen2ddist},
        {"gen2derr",                aux.gen2derr},
        {"gen2dsig",                aux.gen2dsig()},
        {"gen3ddist",               aux.gen3ddist},
        {"gen3derr",                aux.gen3derr},
        {"gen3dsig",                aux.gen3dsig()},
        {"bs2dcompatscss",          aux.bs2dcompatscss},
        {"bs2dcompat",              aux.bs2dcompat},
        {"bs2ddist",                aux.bs2ddist},
        {"bs2derr",                 aux.bs2derr},
        {"bs2dsig",                 aux.bs2dsig()},
        {"bs3ddist",                aux.bs3ddist},
        {"pv2dcompatscss",          aux.pv2dcompatscss},
        {"pv2dcompat",              aux.pv2dcompat},
        {"pv2ddist",                aux.pv2ddist},
        {"pv2derr",                 aux.pv2derr},
        {"pv2dsig",                 aux.pv2dsig()},
        {"pv3dcompatscss",          aux.pv3dcompatscss},
        {"pv3dcompat",              aux.pv3dcompat},
        {"pv3ddist",                aux.pv3ddist},
        {"pv3derr",                 aux.pv3derr},
        {"pv3dsig",                 aux.pv3dsig()},
    };

    fill_multi(h_sv, isv, v, *weight);

    for (PairwiseHistos& h : h_sv_sums)
      h.Fill(v, isv, *weight);
  }

  //////////////////////////////////////////////////////////////////////

  h_nsv->Fill(nsv, *weight);
  h_nsv_v_minlspdist2d->Fill(mevent->minlspdist2d(), nsv, *weight);
  h_nsv_v_lspdist2d->Fill(mevent->lspdist2d(), nsv, *weight);
  h_nsv_v_lspdist3d->Fill(mevent->lspdist3d(), nsv, *weight);

  if (nsv >= 2) {
    const MFVVertexAux& sv0 = auxes->at(0);
    const MFVVertexAux& sv1 = auxes->at(1);
    double svdist2d = mag(sv0.x - sv1.x, sv0.y - sv1.y);
    double svdist3d = mag(sv0.x - sv1.x, sv0.y - sv1.y, sv0.z - sv1.z);
    h_svdist2d->Fill(svdist2d, *weight);
    h_svdist3d->Fill(svdist3d, *weight);
    h_svdist2d_v_lspdist2d->Fill(mevent->lspdist2d(), svdist2d, *weight);
    h_svdist3d_v_lspdist3d->Fill(mevent->lspdist3d(), svdist3d, *weight);
    h_svdist2d_v_minlspdist2d->Fill(mevent->minlspdist2d(), svdist2d, *weight);
  }

  if (use_ref) {
    for (int ivtx = 0; ivtx < nsv; ++ivtx) {
      const reco::Vertex& vtxi = *auxes->at(ivtx).ref;

      for (int jvtx = ivtx + 1; jvtx < nsv; ++jvtx) {
        const reco::Vertex& vtxj = *auxes->at(jvtx).ref;

        Measurement1D pair2ddist = distcalc_2d.distance(vtxi, vtxj);
        Measurement1D pair3ddist = distcalc_3d.distance(vtxi, vtxj);

        std::pair<bool, float> pair2dcompat = mfv::compatibility(vtxi, vtxj, false);
        std::pair<bool, float> pair3dcompat = mfv::compatibility(vtxi, vtxj, true);

        h_pair2dcompatscss->Fill(pair2dcompat.first, *weight);
        h_pair2dcompat->Fill(pair2dcompat.second, *weight);
        h_pair2ddist->Fill(pair2ddist.value(), *weight);
        h_pair2derr->Fill(pair2ddist.error(), *weight);
        h_pair2dsig->Fill(pair2ddist.significance(), *weight);
        h_pair3dcompatscss->Fill(pair3dcompat.first, *weight);
        h_pair3dcompat->Fill(pair3dcompat.second, *weight);
        h_pair3ddist->Fill(pair3ddist.value(), *weight);
        h_pair3derr->Fill(pair3ddist.error(), *weight);
        h_pair3dsig->Fill(pair3ddist.significance(), *weight);
      }
    }
  }
}

DEFINE_FWK_MODULE(MFVVertexHistos);
