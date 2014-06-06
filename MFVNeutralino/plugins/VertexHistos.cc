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
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/TrackerSpaceExtent.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"
#include "JMTucker/MFVNeutralino/plugins/VertexMVAWrap.h"

class MFVVertexHistos : public edm::EDAnalyzer {
 public:
  explicit MFVVertexHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag mfv_event_src;
  const edm::InputTag vertex_aux_src;
  const edm::InputTag vertex_src;
  const edm::InputTag vertex_to_jets_src;
  const edm::InputTag weight_src;
  const bool do_scatterplots;

  MFVVertexMVAWrap mva;

  VertexDistanceXY distcalc_2d;
  VertexDistance3D distcalc_3d;

  TH1F* h_w;

  TH1F* h_nsv;
  TH2F* h_nsv_v_minlspdist2d;
  TH2F* h_nsv_v_lspdist2d;
  TH2F* h_nsv_v_lspdist3d;

  // indices for h_sv below:
  enum sv_index { sv_best0, sv_best1, sv_all, sv_num_indices };
  static const char* sv_index_names[sv_num_indices];

  // max number of extra track-related plots to make
  static const int max_ntracks;

  // indices for h_sv_tracks below:
  enum sv_tracks_index { sv_tracks_all, sv_tracks_jet, sv_tracks_track, sv_tracks_num_indices };
  enum sv_jet_tracks_index { sv_jet_tracks_all, sv_jet_tracks_jet, sv_jet_tracks_vertex, sv_jet_tracks_num_indices }; // if these two enums aren't same length, bazinga
  static const char* sv_tracks_index_names[2][sv_tracks_num_indices];

  void fill_multi(TH1F** hs, const int isv, const double val, const double weight) const;
  void fill_multi(TH2F** hs, const int isv, const double val, const double val2, const double weight) const;
  void fill_multi(PairwiseHistos* hs, const int isv, const PairwiseHistos::ValueMap& val, const double weight) const;

  TH1F* h_sv_pos_1d[2][3];
  TH2F* h_sv_pos_2d[2][3];
  TH2F* h_sv_pos_rz[2];
  TH1F* h_sv_pos_phi[2];
  TH1F* h_sv_pos_phi_2pi[2];

  PairwiseHistos h_sv[sv_num_indices];
  PairwiseHistos h_sv_sumtop2;

  TH1F* h_svdist2d;
  TH1F* h_svdist3d;
  TH2F* h_svdist2d_v_lspdist2d;
  TH2F* h_svdist3d_v_lspdist3d;
  TH2F* h_svdist2d_v_minlspdist2d;
  TH2F* h_svdist2d_v_minbsdist2d;
  TH2F* h_sv0pvdz_v_sv1pvdz;
  TH2F* h_sv0pvdzsig_v_sv1pvdzsig;
  TH1F* h_absdeltaphi01;
  TH2F* h_pvmosttracksshared;
  TH1F* h_fractrackssharedwpv01;
  TH1F* h_fractrackssharedwpvs01;

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

  TH1F* h_sv_tracks_pt[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_eta[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_phi[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_charge[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxybs[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dzbs[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxypv[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dzpv[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxyerr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dzerr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxyipv1[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxyipv[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxyipverr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_d3dipv1[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_d3dipv[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_d3dipverr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxyisv1[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxyisv[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dxyisverr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_d3disv1[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_d3disv[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_d3disverr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_chi2dof[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_nhits[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_npixel[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_nstrip[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_minr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_minz[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_maxr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_maxz[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_jetdr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_jetdphi[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracks_bs2derr_jetdr[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dzpv0[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dzpv1[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_dzpv2[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracks_dzpv2_dzpv0[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracks_dzpv2sig_dzpv0sig[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt1_npixel_eta[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt1_npixel_phi[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt1_nstrip_eta[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt1_nstrip_phi[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt3_npixel_eta[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt3_npixel_phi[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt3_nstrip_eta[2][sv_tracks_num_indices][sv_num_indices];
  TH2F* h_sv_tracksptgt3_nstrip_phi[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_algo[2][sv_tracks_num_indices][sv_num_indices];
  TH1F* h_sv_tracks_quality[2][sv_tracks_num_indices][sv_num_indices];

  TH1F* h_sv_jets_ntracks[sv_num_indices];
  TH1F* h_sv_jets_ntracksinvtx[sv_num_indices];
  TH1F* h_sv_jets_energy[sv_num_indices];
  TH1F* h_sv_jets_pt[sv_num_indices];
  TH1F* h_sv_jets_eta[sv_num_indices];
  TH1F* h_sv_jets_phi[sv_num_indices];
  TH1F* h_sv_jets_mass[sv_num_indices];
  TH1F* h_sv_jets_bdisc[sv_num_indices];
  TH1F* h_sv_jets_numDaughters[sv_num_indices];
  TH1F* h_sv_jets_neutralHadEnFrac[sv_num_indices];
  TH1F* h_sv_jets_neutralEmEnFrac[sv_num_indices];
  TH1F* h_sv_jets_chargedHadEnFrac[sv_num_indices];
  TH1F* h_sv_jets_chargedEmEnFrac[sv_num_indices];
  TH1F* h_sv_jets_chargedMult[sv_num_indices];
  TH1F* h_sv_jets_n60[sv_num_indices];
  TH1F* h_sv_jets_n90[sv_num_indices];
  TH1F* h_sv_jets_area[sv_num_indices];
  TH1F* h_sv_jets_maxDist[sv_num_indices];
};

const char* MFVVertexHistos::sv_index_names[MFVVertexHistos::sv_num_indices] = { "best0", "best1", "all" };
const int MFVVertexHistos::max_ntracks = 5;
const char* MFVVertexHistos::sv_tracks_index_names[2][MFVVertexHistos::sv_tracks_num_indices] = { { "all", "jet", "track" }, {"all", "jet", "vertex" } };

MFVVertexHistos::MFVVertexHistos(const edm::ParameterSet& cfg)
  : mfv_event_src(cfg.getParameter<edm::InputTag>("mfv_event_src")),
    vertex_aux_src(cfg.getParameter<edm::InputTag>("vertex_aux_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    vertex_to_jets_src(cfg.getParameter<edm::InputTag>("vertex_to_jets_src")),
    weight_src(cfg.getParameter<edm::InputTag>("weight_src")),
    do_scatterplots(cfg.getParameter<bool>("do_scatterplots"))
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);

  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices;arb. units", 15, 0, 15);
  h_nsv_v_minlspdist2d = fs->make<TH2F>("h_nsv_v_minlspdist2d", ";min dist2d(gen vtx #0, #1) (cm);# of secondary vertices", 600, 0, 3, 5, 0, 5);
  h_nsv_v_lspdist2d = fs->make<TH2F>("h_nsv_v_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);# of secondary vertices", 600, 0, 3, 5, 0, 5);
  h_nsv_v_lspdist3d = fs->make<TH2F>("h_nsv_v_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);# of secondary vertices", 600, 0, 3, 5, 0, 5);

  PairwiseHistos::HistoDefs hs;

  if (vertex_src.label() != "") {
    for (int itk = 0; itk < max_ntracks; ++itk) {
      hs.add(TString::Format("track%i_pt",        itk).Data(), TString::Format("track%i p_{T} (GeV)",                    itk).Data(), 100,   0,     150);
      hs.add(TString::Format("track%i_eta",       itk).Data(), TString::Format("track%i #eta",                           itk).Data(),  50,  -4,       4);
      hs.add(TString::Format("track%i_phi",       itk).Data(), TString::Format("track%i #phi",                           itk).Data(),  50,  -3.15,    3.15);
      hs.add(TString::Format("track%i_charge",    itk).Data(), TString::Format("track%i charge",                         itk).Data(),   4,  -2,       2);
      hs.add(TString::Format("track%i_dxybs",     itk).Data(), TString::Format("track%i dxy(BS) (cm)",                   itk).Data(), 100,  -2,       2);
      hs.add(TString::Format("track%i_dzbs",      itk).Data(), TString::Format("track%i dz(BS) (cm)",                    itk).Data(), 100, -20,      20);
      hs.add(TString::Format("track%i_dxypv",     itk).Data(), TString::Format("track%i dxy(PV) (cm)",                   itk).Data(), 100,  -2,       2);
      hs.add(TString::Format("track%i_dzpv",      itk).Data(), TString::Format("track%i dz(PV) (cm)",                    itk).Data(), 100, -20,      20);
      hs.add(TString::Format("track%i_dxyerr",    itk).Data(), TString::Format("track%i #sigma(dxy) (cm)",               itk).Data(),  50,   0,       0.5);
      hs.add(TString::Format("track%i_dzerr",     itk).Data(), TString::Format("track%i #sigma(dz) (cm)",                itk).Data(),  50,   0,       2);
      hs.add(TString::Format("track%i_dxyipv1",   itk).Data(), TString::Format("track%i dxyipv success",                 itk).Data(),   2,   0,       2);
      hs.add(TString::Format("track%i_dxyipv",    itk).Data(), TString::Format("track%i transverse IP to the PV (cm)",   itk).Data(),  50,   0,       2);
      hs.add(TString::Format("track%i_dxyipverr", itk).Data(), TString::Format("track%i #sigma(dxyipv) (cm)",            itk).Data(),  50,   0,       0.5);
      hs.add(TString::Format("track%i_d3dipv1",   itk).Data(), TString::Format("track%i d3dipv success",                 itk).Data(),   2,   0,       2);
      hs.add(TString::Format("track%i_d3dipv",    itk).Data(), TString::Format("track%i 3D IP to the PV (cm)",           itk).Data(),  50,   0,      20);
      hs.add(TString::Format("track%i_d3dipverr", itk).Data(), TString::Format("track%i #sigma(d3dipv) (cm)",            itk).Data(),  50,   0,       2);
      hs.add(TString::Format("track%i_dxyisv1",   itk).Data(), TString::Format("track%i dxyisv success",                 itk).Data(),   2,   0,       2);
      hs.add(TString::Format("track%i_dxyisv",    itk).Data(), TString::Format("track%i transverse IP to the SV (cm)",   itk).Data(),  50,   0,       2);
      hs.add(TString::Format("track%i_dxyisverr", itk).Data(), TString::Format("track%i #sigma(dxyisv) (cm)",            itk).Data(),  50,   0,       0.5);
      hs.add(TString::Format("track%i_d3disv1",   itk).Data(), TString::Format("track%i d3disv success",                 itk).Data(),   2,   0,       2);
      hs.add(TString::Format("track%i_d3disv",    itk).Data(), TString::Format("track%i 3D IP to the SV (cm)",           itk).Data(),  50,   0,      20);
      hs.add(TString::Format("track%i_d3disverr", itk).Data(), TString::Format("track%i #sigma(d3disv) (cm)",            itk).Data(),  50,   0,       2);
      hs.add(TString::Format("track%i_chi2dof",   itk).Data(), TString::Format("track%i #chi^2/dof",                     itk).Data(),  50,   0,       7);
      hs.add(TString::Format("track%i_nhits",     itk).Data(), TString::Format("track%i number of hits",                 itk).Data(),  40,   0,      40);
      hs.add(TString::Format("track%i_npixel",    itk).Data(), TString::Format("track%i number of pixel hits",           itk).Data(),  40,   0,      40);
      hs.add(TString::Format("track%i_nstrip",    itk).Data(), TString::Format("track%i number of strip hits",           itk).Data(),  40,   0,      40);
      hs.add(TString::Format("track%i_minr",      itk).Data(), TString::Format("track%i innermost radius of hit module", itk).Data(),  14,   0,      14);
      hs.add(TString::Format("track%i_minz",      itk).Data(), TString::Format("track%i innermost z of hit module",      itk).Data(),  15,   0,      15);
      hs.add(TString::Format("track%i_maxr",      itk).Data(), TString::Format("track%i outermost radius of hit module", itk).Data(),  14,   0,      14);
      hs.add(TString::Format("track%i_maxz",      itk).Data(), TString::Format("track%i outermost z of hit module",      itk).Data(),  15,   0,      15);
      hs.add(TString::Format("track%i_jetdr",     itk).Data(), TString::Format("track%i #DeltaR(jets,track)",            itk).Data(),  50,   0,       7);
      hs.add(TString::Format("track%i_jetdphi",   itk).Data(), TString::Format("track%i #Delta#phi(jets,track)",         itk).Data(),  64,  -3.2,     3.2);
      hs.add(TString::Format("track%i_dzpv0",     itk).Data(), TString::Format("track%i dz(the PV) (cm)",                itk).Data(), 100,   0,       2);
      hs.add(TString::Format("track%i_dzpv1",     itk).Data(), TString::Format("track%i dz(closest PV) (cm)",            itk).Data(), 100,   0,       2);
      hs.add(TString::Format("track%i_dzpv2",     itk).Data(), TString::Format("track%i dz(closest PV not the PV) (cm)", itk).Data(), 100,   0,       2);
      hs.add(TString::Format("track%i_algo",      itk).Data(), TString::Format("track%i algorithm",                      itk).Data(),  30,   0,      30);
    }

    hs.add("ntracksdrlt0p50", "# of tracks/SV w/ #DeltaR(jets,track) < 0.50", 40, 0, 40);
    hs.add("ntracksdr0p50to1p57", "# of tracks/SV w/ 0.50 <= #DeltaR(jets,track) < 1.57", 40, 0, 40);
    hs.add("ntracksdrgt1p57", "# of tracks/SV w/ #DeltaR(jets,track) >= 1.57", 40, 0, 40);

    hs.add("tracksdrlt1p57pt", "SV tracks w/ #DeltaR(jets,track) < 1.57 p_{T}", 100, 0, 300);
    hs.add("tracksdrlt1p57eta", "SV tracks w/ #DeltaR(jets,track) < 1.57 #eta", 50, -4, 4);
    hs.add("tracksdrlt1p57phi", "SV tracks w/ #DeltaR(jets,track) < 1.57 #phi", 50, -3.15, 3.15);
  }

  hs.add("mva", "MVA output", 100, -2, 3);

  hs.add("nlep", "# leptons", 10, 0, 10);

  hs.add("ntracks",                       "# of tracks/SV",                                                               40,    0,      40);
  hs.add("nbadtracks",                    "# of 'bad' tracks/SV",                                                         40,    0,      40);
  hs.add("ntracksptgt3",                  "# of tracks/SV w/ p_{T} > 3 GeV",                                              40,    0,      40);
  hs.add("ntracksptgt5",                  "# of tracks/SV w/ p_{T} > 5 GeV",                                              40,    0,      40);
  hs.add("ntracksptgt10",                 "# of tracks/SV w/ p_{T} > 10 GeV",                                             40,    0,      40);
  hs.add("trackminnhits",                 "min number of hits on track per SV",                                           40,    0,      40);
  hs.add("trackmaxnhits",                 "max number of hits on track per SV",                                           40,    0,      40);
  hs.add("njetsntks",                     "# of jets assoc. by tracks to SV",                                             10,    0,      10);
  hs.add("chi2dof",                       "SV #chi^2/dof",                                                                50,    0,       7);
  hs.add("chi2dofprob",                   "SV p(#chi^2, dof)",                                                            50,    0,       1.2);

  hs.add("msptm",                         "SV p_{T}-corrected mass (GeV)",                                               100,    0,    1500);

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

  hs.add("tksjetsntkp",                   "SV tracks-plus-jets-by-ntracks p (GeV)",                                      100,    0,     300);
  hs.add("tksjetsntkpt",                  "SV tracks-plus-jets-by-ntracks p_{T} (GeV)",                                  100,    0,     300);
  hs.add("tksjetsntketa",                 "SV tracks-plus-jets-by-ntracks #eta",                                          50,   -4,       4);
  hs.add("tksjetsntkrapidity",            "SV tracks-plus-jets-by-ntracks rapidity",                                      50,   -4,       4);
  hs.add("tksjetsntkphi",                 "SV tracks-plus-jets-by-ntracks #phi",                                          50,   -3.15,    3.15);
  hs.add("tksjetsntkmass",                "SV tracks-plus-jets-by-ntracks mass (GeV)",                                   100,    0,    1500);
				        
  hs.add("costhtkonlymombs",              "cos(angle(2-momentum (tracks-only), 2-dist to BS))",                          101,   -1,       1.02);
  hs.add("costhtkonlymompv2d",            "cos(angle(2-momentum (tracks-only), 2-dist to PV))",                          101,   -1,       1.02);
  hs.add("costhtkonlymompv3d",            "cos(angle(3-momentum (tracks-only), 3-dist to PV))",                          101,   -1,       1.02);

  hs.add("costhjetsntkmombs",             "cos(angle(2-momentum (jets-by-ntracks -only), 2-dist to BS))",                101,   -1,       1.02);
  hs.add("costhjetsntkmompv2d",           "cos(angle(2-momentum (jets-by-ntracks -only), 2-dist to PV))",                101,   -1,       1.02);
  hs.add("costhjetsntkmompv3d",           "cos(angle(3-momentum (jets-by-ntracks -only), 3-dist to PV))",                101,   -1,       1.02);

  hs.add("costhtksjetsntkmombs",          "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to BS))",          101,   -1,       1.02);
  hs.add("costhtksjetsntkmompv2d",        "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to PV))",          101,   -1,       1.02);
  hs.add("costhtksjetsntkmompv3d",        "cos(angle(3-momentum (tracks-plus-jets-by-ntracks), 3-dist to PV))",          101,   -1,       1.02);

  hs.add("missdisttkonlypv",              "miss dist. (tracks-only) of SV to PV (cm)",                                   100,    0,       2);
  hs.add("missdisttkonlypverr",           "#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                           100,    0,       0.05);
  hs.add("missdisttkonlypvsig",           "N#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                          100,    0,     100);

  hs.add("missdistjetsntkpv",             "miss dist. (jets-by-ntracks -only) of SV to PV (cm)",                         100,    0,       2);
  hs.add("missdistjetsntkpverr",          "#sigma(miss dist. (jets-by-ntracks -only) of SV to PV) (cm)",                 100,    0,       0.05);
  hs.add("missdistjetsntkpvsig",          "N#sigma(miss dist. (jets-by-ntracks -only) of SV to PV) (cm)",                100,    0,     100);

  hs.add("missdisttksjetsntkpv",          "miss dist. (tracks-plus-jets-by-ntracks) of SV to PV (cm)",                   100,    0,       2);
  hs.add("missdisttksjetsntkpverr",       "#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",           100,    0,       0.05);
  hs.add("missdisttksjetsntkpvsig",       "N#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",          100,    0,     100);
					  
  hs.add("sumpt2",                        "SV #Sigma p_{T}^{2} (GeV^2)",                                                 300,    0,    6000);
  hs.add("maxnhitsbehind",                "max number of hits behind SV",                                                 15,    0,      15);
  hs.add("sumnhitsbehind",                "sum number of hits behind SV",                                                100,    0,     100);

  hs.add("ntrackssharedwpv",  "number of tracks shared with the PV", 40, 0, 40);
  hs.add("ntrackssharedwpvs", "number of tracks shared with any PV", 40, 0, 40);
  hs.add("fractrackssharedwpv",  "fraction of tracks shared with the PV", 41, 0, 1.025);
  hs.add("fractrackssharedwpvs", "fraction of tracks shared with any PV", 41, 0, 1.025);
  hs.add("npvswtracksshared", "number of PVs having tracks shared",  40, 0, 40);
  
  hs.add("mintrackpt",                    "SV min{trk_{i} p_{T}} (GeV)",                                                  50,    0,      10);
  hs.add("maxtrackpt",                    "SV max{trk_{i} p_{T}} (GeV)",                                                 100,    0,     150);
  hs.add("maxm1trackpt",                  "SV max-1{trk_{i} p_{T}} (GeV)",                                               100,    0,     150);
  hs.add("maxm2trackpt",                  "SV max-2{trk_{i} p_{T}} (GeV)",                                               100,    0,     150);
  hs.add("trackptavg",                    "SV avg{trk_{i} p_{T}} (GeV)",                                                  50,    0,      50);
  hs.add("trackptrms",                    "SV rms{trk_{i} p_{T}} (GeV)",                                                  50,    0,      20);

  hs.add("trackdxymin", "SV min{trk_{i} dxy(BS)} (cm)", 50, 0, 0.2);
  hs.add("trackdxymax", "SV max{trk_{i} dxy(BS)} (cm)", 50, 0, 2);
  hs.add("trackdxyavg", "SV avg{trk_{i} dxy(BS)} (cm)", 50, 0, 0.5);
  hs.add("trackdxyrms", "SV rms{trk_{i} dxy(BS)} (cm)", 50, 0, 0.5);

  hs.add("trackdzmin", "SV min{trk_{i} dz(PV)} (cm)", 50, 0, 0.5);
  hs.add("trackdzmax", "SV max{trk_{i} dz(PV)} (cm)", 50, 0, 2);
  hs.add("trackdzavg", "SV avg{trk_{i} dz(PV)} (cm)", 50, 0, 1);
  hs.add("trackdzrms", "SV rms{trk_{i} dz(PV)} (cm)", 50, 0, 0.5);

  hs.add("trackpterrmin", "SV min{frac. #sigma trk_{i} p_{T}}", 50, 0, 0.1);
  hs.add("trackpterrmax", "SV max{frac. #sigma trk_{i} p_{T}}", 50, 0, 2);
  hs.add("trackpterravg", "SV avg{frac. #sigma trk_{i} p_{T}}", 50, 0, 1);
  hs.add("trackpterrrms", "SV rms{frac. #sigma trk_{i} p_{T}}", 50, 0, 2);

  hs.add("trackdxyerrmin", "SV min{#sigma trk_{i} dxy(BS)} (cm)", 50, 0, 0.01);
  hs.add("trackdxyerrmax", "SV max{#sigma trk_{i} dxy(BS)} (cm)", 50, 0, 0.5);
  hs.add("trackdxyerravg", "SV avg{#sigma trk_{i} dxy(BS)} (cm)", 50, 0, 0.1);
  hs.add("trackdxyerrrms", "SV rms{#sigma trk_{i} dxy(BS)} (cm)", 50, 0, 0.1);

  hs.add("trackdzerrmin", "SV min{#sigma trk_{i} dz(PV)} (cm)", 50, 0, 0.01);
  hs.add("trackdzerrmax", "SV max{#sigma trk_{i} dz(PV)} (cm)", 50, 0, 2);
  hs.add("trackdzerravg", "SV avg{#sigma trk_{i} dz(PV)} (cm)", 50, 0, 1);
  hs.add("trackdzerrrms", "SV rms{#sigma trk_{i} dz(PV)} (cm)", 50, 0, 0.4);

  hs.add("trackpairmassmin", "SV min{mass(trk_{i}, trk_{j})} (GeV)", 50, 0, 2);
  hs.add("trackpairmassmax", "SV max{mass(trk_{i}, trk_{j})} (GeV)", 50, 0, 100);
  hs.add("trackpairmassavg", "SV avg{mass(trk_{i}, trk_{j})} (GeV)", 50, 0, 20);
  hs.add("trackpairmassrms", "SV rms{mass(trk_{i}, trk_{j})} (GeV)", 50, 0, 20);

  hs.add("tracktripmassmin", "SV min{mass(trk_{i}, trk_{j}, trk_{k})} (GeV)", 50, 0, 6);
  hs.add("tracktripmassmax", "SV max{mass(trk_{i}, trk_{j}, trk_{k})} (GeV)", 50, 0, 150);
  hs.add("tracktripmassavg", "SV avg{mass(trk_{i}, trk_{j}, trk_{k})} (GeV)", 50, 0, 50);
  hs.add("tracktripmassrms", "SV rms{mass(trk_{i}, trk_{j}, trk_{k})} (GeV)", 50, 0, 40);

  hs.add("trackquadmassmin", "SV min{mass(trk_{i}, trk_{j}, trk_{k}, trk_{l})} (GeV)", 50, 0, 15);
  hs.add("trackquadmassmax", "SV max{mass(trk_{i}, trk_{j}, trk_{k}, trk_{l})} (GeV)", 50, 0, 200);
  hs.add("trackquadmassavg", "SV avg{mass(trk_{i}, trk_{j}, trk_{k}, trk_{l})} (GeV)", 50, 0, 50);
  hs.add("trackquadmassrms", "SV rms{mass(trk_{i}, trk_{j}, trk_{k}, trk_{l})} (GeV)", 50, 0, 30);

  hs.add("trackpairdetamin", "SV min{#Delta #eta(i,j)}", 150,    0,       1.5);
  hs.add("trackpairdetamax", "SV max{#Delta #eta(i,j)}", 150,    0,       7);
  hs.add("trackpairdetaavg", "SV avg{#Delta #eta(i,j)}", 150,    0,       5);
  hs.add("trackpairdetarms", "SV rms{#Delta #eta(i,j)}", 150,    0,       3);

  hs.add("trackpairdphimax",   "SV max{|#Delta #phi(i,j)|}",   100, 0, 3.15);
  hs.add("trackpairdphimaxm1", "SV max-1{|#Delta #phi(i,j)|}", 100, 0, 3.15);
  hs.add("trackpairdphimaxm2", "SV max-2{|#Delta #phi(i,j)|}", 100, 0, 3.15);

  hs.add("drmin",                         "SV min{#Delta R(i,j)}",                                                       150,    0,       1.5);
  hs.add("drmax",                         "SV max{#Delta R(i,j)}",                                                       150,    0,       7);
  hs.add("dravg",                         "SV avg{#Delta R(i,j)}",                                                       150,    0,       5);
  hs.add("drrms",                         "SV rms{#Delta R(i,j)}",                                                       150,    0,       3);

  hs.add("jetpairdetamin", "SV min{#Delta #eta(jet_{i}, jet_{j})}", 50, 0, 5);
  hs.add("jetpairdetamax", "SV max{#Delta #eta(jet_{i}, jet_{j})}", 50, 0, 7);
  hs.add("jetpairdetaavg", "SV avg{#Delta #eta(jet_{i}, jet_{j})}", 50, 0, 5);
  hs.add("jetpairdetarms", "SV rms{#Delta #eta(jet_{i}, jet_{j})}", 50, 0, 1.5);

  hs.add("jetpairdrmin", "SV min{#Delta R(jet_{i}, jet_{j})}", 50, 0, 5);
  hs.add("jetpairdrmax", "SV max{#Delta R(jet_{i}, jet_{j})}", 50, 0, 7);
  hs.add("jetpairdravg", "SV avg{#Delta R(jet_{i}, jet_{j})}", 50, 0, 5);
  hs.add("jetpairdrrms", "SV rms{#Delta R(jet_{i}, jet_{j})}", 50, 0, 1.5);

  hs.add("costhtkmomvtxdispmin", "SV min{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdispmax", "SV max{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdispavg", "SV avg{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdisprms", "SV rms{cos(angle(trk_{i}, SV-PV))}", 50,  0, 1);

  hs.add("costhjetmomvtxdispmin", "SV min{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdispmax", "SV max{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdispavg", "SV avg{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdisprms", "SV rms{cos(angle(jet_{i}, SV-PV))}", 50,  0, 1);

  hs.add("gen2ddist",                     "dist2d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  hs.add("gen2derr",                      "#sigma(dist2d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  hs.add("gen2dsig",                      "N#sigma(dist2d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  hs.add("gen3ddist",                     "dist3d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  hs.add("gen3derr",                      "#sigma(dist3d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  hs.add("gen3dsig",                      "N#sigma(dist3d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  hs.add("bs2dcompatscss",                "compat2d(SV, beamspot) success",                                                2,    0,       2);
  hs.add("bs2dcompat",                    "compat2d(SV, beamspot)",                                                      100,    0,    1000);
  hs.add("bs2ddist",                      "dist2d(SV, beamspot) (cm)",                                                   500,    0,       5);
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
  hs.add("pvdz",                          "dz(SV, PV) (cm)",                                                             100,    0,       0.5);
  hs.add("pvdzerr",                       "#sigma(dz(SV, PV)) (cm)",                                                     100,    0,       0.1);
  hs.add("pvdzsig",                       "N#sigma(dz(SV, PV))",                                                         100,    0,     100);

  for (int j = 0; j < sv_num_indices; ++j) {
    const char* exc = sv_index_names[j];

    if (j < 2) {
      for (int i = 0; i < 3; ++i) {
        float l = i == 2 ? 25 : 20;
        h_sv_pos_1d[j][i] = fs->make<TH1F>(TString::Format("h_sv_pos_1d_%i%i", j, i), TString::Format(";%s SV pos[%i] (cm);arb. units", exc, i), 100, -l, l);
      }
      h_sv_pos_2d[j][0] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixy", j), TString::Format(";%s SV x (cm);%s SV y (cm)", exc, exc), 100, -20, 20, 100, -20, 20);
      h_sv_pos_2d[j][1] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%ixz", j), TString::Format(";%s SV x (cm);%s SV z (cm)", exc, exc), 100, -20, 20, 100, -25, 25);
      h_sv_pos_2d[j][2] = fs->make<TH2F>(TString::Format("h_sv_pos_2d_%iyz", j), TString::Format(";%s SV y (cm);%s SV z (cm)", exc, exc), 100, -20, 20, 100, -25, 25);
      h_sv_pos_rz[j]    = fs->make<TH2F>(TString::Format("h_sv_pos_rz_%i",   j), TString::Format(";%s SV r (cm);%s SV z (cm)", exc, exc), 100, -20, 20, 100, -25, 25);
      h_sv_pos_phi[j]   = fs->make<TH1F>(TString::Format("h_sv_pos_phi_%i",  j), TString::Format(";%s SV phi;arb. units", exc), 50, -3.15, 3.15);
      h_sv_pos_phi_2pi[j] = fs->make<TH1F>(TString::Format("h_sv_pos_phi_2pi_%i", j), TString::Format(";%s SV phi from 0 to 2#pi;arb. units", exc), 50, 0, 6.30);
    }

    h_sv[j].Init("h_sv_" + std::string(exc), hs, true, do_scatterplots);

    if (vertex_src.label() != "") {
      assert(int(sv_tracks_num_indices) == int(sv_jet_tracks_num_indices));
      for (int k = 0; k < 2; ++k) {
        for (int i = 0; i < sv_tracks_num_indices; ++i) {
          const char* extc = sv_tracks_index_names[k][i];
          const char* extc2 = k == 1 ? "jet_" : "";

          h_sv_tracks_pt[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_pt", exc, extc2, extc), TString::Format(";%s SV %s %stracks p_{T} (GeV);arb. units", exc, extc2, extc), 100, 0, 150);
          h_sv_tracks_eta[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_eta", exc, extc2, extc), TString::Format(";%s SV %s %stracks #eta;arb. units", exc, extc2, extc), 50, -4, 4);
          h_sv_tracks_phi[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_phi", exc, extc2, extc), TString::Format(";%s SV %s %stracks #phi;arb. units", exc, extc2, extc), 50, -3.15, 3.15);
          h_sv_tracks_charge[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_charge", exc, extc2, extc), TString::Format(";%s SV %s %stracks charge;arb. units", exc, extc2, extc), 4, -2, 2);
          h_sv_tracks_dxybs[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxybs", exc, extc2, extc), TString::Format(";%s SV %s %stracks dxy(BS) (cm);arb. units", exc, extc2, extc), 100, -2, 2);
          h_sv_tracks_dzbs[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dzbs", exc, extc2, extc), TString::Format(";%s SV %s %stracks dz(BS) (cm);arb. units", exc, extc2, extc), 100, -20, 20);
          h_sv_tracks_dxypv[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxypv", exc, extc2, extc), TString::Format(";%s SV %s %stracks dxy(PV) (cm);arb. units", exc, extc2, extc), 100, -2, 2);
          h_sv_tracks_dzpv[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dzpv", exc, extc2, extc), TString::Format(";%s SV %s %stracks dz(PV) (cm);arb. units", exc, extc2, extc), 100, -20, 20);
          h_sv_tracks_dxyerr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxyerr", exc, extc2, extc), TString::Format(";%s SV %s %stracks #sigma(dxy) (cm);arb. units", exc, extc2, extc), 50, 0, 0.5);
          h_sv_tracks_dzerr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dzerr", exc, extc2, extc), TString::Format(";%s SV %s %stracks #sigma(dz) (cm);arb. units", exc, extc2, extc), 50, 0, 2);
          h_sv_tracks_dxyipv1[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxyipv1", exc, extc2, extc), TString::Format(";%s SV %s %stracks dxyipv success;arb. units", exc, extc2, extc), 2, 0, 2);
          h_sv_tracks_dxyipv[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxyipv", exc, extc2, extc), TString::Format(";%s SV %s %stracks transverse IP to the PV (cm);arb. units", exc, extc2, extc), 50, 0, 2);
          h_sv_tracks_dxyipverr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxyipverr", exc, extc2, extc), TString::Format(";%s SV %s %stracks #sigma(dxyipv) (cm);arb. units", exc, extc2, extc), 50, 0, 0.5);
          h_sv_tracks_d3dipv1[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_d3dipv1", exc, extc2, extc), TString::Format(";%s SV %s %stracks d3dipv success;arb. units", exc, extc2, extc), 2, 0, 2);
          h_sv_tracks_d3dipv[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_d3dipv", exc, extc2, extc), TString::Format(";%s SV %s %stracks 3D IP to the PV (cm);arb. units", exc, extc2, extc), 50, 0, 20);
          h_sv_tracks_d3dipverr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_d3dipverr", exc, extc2, extc), TString::Format(";%s SV %s #sigma(%s d3dipv) (cm);arb. units", exc, extc2, extc), 50, 0, 2);
          h_sv_tracks_dxyisv1[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxyisv1", exc, extc2, extc), TString::Format(";%s SV %s %stracks dxyisv success;arb. units", exc, extc2, extc), 2, 0, 2);
          h_sv_tracks_dxyisv[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxyisv", exc, extc2, extc), TString::Format(";%s SV %s %stracks transverse IP to the SV (cm);arb. units", exc, extc2, extc), 50, 0, 2);
          h_sv_tracks_dxyisverr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dxyisverr", exc, extc2, extc), TString::Format(";%s SV %s %stracks #sigma(dxyisv) (cm);arb. units", exc, extc2, extc), 50, 0, 0.5);
          h_sv_tracks_d3disv1[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_d3disv1", exc, extc2, extc), TString::Format(";%s SV %s %stracks d3disv success;arb. units", exc, extc2, extc), 2, 0, 2);
          h_sv_tracks_d3disv[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_d3disv", exc, extc2, extc), TString::Format(";%s SV %s %stracks 3D IP to the SV (cm);arb. units", exc, extc2, extc), 50, 0, 20);
          h_sv_tracks_d3disverr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_d3disverr", exc, extc2, extc), TString::Format(";%s SV %s #sigma(%s d3disv) (cm);arb. units", exc, extc2, extc), 50, 0, 2);
          h_sv_tracks_chi2dof[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_chi2dof", exc, extc2, extc), TString::Format(";%s SV %s %stracks #chi^2/dof;arb. units", exc, extc2, extc), 50, 0, 7);
          h_sv_tracks_nhits[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_nhits", exc, extc2, extc), TString::Format(";%s SV %s %stracks number of hits;arb. units", exc, extc2, extc), 40, 0, 40);
          h_sv_tracks_npixel[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_npixel", exc, extc2, extc), TString::Format(";%s SV %s %stracks number of pixel hits;arb. units", exc, extc2, extc), 40, 0, 40);
          h_sv_tracks_nstrip[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_nstrip", exc, extc2, extc), TString::Format(";%s SV %s %stracks number of strip hits;arb. units", exc, extc2, extc), 40, 0, 40);
          h_sv_tracks_minr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_minr", exc, extc2, extc), TString::Format(";%s SV %s %stracks innermost radius of hit module;arb. units", exc, extc2, extc), 14, 0, 14);
          h_sv_tracks_minz[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_minz", exc, extc2, extc), TString::Format(";%s SV %s %stracks innermost z of hit module;arb. units", exc, extc2, extc), 15, 0, 15);
          h_sv_tracks_maxr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_maxr", exc, extc2, extc), TString::Format(";%s SV %s %stracks outermost radius of hit module;arb. units", exc, extc2, extc), 14, 0, 14);
          h_sv_tracks_maxz[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_maxz", exc, extc2, extc), TString::Format(";%s SV %s %stracks outermost z of hit module;arb. units", exc, extc2, extc), 15, 0, 15);
          h_sv_tracks_jetdr[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_jetdr", exc, extc2, extc), TString::Format(";%s SV %s %stracks #DeltaR(jets,track);arb. units", exc, extc2, extc), 50, 0, 7);
          h_sv_tracks_jetdphi[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_jetdphi", exc, extc2, extc), TString::Format(";%s SV %s %stracks #Delta#phi(jets,track);arb. units", exc, extc2, extc), 64, -3.2, 3.2);
          h_sv_tracks_bs2derr_jetdr[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracks_%s_bs2derr_jetdr", exc, extc2, extc), TString::Format(";%s SV %s %stracks #DeltaR(jets,track);bs2derr", exc, extc2, extc), 50, 0, 7, 100, 0, 0.05);
          h_sv_tracks_dzpv0[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dzpv0", exc, extc2, extc), TString::Format(";%s SV %s %stracks dz(the PV) (cm);arb. units", exc, extc2, extc), 100, 0, 2);
          h_sv_tracks_dzpv1[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dzpv1", exc, extc2, extc), TString::Format(";%s SV %s %stracks dz(closest PV) (cm);arb. units", exc, extc2, extc), 100, 0, 2);
          h_sv_tracks_dzpv2[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_dzpv2", exc, extc2, extc), TString::Format(";%s SV %s %stracks dz(closest PV not the PV) (cm);arb. units", exc, extc2, extc), 100, 0, 2);
          h_sv_tracks_dzpv2_dzpv0[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracks_%s_dzpv2_dzpv0", exc, extc2, extc), TString::Format(";%s SV %s %stracks dz(the PV) (cm);%s SV %s %stracks dz(closest PV not the PV) (cm)", exc, extc2, extc, exc, extc2, extc), 100, 0, 2, 100, 0, 2);
          h_sv_tracks_dzpv2sig_dzpv0sig[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracks_%s_dzpv2sig_dzpv0sig", exc, extc2, extc), TString::Format(";%s SV %s %stracks N#sigma(dz(the PV));%s SV %s %stracks N#sigma(dz(closest PV not the PV))", exc, extc2, extc, exc, extc2, extc), 100, 0, 100, 100, 0, 100);
          h_sv_tracksptgt1_npixel_eta[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt1_%s_npixel_eta", exc, extc2, extc), TString::Format(";%s SV %s %stracks eta;%s SV %s %stracks number of pixel hits", exc, extc2, extc, exc, extc2, extc), 50, -4, 4, 40, 0, 40);
          h_sv_tracksptgt1_npixel_phi[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt1_%s_npixel_phi", exc, extc2, extc), TString::Format(";%s SV %s %stracks phi;%s SV %s %stracks number of pixel hits", exc, extc2, extc, exc, extc2, extc), 50, -3.15, 3.15, 40, 0, 40);
          h_sv_tracksptgt1_nstrip_eta[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt1_%s_nstrip_eta", exc, extc2, extc), TString::Format(";%s SV %s %stracks eta;%s SV %s %stracks number of strip hits", exc, extc2, extc, exc, extc2, extc), 50, -4, 4, 40, 0, 40);
          h_sv_tracksptgt1_nstrip_phi[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt1_%s_nstrip_phi", exc, extc2, extc), TString::Format(";%s SV %s %stracks phi;%s SV %s %stracks number of strip hits", exc, extc2, extc, exc, extc2, extc), 50, -3.15, 3.15, 40, 0, 40);
          h_sv_tracksptgt3_npixel_eta[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt3_%s_npixel_eta", exc, extc2, extc), TString::Format(";%s SV %s %stracks eta;%s SV %s %stracks number of pixel hits", exc, extc2, extc, exc, extc2, extc), 50, -4, 4, 40, 0, 40);
          h_sv_tracksptgt3_npixel_phi[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt3_%s_npixel_phi", exc, extc2, extc), TString::Format(";%s SV %s %stracks phi;%s SV %s %stracks number of pixel hits", exc, extc2, extc, exc, extc2, extc), 50, -3.15, 3.15, 40, 0, 40);
          h_sv_tracksptgt3_nstrip_eta[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt3_%s_nstrip_eta", exc, extc2, extc), TString::Format(";%s SV %s %stracks eta;%s SV %s %stracks number of strip hits", exc, extc2, extc, exc, extc2, extc), 50, -4, 4, 40, 0, 40);
          h_sv_tracksptgt3_nstrip_phi[k][i][j] = fs->make<TH2F>(TString::Format("h_sv_%s_%stracksptgt3_%s_nstrip_phi", exc, extc2, extc), TString::Format(";%s SV %s %stracks phi;%s SV %s %stracks number of strip hits", exc, extc2, extc, exc, extc2, extc), 50, -3.15, 3.15, 40, 0, 40);
          h_sv_tracks_algo[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_algo", exc, extc2, extc), TString::Format(";%s SV %s %stracks algorithm;arb. units", exc, extc2, extc), 30, 0, 30);
          h_sv_tracks_quality[k][i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%stracks_%s_quality", exc, extc2, extc), TString::Format(";%s SV %s %stracks quality;arb.units", exc, extc2, extc), 7, 0, 7);
        }
      }

      h_sv_jets_ntracks[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_ntracks", exc), TString::Format("h_sv_%s_jets_ntracks", exc), 50, 0, 50);
      h_sv_jets_ntracksinvtx[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_ntracksinvtx", exc), TString::Format("h_sv_%s_jets_ntracksinvtx", exc), 20, 0, 20);
      h_sv_jets_energy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_energy", exc), TString::Format("h_sv_%s_jets_energy", exc), 50, 0, 1000);
      h_sv_jets_pt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_pt", exc), TString::Format("h_sv_%s_jets_pt", exc), 50, 0, 1000);
      h_sv_jets_eta[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_eta", exc), TString::Format("h_sv_%s_jets_eta", exc), 50, -3, 3);
      h_sv_jets_phi[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_phi", exc), TString::Format("h_sv_%s_jets_phi", exc), 50, -3.15, 3.15);
      h_sv_jets_mass[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_mass", exc), TString::Format("h_sv_%s_jets_mass", exc), 50, 0, 100);
      h_sv_jets_bdisc[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_bdisc", exc), TString::Format("h_sv_%s_jets_bdisc", exc), 50, 0, 1);
      h_sv_jets_numDaughters[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_numDaughters", exc), TString::Format("h_sv_%s_jets_numDaughters", exc), 25, 0, 75);
      h_sv_jets_neutralHadEnFrac[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_neutralHadEnFrac", exc), TString::Format("h_sv_%s_jets_neutralHadEnFrac", exc), 26, 0, 1.04);
      h_sv_jets_neutralEmEnFrac[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_neutralEmEnFrac", exc), TString::Format("h_sv_%s_jets_neutralEmEnFrac", exc), 26, 0, 1.04);
      h_sv_jets_chargedHadEnFrac[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_chargedHadEnFrac", exc), TString::Format("h_sv_%s_jets_chargedHadEnFrac", exc), 26, 0, 1.04);
      h_sv_jets_chargedEmEnFrac[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_chargedEmEnFrac", exc), TString::Format("h_sv_%s_jets_chargedEmEnFrac", exc), 26, 0, 1.04);
      h_sv_jets_chargedMult[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_chargedMult", exc), TString::Format("h_sv_%s_jets_chargedMult", exc), 25, 0, 50);
      h_sv_jets_n60[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_n60", exc), TString::Format("h_sv_%s_jets_n60", exc), 25, 0, 50);
      h_sv_jets_n90[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_n90", exc), TString::Format("h_sv_%s_jets_n90", exc), 25, 0, 50);
      h_sv_jets_area[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_area", exc), TString::Format("h_sv_%s_jets_area", exc), 20, 0, 1);
      h_sv_jets_maxDist[j] = fs->make<TH1F>(TString::Format("h_sv_%s_jets_maxDist", exc), TString::Format("h_sv_%s_jets_maxDist", exc), 20, 0, 1);
    }
  }

  h_sv_sumtop2.Init("h_sv_sumtop2", hs, true, do_scatterplots, 2);

  h_svdist2d = fs->make<TH1F>("h_svdist2d", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist3d = fs->make<TH1F>("h_svdist3d", ";dist3d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist2d_v_lspdist2d = fs->make<TH2F>("h_svdist2d_v_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist3d_v_lspdist3d = fs->make<TH2F>("h_svdist3d_v_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);dist3d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist2d_v_minlspdist2d = fs->make<TH2F>("h_svdist2d_v_minlspdist2d", ";min dist2d(gen vtx #0, #1) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_svdist2d_v_minbsdist2d = fs->make<TH2F>("h_svdist2d_v_mindist2d", ";min dist2d(sv, bs) (cm);dist2d(sv #0, #1) (cm)", 600, 0, 3, 600, 0, 3);
  h_sv0pvdz_v_sv1pvdz = fs->make<TH2F>("h_sv0pvdz_v_sv1pvdz", ";sv #1 dz to PV (cm);sv #0 dz to PV (cm)", 100, 0, 0.5, 100, 0, 0.5);
  h_sv0pvdzsig_v_sv1pvdzsig = fs->make<TH2F>("h_sv0pvdzsig_v_sv1pvdzsig", ";N#sigma(sv #1 dz to PV);sv N#sigma(#0 dz to PV)", 100, 0, 50, 100, 0, 50);
  h_absdeltaphi01 = fs->make<TH1F>("h_absdeltaphi01", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 315, 0, 3.15);
  h_fractrackssharedwpv01 = fs->make<TH1F>("h_fractrackssharedwpv01", ";fraction of sv #0 and sv #1 tracks shared with the PV;arb. units", 41, 0, 1.025);
  h_fractrackssharedwpvs01 = fs->make<TH1F>("h_fractrackssharedwpvs01", ";fraction of sv #0 and sv #1 tracks shared with any PV;arb. units", 41, 0, 1.025);
  h_pvmosttracksshared = fs->make<TH2F>("h_pvmosttracksshared", ";index of pv most-shared to sv #0; index of pv most-shared to sv #1", 71, -1, 70, 71, -1, 70);

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

// JMTBAD ugh
void MFVVertexHistos::fill_multi(TH1F** hs, const int isv, const double val, const double weight) const {
  if (isv < sv_all)
    hs[isv]->Fill(val, weight);
  hs[sv_all]->Fill(val, weight);
}

void MFVVertexHistos::fill_multi(TH2F** hs, const int isv, const double val, const double val2, const double weight) const {
  if (isv < sv_all)
    hs[isv]->Fill(val, val2, weight);
  hs[sv_all]->Fill(val, val2, weight);
}

void MFVVertexHistos::fill_multi(PairwiseHistos* hs, const int isv, const PairwiseHistos::ValueMap& val, const double weight) const {
  if (isv < sv_all)
    hs[isv].Fill(val, -1, weight);
  hs[sv_all].Fill(val, -1, weight);
}

void MFVVertexHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mfv_event_src, mevent);

  edm::Handle<double> weight;
  event.getByLabel(weight_src, weight);
  const double w = *weight;
  h_w->Fill(w);

  const float bsx = mevent->bsx;
  const float bsy = mevent->bsy;
  const float bsz = mevent->bsz;
  const math::XYZPoint bs(bsx, bsy, bsz);
  const math::XYZPoint pv(mevent->pvx, mevent->pvy, mevent->pvz);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByLabel(vertex_aux_src, auxes);

  edm::Handle<reco::VertexCollection> primary_vertices;
  edm::Handle<reco::VertexCollection> vertices;
  edm::Handle<mfv::JetVertexAssociation> vertices_to_jets;
  edm::ESHandle<TransientTrackBuilder> tt_builder;
  TrackerSpaceExtents tracker_extents;
  
  if (vertex_src.label() != "") { 
    event.getByLabel("offlinePrimaryVertices", primary_vertices);
    event.getByLabel(vertex_src, vertices);
    setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);
    tracker_extents.fill(setup, GlobalPoint(bsx, bsy, bsz));
    if (vertex_to_jets_src.label() != "")
      event.getByLabel(vertex_to_jets_src, vertices_to_jets);
  }

  const int nsv = int(auxes->size());

  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);

    if (isv < 2) {
      h_sv_pos_1d[isv][0]->Fill(aux.x - bsx, w);
      h_sv_pos_1d[isv][1]->Fill(aux.y - bsy, w);
      h_sv_pos_1d[isv][2]->Fill(aux.z - bsz, w);
      h_sv_pos_2d[isv][0]->Fill(aux.x - bsx, aux.y - bsy, w);
      h_sv_pos_2d[isv][1]->Fill(aux.x - bsx, aux.z - bsz, w);
      h_sv_pos_2d[isv][2]->Fill(aux.y - bsy, aux.z - bsz, w);
      h_sv_pos_rz[isv]->Fill(aux.bs2ddist * (aux.y - bsy >= 0 ? 1 : -1), aux.z - bsz, w);
      const double pos_phi = atan2(aux.y - bsy, aux.x - bsx);
      h_sv_pos_phi[isv]->Fill(pos_phi, w);
      h_sv_pos_phi_2pi[isv]->Fill(pos_phi >= 0 ? pos_phi : pos_phi + 6.2832, w);
    }

    PairwiseHistos::ValueMap v = {
        {"mva",                     mva.value(aux)},
        {"nlep",                    aux.which_lep.size()},
        {"ntracks",                 aux.ntracks()},
        {"nbadtracks",              aux.nbadtracks()},
        {"ntracksptgt3",            aux.ntracksptgt(3)},
        {"ntracksptgt5",            aux.ntracksptgt(5)},
        {"ntracksptgt10",           aux.ntracksptgt(10)},
        {"trackminnhits",           aux.trackminnhits()},
        {"trackmaxnhits",           aux.trackmaxnhits()},
        {"njetsntks",               aux.njets[mfv::JByNtracks]},
        {"chi2dof",                 aux.chi2/aux.ndof},
        {"chi2dofprob",             TMath::Prob(aux.chi2, aux.ndof)},

        {"msptm",                   sqrt(aux.mass[mfv::PTracksOnly] * aux.mass[mfv::PTracksOnly] + aux.pt[mfv::PTracksOnly] * aux.pt[mfv::PTracksOnly]) + fabs(aux.pt[mfv::PTracksOnly])},

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

        {"tksjetsntkp",             aux.p4(mfv::PTracksPlusJetsByNtracks).P()},
        {"tksjetsntkpt",            aux.pt[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntketa",           aux.eta[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkrapidity",      aux.p4(mfv::PTracksPlusJetsByNtracks).Rapidity()},
        {"tksjetsntkphi",           aux.phi[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkmass",          aux.mass[mfv::PTracksPlusJetsByNtracks]},

        {"costhtkonlymombs",         aux.costhmombs  [mfv::PTracksOnly]},
        {"costhtkonlymompv2d",       aux.costhmompv2d[mfv::PTracksOnly]},
        {"costhtkonlymompv3d",       aux.costhmompv3d[mfv::PTracksOnly]},

        {"costhjetsntkmombs",        aux.costhmombs  [mfv::PJetsByNtracks]},
        {"costhjetsntkmompv2d",      aux.costhmompv2d[mfv::PJetsByNtracks]},
        {"costhjetsntkmompv3d",      aux.costhmompv3d[mfv::PJetsByNtracks]},

        {"costhtksjetsntkmombs",     aux.costhmombs  [mfv::PTracksPlusJetsByNtracks]},
        {"costhtksjetsntkmompv2d",   aux.costhmompv2d[mfv::PTracksPlusJetsByNtracks]},
        {"costhtksjetsntkmompv3d",   aux.costhmompv3d[mfv::PTracksPlusJetsByNtracks]},

        {"missdisttkonlypv",        aux.missdistpv   [mfv::PTracksOnly]},
        {"missdisttkonlypverr",     aux.missdistpverr[mfv::PTracksOnly]},
        {"missdisttkonlypvsig",     aux.missdistpvsig(mfv::PTracksOnly)},

        {"missdistjetsntkpv",        aux.missdistpv   [mfv::PJetsByNtracks]},
        {"missdistjetsntkpverr",     aux.missdistpverr[mfv::PJetsByNtracks]},
        {"missdistjetsntkpvsig",     aux.missdistpvsig(mfv::PJetsByNtracks)},

        {"missdisttksjetsntkpv",        aux.missdistpv   [mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpverr",     aux.missdistpverr[mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpvsig",     aux.missdistpvsig(mfv::PTracksPlusJetsByNtracks)},

        {"sumpt2",                  aux.sumpt2()},
        {"sumnhitsbehind",          aux.sumnhitsbehind()},
        {"maxnhitsbehind",          aux.maxnhitsbehind()},

        {"ntrackssharedwpv", aux.ntrackssharedwpv()},
        {"ntrackssharedwpvs", aux.ntrackssharedwpvs()},
        {"fractrackssharedwpv", float(aux.ntrackssharedwpv()) / aux.ntracks()},
        {"fractrackssharedwpvs", float(aux.ntrackssharedwpvs()) / aux.ntracks()},
        {"npvswtracksshared", aux.npvswtracksshared()},

        {"mintrackpt",              aux.mintrackpt()},
        {"maxtrackpt",              aux.maxtrackpt()},
        {"maxm1trackpt",            aux.maxmntrackpt(1)},
        {"maxm2trackpt",            aux.maxmntrackpt(2)},

        {"trackptavg", aux.trackptavg()},
        {"trackptrms", aux.trackptrms()},

        {"trackdxymin", aux.trackdxymin()},
        {"trackdxymax", aux.trackdxymax()},
        {"trackdxyavg", aux.trackdxyavg()},
        {"trackdxyrms", aux.trackdxyrms()},

        {"trackdzmin", aux.trackdzmin()},
        {"trackdzmax", aux.trackdzmax()},
        {"trackdzavg", aux.trackdzavg()},
        {"trackdzrms", aux.trackdzrms()},

        {"trackpterrmin", aux.trackpterrmin()},
        {"trackpterrmax", aux.trackpterrmax()},
        {"trackpterravg", aux.trackpterravg()},
        {"trackpterrrms", aux.trackpterrrms()},

        {"trackdxyerrmin", aux.trackdxyerrmin()},
        {"trackdxyerrmax", aux.trackdxyerrmax()},
        {"trackdxyerravg", aux.trackdxyerravg()},
        {"trackdxyerrrms", aux.trackdxyerrrms()},

        {"trackdzerrmin", aux.trackdzerrmin()},
        {"trackdzerrmax", aux.trackdzerrmax()},
        {"trackdzerravg", aux.trackdzerravg()},
        {"trackdzerrrms", aux.trackdzerrrms()},

        {"trackpairmassmin", aux.trackpairmassmin()},
        {"trackpairmassmax", aux.trackpairmassmax()},
        {"trackpairmassavg", aux.trackpairmassavg()},
        {"trackpairmassrms", aux.trackpairmassrms()},

        {"tracktripmassmin", aux.tracktripmassmin()},
        {"tracktripmassmax", aux.tracktripmassmax()},
        {"tracktripmassavg", aux.tracktripmassavg()},
        {"tracktripmassrms", aux.tracktripmassrms()},

        {"trackquadmassmin", aux.trackquadmassmin()},
        {"trackquadmassmax", aux.trackquadmassmax()},
        {"trackquadmassavg", aux.trackquadmassavg()},
        {"trackquadmassrms", aux.trackquadmassrms()},

        {"trackpairdetamin", aux.trackpairdetamin()},
        {"trackpairdetamax", aux.trackpairdetamax()},
        {"trackpairdetaavg", aux.trackpairdetaavg()},
        {"trackpairdetarms", aux.trackpairdetarms()},

        {"drmin",  aux.drmin()},
        {"drmax",  aux.drmax()},
        {"dravg",  aux.dravg()},
        {"drrms",  aux.drrms()},

        {"jetpairdetamin", aux.jetpairdetamin},
        {"jetpairdetamax", aux.jetpairdetamax},
        {"jetpairdetaavg", aux.jetpairdetaavg},
        {"jetpairdetarms", aux.jetpairdetarms},

        {"jetpairdrmin", aux.jetpairdrmin},
        {"jetpairdrmax", aux.jetpairdrmax},
        {"jetpairdravg", aux.jetpairdravg},
        {"jetpairdrrms", aux.jetpairdrrms},

        {"costhtkmomvtxdispmin", aux.costhtkmomvtxdispmin},
        {"costhtkmomvtxdispmax", aux.costhtkmomvtxdispmax},
        {"costhtkmomvtxdispavg", aux.costhtkmomvtxdispavg},
        {"costhtkmomvtxdisprms", aux.costhtkmomvtxdisprms},

        {"costhjetmomvtxdispmin", aux.costhjetmomvtxdispmin},
        {"costhjetmomvtxdispmax", aux.costhjetmomvtxdispmax},
        {"costhjetmomvtxdispavg", aux.costhjetmomvtxdispavg},
        {"costhjetmomvtxdisprms", aux.costhjetmomvtxdisprms},

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
        {"pvdz",                    aux.pvdz()},
        {"pvdzerr",                 aux.pvdzerr()},
        {"pvdzsig",                 aux.pvdzsig()}
    };

    std::vector<float> trackpairdphis = aux.trackpairdphis();
    int npairs = trackpairdphis.size();
    for (int i = 0; i < npairs; ++i) {
      trackpairdphis[i] = fabs(trackpairdphis[i]);
    }
    std::sort(trackpairdphis.begin(), trackpairdphis.end());
    v["trackpairdphimax"] = 0 > npairs - 1 ? -1 : trackpairdphis[npairs-1-0];
    v["trackpairdphimaxm1"] = 1 > npairs - 1 ? -1 : trackpairdphis[npairs-1-1];
    v["trackpairdphimaxm2"] = 2 > npairs - 1 ? -1 : trackpairdphis[npairs-1-2];

    if (vertex_src.label() != "") {
      const reco::Vertex& thepv = primary_vertices->at(0);

      const reco::Vertex& rv = vertices->at(aux.which);
      const reco::VertexRef rvref(vertices, aux.which);
      std::vector<reco::TrackBase> tracks;
      for (auto it = rv.tracks_begin(), ite = rv.tracks_end(); it != ite; ++it) {
        const reco::TrackBaseRef& tk = *it;
        tracks.push_back(*tk);
      }
      std::sort(tracks.begin(), tracks.end(), [](const reco::TrackBase& tk1, const reco::TrackBase& tk2) { return tk1.pt() > tk2.pt(); });

      int ntracksdrlt0p50 = 0;
      int ntracksdr0p50to1p57 = 0;
      int ntracksdrgt1p57 = 0;
      TVector3 tracksdrlt1p57 = aux.p4(mfv::PTracksOnly).Vect();
      for (int itk = 0, itke = int(tracks.size()); itk < itke; ++itk) {
        const reco::TransientTrack& ttk = tt_builder->build((const reco::Track*)(&tracks[itk]));
        auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, thepv);
        auto dxy_isv = IPTools::absoluteTransverseImpactParameter(ttk, rv);
        auto d3d_ipv = IPTools::absoluteImpactParameter3D(ttk, thepv);
        auto d3d_isv = IPTools::absoluteImpactParameter3D(ttk, rv);

        NumExtents se = tracker_extents.numExtentInRAndZ(tracks[itk].hitPattern());
        double trackjetdr = reco::deltaR(aux.eta[mfv::PJetsByNtracks], aux.phi[mfv::PJetsByNtracks], tracks[itk].eta(), tracks[itk].phi());
        if (trackjetdr < 0.5) {
          ntracksdrlt0p50++;
        } else if (trackjetdr < 1.57) {
          ntracksdr0p50to1p57++;
        } else {
          ntracksdrgt1p57++;
          tracksdrlt1p57 -= TVector3(tracks[itk].px(), tracks[itk].py(), tracks[itk].pz());
        }

        double absdz = 100000;
        for (int i = 1; i < int(primary_vertices->size()); ++i) {
          const reco::Vertex& pvi = primary_vertices->at(i);
          const math::XYZPoint pvi_xyz(pvi.x(), pvi.y(), pvi.z());
            if (fabs(tracks[itk].dz(pvi_xyz)) < absdz) {
              absdz = fabs(tracks[itk].dz(pvi_xyz));
            }
        }
        double absdz0 = fabs(tracks[itk].dz(pv));
        double absdz1 = absdz0 < absdz ? absdz0 : absdz;
        double absdz2 = absdz;

        if (itk < max_ntracks) {
          v[TString::Format("track%i_pt",        itk).Data()] = tracks[itk].pt();
          v[TString::Format("track%i_eta",       itk).Data()] = tracks[itk].eta();
          v[TString::Format("track%i_phi",       itk).Data()] = tracks[itk].phi();
          v[TString::Format("track%i_charge",    itk).Data()] = tracks[itk].charge();
          v[TString::Format("track%i_dxybs",     itk).Data()] = tracks[itk].dxy(bs);
          v[TString::Format("track%i_dzbs",      itk).Data()] = tracks[itk].dz(bs);
          v[TString::Format("track%i_dxypv",     itk).Data()] = tracks[itk].dxy(pv);
          v[TString::Format("track%i_dzpv",      itk).Data()] = tracks[itk].dz(pv);
          v[TString::Format("track%i_dxyerr",    itk).Data()] = tracks[itk].dxyError();
          v[TString::Format("track%i_dzerr",     itk).Data()] = tracks[itk].dzError();
          v[TString::Format("track%i_dxyipv1",   itk).Data()] = dxy_ipv.first;
          v[TString::Format("track%i_dxyipv",    itk).Data()] = dxy_ipv.second.value();
          v[TString::Format("track%i_dxyipverr", itk).Data()] = dxy_ipv.second.error();
          v[TString::Format("track%i_d3dipv1",   itk).Data()] = d3d_ipv.first;
          v[TString::Format("track%i_d3dipv",    itk).Data()] = d3d_ipv.second.value();
          v[TString::Format("track%i_d3dipverr", itk).Data()] = d3d_ipv.second.error();
          v[TString::Format("track%i_dxyisv1",   itk).Data()] = dxy_isv.first;
          v[TString::Format("track%i_dxyisv",    itk).Data()] = dxy_isv.second.value();
          v[TString::Format("track%i_dxyisverr", itk).Data()] = dxy_isv.second.error();
          v[TString::Format("track%i_d3disv1",   itk).Data()] = d3d_isv.first;
          v[TString::Format("track%i_d3disv",    itk).Data()] = d3d_isv.second.value();
          v[TString::Format("track%i_d3disverr", itk).Data()] = d3d_isv.second.error();
          v[TString::Format("track%i_chi2dof",   itk).Data()] = tracks[itk].chi2() / tracks[itk].ndof();
          v[TString::Format("track%i_nhits",     itk).Data()] = tracks[itk].hitPattern().numberOfValidPixelHits() + tracks[itk].hitPattern().numberOfValidStripHits();
          v[TString::Format("track%i_npixel",    itk).Data()] = tracks[itk].hitPattern().numberOfValidPixelHits();
          v[TString::Format("track%i_nstrip",    itk).Data()] = tracks[itk].hitPattern().numberOfValidStripHits();
          v[TString::Format("track%i_minr",      itk).Data()] = se.min_r;
          v[TString::Format("track%i_minz",      itk).Data()] = se.min_z;
          v[TString::Format("track%i_maxr",      itk).Data()] = se.max_r;
          v[TString::Format("track%i_maxz",      itk).Data()] = se.max_z;
          v[TString::Format("track%i_jetdr",     itk).Data()] = reco::deltaR(aux.eta[mfv::PJetsByNtracks], aux.phi[mfv::PJetsByNtracks], tracks[itk].eta(), tracks[itk].phi());
          v[TString::Format("track%i_jetdphi",   itk).Data()] = reco::deltaPhi(aux.phi[mfv::PJetsByNtracks], tracks[itk].phi());
          v[TString::Format("track%i_dzpv0",     itk).Data()] = absdz0;
          v[TString::Format("track%i_dzpv1",     itk).Data()] = absdz1;
          v[TString::Format("track%i_dzpv2",     itk).Data()] = absdz2;
          v[TString::Format("track%i_algo",      itk).Data()] = tracks[itk].algo();
        }

        for (int i = 0; i < sv_tracks_num_indices; ++i) {
          if (i == 1 && trackjetdr >= 0.5) continue;
          if (i == 2 && (trackjetdr < 1.57 || tracks[itk].dxyError() < 0.02)) continue;
          fill_multi(h_sv_tracks_pt[0][i],        isv, tracks[itk].pt(), w);
          fill_multi(h_sv_tracks_eta[0][i],       isv, tracks[itk].eta(), w);
          fill_multi(h_sv_tracks_phi[0][i],       isv, tracks[itk].phi(), w);
          fill_multi(h_sv_tracks_charge[0][i],    isv, tracks[itk].charge(), w);
          fill_multi(h_sv_tracks_dxybs[0][i],     isv, tracks[itk].dxy(bs), w);
          fill_multi(h_sv_tracks_dzbs[0][i],      isv, tracks[itk].dz(bs), w);
          fill_multi(h_sv_tracks_dxypv[0][i],     isv, tracks[itk].dxy(pv), w);
          fill_multi(h_sv_tracks_dzpv[0][i],      isv, tracks[itk].dz(pv), w);
          fill_multi(h_sv_tracks_dxyerr[0][i],    isv, tracks[itk].dxyError(), w);
          fill_multi(h_sv_tracks_dzerr[0][i],     isv, tracks[itk].dzError(), w);
          fill_multi(h_sv_tracks_dxyipv1[0][i],   isv, dxy_ipv.first, w);
          fill_multi(h_sv_tracks_dxyipv[0][i],    isv, dxy_ipv.second.value(), w);
          fill_multi(h_sv_tracks_dxyipverr[0][i], isv, dxy_ipv.second.error(), w);
          fill_multi(h_sv_tracks_d3dipv1[0][i],   isv, d3d_ipv.first, w);
          fill_multi(h_sv_tracks_d3dipv[0][i],    isv, d3d_ipv.second.value(), w);
          fill_multi(h_sv_tracks_d3dipverr[0][i], isv, d3d_ipv.second.error(), w);
          fill_multi(h_sv_tracks_dxyisv1[0][i],   isv, dxy_isv.first, w);
          fill_multi(h_sv_tracks_dxyisv[0][i],    isv, dxy_isv.second.value(), w);
          fill_multi(h_sv_tracks_dxyisverr[0][i], isv, dxy_isv.second.error(), w);
          fill_multi(h_sv_tracks_d3disv1[0][i],   isv, d3d_isv.first, w);
          fill_multi(h_sv_tracks_d3disv[0][i],    isv, d3d_isv.second.value(), w);
          fill_multi(h_sv_tracks_d3disverr[0][i], isv, d3d_isv.second.error(), w);
          fill_multi(h_sv_tracks_chi2dof[0][i],   isv, tracks[itk].chi2() / tracks[itk].ndof(), w);
          fill_multi(h_sv_tracks_nhits[0][i],     isv, tracks[itk].hitPattern().numberOfValidPixelHits() + tracks[itk].hitPattern().numberOfValidStripHits(), w);
          fill_multi(h_sv_tracks_npixel[0][i],    isv, tracks[itk].hitPattern().numberOfValidPixelHits(), w);
          fill_multi(h_sv_tracks_nstrip[0][i],    isv, tracks[itk].hitPattern().numberOfValidStripHits(), w);
          fill_multi(h_sv_tracks_minr[0][i],      isv, se.min_r, w);
          fill_multi(h_sv_tracks_minz[0][i],      isv, se.min_z, w);
          fill_multi(h_sv_tracks_maxr[0][i],      isv, se.max_r, w);
          fill_multi(h_sv_tracks_maxz[0][i],      isv, se.max_z, w);
          fill_multi(h_sv_tracks_jetdr[0][i],     isv, trackjetdr, w);
          fill_multi(h_sv_tracks_jetdphi[0][i],   isv, reco::deltaPhi(aux.phi[mfv::PJetsByNtracks], tracks[itk].phi()), w);
          fill_multi(h_sv_tracks_bs2derr_jetdr[0][i], isv, trackjetdr, aux.bs2derr, w);
          fill_multi(h_sv_tracks_dzpv0[0][i],     isv, absdz0, w);
          fill_multi(h_sv_tracks_dzpv1[0][i],     isv, absdz1, w);
          fill_multi(h_sv_tracks_dzpv2[0][i],     isv, absdz2, w);
          fill_multi(h_sv_tracks_dzpv2_dzpv0[0][i], isv, absdz0, absdz2, w);
          fill_multi(h_sv_tracks_dzpv2sig_dzpv0sig[0][i], isv, absdz0 / tracks[itk].dzError(), absdz2 / tracks[itk].dzError(), w);
          if (tracks[itk].pt() > 1) {
            fill_multi(h_sv_tracksptgt1_npixel_eta[0][i], isv, tracks[itk].eta(), tracks[itk].hitPattern().numberOfValidPixelHits(), w);
            fill_multi(h_sv_tracksptgt1_npixel_phi[0][i], isv, tracks[itk].phi(), tracks[itk].hitPattern().numberOfValidPixelHits(), w);
            fill_multi(h_sv_tracksptgt1_nstrip_eta[0][i], isv, tracks[itk].eta(), tracks[itk].hitPattern().numberOfValidStripHits(), w);
            fill_multi(h_sv_tracksptgt1_nstrip_phi[0][i], isv, tracks[itk].phi(), tracks[itk].hitPattern().numberOfValidStripHits(), w);
          }
          if (tracks[itk].pt() > 3) {
            fill_multi(h_sv_tracksptgt3_npixel_eta[0][i], isv, tracks[itk].eta(), tracks[itk].hitPattern().numberOfValidPixelHits(), w);
            fill_multi(h_sv_tracksptgt3_npixel_phi[0][i], isv, tracks[itk].phi(), tracks[itk].hitPattern().numberOfValidPixelHits(), w);
            fill_multi(h_sv_tracksptgt3_nstrip_eta[0][i], isv, tracks[itk].eta(), tracks[itk].hitPattern().numberOfValidStripHits(), w);
            fill_multi(h_sv_tracksptgt3_nstrip_phi[0][i], isv, tracks[itk].phi(), tracks[itk].hitPattern().numberOfValidStripHits(), w);
          }
          fill_multi(h_sv_tracks_algo[0][i],      isv, tracks[itk].algo(), w);
          for (int j = 0; j < 7; ++j) {
            if (tracks[itk].quality(reco::Track::TrackQuality(j))) fill_multi(h_sv_tracks_quality[0][i], isv, j, w);
          }
        }
      }
      v["ntracksdrlt0p50"] = ntracksdrlt0p50;
      v["ntracksdr0p50to1p57"] = ntracksdr0p50to1p57;
      v["ntracksdrgt1p57"] = ntracksdrgt1p57;
      v["tracksdrlt1p57pt"] = tracksdrlt1p57.Pt();
      v["tracksdrlt1p57eta"] = tracksdrlt1p57.Eta();
      v["tracksdrlt1p57phi"] = tracksdrlt1p57.Phi();

      if (vertex_to_jets_src.label() != "") {
        int njets = vertices_to_jets->numberOfAssociations(rvref);
        assert(njets == aux.njets[0]); // JMTBAD

        if (njets > 0) {
          const edm::RefVector<pat::JetCollection>& jets = (*vertices_to_jets)[rvref];
          std::set<reco::TrackRef> vertex_tracks;

          for (auto it = rv.tracks_begin(), ite = rv.tracks_end(); it != ite; ++it)
            if (rv.trackWeight(*it) >= mfv::track_vertex_weight_min)
              vertex_tracks.insert(it->castTo<reco::TrackRef>());
     
          for (int ijet = 0; ijet < njets; ++ijet) {
            int njettk = 0, njettkinvtx = 0;
            for (const reco::PFCandidatePtr& pfcand : jets[ijet]->getPFConstituents()) {
              const reco::TrackRef& tk = pfcand->trackRef();
              if (tk.isNonnull()) {
                ++njettk;
                const bool tk_in_vtx = vertex_tracks.count(tk);
                if (tk_in_vtx)
                  ++njettkinvtx;
                const reco::TransientTrack& ttk = tt_builder->build((const reco::Track*)(&*tk));
                auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, thepv);
                auto dxy_isv = IPTools::absoluteTransverseImpactParameter(ttk, rv);
                auto d3d_ipv = IPTools::absoluteImpactParameter3D(ttk, thepv);
                auto d3d_isv = IPTools::absoluteImpactParameter3D(ttk, rv);
                NumExtents se = tracker_extents.numExtentInRAndZ(tk->hitPattern());

                for (int i = 0; i < sv_jet_tracks_num_indices; ++i) {
                  if ((i == sv_jet_tracks_jet && tk_in_vtx) ||
                      (i == sv_jet_tracks_vertex && !tk_in_vtx))
                    continue;

                  fill_multi(h_sv_tracks_pt[1][i],        isv, tk->pt(), w);
                  fill_multi(h_sv_tracks_eta[1][i],       isv, tk->eta(), w);
                  fill_multi(h_sv_tracks_phi[1][i],       isv, tk->phi(), w);
                  fill_multi(h_sv_tracks_charge[1][i],    isv, tk->charge(), w);
                  fill_multi(h_sv_tracks_dxybs[1][i],     isv, tk->dxy(bs), w);
                  fill_multi(h_sv_tracks_dzbs[1][i],      isv, tk->dz(bs), w);
                  fill_multi(h_sv_tracks_dxypv[1][i],     isv, tk->dxy(pv), w);
                  fill_multi(h_sv_tracks_dzpv[1][i],      isv, tk->dz(pv), w);
                  fill_multi(h_sv_tracks_dxyerr[1][i],    isv, tk->dxyError(), w);
                  fill_multi(h_sv_tracks_dzerr[1][i],     isv, tk->dzError(), w);
                  fill_multi(h_sv_tracks_dxyipv1[1][i],   isv, dxy_ipv.first, w);
                  fill_multi(h_sv_tracks_dxyipv[1][i],    isv, dxy_ipv.second.value(), w);
                  fill_multi(h_sv_tracks_dxyipverr[1][i], isv, dxy_ipv.second.error(), w);
                  fill_multi(h_sv_tracks_d3dipv1[1][i],   isv, d3d_ipv.first, w);
                  fill_multi(h_sv_tracks_d3dipv[1][i],    isv, d3d_ipv.second.value(), w);
                  fill_multi(h_sv_tracks_d3dipverr[1][i], isv, d3d_ipv.second.error(), w);
                  fill_multi(h_sv_tracks_dxyisv1[1][i],   isv, dxy_isv.first, w);
                  fill_multi(h_sv_tracks_dxyisv[1][i],    isv, dxy_isv.second.value(), w);
                  fill_multi(h_sv_tracks_dxyisverr[1][i], isv, dxy_isv.second.error(), w);
                  fill_multi(h_sv_tracks_d3disv1[1][i],   isv, d3d_isv.first, w);
                  fill_multi(h_sv_tracks_d3disv[1][i],    isv, d3d_isv.second.value(), w);
                  fill_multi(h_sv_tracks_d3disverr[1][i], isv, d3d_isv.second.error(), w);
                  fill_multi(h_sv_tracks_chi2dof[1][i],   isv, tk->chi2() / tk->ndof(), w);
                  fill_multi(h_sv_tracks_nhits[1][i],     isv, tk->hitPattern().numberOfValidPixelHits() + tk->hitPattern().numberOfValidStripHits(), w);
                  fill_multi(h_sv_tracks_npixel[1][i],    isv, tk->hitPattern().numberOfValidPixelHits(), w);
                  fill_multi(h_sv_tracks_nstrip[1][i],    isv, tk->hitPattern().numberOfValidStripHits(), w);
                  fill_multi(h_sv_tracks_minr[1][i],      isv, se.min_r, w);
                  fill_multi(h_sv_tracks_minz[1][i],      isv, se.min_z, w);
                  fill_multi(h_sv_tracks_maxr[1][i],      isv, se.max_r, w);
                  fill_multi(h_sv_tracks_maxz[1][i],      isv, se.max_z, w);
                }
              }
            }

            fill_multi(h_sv_jets_ntracks,      isv, njettk,                                                        w);
            fill_multi(h_sv_jets_ntracksinvtx, isv, njettkinvtx,                                                   w);
            fill_multi(h_sv_jets_energy,       isv, jets[ijet]->energy(),                                          w);
            fill_multi(h_sv_jets_pt,           isv, jets[ijet]->pt(),                                              w);
            fill_multi(h_sv_jets_eta,          isv, jets[ijet]->eta(),                                             w);
            fill_multi(h_sv_jets_phi,          isv, jets[ijet]->phi(),                                             w);
            fill_multi(h_sv_jets_mass,         isv, jets[ijet]->mass(),                                            w);
            fill_multi(h_sv_jets_bdisc,        isv, jets[ijet]->bDiscriminator("combinedSecondaryVertexBJetTags"), w);
            fill_multi(h_sv_jets_numDaughters, isv, jets[ijet]->numberOfDaughters(), w);
            fill_multi(h_sv_jets_neutralHadEnFrac, isv, jets[ijet]->neutralHadronEnergyFraction(), w);
            fill_multi(h_sv_jets_neutralEmEnFrac, isv, jets[ijet]->neutralEmEnergyFraction(), w);
            fill_multi(h_sv_jets_chargedHadEnFrac, isv, jets[ijet]->chargedHadronEnergyFraction(), w);
            fill_multi(h_sv_jets_chargedEmEnFrac, isv, jets[ijet]->chargedEmEnergyFraction(), w);
            fill_multi(h_sv_jets_chargedMult, isv, jets[ijet]->chargedMultiplicity(), w);
            fill_multi(h_sv_jets_n60, isv, jets[ijet]->n60(), w);
            fill_multi(h_sv_jets_n90, isv, jets[ijet]->n90(), w);
            fill_multi(h_sv_jets_area, isv, jets[ijet]->jetArea(), w);
            fill_multi(h_sv_jets_maxDist, isv, jets[ijet]->maxDistance(), w);
          }
        }
      }
    }

    fill_multi(h_sv, isv, v, w);

    h_sv_sumtop2.Fill(v, isv, w);
  }

  //////////////////////////////////////////////////////////////////////

  h_nsv->Fill(nsv, w);
  h_nsv_v_minlspdist2d->Fill(mevent->minlspdist2d(), nsv, w);
  h_nsv_v_lspdist2d->Fill(mevent->lspdist2d(), nsv, w);
  h_nsv_v_lspdist3d->Fill(mevent->lspdist3d(), nsv, w);

  if (nsv >= 2) {
    const MFVVertexAux& sv0 = auxes->at(0);
    const MFVVertexAux& sv1 = auxes->at(1);
    double svdist2d = mag(sv0.x - sv1.x, sv0.y - sv1.y);
    double svdist3d = mag(sv0.x - sv1.x, sv0.y - sv1.y, sv0.z - sv1.z);
    h_svdist2d->Fill(svdist2d, w);
    h_svdist3d->Fill(svdist3d, w);
    h_svdist2d_v_lspdist2d->Fill(mevent->lspdist2d(), svdist2d, w);
    h_svdist3d_v_lspdist3d->Fill(mevent->lspdist3d(), svdist3d, w);
    h_svdist2d_v_minlspdist2d->Fill(mevent->minlspdist2d(), svdist2d, w);
    h_sv0pvdz_v_sv1pvdz->Fill(sv0.pvdz(), sv1.pvdz(), w);
    h_sv0pvdzsig_v_sv1pvdzsig->Fill(sv0.pvdzsig(), sv1.pvdzsig(), w);
    double phi0 = atan2(sv0.y - mevent->bsy, sv0.x - mevent->bsx);
    double phi1 = atan2(sv1.y - mevent->bsy, sv1.x - mevent->bsx);
    h_absdeltaphi01->Fill(fabs(reco::deltaPhi(phi0, phi1)), w);

    h_fractrackssharedwpv01 ->Fill(float(sv0.ntrackssharedwpv () + sv1.ntrackssharedwpv ())/(sv0.ntracks() + sv1.ntracks()), w);
    h_fractrackssharedwpvs01->Fill(float(sv0.ntrackssharedwpvs() + sv1.ntrackssharedwpvs())/(sv0.ntracks() + sv1.ntracks()), w);
    h_pvmosttracksshared->Fill(sv0.ntrackssharedwpvs() ? sv0.pvmosttracksshared() : -1,
                               sv1.ntrackssharedwpvs() ? sv1.pvmosttracksshared() : -1,
                               w);
  }

  for (int ivtx = 0; ivtx < nsv; ++ivtx) {
    const MFVVertexAux& auxi = auxes->at(ivtx);
    const reco::Vertex vtxi = mfv::aux_to_reco(auxi);

    for (int jvtx = ivtx + 1; jvtx < nsv; ++jvtx) {
      const MFVVertexAux& auxj = auxes->at(jvtx);
      const reco::Vertex vtxj = mfv::aux_to_reco(auxj);

      Measurement1D pair2ddist = distcalc_2d.distance(vtxi, vtxj);
      Measurement1D pair3ddist = distcalc_3d.distance(vtxi, vtxj);

      std::pair<bool, float> pair2dcompat = mfv::compatibility(vtxi, vtxj, false);
      std::pair<bool, float> pair3dcompat = mfv::compatibility(vtxi, vtxj, true);

      h_pair2dcompatscss->Fill(pair2dcompat.first, w);
      h_pair2dcompat->Fill(pair2dcompat.second, w);
      h_pair2ddist->Fill(pair2ddist.value(), w);
      h_pair2derr->Fill(pair2ddist.error(), w);
      h_pair2dsig->Fill(pair2ddist.significance(), w);
      h_pair3dcompatscss->Fill(pair3dcompat.first, w);
      h_pair3dcompat->Fill(pair3dcompat.second, w);
      h_pair3ddist->Fill(pair3ddist.value(), w);
      h_pair3derr->Fill(pair3ddist.error(), w);
      h_pair3dsig->Fill(pair3ddist.significance(), w);
    }
  }
}

DEFINE_FWK_MODULE(MFVVertexHistos);
