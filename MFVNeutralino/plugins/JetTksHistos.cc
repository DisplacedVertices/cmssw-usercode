#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

class MFVJetTksHistos : public edm::EDAnalyzer {
 public:
  explicit MFVJetTksHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<reco::GenParticleCollection> gen_token;

  TH1F* h_w;

  static const int CATEGORIES = 2;
  TH1F* h_jet_pt[CATEGORIES];
  TH1F* h_jet_eta[CATEGORIES];
  TH1F* h_jet_phi[CATEGORIES];
  TH1F* h_jet_ntks[CATEGORIES];
  TH1F* h_jet_bdisc[CATEGORIES];
  TH1F* h_jet_bdisc_old[CATEGORIES];

  TH1F* h_jet_tks_pt[CATEGORIES];  
  TH1F* h_jet_tks_pt_rel[CATEGORIES];  
  TH1F* h_jet_tks_eta[CATEGORIES];  
  TH1F* h_jet_tks_eta_rel[CATEGORIES];  
  TH1F* h_jet_tks_dR[CATEGORIES];  
  TH1F* h_jet_tks_nsigmadxy[CATEGORIES];  
  TH1F* h_jet_tks_nsigmadxyz[CATEGORIES];  

  TH1F* h_jet_sumtk_pt_ratio[CATEGORIES];
  TH1F* h_jet_sumtk_dR[CATEGORIES];
};

MFVJetTksHistos::MFVJetTksHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    gen_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_src")))

{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);


  for (int i = 0; i < CATEGORIES; ++i) {
    TString bres = i == 1 ? TString("fail") : TString("pass");
    h_jet_pt[i] = fs->make<TH1F>(TString::Format("h_jet_pt_%s", bres.Data()), TString::Format(";p_{T} of jets that %s b-tag(GeV);events/10 GeV", bres.Data()), 200, 0, 800);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", bres.Data()), TString::Format(";absv#eta of jets that %s b-tag;events/bin", bres.Data()), 120, 0, 2.5);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", bres.Data()), TString::Format(";#phi of jets that %s b-tag;events/bin", bres.Data()), 100, -3.1416, 3.1416);
    h_jet_ntks[i] = fs->make<TH1F>(TString::Format("h_jet_ntks_%s", bres.Data()), TString::Format(";#tks in jets that %s b-tag;events/bin", bres.Data()), 40, 0, 40);
    h_jet_bdisc[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_%s", bres.Data()), TString::Format(";DeepJet of jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.0);
    h_jet_bdisc_old[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_old_%s", bres.Data()), TString::Format(";CSV of jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.0);

    h_jet_tks_pt[i] = fs->make<TH1F>(TString::Format("h_jet_tks_pt_%s", bres.Data()), TString::Format(";p_{T} of tks in jets that %s b-tag (GeV);events/bin", bres.Data()), 200, 0, 40);
    h_jet_tks_pt_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_ptrel_%s", bres.Data()), TString::Format(";rel p_{T} of tks in jets that %s b-tag (GeV);events/bin", bres.Data()), 200, 0, 20);
    h_jet_tks_eta[i] = fs->make<TH1F>(TString::Format("h_jet_tks_eta_%s", bres.Data()), TString::Format(";abs #eta of tks in jets that %s b-tag;events/bin", bres.Data()), 100, 0, 4);
    h_jet_tks_eta_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_etarel_%s", bres.Data()), TString::Format(";rel #eta of tks in jets that %s b-tag;events/bin", bres.Data()), 300, 0, 10);
    h_jet_tks_dR[i] = fs->make<TH1F>(TString::Format("h_jet_tks_dR_%s", bres.Data()), TString::Format(";dR between jet and tks in jets - %s b-tag;events/bin", bres.Data()), 100, 0, 0.6);
    h_jet_tks_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxy_%s", bres.Data()), TString::Format("; n #sigma(dxy) of tks in jets which %s b-tag;events/bin", bres.Data()), 150, 0, 15);
    h_jet_tks_nsigmadxyz[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxyz_%s", bres.Data()), TString::Format("; n#sigma(dxyz) of tks in jets which %s b-tag;events/bin", bres.Data()), 150, 0, 15);

    h_jet_sumtk_pt_ratio[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_pt_ratio_%s", bres.Data()), TString::Format(";pT(jet tracks) / pT(jet) - %s b-tag;events/bin", bres.Data()), 100, 0, 4);
    h_jet_sumtk_dR[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_dR_%s", bres.Data()), TString::Format(";dR between jet and tks in jets - %s b-tag;events/bin", bres.Data()), 100, 0, 0.6);
  }

}

void MFVJetTksHistos::analyze(const edm::Event& event, const edm::EventSetup&) {

  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByToken(gen_token, gen_particles);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  float bcut = 0.7;

  h_w->Fill(w);

  //////////////////////////////////////////////////////////////////////////////

  for (int i = 0; i < mevent->njets(); ++i) {
    bool jet_has_qrk_match = false;
    float b      = (i < (int)(mevent->jet_bdisc_old.size()) ? mevent->jet_bdisc_old[i] : -9.9);
    int   n_hist = b > bcut ? 0 : (b > 0.0 ? 1 : -9);
    if (n_hist == -9) continue;
 
    TVector3 jet_vector;
    jet_vector.SetPtEtaPhi(mevent->nth_jet_pt(i), mevent->nth_jet_eta(i), mevent->nth_jet_phi(i));       
    jet_vector.SetMag(1.0);

    for (const reco::GenParticle& gen : *gen_particles) {
       if (abs(gen.pdgId()) != 1) continue;

       TVector3 qrk_vector;
       qrk_vector.SetPtEtaPhi(gen.pt(), gen.eta(), gen.phi());

       if ((qrk_vector.DeltaR(jet_vector) < 0.4) and (fabs(((gen.pt() - mevent->nth_jet_pt(i))/gen.pt())) < 0.2))
         jet_has_qrk_match = true;
       
    }
    
    if (not jet_has_qrk_match)
      continue;
    
    TVector3 jet_sumtk_vector;
    jet_sumtk_vector.SetPtEtaPhi(0.0, 0.0, 0.0);

    h_jet_pt[n_hist]->Fill(mevent->nth_jet_pt(i), w);
    h_jet_eta[n_hist]->Fill(fabs(mevent->nth_jet_eta(i)), w);
    h_jet_phi[n_hist]->Fill(mevent->nth_jet_phi(i), w);
    h_jet_ntks[n_hist]->Fill((int)(mevent->n_jet_tracks(i)));
    h_jet_bdisc[n_hist]->Fill((i < (int)(mevent->jet_bdisc.size()) ? mevent->jet_bdisc[i] : -9.9), w);
    h_jet_bdisc_old[n_hist]->Fill((i < (int)(mevent->jet_bdisc_old.size()) ? mevent->jet_bdisc_old[i] : -9.9), w);

    for (size_t ntk = 0 ; ntk < mevent->n_jet_tracks_all() ; ntk++) {
       if (mevent->jet_track_which_jet[ntk] == i) {

         // Vars needed to get 3D IP dist significance
         float dr = mevent->jet_track_dxy[ntk];
         float dz = mevent->jet_track_dz[ntk];
         float drerr = mevent->jet_track_dxy_err[ntk];
         float dzerr = mevent->jet_track_dz_err[ntk];

         // Calculate 3D IP dist significance
         float drz = std::hypot(dr, dz);
         float drzerr = std::hypot(dr*drerr/drz , dz*dzerr/drz);
         

         TVector3 tk_vector;
         tk_vector.SetPtEtaPhi(fabs(mevent->jet_track_qpt[ntk]), mevent->jet_track_eta[ntk], mevent->jet_track_phi[ntk]);

         jet_sumtk_vector += tk_vector;        

         float pt_rel = (tk_vector.Cross(jet_vector)).Mag();
         //float pt_rel = perp.Mag();
         float eta_rel = std::atanh( tk_vector.Dot(jet_vector) / tk_vector.Mag() );

         h_jet_tks_pt[n_hist]->Fill(fabs(mevent->jet_track_qpt[ntk]), w);
         h_jet_tks_pt_rel[n_hist]->Fill(pt_rel, w);
         h_jet_tks_eta[n_hist]->Fill(fabs(mevent->jet_track_eta[ntk]), w);
         h_jet_tks_eta_rel[n_hist]->Fill(eta_rel, w);
         h_jet_tks_dR[n_hist]->Fill(tk_vector.DeltaR(jet_vector), w);
         h_jet_tks_nsigmadxy[n_hist]->Fill(fabs(dr/drerr), w);
         h_jet_tks_nsigmadxyz[n_hist]->Fill(fabs(drz/drzerr), w);
       }
    }

    h_jet_sumtk_pt_ratio[n_hist]->Fill(mevent->nth_jet_pt(i) / jet_sumtk_vector.Pt(), w);
    h_jet_sumtk_dR[n_hist]->Fill(jet_vector.DeltaR(jet_sumtk_vector), w);
    
  }

  //////////////////////////////////////////////////////////////////////////////



}
DEFINE_FWK_MODULE(MFVJetTksHistos);
