#include "TH2F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

class EffCheck : public edm::EDAnalyzer {
 public:
  explicit EffCheck(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::InputTag track_src;

  TH1F* h_tracks_pt;
  TH1F* h_tracks_eta;
  TH1F* h_tracks_phi;

  TH2F* h_tracksptgt1_npixel_eta;
  TH2F* h_tracksptgt1_npixel_phi;
  TH2F* h_tracksptgt1_nstrip_eta;
  TH2F* h_tracksptgt1_nstrip_phi;
  TH2F* h_tracksptgt3_npixel_eta;
  TH2F* h_tracksptgt3_npixel_phi;
  TH2F* h_tracksptgt3_nstrip_eta;
  TH2F* h_tracksptgt3_nstrip_phi;
};

EffCheck::EffCheck(const edm::ParameterSet& cfg)
  : track_src(cfg.getParameter<edm::InputTag>("track_src"))
{
  edm::Service<TFileService> fs;

  h_tracks_pt = fs->make<TH1F>("h_tracks_pt", ";tracks pt;arb. units", 150, 0, 150);
  h_tracks_phi = fs->make<TH1F>("h_tracks_phi", ";tracks phi;arb. units", 50, -3.15, 3.15);
  h_tracks_eta = fs->make<TH1F>("h_tracks_eta", ";tracks eta;arb. units", 50, -4, 4);

  h_tracksptgt1_npixel_eta = fs->make<TH2F>("h_tracksptgt1_npixel_eta", "tracks w/ p_{T} > 1 GeV;eta;number of pixel hits", 50, -4.00, 4.00, 40, 0, 40);
  h_tracksptgt1_npixel_phi = fs->make<TH2F>("h_tracksptgt1_npixel_phi", "tracks w/ p_{T} > 1 GeV;phi;number of pixel hits", 50, -3.15, 3.15, 40, 0, 40);
  h_tracksptgt1_nstrip_eta = fs->make<TH2F>("h_tracksptgt1_nstrip_eta", "tracks w/ p_{T} > 1 GeV;eta;number of strip hits", 50, -4.00, 4.00, 40, 0, 40);
  h_tracksptgt1_nstrip_phi = fs->make<TH2F>("h_tracksptgt1_nstrip_phi", "tracks w/ p_{T} > 1 GeV;phi;number of strip hits", 50, -3.15, 3.15, 40, 0, 40);
  h_tracksptgt3_npixel_eta = fs->make<TH2F>("h_tracksptgt3_npixel_eta", "tracks w/ p_{T} > 3 GeV;eta;number of pixel hits", 50, -4.00, 4.00, 40, 0, 40);
  h_tracksptgt3_npixel_phi = fs->make<TH2F>("h_tracksptgt3_npixel_phi", "tracks w/ p_{T} > 3 GeV;phi;number of pixel hits", 50, -3.15, 3.15, 40, 0, 40);
  h_tracksptgt3_nstrip_eta = fs->make<TH2F>("h_tracksptgt3_nstrip_eta", "tracks w/ p_{T} > 3 GeV;eta;number of strip hits", 50, -4.00, 4.00, 40, 0, 40);
  h_tracksptgt3_nstrip_phi = fs->make<TH2F>("h_tracksptgt3_nstrip_phi", "tracks w/ p_{T} > 3 GeV;phi;number of strip hits", 50, -3.15, 3.15, 40, 0, 40);
}

void EffCheck::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(track_src, tracks);

  for (const reco::Track& tk : *tracks) {
    h_tracks_pt->Fill(tk.pt());
    h_tracks_phi->Fill(tk.phi());
    h_tracks_eta->Fill(tk.eta());
    if (tk.pt() > 1) {
      h_tracksptgt1_npixel_eta->Fill(tk.eta(), tk.hitPattern().numberOfValidPixelHits());
      h_tracksptgt1_npixel_phi->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
      h_tracksptgt1_nstrip_eta->Fill(tk.eta(), tk.hitPattern().numberOfValidStripHits());
      h_tracksptgt1_nstrip_phi->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits());
    }
    if (tk.pt() > 3) {
      h_tracksptgt3_npixel_eta->Fill(tk.eta(), tk.hitPattern().numberOfValidPixelHits());
      h_tracksptgt3_npixel_phi->Fill(tk.phi(), tk.hitPattern().numberOfValidPixelHits());
      h_tracksptgt3_nstrip_eta->Fill(tk.eta(), tk.hitPattern().numberOfValidStripHits());
      h_tracksptgt3_nstrip_phi->Fill(tk.phi(), tk.hitPattern().numberOfValidStripHits()); 
    }
  }
}

DEFINE_FWK_MODULE(EffCheck);
