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
  const edm::EDGetTokenT<reco::GenJetCollection> gen_jets_token;
  const edm::EDGetTokenT<std::vector<double>> gen_vertex_token;
  const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  const double max_dist;
  const bool verbose;

  TH1F* h_gen_valid;

  TH1F* h_genJet_njets;
  TH1F* h_genJet_ht40;

  TH1F* h_gen_parton_njets;
  TH1F* h_gen_parton_ht40;
  TH1F* h_gen_parton_accepted_njets;
  TH1F* h_gen_parton_accepted_ht40;
  TH1F* h_gen_quark_njets;
  TH1F* h_gen_quark_ht40;
  TH1F* h_gen_quark_accepted_njets;
  TH1F* h_gen_quark_accepted_ht40;

  TH1F* h_gen_dxy;
  TH1F* h_gen_ntracks;
  TH1F* h_gen_sumpt;
  TH1F* h_gen_nbquarks;
  TH1F* h_gen_dbv;
  TH1F* h_gen_dvv;

  TH1F* h_rec_njets;
  TH1F* h_rec_ht40;
  TH1F* h_rec_dxy;
  TH1F* h_rec_ntracks;
  TH1F* h_rec_bs2derr;
  TH1F* h_rec_dbv;
  TH1F* h_rec_dvv;

  TH2F* h_rec_v_gen_njets;
  TH2F* h_rec_v_gen_jet_pt;
  TH2F* h_rec_v_gen_jet_pt40;
  TH2F* h_rec_v_gen_ht40;

  TH1F* h_dist;
  TH1F* h_ddbv;
  TH1F* h_dphi;
  TH1F* h_lspsnmatch;

  TH1F* h_gen_match_dxy;
  TH1F* h_gen_match_ntracks;
  TH1F* h_gen_match_sumpt;
  TH1F* h_gen_match_dbv;
  TH1F* h_gen_match_dvv;

  TH1F* h_rec_match_dxy;
  TH1F* h_rec_match_ntracks;
  TH1F* h_rec_match_bs2derr;
  TH1F* h_rec_match_dbv;
  TH1F* h_rec_match_dvv;
};

MFVTheoristRecipe::MFVTheoristRecipe(const edm::ParameterSet& cfg)
  : gen_jets_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("gen_jets_src"))),
    gen_vertex_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
    mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    max_dist(cfg.getParameter<double>("max_dist")),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false))
{
  edm::Service<TFileService> fs;

  h_gen_valid = fs->make<TH1F>("h_gen_valid", "", 2, 0, 2);

  h_genJet_njets = fs->make<TH1F>("h_genJet_njets", ";number of genJets;events", 20, 0, 20);
  h_genJet_ht40 = fs->make<TH1F>("h_genJet_ht40", ";H_{T} of genJets with p_{T} > 40 GeV;events", 500, 0, 5000);

  h_gen_parton_njets = fs->make<TH1F>("h_gen_parton_njets", ";number of partons;events", 20, 0, 20);
  h_gen_parton_ht40 = fs->make<TH1F>("h_gen_parton_ht40", ";H_{T} of partons with p_{T} > 40 GeV", 500, 0, 5000);
  h_gen_parton_accepted_njets = fs->make<TH1F>("h_gen_parton_accepted_njets", ";number of accepted partons;events", 20, 0, 20);
  h_gen_parton_accepted_ht40 = fs->make<TH1F>("h_gen_parton_accepted_ht40", ";H_{T} of accepted partons with p_{T} > 40 GeV", 500, 0, 5000);
  h_gen_quark_njets = fs->make<TH1F>("h_gen_quark_njets", ";number of quarks;events", 20, 0, 20);
  h_gen_quark_ht40 = fs->make<TH1F>("h_gen_quark_ht40", ";H_{T} of quarks with p_{T} > 40 GeV", 500, 0, 5000);
  h_gen_quark_accepted_njets = fs->make<TH1F>("h_gen_quark_accepted_njets", ";number of accepted quarks;events", 20, 0, 20);
  h_gen_quark_accepted_ht40 = fs->make<TH1F>("h_gen_quark_accepted_ht40", ";H_{T} of accepted quarks with p_{T} > 40 GeV;events", 500, 0, 5000);

  h_gen_dxy = fs->make<TH1F>("h_gen_dxy", ";d_{xy} of accepted daughter particles (cm);LSP daughter particles", 100, 0, 1);
  h_gen_ntracks = fs->make<TH1F>("h_gen_ntracks", ";number of accepted displaced daughter particles;LSPs", 40, 0, 40);
  h_gen_sumpt = fs->make<TH1F>("h_gen_sumpt", ";#Sigmap_{T} of accepted displaced daughter particles (GeV);LSPs", 500, 0, 5000);
  h_gen_nbquarks = fs->make<TH1F>("h_gen_nbquarks", ";number of accepted displaced b quarks;events", 40, 0, 40);
  h_gen_dbv = fs->make<TH1F>("h_gen_dbv", ";generated d_{BV} (cm);LSPs", 250, 0, 2.5);
  h_gen_dvv = fs->make<TH1F>("h_gen_dvv", ";generated d_{VV} (cm);events", 500, 0, 5);

  h_rec_njets = fs->make<TH1F>("h_rec_njets", ";reconstructed number of jets;events", 20, 0, 20);
  h_rec_ht40 = fs->make<TH1F>("h_rec_ht40", ";reconstructed H_{T} of jets with p_{T} > 40 GeV;events", 500, 0, 5000);
  h_rec_dxy = fs->make<TH1F>("h_rec_dxy", ";reconstructed d_{xy} (cm);tracks", 100, 0, 1);
  h_rec_ntracks = fs->make<TH1F>("h_rec_ntracks", ";number of tracks;vertices", 40, 0, 40);
  h_rec_bs2derr = fs->make<TH1F>("h_rec_bs2derr", ";#sigma(d_{BV}) (cm);vertices", 25, 0, 0.0025);
  h_rec_dbv = fs->make<TH1F>("h_rec_dbv", ";reconstructed d_{BV} (cm);vertices", 250, 0, 2.5);
  h_rec_dvv = fs->make<TH1F>("h_rec_dvv", ";reconstructed d_{VV} (cm);events", 500, 0, 5);

  h_rec_v_gen_njets = fs->make<TH2F>("h_rec_v_gen_njets", ";number of accepted quarks;reconstructed number of jets", 20, 0, 20, 20, 0, 20);
  h_rec_v_gen_jet_pt = fs->make<TH2F>("h_rec_v_gen_jet_pt", "#DeltaR(quark, jet) < 0.4;p_{T} of accepted quarks;reconstructed p_{T} of jets", 500, 0, 500, 500, 0, 500);
  h_rec_v_gen_jet_pt40 = fs->make<TH2F>("h_rec_v_gen_jet_pt40", "#DeltaR(quark, jet) < 0.4;p_{T} of accepted quarks with p_{T} > 40 GeV;reconstructed p_{T} of jets with p_{T} > 40 GeV", 500, 0, 500, 500, 0, 500);
  h_rec_v_gen_ht40 = fs->make<TH2F>("h_rec_v_gen_ht40", ";H_{T} of accepted quarks with p_{T} > 40 GeV;reconstructed H_{T} of jets with p_{T} > 40 GeV", 500, 0, 5000, 500, 0, 5000);

  h_dist = fs->make<TH1F>("h_dist", ";distance to closest LSP;vertices", 100, 0, 0.01);
  h_ddbv = fs->make<TH1F>("h_ddbv", ";d_{BV}(vertex) - d_{BV}(LSP);vertices", 200, -0.01, 0.01);
  h_dphi = fs->make<TH1F>("h_dphi", ";#phi(vertex) - #phi(LSP);vertices", 200, -1, 1);
  h_lspsnmatch = fs->make<TH1F>("h_lspsnmatch", ";number of vertices that match LSP;LSPs", 15, 0, 15);

  h_gen_match_dxy = fs->make<TH1F>("h_gen_match_dxy", ";d_{xy} of accepted daughter particles (cm);LSP daughter particles", 100, 0, 1);
  h_gen_match_ntracks = fs->make<TH1F>("h_gen_match_ntracks", ";number of accepted displaced daughter particles;LSPs", 40, 0, 40);
  h_gen_match_sumpt = fs->make<TH1F>("h_gen_match_sumpt", ";#Sigmap_{T} of accepted displaced daughter particles (GeV);LSPs", 500, 0, 5000);
  h_gen_match_dbv = fs->make<TH1F>("h_gen_match_dbv", ";generated d_{BV} (cm);LSPs", 250, 0, 2.5);
  h_gen_match_dvv = fs->make<TH1F>("h_gen_match_dvv", ";generated d_{VV} (cm);events", 500, 0, 5);

  h_rec_match_dxy = fs->make<TH1F>("h_rec_match_dxy", ";reconstructed d_{xy} (cm);tracks", 100, 0, 1);
  h_rec_match_ntracks = fs->make<TH1F>("h_rec_match_ntracks", ";number of tracks;vertices", 40, 0, 40);
  h_rec_match_bs2derr = fs->make<TH1F>("h_rec_match_bs2derr", ";#sigma(d_{BV}) (cm);vertices", 25, 0, 0.0025);
  h_rec_match_dbv = fs->make<TH1F>("h_rec_match_dbv", ";reconstructed d_{BV} (cm);vertices", 250, 0, 2.5);
  h_rec_match_dvv = fs->make<TH1F>("h_rec_match_dvv", ";reconstructed d_{VV} (cm);events", 500, 0, 5);
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

  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByToken(gen_jets_token, gen_jets);

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
      partons[i].push_back((reco::GenParticle*)first_candidate(&*ref));
    auto x = mci->decay_point(i);
    v[i][0] = x.x - x0;
    v[i][1] = x.y - y0;
    v[i][2] = x.z - z0;
    lsp_p4s[i] = make_tlv(mci->primaries()[i]);
  }

  const double dbv[2] = { mag(v[0][0], v[0][1]), mag(v[1][0], v[1][1]) };
  const double dvv = mci->dvv();

  //////////////////////////////////////////////////////////////////////////////

  int ngenJets = 0; float genJet_ht40 = 0;
  for (const reco::GenJet& jet : *gen_jets) {
    double mue = 0;
    for (auto c : jet.getJetConstituents())
      if (abs(c->pdgId()) == 13)
        mue += c->energy();

    if (jet.pt() > 20 && fabs(jet.eta()) < 2.5 && mue / jet.energy() < 0.8) {
      ++ngenJets; if (jet.pt() > 40) genJet_ht40 += jet.pt();
    }
  }
  h_genJet_njets->Fill(ngenJets);
  h_genJet_ht40->Fill(genJet_ht40);

  //plot generator-level variables
  int npartons = 0; float parton_ht40 = 0;
  int npartons_accepted = 0; float parton_accepted_ht40 = 0;
  int nquarks = 0; float quark_ht40 = 0;
  int nquarks_accepted = 0; float quark_accepted_ht40 = 0;
  int nbquarks = 0;
  for (int i = 0; i < 2; ++i) {
    int ntracks = 0;
    float sumpt = 0;
    for (const reco::GenParticle* p : partons[i]) {
      ++npartons; if (p->pt() > 40) parton_ht40 += p->pt();
      if (is_quark(p)) {++nquarks; if (p->pt() > 40) quark_ht40 += p->pt();}

      if (p->pt() > 20 && fabs(p->eta()) < 2.5) {
        ++npartons_accepted; if (p->pt() > 40) parton_accepted_ht40 += p->pt();
        if (is_quark(p)) {++nquarks_accepted; if (p->pt() > 40) quark_accepted_ht40 += p->pt();}

        float dxy = fabs(dbv[i] * sin(p->phi() - atan2(v[i][1], v[i][0])));
        h_gen_dxy->Fill(dxy);
        if (dxy >= 0.01) {
          ++ntracks;
          sumpt += p->pt();
          if (abs(p->pdgId()) == 5) ++nbquarks;
        }
      }
    }
    h_gen_ntracks->Fill(ntracks);
    h_gen_sumpt->Fill(sumpt);
    h_gen_dbv->Fill(dbv[i]);
  }
  h_gen_parton_njets->Fill(npartons);
  h_gen_parton_ht40->Fill(parton_ht40);
  h_gen_parton_accepted_njets->Fill(npartons_accepted);
  h_gen_parton_accepted_ht40->Fill(parton_accepted_ht40);
  h_gen_quark_njets->Fill(nquarks);
  h_gen_quark_ht40->Fill(quark_ht40);
  h_gen_quark_accepted_njets->Fill(nquarks_accepted);
  h_gen_quark_accepted_ht40->Fill(quark_accepted_ht40);
  h_gen_nbquarks->Fill(nbquarks);
  h_gen_dvv->Fill(dvv);

  //plot reconstructed-level variables
  h_rec_njets->Fill(mevent->njets());
  h_rec_ht40->Fill(mevent->jet_ht(40));
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

  //plot reconstructed-level vs. generator-level variables
  h_rec_v_gen_njets->Fill(nquarks_accepted, mevent->njets());
  h_rec_v_gen_ht40->Fill(quark_accepted_ht40, mevent->jet_ht(40));

  //match jets to partons
  if (verbose) printf("\nrun = %u, lumi = %u, event = %llu: number of accepted quarks = %d, number of jets = %d, generated HT(40) = %.2f GeV, reconstructed HT(40) = %.2f GeV\n", event.id().run(), event.luminosityBlock(), event.id().event(), nquarks_accepted, mevent->njets(), quark_accepted_ht40, mevent->jet_ht(40));
  for (int i = 0; i < 2; ++i) {
    for (const reco::GenParticle* p : partons[i]) {
      if (verbose) printf("\tparton pdgId %3d: pT = %6.2f GeV, eta = %5.2f, phi = %5.2f", p->pdgId(), p->pt(), p->eta(), p->phi());
      for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
        float deltaR = reco::deltaR(p->eta(), p->phi(), mevent->jet_eta[ijet], mevent->jet_phi[ijet]);
        if (deltaR < 0.4) {
          if (verbose) printf("\tjet %2d: pT = %6.2f GeV, eta = %5.2f, phi = %5.2f, deltaR(parton, jet) = %4.2f", int(ijet), mevent->jet_pt[ijet], mevent->jet_eta[ijet], mevent->jet_phi[ijet], deltaR);
          if (p->pt() > 20 && fabs(p->eta()) < 2.5 && is_quark(p)) {
            h_rec_v_gen_jet_pt->Fill(p->pt(), mevent->jet_pt[ijet]);
            if (p->pt() > 40 && mevent->jet_pt[ijet] > 40) h_rec_v_gen_jet_pt40->Fill(p->pt(), mevent->jet_pt[ijet]);
          }
        }
      }
      if (verbose) printf("\n");
    }
  }

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

    h_dist->Fill(dist);
    h_ddbv->Fill(mevent->bs2ddist(vtx) - dbv[ilsp]);
    h_dphi->Fill(reco::deltaPhi(atan2(vtx.y - mevent->bsy, vtx.x - mevent->bsx), atan2(v[ilsp][1], v[ilsp][0])));
    ++lsp_nmatch[ilsp];

    int ntracks = 0;
    float sumpt = 0;
    for (const reco::GenParticle* p : partons[ilsp]) {
      if (p->pt() > 20 && fabs(p->eta()) < 2.5) {
        float dxy = fabs(dbv[ilsp] * sin(p->phi() - atan2(v[ilsp][1], v[ilsp][0])));
        h_gen_match_dxy->Fill(dxy);
        if (dxy >= 0.01) {
          ++ntracks;
          sumpt += p->pt();
        }
      }
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

  for (int i = 0; i < 2; ++i) {
    h_lspsnmatch->Fill(lsp_nmatch[i]);
  }

  if (lsp_nmatch[0] + lsp_nmatch[1] >= 2) {
    h_gen_match_dvv->Fill(dvv);
    h_rec_match_dvv->Fill(mag(vertices->at(0).x - vertices->at(1).x, vertices->at(0).y - vertices->at(1).y));
  }
}

DEFINE_FWK_MODULE(MFVTheoristRecipe);
