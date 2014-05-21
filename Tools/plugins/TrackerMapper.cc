#include "TH2F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

//#define USE_DUMPERS // you also have to add JMTucker/Dumpers to the BuildFile.xml for this
#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/SiStripDetId/interface/TIBDetId.h"
#include "DataFormats/SiStripDetId/interface/TOBDetId.h"
#include "DataFormats/SiStripDetId/interface/TIDDetId.h"
#include "DataFormats/SiStripDetId/interface/TECDetId.h"
#include "JMTucker/Tools/interface/TrackHistos.h"

#ifdef USE_DUMPERS
#include "JMTucker/Dumpers/interface/Dumpers.h"
#endif

class TrackerMapper : public edm::EDAnalyzer {
 public:
  explicit TrackerMapper(const edm::ParameterSet&);
  ~TrackerMapper() {
    delete h_v1ptgt3_tracks;
    delete h_weird_tracks;
  }
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::InputTag track_src;
  const bool use_rechits;

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

  TrackHistos* h_v1ptgt3_tracks;
  TH1F* h_n_weird_tracks;
  TrackHistos* h_weird_tracks;

  TH2F* h_gen_eta_phi;
};

TrackerMapper::TrackerMapper(const edm::ParameterSet& cfg)
  : track_src(cfg.getParameter<edm::InputTag>("track_src")),
    use_rechits(cfg.getParameter<bool>("use_rechits"))
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

  const int par_nbins[5] = { 500,  100,    100,  400, 400 };
  const double par_lo[5] = {   0, -2.6, -2.772,   -2, -20 };
  const double par_hi[5] = { 100, -2.4, -2.646,    2,  20 };
  const int err_nbins[5] = { 100, 100, 100, 200, 200 };
  const double err_lo[5] = { 0 };
  const double err_hi[5] = {   5, 0.1, 0.1, 0.5, 2 };
  h_v1ptgt3_tracks = new TrackHistos("v1ptgt3", use_rechits, par_nbins, par_lo, par_hi, err_nbins, err_lo, err_hi);
  h_n_weird_tracks = fs->make<TH1F>("h_n_weird_tracks", "", 200, 0, 200);
  h_weird_tracks   = new TrackHistos("weird",   use_rechits, par_nbins, par_lo, par_hi, err_nbins, err_lo, err_hi);

  h_gen_eta_phi = fs->make<TH2F>("h_gen_eta_phi", "charged gen particles w/ status 1;phi;eta", 50, -3.15, 3.15, 50, -4, 4);
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
    //std::cout << "a track:\n" << tk;
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

        const double etabins[9] = { -1e99, -2.5, -1.5, -0.9, 0, 0.9, 1.5, 2.5, 1e99 };
        for (int k = 0; k < 8; ++k) {
          if (tk.eta() > etabins[k] && tk.eta() < etabins[k+1]) {
            h_tracks_npixel_phi_eta_eq[i][j][k]->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
            h_tracks_nstrip_phi_eta_eq[i][j][k]->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
          }
        }
      }
    }
    
    if (v1 && tk.pt() > 3) {
      h_v1ptgt3_tracks->Fill(tk);

      if (tk.dxyError() >= 0.05 && tk.phi() >= -2.772 && tk.phi() <= -2.646 && tk.eta() >= -2.56 && tk.eta() <= -2.4) {
        ++n_weird;
        h_weird_tracks->Fill(tk);

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
  }

  h_n_weird_tracks->Fill(n_weird);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel("genParticles", gen_particles);
  for (const reco::GenParticle& gen : *gen_particles) {
    if (gen.status() == 1 && gen.charge() != 0) {
      h_gen_eta_phi->Fill(gen.phi(), gen.eta());
    }
  }
}

DEFINE_FWK_MODULE(TrackerMapper);
