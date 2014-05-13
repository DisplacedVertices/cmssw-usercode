#include "TH2F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

//#define USE_DUMPERS // you also have to add JMTucker/Dumpers to the BuildFile.xml for this
#ifdef USE_DUMPERS
#include "JMTucker/Dumpers/interface/Dumpers.h"
#endif

class TrackerMapper : public edm::EDAnalyzer {
 public:
  explicit TrackerMapper(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::InputTag track_src;

  TH1F* h_ntracks;

  TH1F* h_tracks_pt[2][3];
  TH1F* h_tracks_eta[2][3];
  TH1F* h_tracks_phi[2][3];
  TH1F* h_tracks_dxyerr[2][3];
  TH1F* h_tracks_dzerr[2][3];
  TH1F* h_tracks_npixel[2][3];
  TH1F* h_tracks_nstrip[2][3];

  TH2F* h_tracks_dxyerr_eta[2][3];
  TH2F* h_tracks_dxyerr_phi[2][3];
  TH2F* h_tracks_dzerr_eta[2][3];
  TH2F* h_tracks_dzerr_phi[2][3];

  TH2F* h_tracks_eta_phi_dxyerr_eq[2][3][11];
  TH2F* h_tracks_eta_phi_dxyerr_lt[2][3][11];
  TH2F* h_tracks_eta_phi_dzerr_eq[2][3][11];
  TH2F* h_tracks_eta_phi_dzerr_lt[2][3][11];

  TH2F* h_tracks_npixel_eta[2][3];
  TH2F* h_tracks_npixel_phi[2][3];
  TH2F* h_tracks_nstrip_eta[2][3];
  TH2F* h_tracks_nstrip_phi[2][3];

  TH2F* h_tracks_eta_phi_npixel_eq[2][3][6];
  TH2F* h_tracks_eta_phi_npixel_gt[2][3][6];
  TH2F* h_tracks_eta_phi_nstrip_eq[2][3][9];
  TH2F* h_tracks_eta_phi_nstrip_gt[2][3][9];

  TH2F* h_tracks_npixel_phi_eta_eq[2][3][8];
  TH2F* h_tracks_nstrip_phi_eta_eq[2][3][8];

  TH1F* h_n_weird_tracks;
  TH1F* h_weird_track_pars[5];
  TH1F* h_weird_track_errs[5];
  TH2F* h_weird_track_pars_v_pars[5][4];
  TH2F* h_weird_track_errs_v_pars[5][5];
  TH1F* h_weird_track_q;
  TH1F* h_weird_track_nhits;
  TH1F* h_weird_track_npxhits;
  TH1F* h_weird_track_nsthits;
  TH1F* h_weird_track_chi2;
  TH1F* h_weird_track_dof;
  TH1F* h_weird_track_chi2dof;
  TH1F* h_weird_track_algo;
  TH1F* h_weird_track_quality;
  TH1F* h_weird_track_nloops;
};

TrackerMapper::TrackerMapper(const edm::ParameterSet& cfg)
  : track_src(cfg.getParameter<edm::InputTag>("track_src"))
{
  edm::Service<TFileService> fs;

  h_ntracks = fs->make<TH1F>("h_ntracks", ";number of tracks;events", 100, 0, 5000);

  const char* exi[2] = {"all", "v1"};
  const char* exj[3] = {"ptgt0", "ptgt1", "ptgt3"};
  for (int i = 0; i < 2; ++i) {
    for (int j = 0; j < 3; ++j) {
      h_tracks_pt[i][j] = fs->make<TH1F>(TString::Format("h_tracks_%s_%s_pt", exi[i], exj[j]), TString::Format("%s tracks%s;tracks pt;arb. units", exi[i], exj[j]), 150, 0, 150);
      h_tracks_phi[i][j] = fs->make<TH1F>(TString::Format("h_tracks_%s_%s_phi", exi[i], exj[j]), TString::Format("%s tracks%s;tracks phi;arb. units", exi[i], exj[j]), 50, -3.15, 3.15);
      h_tracks_eta[i][j] = fs->make<TH1F>(TString::Format("h_tracks_%s_%s_eta", exi[i], exj[j]), TString::Format("%s tracks%s;tracks eta;arb. units", exi[i], exj[j]), 50, -4, 4);
      h_tracks_dxyerr[i][j] = fs->make<TH1F>(TString::Format("h_tracks_%s_%s_dxyerr", exi[i], exj[j]), TString::Format("%s tracks%s;tracks dxyerr;arb. units", exi[i], exj[j]), 1000, 0, 2);
      h_tracks_dzerr[i][j] = fs->make<TH1F>(TString::Format("h_tracks_%s_%s_dzerr", exi[i], exj[j]), TString::Format("%s tracks%s;tracks dzerr;arb. units", exi[i], exj[j]), 1000, 0, 2);
      h_tracks_npixel[i][j] = fs->make<TH1F>(TString::Format("h_tracks_%s_%s_npixel", exi[i], exj[j]), TString::Format("%s tracks%s;tracks npixel;arb. units", exi[i], exj[j]), 40, 0, 40);
      h_tracks_nstrip[i][j] = fs->make<TH1F>(TString::Format("h_tracks_%s_%s_nstrip", exi[i], exj[j]), TString::Format("%s tracks%s;tracks nstrip;arb. units", exi[i], exj[j]), 40, 0, 40);

      h_tracks_dxyerr_eta[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_dxyerr_eta", exi[i], exj[j]), TString::Format("%s tracks%s;eta;dxyerr", exi[i], exj[j]), 50, -4.00, 4.00, 1000, 0, 2);
      h_tracks_dxyerr_phi[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_dxyerr_phi", exi[i], exj[j]), TString::Format("%s tracks%s;phi;dxyerr", exi[i], exj[j]), 50, -3.15, 3.15, 1000, 0, 2);
      h_tracks_dzerr_eta[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_dzerr_eta", exi[i], exj[j]), TString::Format("%s tracks%s;eta;dzerr", exi[i], exj[j]), 50, -4.00, 4.00, 1000, 0, 2);
      h_tracks_dzerr_phi[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_dzerr_phi", exi[i], exj[j]), TString::Format("%s tracks%s;phi;dzerr", exi[i], exj[j]), 50, -3.15, 3.15, 1000, 0, 2);

      for (int k = 0; k < 11; ++k) {
        h_tracks_eta_phi_dxyerr_eq[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_dxyerr_eq_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ %4.3f <= dxyerr < %4.3f;phi;eta", exi[i], exj[j], 0.005*k, 0.005*(k+1)), 50, -3.15, 3.15, 50, -4, 4);
      }
      for (int k = 0; k < 11; ++k) {
        h_tracks_eta_phi_dxyerr_lt[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_dxyerr_lt_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ dxyerr < %4.3f;phi;eta", exi[i], exj[j], 0.005*(k+1)), 50, -3.15, 3.15, 50, -4, 4);
      }
      for (int k = 0; k < 11; ++k) {
        h_tracks_eta_phi_dzerr_eq[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_dzerr_eq_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ %4.3f <= dzerr < %4.3f;phi;eta", exi[i], exj[j], 0.005*k, 0.005*(k+1)), 50, -3.15, 3.15, 50, -4, 4);
      }
      for (int k = 0; k < 11; ++k) {
        h_tracks_eta_phi_dzerr_lt[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_dzerr_lt_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ dzerr < %4.3f;phi;eta", exi[i], exj[j], 0.005*(k+1)), 50, -3.15, 3.15, 50, -4, 4);
      }

      h_tracks_npixel_eta[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_eta", exi[i], exj[j]), TString::Format("%s tracks%s;eta;number of pixel hits", exi[i], exj[j]), 50, -4.00, 4.00, 40, 0, 40);
      h_tracks_npixel_phi[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi", exi[i], exj[j]), TString::Format("%s tracks%s;phi;number of pixel hits", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_eta[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_eta", exi[i], exj[j]), TString::Format("%s tracks%s;eta;number of strip hits", exi[i], exj[j]), 50, -4.00, 4.00, 40, 0, 40);
      h_tracks_nstrip_phi[i][j] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi", exi[i], exj[j]), TString::Format("%s tracks%s;phi;number of strip hits", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);

      for (int k = 0; k < 6; ++k) {
        h_tracks_eta_phi_npixel_eq[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_npixel_eq_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ npixel = %d;phi;eta", exi[i], exj[j], k), 50, -3.15, 3.15, 50, -4, 4);
      }
      for (int k = 0; k < 6; ++k) {
        h_tracks_eta_phi_npixel_gt[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_npixel_gt_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ npixel >= %d;phi;eta", exi[i], exj[j], k), 50, -3.15, 3.15, 50, -4, 4);
      }
      for (int k = 0; k < 9; ++k) {
        h_tracks_eta_phi_nstrip_eq[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_nstrip_eq_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ nstrip = %d,%d;phi;eta", exi[i], exj[j], 2*k, 2*k+1), 50, -3.15, 3.15, 50, -4, 4);
      }
      for (int k = 0; k < 9; ++k) {
        h_tracks_eta_phi_nstrip_gt[i][j][k] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_eta_phi_nstrip_gt_%d", exi[i], exj[j], k), TString::Format("%s tracks%s w/ nstrip >= %d;phi;eta", exi[i], exj[j], 2*k), 50, -3.15, 3.15, 50, -4, 4);
      }

      h_tracks_npixel_phi_eta_eq[i][j][0] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_0", exi[i], exj[j]), TString::Format("%s tracks%s w/ eta < -2.5;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_npixel_phi_eta_eq[i][j][1] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_1", exi[i], exj[j]), TString::Format("%s tracks%s w/ -2.5 <= eta < -1.5;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_npixel_phi_eta_eq[i][j][2] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_2", exi[i], exj[j]), TString::Format("%s tracks%s w/ -1.5 <= eta < -0.9;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_npixel_phi_eta_eq[i][j][3] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_3", exi[i], exj[j]), TString::Format("%s tracks%s w/ -0.9 <= eta < 0.0;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_npixel_phi_eta_eq[i][j][4] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_4", exi[i], exj[j]), TString::Format("%s tracks%s w/ 0.0 <= eta < 0.9;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_npixel_phi_eta_eq[i][j][5] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_5", exi[i], exj[j]), TString::Format("%s tracks%s w/ 0.9 <= eta < 1.5;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_npixel_phi_eta_eq[i][j][6] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_6", exi[i], exj[j]), TString::Format("%s tracks%s w/ 1.5 <= eta < 2.5;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_npixel_phi_eta_eq[i][j][7] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_npixel_phi_eta_eq_7", exi[i], exj[j]), TString::Format("%s tracks%s w/ eta >= 2.5;phi;npixel", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);

      h_tracks_nstrip_phi_eta_eq[i][j][0] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_0", exi[i], exj[j]), TString::Format("%s tracks%s w/ eta < -2.5;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_phi_eta_eq[i][j][1] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_1", exi[i], exj[j]), TString::Format("%s tracks%s w/ -2.5 <= eta < -1.5;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_phi_eta_eq[i][j][2] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_2", exi[i], exj[j]), TString::Format("%s tracks%s w/ -1.5 <= eta < -0.9;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_phi_eta_eq[i][j][3] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_3", exi[i], exj[j]), TString::Format("%s tracks%s w/ -0.9 <= eta < 0.0;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_phi_eta_eq[i][j][4] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_4", exi[i], exj[j]), TString::Format("%s tracks%s w/ 0.0 <= eta < 0.9;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_phi_eta_eq[i][j][5] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_5", exi[i], exj[j]), TString::Format("%s tracks%s w/ 0.9 <= eta < 1.5;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_phi_eta_eq[i][j][6] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_6", exi[i], exj[j]), TString::Format("%s tracks%s w/ 1.5 <= eta < 2.5;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
      h_tracks_nstrip_phi_eta_eq[i][j][7] = fs->make<TH2F>(TString::Format("h_tracks_%s_%s_nstrip_phi_eta_eq_7", exi[i], exj[j]), TString::Format("%s tracks%s w/ eta >= 2.5;phi;nstrip", exi[i], exj[j]), 50, -3.15, 3.15, 40, 0, 40);
    }
  }

  h_n_weird_tracks = fs->make<TH1F>("h_n_weird_tracks", "", 200, 0, 200);
  const char* par_names[5] = {"pt", "eta", "phi", "dxy", "dz"};
  const int par_nbins[5] = { 500,  100,    100,  400, 400 };
  const double par_lo[5] = {   0, -2.6, -2.772,   -2, -20 };
  const double par_hi[5] = { 100, -2.4, -2.646,    2,  20 };
  const int err_nbins[5] = { 100, 100, 100, 200, 200 };
  const double err_lo[5] = { 0 };
  const double err_hi[5] = {   5, 0.1, 0.1, 0.5, 2 };
  for (int i = 0; i < 5; ++i)
    h_weird_track_pars[i] = fs->make<TH1F>(TString::Format("h_weird_track_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
  for (int i = 0; i < 5; ++i)
    h_weird_track_errs[i] = fs->make<TH1F>(TString::Format("h_weird_track_err%s", par_names[i]), "", err_nbins[i], err_lo[i], err_hi[i]);
  for (int i = 0; i < 5; ++i)
    for (int j = i+1; j < 5; ++j)
      h_weird_track_pars_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_weird_track_%s_v_%s", par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[j], par_lo[j], par_hi[j]);
  for (int i = 0; i < 5; ++i)
    for (int j = 0; j < 5; ++j)
      h_weird_track_errs_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_weird_track_err%s_v_%s", par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], err_nbins[j], err_lo[j], err_hi[j]);
  h_weird_track_q = fs->make<TH1F>("h_weird_track_q", "", 3, -1, 2);
  h_weird_track_nhits   = fs->make<TH1F>("h_weird_track_nhits",   "",  40, 0, 40);
  h_weird_track_npxhits = fs->make<TH1F>("h_weird_track_npxhits", "",  12, 0, 12);
  h_weird_track_nsthits = fs->make<TH1F>("h_weird_track_nsthits", "",  28, 0, 28);
  h_weird_track_chi2 = fs->make<TH1F>("h_weird_track_chi2", "", 50, 0, 100);
  h_weird_track_dof = fs->make<TH1F>("h_weird_track_dof", "", 50, 0, 100);
  h_weird_track_chi2dof = fs->make<TH1F>("h_weird_track_chi2dof", "", 50, 0, 10);
  h_weird_track_algo = fs->make<TH1F>("h_weird_track_algo", "", 30, 0, 30);
  h_weird_track_quality = fs->make<TH1F>("h_weird_track_quality", "", 7, 0, 7);
  h_weird_track_nloops = fs->make<TH1F>("h_weird_track_nloops", "", 10, 0, 10);
}

void TrackerMapper::analyze(const edm::Event& event, const edm::EventSetup& setup) {
#ifdef USE_DUMPERS
  bool dumpers_evented = false;
#endif

  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(track_src, tracks);

  h_ntracks->Fill(int(tracks->size()));

  int n_weird = 0;

  for (const reco::Track& tk : *tracks) {
    const bool v1 = tk.vx()*tk.vx() + tk.vy()*tk.vy() + tk.vz()*tk.vz() < 1;

    for (int i = 0; i < 2; ++i) {
      if (i == 1 && !v1) continue;

      for (int j = 0; j < 3; ++j) {
        if (j == 1 && tk.pt() <= 1) continue;
        if (j == 2 && tk.pt() <= 3) continue;

        h_tracks_pt[i][j]->Fill(tk.pt());
        h_tracks_eta[i][j]->Fill(tk.eta());
        h_tracks_phi[i][j]->Fill(tk.phi());
        h_tracks_dxyerr[i][j]->Fill(tk.dxyError());
        h_tracks_dzerr[i][j]->Fill(tk.dzError());
        h_tracks_npixel[i][j]->Fill(tk.hitPattern().numberOfValidPixelHits());
        h_tracks_nstrip[i][j]->Fill(tk.hitPattern().numberOfValidStripHits());

        h_tracks_dxyerr_eta[i][j]->Fill(tk.eta(), tk.dxyError());
        h_tracks_dxyerr_phi[i][j]->Fill(tk.phi(), tk.dxyError());
        h_tracks_dzerr_eta[i][j]->Fill(tk.eta(), tk.dzError());
        h_tracks_dzerr_phi[i][j]->Fill(tk.phi(), tk.dzError());

        for (int k = 0; k < 11; ++k) {
          if ((tk.dxyError() >= 0.005*k && tk.dxyError() < 0.005*(k+1)) || (tk.dxyError() >= 0.05 && k==10)) h_tracks_eta_phi_dxyerr_eq[i][j][k]->Fill(tk.phi(), tk.eta());
          if (tk.dxyError() < 0.005*(k+1) || k==10) h_tracks_eta_phi_dxyerr_lt[i][j][k]->Fill(tk.phi(), tk.eta());
        }
        for (int k = 0; k < 11; ++k) {
          if ((tk.dzError() >= 0.005*k && tk.dzError() < 0.005*(k+1)) || (tk.dzError() >= 0.05 && k==10)) h_tracks_eta_phi_dzerr_eq[i][j][k]->Fill(tk.phi(), tk.eta());
          if (tk.dzError() < 0.005*(k+1) || k==10) h_tracks_eta_phi_dzerr_lt[i][j][k]->Fill(tk.phi(), tk.eta());
        }

        h_tracks_npixel_eta[i][j]->Fill(tk.eta(), tk.hitPattern().numberOfValidPixelHits());
        h_tracks_npixel_phi[i][j]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
        h_tracks_nstrip_eta[i][j]->Fill(tk.eta(), tk.hitPattern().numberOfValidStripHits());
        h_tracks_nstrip_phi[i][j]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());

        for (int k = 0; k < 6; ++k) {
          if (tk.hitPattern().numberOfValidPixelHits() == k) h_tracks_eta_phi_npixel_eq[i][j][k]->Fill(tk.phi(), tk.eta());
          if (tk.hitPattern().numberOfValidPixelHits() >= k) h_tracks_eta_phi_npixel_gt[i][j][k]->Fill(tk.phi(), tk.eta());
        }
        for (int k = 0; k < 9; ++k) {
          if (tk.hitPattern().numberOfValidStripHits() == 2*k || tk.hitPattern().numberOfValidStripHits() == 2*k+1) h_tracks_eta_phi_nstrip_eq[i][j][k]->Fill(tk.phi(), tk.eta());
          if (tk.hitPattern().numberOfValidStripHits() >= 2*k) h_tracks_eta_phi_nstrip_gt[i][j][k]->Fill(tk.phi(), tk.eta());
        }

        if (tk.eta() < -2.5) {
          h_tracks_npixel_phi_eta_eq[i][j][0]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][0]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        } else if (tk.eta() < -1.5) {
          h_tracks_npixel_phi_eta_eq[i][j][1]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][1]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        } else if (tk.eta() < -0.9) {
          h_tracks_npixel_phi_eta_eq[i][j][2]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][2]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        } else if (tk.eta() < 0.0) {
          h_tracks_npixel_phi_eta_eq[i][j][3]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][3]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        } else if (tk.eta() < 0.9) {
          h_tracks_npixel_phi_eta_eq[i][j][4]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][4]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        } else if (tk.eta() < 1.5) {
          h_tracks_npixel_phi_eta_eq[i][j][5]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][5]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        } else if (tk.eta() < 2.5) {
          h_tracks_npixel_phi_eta_eq[i][j][6]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][6]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        } else {
          h_tracks_npixel_phi_eta_eq[i][j][7]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
          h_tracks_nstrip_phi_eta_eq[i][j][7]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
        }
      }
    }
    
    if (v1 && tk.dxyError() >= 0.05 && tk.pt() > 3 && tk.phi() >= -2.772 && tk.phi() <= -2.646 && tk.eta() >= -2.56 && tk.eta() <= -2.4) {
      ++n_weird;

      const double pars[5] = { tk.pt(),      tk.eta(),      tk.phi(),      tk.dxy(),      tk.dz()      };
      const double errs[5] = { tk.ptError(), tk.etaError(), tk.phiError(), tk.dxyError(), tk.dzError() };

      for (int i = 0; i < 5; ++i) {
        h_weird_track_pars[i]->Fill(pars[i]);
        h_weird_track_errs[i]->Fill(errs[i]);
        for (int j = 0; j < 5; ++j) {
          if (j >= i+1)
            h_weird_track_pars_v_pars[i][j]->Fill(pars[i], pars[j]);
          h_weird_track_errs_v_pars[i][j]->Fill(pars[i], errs[j]);
        }
      }

      h_weird_track_q->Fill(tk.charge());
      h_weird_track_nhits  ->Fill(tk.hitPattern().numberOfValidHits());
      h_weird_track_npxhits->Fill(tk.hitPattern().numberOfValidPixelHits());
      h_weird_track_nsthits->Fill(tk.hitPattern().numberOfValidStripHits());
      h_weird_track_chi2->Fill(tk.chi2());
      h_weird_track_dof->Fill(tk.ndof());
      h_weird_track_chi2dof->Fill(tk.chi2()/tk.ndof());
      h_weird_track_algo->Fill(int(tk.algo()));
      for (int i = 0; i < 7; ++i)
        if (tk.quality(reco::Track::TrackQuality(i))) h_weird_track_quality->Fill(i);
      h_weird_track_nloops->Fill(tk.nLoops());

#ifdef USE_DUMPERS
      if (!dumpers_evented) {
        JMTDumper::set(event, setup);
        std::cout << event;
        dumpers_evented = true;
      }

      std::cout << "weird track:\n" << tk;
#endif
    }
  }

  h_n_weird_tracks->Fill(n_weird);
}

DEFINE_FWK_MODULE(TrackerMapper);
