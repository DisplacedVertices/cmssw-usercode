#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class CosmicMuons : public edm::EDAnalyzer {
 public:
  explicit CosmicMuons(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag track_src;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_particle_src;
  const double min_pt;
  const double max_eta;
  const int min_npxhits;
  const int min_nsthits;
  const int min_nmuhits;
  const double min_dxy;
  const double max_relpterr;

  TH1F* h_ntracks;
  TH1F* h_ntracks_wcuts;

  TH1F* h_tracks_pt;
  TH1F* h_tracks_pterr;
  TH1F* h_tracks_relpterr;
  TH1F* h_tracks_eta;
  TH1F* h_tracks_etaerr;
  TH1F* h_tracks_phi;
  TH1F* h_tracks_phierr;
  TH1F* h_tracks_dxy;
  TH1F* h_tracks_dxyerr;
  TH1F* h_tracks_dz;
  TH1F* h_tracks_dzerr;

  TH1F* h_tracks_nhits;
  TH1F* h_tracks_npxhits;
  TH1F* h_tracks_nsthits;
  TH1F* h_tracks_nmuhits;
  TH1F* h_tracks_chi2dof;

  TH2F* h_ntracks_nmuons;

  TH1F* h_2tracks_deltaphi;
  TH1F* h_2tracks_deltaR;
  TH1F* h_2tracks_theta;
  TH1F* h_2tracks_nmuons;
};

CosmicMuons::CosmicMuons(const edm::ParameterSet& cfg)
  : track_src(cfg.getParameter<edm::InputTag>("track_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_particle_src(cfg.getParameter<edm::InputTag>("gen_particle_src")),
    min_pt(cfg.getParameter<double>("min_pt")),
    max_eta(cfg.getParameter<double>("max_eta")),
    min_npxhits(cfg.getParameter<int>("min_npxhits")),
    min_nsthits(cfg.getParameter<int>("min_nsthits")),
    min_nmuhits(cfg.getParameter<int>("min_nmuhits")),
    min_dxy(cfg.getParameter<double>("min_dxy")),
    max_relpterr(cfg.getParameter<double>("max_relpterr"))
{
  edm::Service<TFileService> fs;

  h_ntracks = fs->make<TH1F>("h_ntracks", ";number of tracks;events", 10, 0, 10);
  h_ntracks_wcuts = fs->make<TH1F>("h_ntracks_wcuts", TString::Format("p_{T} > %3.1f GeV, |#eta| < %3.1f, %d pixel hit, %d strip hits, %d muon hits, |dxy| > %4.2f cm, #sigma(p_{T})/p_{T} < %3.1f;number of tracks;events", min_pt, max_eta, min_npxhits, min_nsthits, min_nmuhits, min_dxy, max_relpterr), 10, 0, 10);

  h_tracks_pt = fs->make<TH1F>("h_tracks_pt", ";tracks p_{T} (GeV);arb. units", 150, 0, 150);
  h_tracks_pterr = fs->make<TH1F>("h_tracks_pterr", ";tracks #sigma(p_{T}) (GeV);arb. units", 100, 0, 5);
  h_tracks_relpterr= fs->make<TH1F>("h_tracks_relpterr", ";tracks #sigma(p_{T})/p_{T};arb. units", 100, 0, 0.1);
  h_tracks_eta = fs->make<TH1F>("h_tracks_eta", ";tracks #eta;arb. units", 50, -4, 4);
  h_tracks_etaerr = fs->make<TH1F>("h_tracks_etaerr", ";tracks #sigma(#eta);arb. units", 100, 0, 0.01);
  h_tracks_phi = fs->make<TH1F>("h_tracks_phi", ";tracks #phi;arb. units", 50, -3.15, 3.15);
  h_tracks_phierr = fs->make<TH1F>("h_tracks_phierr", ";tracks #sigma(#phi);arb. units", 100, 0, 0.01);
  h_tracks_dxy = fs->make<TH1F>("h_tracks_dxy", ";tracks dxy(PV) (cm);arb. units", 100, -2, 2);
  h_tracks_dxyerr = fs->make<TH1F>("h_tracks_dxyerr", ";tracks #sigma(dxy) (cm)", 100, 0, 0.1);
  h_tracks_dz = fs->make<TH1F>("h_tracks_dz", ";tracks dz(PV) (cm);arb. units", 100, -2, 2);
  h_tracks_dzerr = fs->make<TH1F>("h_tracks_dzerr", ";tracks #sigma(dz) (cm);arb. units", 100, 0, 0.1);

  h_tracks_nhits = fs->make<TH1F>("h_tracks_nhits", ";tracks number of hits; arb. units", 100, 0, 100);
  h_tracks_npxhits = fs->make<TH1F>("h_tracks_npxhits", ";tracks number of pixel hits; arb. units", 12, 0, 12);
  h_tracks_nsthits = fs->make<TH1F>("h_tracks_nsthits", ";tracks number of strip hits; arb. units", 28, 0, 28);
  h_tracks_nmuhits = fs->make<TH1F>("h_tracks_nmuhits", ";tracks number of muon hits; arb. units", 5, 0, 5);
  h_tracks_chi2dof = fs->make<TH1F>("h_tracks_chi2dof", ";tracks #chi^2/dof;arb. units", 100, 0, 100);

  h_ntracks_nmuons = fs->make<TH2F>("h_ntracks_nmuons", ";number of generated muons;number of tracks", 10, 0, 10, 10, 0, 10);

  h_2tracks_deltaphi = fs->make<TH1F>("h_2tracks_deltaphi", "events with 2 tracks;#Delta#phi;arb. units", 50, -3.15, 3.15);
  h_2tracks_deltaR = fs->make<TH1F>("h_2tracks_deltaR", "events with 2 tracks;#DeltaR;arb. units", 50, 0, 7);
  h_2tracks_theta = fs->make<TH1F>("h_2tracks_theta", "events with 2 tracks;3D space angle;arb. units", 50, 0, 3.15);
  h_2tracks_nmuons = fs->make<TH1F>("h_2tracks_nmuons", "events with 2 tracks;number of generated muons;arb. units", 10, 0, 10);
}

void CosmicMuons::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(track_src, tracks);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  const reco::Vertex& primary_vertex = primary_vertices->at(0);
  const math::XYZPoint pv(primary_vertex.x(), primary_vertex.y(), primary_vertex.z());

  h_ntracks->Fill(int(tracks->size()));

  int ntracks = 0;
  for (const reco::Track& tk : *tracks) {
    if (tk.pt() < min_pt || fabs(tk.eta()) > max_eta || tk.hitPattern().numberOfValidPixelHits() < min_npxhits || tk.hitPattern().numberOfValidStripHits() < min_nsthits || tk.hitPattern().muonStationsWithValidHits() < min_nmuhits || fabs(tk.dxy(pv)) < min_dxy || tk.ptError()/tk.pt() > max_relpterr) continue;
    ntracks++;

    h_tracks_pt->Fill(tk.pt());
    h_tracks_pterr->Fill(tk.ptError());
    h_tracks_relpterr->Fill(tk.ptError() / tk.pt());
    h_tracks_eta->Fill(tk.eta());
    h_tracks_etaerr->Fill(tk.etaError());
    h_tracks_phi->Fill(tk.phi());
    h_tracks_phierr->Fill(tk.phiError());
    h_tracks_dxy->Fill(tk.dxy(pv));
    h_tracks_dxyerr->Fill(tk.dxyError());
    h_tracks_dz->Fill(tk.dz(pv));
    h_tracks_dzerr->Fill(tk.dzError());

    h_tracks_nhits->Fill(tk.hitPattern().numberOfValidHits());
    h_tracks_npxhits->Fill(tk.hitPattern().numberOfValidPixelHits());
    h_tracks_nsthits->Fill(tk.hitPattern().numberOfValidStripHits());
    h_tracks_nmuhits->Fill(tk.hitPattern().muonStationsWithValidHits());
    h_tracks_chi2dof->Fill(tk.chi2()/tk.ndof());
  }
  h_ntracks_wcuts->Fill(ntracks);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_particle_src, gen_particles);

  int nmuons = 0;
  for (const reco::GenParticle& gen : *gen_particles) {
    if (gen.status() == 1 && abs(gen.pdgId()) == 13) {
      if (gen.pt() < min_pt || fabs(gen.eta()) > max_eta) continue;
      nmuons++;
    }
  }
  h_ntracks_nmuons->Fill(nmuons, ntracks);

  if (ntracks == 2) {
    std::vector<reco::Track> tracks_wcuts;
    for (const reco::Track& tk : *tracks) {
      if (tk.pt() < min_pt || fabs(tk.eta()) > max_eta || tk.hitPattern().numberOfValidPixelHits() < min_npxhits || tk.hitPattern().numberOfValidStripHits() < min_nsthits || tk.hitPattern().muonStationsWithValidHits() < min_nmuhits || fabs(tk.dxy(pv)) < min_dxy || tk.ptError()/tk.pt() > max_relpterr) continue;
      tracks_wcuts.push_back(tk);
    }
    const reco::Track& tk0 = tracks_wcuts[0];
    const reco::Track& tk1 = tracks_wcuts[1];
    h_2tracks_deltaphi->Fill(reco::deltaPhi(tk0.phi(), tk1.phi()));
    h_2tracks_deltaR->Fill(reco::deltaR(tk0.eta(), tk0.phi(), tk1.eta(), tk1.phi()));
    h_2tracks_theta->Fill(acos(tk0.momentum().Dot(tk1.momentum()) / (tk0.p() * tk1.p())));
    h_2tracks_nmuons->Fill(nmuons);
  }
}

DEFINE_FWK_MODULE(CosmicMuons);
