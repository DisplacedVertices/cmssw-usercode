#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralino/interface/Event.h"

class MFVEventHistos : public edm::EDAnalyzer {
 public:
  explicit MFVEventHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag mfv_event_src;

  TH2F* h_gen_decay;
  TH1F* h_gen_partons_in_acc;

  TH1F* h_minlspdist2d;
  TH1F* h_lspdist2d;
  TH1F* h_lspdist3d;

  TH1F* h_pass_trigger[MFVEvent::n_trigger_paths];

  TH1F* h_npfjets;
  TH1F* h_pfjetpt4;
  TH1F* h_pfjetpt5;
  TH1F* h_pfjetpt6;

  TH1F* h_npu;

  TH1F* h_bsx;
  TH1F* h_bsy;
  TH1F* h_bsz;

  TH1F* h_npv;
  TH1F* h_pvx;
  TH1F* h_pvy;
  TH1F* h_pvz;
  TH1F* h_pv_ntracks;
  TH1F* h_pv_sumpt2;
  TH1F* h_pv_rho;

  TH1F* h_njets;
  TH1F* h_jetpt4;
  TH1F* h_jetpt5;
  TH1F* h_jetpt6;
  TH1F* h_jet_sum_ht;
  TH1F* h_nbtags;
  TH1F* h_nmuons[3];
  TH1F* h_nelectrons[3];
  TH1F* h_nleptons[3];
};

MFVEventHistos::MFVEventHistos(const edm::ParameterSet& cfg)
  : mfv_event_src(cfg.getParameter<edm::InputTag>("mfv_event_src"))
{
  edm::Service<TFileService> fs;

  h_gen_decay = fs->make<TH2F>("h_gen_decay", "0-2=e,mu,tau, 3=h;decay code #0;decay code #1", 4, 0, 4, 4, 0, 4);
  h_gen_partons_in_acc = fs->make<TH1F>("h_gen_partons_in_acc", ";# partons from LSP in acceptance;events", 10, 0, 10);

  h_minlspdist2d = fs->make<TH1F>("h_minlspdist2d", ";min dist2d(gen vtx #i) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist2d = fs->make<TH1F>("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist3d = fs->make<TH1F>("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);

  for (int i = 0; i < MFVEvent::n_trigger_paths; ++i)
    h_pass_trigger[i] = fs->make<TH1F>(TString::Format("h_pass_trigger_%i", i), TString::Format(";pass_trigger[%i];events", i), 2, 0, 2);

  h_npfjets = fs->make<TH1F>("h_npfjets", ";# of PF jets;events", 30, 0, 30);
  h_pfjetpt4 = fs->make<TH1F>("h_pfjetpt4", ";p_{T} of 4th PF jet (GeV);events/5 GeV", 100, 0, 500);
  h_pfjetpt5 = fs->make<TH1F>("h_pfjetpt5", ";p_{T} of 5th PF jet (GeV);events/5 GeV", 100, 0, 500);
  h_pfjetpt6 = fs->make<TH1F>("h_pfjetpt6", ";p_{T} of 6th PF jet (GeV);events/5 GeV", 100, 0, 500);

  h_npu = fs->make<TH1F>("h_npu", ";true nPU;events", 65, 0, 65);

  h_bsx = fs->make<TH1F>("h_bsx", ";beamspot x (cm);events/0.1 mm", 200, -1, 1);
  h_bsy = fs->make<TH1F>("h_bsy", ";beamspot y (cm);events/0.1 mm", 200, -1, 1);
  h_bsz = fs->make<TH1F>("h_bsz", ";beamspot z (cm);events/mm", 200, -10, 10);

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices;events", 65, 0, 65);
  h_pvx = fs->make<TH1F>("h_pvx", ";primary vertex x (cm);events/0.1 mm", 200, -1, 1);
  h_pvy = fs->make<TH1F>("h_pvy", ";primary vertex y (cm);events/0.1 mm", 200, -1, 1);
  h_pvz = fs->make<TH1F>("h_pvz", ";primary vertex z (cm);events/mm", 200, -10, 10);
  h_pv_ntracks = fs->make<TH1F>("h_pv_ntracks", ";# of tracks in primary vertex;events", 200, 0, 200);
  h_pv_sumpt2 = fs->make<TH1F>("h_pv_sumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/100 GeV^{2}", 200, 0, 20000);
  h_pv_rho = fs->make<TH1F>("h_pv_rho", ";PV rho (cm);events/0.1 mm", 200, 0, 2);

  h_njets = fs->make<TH1F>("h_njets", ";# of jets;events", 20, 0, 20);
  h_jetpt4 = fs->make<TH1F>("h_jetpt4", ";p_{T} of 4th jet (GeV);events/5 GeV", 100, 0, 500);
  h_jetpt5 = fs->make<TH1F>("h_jetpt5", ";p_{T} of 5th jet (GeV);events/5 GeV", 100, 0, 500);
  h_jetpt6 = fs->make<TH1F>("h_jetpt6", ";p_{T} of 6th jet (GeV);events/5 GeV", 100, 0, 500);
  h_jet_sum_ht = fs->make<TH1F>("h_jet_sum_ht", ";#Sigma H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_nbtags = fs->make<TH1F>("h_nbtags", ";# of b-tags;events", 20, 0, 20);

  const char* lep_ex[3] = {"veto", "semilep", "dilep"};
  for (int i = 0; i < 3; ++i) {
    h_nmuons[i] = fs->make<TH1F>(TString::Format("h_nmuons_%s", lep_ex[i]), TString::Format(";# of %s muons;events", lep_ex[i]), 5, 0, 5);
    h_nelectrons[i] = fs->make<TH1F>(TString::Format("h_nelectrons_%s", lep_ex[i]), TString::Format(";# of %s electrons;events", lep_ex[i]), 5, 0, 5);
    h_nleptons[i] = fs->make<TH1F>(TString::Format("h_nleptons_%s", lep_ex[i]), TString::Format(";# of %s leptons;events", lep_ex[i]), 5, 0, 5);
  }
}

void MFVEventHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mfv_event_src, mevent);

  h_gen_decay->Fill(mevent->gen_decay_type[0], mevent->gen_decay_type[1]);
  h_gen_partons_in_acc->Fill(mevent->gen_partons_in_acc);

  h_minlspdist2d->Fill(mevent->minlspdist2d());
  h_lspdist2d->Fill(mevent->lspdist2d());
  h_lspdist3d->Fill(mevent->lspdist3d());

  for (int i = 0; i < MFVEvent::n_trigger_paths; ++i)
    h_pass_trigger[i]->Fill(mevent->pass_trigger[i]);

  h_npfjets->Fill(mevent->npfjets);
  h_pfjetpt4->Fill(mevent->pfjetpt4);
  h_pfjetpt5->Fill(mevent->pfjetpt5);
  h_pfjetpt6->Fill(mevent->pfjetpt6);

  h_npu->Fill(mevent->npu);

  h_bsx->Fill(mevent->bsx);
  h_bsy->Fill(mevent->bsy);
  h_bsz->Fill(mevent->bsz);

  h_npv->Fill(mevent->npv);
  h_pvx->Fill(mevent->pvx);
  h_pvy->Fill(mevent->pvy);
  h_pvz->Fill(mevent->pvz);
  h_pv_ntracks->Fill(mevent->pv_ntracks);
  h_pv_sumpt2->Fill(mevent->pv_sumpt2);
  h_pv_rho->Fill(mevent->pv_rho());

  h_njets->Fill(mevent->njets);
  h_jetpt4->Fill(mevent->jetpt4);
  h_jetpt5->Fill(mevent->jetpt5);
  h_jetpt6->Fill(mevent->jetpt6);
  h_jet_sum_ht->Fill(mevent->jet_sum_ht);
  h_nbtags->Fill(mevent->nbtags);

  for (int i = 0; i < 3; ++i) {
    h_nmuons[i]->Fill(mevent->nmu[i]);
    h_nelectrons[i]->Fill(mevent->nel[i]);
    h_nleptons[i]->Fill(mevent->nlep(i));
  }
}

DEFINE_FWK_MODULE(MFVEventHistos);
