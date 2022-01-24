#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

class MFVFilterHistos : public edm::EDAnalyzer {
 public:
  explicit MFVFilterHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;


  static const int MAX_NJETS = 10;
  TH2F* h_jet_pt[MAX_NJETS+1];
  TH2F* h_jet_eta[MAX_NJETS+1];
  TH2F* h_jet_phi[MAX_NJETS+1];
  TH2F* h_jet_energy;
  TH2F* h_jet_ht;
  TH2F* h_jet_ht_40;

};

MFVFilterHistos::MFVFilterHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src")))
{
  edm::Service<TFileService> fs;

  for (int i = 0; i < MAX_NJETS+1; ++i) {
    TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
    h_jet_pt[i] = fs->make<TH2F>(TString::Format("h_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of jet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 2000);
    h_jet_eta[i] = fs->make<TH2F>(TString::Format("h_jet_eta_%s", ijet.Data()), TString::Format(";;eta of jet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, -3, 3);
    h_jet_phi[i] = fs->make<TH2F>(TString::Format("h_jet_phi_%s", ijet.Data()), TString::Format(";;phi of jet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, -3.1416, 3.1416);
  }

  h_jet_energy = fs->make<TH2F>("h_jet_energy", ";;jets energy (GeV)", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 2000);
  h_jet_ht = fs->make<TH2F>("h_jet_ht", ";;H_{T} of jetsevents/25 GeV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 5000);
  h_jet_ht_40 = fs->make<TH2F>("h_jet_ht_40", ";;H_{T} of jets with p_{T} > 40 GeV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 5000);

  h_jet_energy->GetXaxis()->SetBinLabel(1, "no filter");
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_jet_energy->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
  }

  h_jet_ht->GetXaxis()->SetBinLabel(1, "no filter");
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_jet_ht->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
  }

  h_jet_ht_40->GetXaxis()->SetBinLabel(1, "no filter");
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_jet_ht_40->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
  }

}




void MFVFilterHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;


  for (int i = -1; i < mfv::n_filter_paths; ++i){
    bool passes_seq_filters = true;
        for (int j = 0; j <= i; ++j){
          if (not mevent->pass_filter(j))
            passes_seq_filters = false;
        }

    if (passes_seq_filters) {
      for (int k = 0; k < MAX_NJETS; ++k) {
        h_jet_pt[k]->Fill(i+1, mevent->nth_jet_pt(k), w);
        h_jet_eta[k]->Fill(i+1, mevent->nth_jet_eta(k), w);
        h_jet_phi[k]->Fill(i+1, mevent->nth_jet_phi(k), w);
      }

      h_jet_ht->Fill(i+1, mevent->jet_ht(mfv::min_jet_pt), w);
      h_jet_ht_40->Fill(i+1, mevent->jet_ht(40), w);
    }
  }



}

DEFINE_FWK_MODULE(MFVFilterHistos);
