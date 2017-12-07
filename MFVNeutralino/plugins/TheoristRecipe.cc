#include "TH2.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVTheoristRecipe : public edm::EDAnalyzer {
public:
  explicit MFVTheoristRecipe(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  const edm::EDGetTokenT<std::vector<double>> gen_vertex_token;
  const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  const double max_dist;

  TH1F* h_gen_valid;

  TH1F* h_gen_njets;
  TH1F* h_gen_jet_pt;
  TH1F* h_gen_jet_pt40;
  TH1F* h_gen_ht40;
  TH1F* h_gen_dxy;
  TH1F* h_gen_ntracks;
  TH1F* h_gen_sumpt;
  TH1F* h_gen_dbv;
  TH1F* h_gen_dvv;

  TH1F* h_rec_njets;
  TH1F* h_rec_jet_pt;
  TH1F* h_rec_jet_pt40;
  TH1F* h_rec_ht40;
  TH1F* h_rec_dxy;
  TH1F* h_rec_ntracks;
  TH1F* h_rec_bs2derr;
  TH1F* h_rec_dbv;
  TH1F* h_rec_dvv;

  TH1F* h_gen_match_dxy;
  TH1F* h_gen_match_ntracks;
  TH1F* h_gen_match_sumpt;
  TH1F* h_gen_match_dbv;

  TH1F* h_rec_match_dxy;
  TH1F* h_rec_match_ntracks;
  TH1F* h_rec_match_bs2derr;
  TH1F* h_rec_match_dbv;

  TH1F* h_dist;
  TH1F* h_lspsnmatch;
};

MFVTheoristRecipe::MFVTheoristRecipe(const edm::ParameterSet& cfg)
  : gen_vertex_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
    mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    max_dist(cfg.getParameter<double>("max_dist"))
{
  edm::Service<TFileService> fs;

  h_gen_valid = fs->make<TH1F>("h_gen_valid", "", 2, 0, 2);

  h_gen_njets = fs->make<TH1F>("h_gen_njets", ";number of accepted quarks;events", 20, 0, 20);
  h_gen_jet_pt = fs->make<TH1F>("h_gen_jet_pt", ";p_{T} of accepted quarks;quarks", 500, 0, 500);
  h_gen_jet_pt40 = fs->make<TH1F>("h_gen_jet_pt40", ";p_{T} of accepted quarks with p_{T} > 40 GeV;quarks", 500, 0, 500);
  h_gen_ht40 = fs->make<TH1F>("h_gen_ht40", ";H_{T} of accepted quarks with p_{T} > 40 GeV;events", 500, 0, 5000);
  h_gen_dxy = fs->make<TH1F>("h_gen_dxy", ";generated d_{xy} (cm);LSP daughter particles", 100, 0, 1);
  h_gen_ntracks = fs->make<TH1F>("h_gen_ntracks", ";number of accepted displaced daughter particles;LSPs", 40, 0, 40);
  h_gen_sumpt = fs->make<TH1F>("h_gen_sumpt", ";#Sigmap_{T} of accepted displaced daughter particles (GeV);LSPs", 100, 0, 1000);
  h_gen_dbv = fs->make<TH1F>("h_gen_dbv", ";generated d_{BV} (cm);LSPs", 250, 0, 2.5);
  h_gen_dvv = fs->make<TH1F>("h_gen_dvv", ";generated d_{VV} (cm);events", 500, 0, 5);

  h_rec_njets = fs->make<TH1F>("h_rec_njets", ";reconstructed number of jets;events", 20, 0, 20);
  h_rec_jet_pt = fs->make<TH1F>("h_rec_jet_pt", ";reconstructed p_{T} of jets;jets", 500, 0, 500);
  h_rec_jet_pt40 = fs->make<TH1F>("h_rec_jet_pt40", ";reconstructed p_{T} of jets with p_{T} > 40 GeV;jets", 500, 0, 500);
  h_rec_ht40 = fs->make<TH1F>("h_rec_ht40", ";reconstructed H_{T} of jets with p_{T} > 40 GeV;events", 500, 0, 5000);
  h_rec_dxy = fs->make<TH1F>("h_rec_dxy", ";reconstructed d_{xy} (cm);tracks", 100, 0, 1);
  h_rec_ntracks = fs->make<TH1F>("h_rec_ntracks", ";number of tracks;vertices", 40, 0, 40);
  h_rec_bs2derr = fs->make<TH1F>("h_rec_bs2derr", ";#sigma(d_{BV}) (cm);vertices", 25, 0, 0.0025);
  h_rec_dbv = fs->make<TH1F>("h_rec_dbv", ";reconstructed d_{BV} (cm);vertices", 250, 0, 2.5);
  h_rec_dvv = fs->make<TH1F>("h_rec_dvv", ";reconstructed d_{VV} (cm);events", 500, 0, 5);

  h_dist = fs->make<TH1F>("h_dist", ";distance to closest LSP;vertices", 100, 0, 0.01);
  h_lspsnmatch = fs->make<TH1F>("h_lspsnmatch", ";number of vertices that match LSP;LSPs", 15, 0, 15);

  h_gen_match_dxy = fs->make<TH1F>("h_gen_match_dxy", ";generated d_{xy} (cm);LSP daughter particles", 100, 0, 1);
  h_gen_match_ntracks = fs->make<TH1F>("h_gen_match_ntracks", ";number of accepted displaced daughter particles;LSPs", 40, 0, 40);
  h_gen_match_sumpt = fs->make<TH1F>("h_gen_match_sumpt", ";#Sigmap_{T} of accepted displaced daughter particles (GeV);LSPs", 100, 0, 1000);
  h_gen_match_dbv = fs->make<TH1F>("h_gen_match_dbv", ";generated d_{BV} (cm);LSPs", 250, 0, 2.5);

  h_rec_match_dxy = fs->make<TH1F>("h_rec_match_dxy", ";reconstructed d_{xy} (cm);tracks", 100, 0, 1);
  h_rec_match_ntracks = fs->make<TH1F>("h_rec_match_ntracks", ";number of tracks;vertices", 40, 0, 40);
  h_rec_match_bs2derr = fs->make<TH1F>("h_rec_match_bs2derr", ";#sigma(d_{BV}) (cm);vertices", 25, 0, 0.0025);
  h_rec_match_dbv = fs->make<TH1F>("h_rec_match_dbv", ";reconstructed d_{BV} (cm);vertices", 250, 0, 2.5);
}

void MFVTheoristRecipe::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<mfv::MCInteraction> mci;
  event.getByToken(mci_token, mci);

  h_gen_valid->Fill(mci->valid());
  if (!mci->valid()) {
    std::cout << "MFVTheoristRecipe: MCInteraction not valid--model not implemented? skipping event" << std::endl;
    return;
  }

  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<std::vector<double>> gen_vertex;
  event.getByToken(gen_vertex_token, gen_vertex);
    
  const double x0 = (*gen_vertex)[0];
  const double y0 = (*gen_vertex)[1];
  const double z0 = (*gen_vertex)[2];

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertex_token, vertices);

  std::vector<const reco::GenParticle*> partons[2];
  double v[2][3] = {{0}};
  TLorentzVector lsp_p4s[2];
 
  for (int i : {0,1}) {
    for (auto ref : mci->visible(i))
      partons[i].push_back(&*ref);
    auto x = mci->decay_point(i);
    v[i][0] = x.x - x0;
    v[i][1] = x.y - y0;
    v[i][2] = x.z - z0;
    lsp_p4s[i] = make_tlv(mci->primaries()[i]);
  }

  const double dbv[2] = { mag(v[0][0], v[0][1]), mag(v[1][0], v[1][1]) };
  const double dvv = mci->dvv();

  //////////////////////////////////////////////////////////////////////////////

  //plot generator-level variables
  int nquarks = 0;
  float ht40 = 0;
  for (int i = 0; i < 2; ++i) {
    int ntracks = 0;
    float sumpt = 0;
    for (const reco::GenParticle* p : partons[i]) {
      float dxy = fabs(dbv[i] * sin(p->phi() - atan2(v[i][1], v[i][0])));
      if (p->pt() > 20 && fabs(p->eta()) < 2.5) {
        if (is_quark(p)) {
          ++nquarks;
          h_gen_jet_pt->Fill(p->pt());
          if (p->pt() > 40) {
            ht40 += p->pt();
            h_gen_jet_pt40->Fill(p->pt());
          }
        }
        if (dxy >= 0.01) {
          ++ntracks;
          sumpt += p->pt();
        }
      }
      h_gen_dxy->Fill(dxy);
    }
    h_gen_ntracks->Fill(ntracks);
    h_gen_sumpt->Fill(sumpt);
    h_gen_dbv->Fill(dbv[i]);
  }
  h_gen_njets->Fill(nquarks);
  h_gen_ht40->Fill(ht40);
  h_gen_dvv->Fill(dvv);

  //plot reconstructed-level variables
  h_rec_njets->Fill(mevent->njets());
  h_rec_ht40->Fill(mevent->jet_ht(40));
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    h_rec_jet_pt->Fill(mevent->jet_pt[ijet]);
    if (mevent->jet_pt[ijet] > 40) h_rec_jet_pt40->Fill(mevent->jet_pt[ijet]);
  }
  for (const MFVVertexAux& vtx : *vertices) {
    for (size_t i = 0, n = vtx.ntracks(); i < n; ++i) {
      h_rec_dxy->Fill(vtx.track_dxy[i]);
    }
    h_rec_ntracks->Fill(vtx.ntracks());
    h_rec_bs2derr->Fill(vtx.bs2derr);
    h_rec_dbv->Fill(mevent->bs2ddist(vtx));
  }
  if (vertices->size() >= 2) {
    h_rec_dvv->Fill(mag(vertices->at(0).x - vertices->at(1).x, vertices->at(0).y - vertices->at(1).y));
  }

/*
  //match jets to partons
  printf("\nrun = %u, lumi = %u, event = %llu: number of accepted quarks = %d, number of jets = %d, generated HT(40) = %.2f GeV, reconstructed HT(40) = %.2f GeV\n", event.id().run(), event.luminosityBlock(), event.id().event(), nquarks, mevent->njets(), ht40, mevent->jet_ht(40));
  for (int i = 0; i < 2; ++i) {
    for (const reco::GenParticle* p : partons[i]) {
      printf("\tparton pdgId %3d: pT = %6.2f GeV, eta = %5.2f, phi = %5.2f", p->pdgId(), p->pt(), p->eta(), p->phi());
      for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
        float deltaR = reco::deltaR(p->eta(), p->phi(), mevent->jet_eta[ijet], mevent->jet_phi[ijet]);
        if (deltaR < 0.4) {
          printf("\tjet %2d: pT = %6.2f GeV, eta = %5.2f, phi = %5.2f, deltaR(parton, jet) = %4.2f", int(ijet), mevent->jet_pt[ijet], mevent->jet_eta[ijet], mevent->jet_phi[ijet], deltaR);
        }
      }
      printf("\n");
    }
  }
*/

  //match vertices to LSPs
  int lsp_nmatch[2] = {0,0};
  for (const MFVVertexAux& vtx : *vertices) {
    double dist = 1e99;
    int ilsp = -1;

    double dists[2] = {
      mag(v[0][0] - (vtx.x - x0),
          v[0][1] - (vtx.y - y0),
          v[0][2] - (vtx.z - z0)),
      mag(v[1][0] - (vtx.x - x0),
          v[1][1] - (vtx.y - y0),
          v[1][2] - (vtx.z - z0)),
    };

    for (int i = 0; i < 2; ++i) {
      if (dists[i] < dist) {
        dist = dists[i];
        ilsp = i;
      }
    }

    if (ilsp < 0 || dist > max_dist) {
      continue;
    }

    ++lsp_nmatch[ilsp];

    //plot variables for first matched vertex
    if (lsp_nmatch[ilsp] == 1) {
      h_dist->Fill(dist);

      int ntracks = 0;
      float sumpt = 0;
      for (const reco::GenParticle* p : partons[ilsp]) {
        float dxy = fabs(dbv[ilsp] * sin(p->phi() - atan2(v[ilsp][1], v[ilsp][0])));
        if (p->pt() > 20 && fabs(p->eta()) < 2.5 && dxy >= 0.01) {
          ++ntracks;
          sumpt += p->pt();
        }
        h_gen_match_dxy->Fill(dxy);
      }
      h_gen_match_ntracks->Fill(ntracks);
      h_gen_match_sumpt->Fill(sumpt);
      h_gen_match_dbv->Fill(dbv[ilsp]);

      for (size_t i = 0, n = vtx.ntracks(); i < n; ++i) {
        h_rec_match_dxy->Fill(vtx.track_dxy[i]);
      }
      h_rec_match_ntracks->Fill(vtx.ntracks());
      h_rec_match_bs2derr->Fill(vtx.bs2derr);
      h_rec_match_dbv->Fill(mevent->bs2ddist(vtx));
    }
  }

  for (int i = 0; i < 2; ++i) {
    h_lspsnmatch->Fill(lsp_nmatch[i]);
  }
}

DEFINE_FWK_MODULE(MFVTheoristRecipe);
