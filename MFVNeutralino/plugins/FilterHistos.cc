#include "TH2F.h"
#include "TH3F.h"
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
  const bool is_dibjet;

  const int di_bitL1;
  const int di_minfiltjets;
  const double di_minfiltjetpt;
  const double di_maxfiltjeteta;
  const double di_minfiltjetbdisc;

  const int tri_bitL1;
  const int tri_minfiltjets;
  const double tri_minfiltjetpt;
  const double tri_maxfiltjeteta;
  const double tri_minfiltjetbdisc;

  const double min_pt_for_deta;
  const double min_pt_for_bfilter;

  TH1F* h_hlt_bits;
  TH1F* h_l1_bits;
  TH1F* h_filter_bits;
  TH2F* h_filter_bit_matrix;
  TH2F* h_seqfilt_bit_matrix;

  TH2F* h_jet_pt[MAX_NJETS+1];
  TH2F* h_jet_eta[MAX_NJETS+1];

  TH2F* h_bsort_jet_pt[MAX_NJETS+1];
  TH2F* h_bsort_jet_eta[MAX_NJETS+1];
  TH2F* h_bsort_jet_csv[MAX_NJETS+1];

  TH2F* h_jet_energy;
  TH2F* h_jet_ht;
  TH2F* h_jet_ht_alt;
  TH2F* h_jet_ht_40;
  TH2F* h_jet_maxdeta;
  TH2F* h_jet_mindeta;

  TH3F* h_online_offline_pfjet_pt[MAX_NJETS+1];

  TH2F* h_calo_jet_pt[MAX_NJETS+1];
  TH2F* h_calo_jet_eta[MAX_NJETS+1];
  TH2F* h_calo_jet_energy;
  TH2F* h_calo_jet_ht;
  TH2F* h_calo_jet_ht_alt;
  TH2F* h_calo_jet_ht_40;

  TH2F* h_hlt_jet_pt[MAX_NJETS+1];
  TH2F* h_hlt_jet_eta[MAX_NJETS+1];
  TH2F* h_hlt_jet_ht;

  TH2F* h_hlt_calo_jet_pt[MAX_NJETS+1];
  TH2F* h_hlt_calo_jet_eta[MAX_NJETS+1];
  TH2F* h_hlt_calo_jet_ht;

  TH2F* h_bdisc_0;
  TH2F* h_bdisc_1;
  TH2F* h_bdisc_2;

  TH2F* h_thresh_bdisc_0;
  TH2F* h_thresh_bdisc_1;
  TH2F* h_thresh_bdisc_2;

  TH2F* h_old_bdisc_0;
  TH2F* h_old_bdisc_1;
  TH2F* h_old_bdisc_2;

  TH2F* h_thresh_old_bdisc_0;
  TH2F* h_thresh_old_bdisc_1;
  TH2F* h_thresh_old_bdisc_2;

};

MFVFilterHistos::MFVFilterHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    is_dibjet(cfg.getParameter<bool>("is_dibjet")),
    di_bitL1(cfg.getParameter<int>("di_bitL1")),
    di_minfiltjets(cfg.getParameter<int>("di_minfiltjets")),
    di_minfiltjetpt(cfg.getParameter<double>("di_minfiltjetpt")),
    di_maxfiltjeteta(cfg.getParameter<double>("di_maxfiltjeteta")),
    di_minfiltjetbdisc(cfg.getParameter<double>("di_minfiltjetbdisc")),
    tri_bitL1(cfg.getParameter<int>("tri_bitL1")),
    tri_minfiltjets(cfg.getParameter<int>("tri_minfiltjets")),
    tri_minfiltjetpt(cfg.getParameter<double>("tri_minfiltjetpt")),
    tri_maxfiltjeteta(cfg.getParameter<double>("tri_maxfiltjeteta")),
    tri_minfiltjetbdisc(cfg.getParameter<double>("tri_minfiltjetbdisc")),
    min_pt_for_deta(cfg.getParameter<double>("min_pt_for_deta")),
    min_pt_for_bfilter(cfg.getParameter<double>("min_pt_for_bfilter"))
    
{
  edm::Service<TFileService> fs;

 
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  h_hlt_bits = fs->make<TH1F>("h_hlt_bits", ";;events", 2*mfv::n_hlt_paths+1, 0, 2*mfv::n_hlt_paths+1);
  h_l1_bits  = fs->make<TH1F>("h_l1_bits",  ";;events", 2*mfv::n_l1_paths +1, 0, 2*mfv::n_l1_paths +1);
  h_filter_bits  = fs->make<TH1F>("h_filter_bits",  ";;events", mfv::n_filter_paths +1, 0, mfv::n_filter_paths +1);
  h_filter_bit_matrix = fs->make<TH2F>("h_filter_bit_matrix", ";;", mfv::n_filter_paths, 0, mfv::n_filter_paths, mfv::n_filter_paths, 0, mfv::n_filter_paths);
  h_seqfilt_bit_matrix = fs->make<TH2F>("h_seqfilt_bit_matrix", ";sequential;non-sequential", mfv::n_filter_paths, 0, mfv::n_filter_paths, mfv::n_filter_paths, 0, mfv::n_filter_paths);
  

  h_hlt_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::hlt_paths[i]));
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::hlt_paths[i]));
  }
  h_l1_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::l1_paths[i]));
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::l1_paths[i]));
  }

  h_filter_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_filter_bits->GetXaxis()->SetBinLabel(i+2, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_filter_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_filter_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_seqfilt_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_seqfilt_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
  }

  for (int i = 0; i < MAX_NJETS+1; ++i) {

    TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
    h_jet_pt[i] = fs->make<TH2F>(TString::Format("h_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of jet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    h_jet_eta[i] = fs->make<TH2F>(TString::Format("h_jet_eta_%s", ijet.Data()), TString::Format(";;abs #eta of jet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, 0, 6);

    h_bsort_jet_pt[i] = fs->make<TH2F>(TString::Format("h_bsort_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of jet  w/ #%s-highest CSV (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    h_bsort_jet_eta[i] = fs->make<TH2F>(TString::Format("h_bsort_jet_eta_%s", ijet.Data()), TString::Format(";;abs #eta of jet w/ #%s-highest CSV", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, 0, 6);
    h_bsort_jet_csv[i] = fs->make<TH2F>(TString::Format("h_bsort_jet_csv_%s", ijet.Data()), TString::Format(";;CSV of jet #%s-highest CSV", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);

    h_calo_jet_pt[i] = fs->make<TH2F>(TString::Format("h_calo_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of calojet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    h_calo_jet_eta[i] = fs->make<TH2F>(TString::Format("h_calo_jet_eta_%s", ijet.Data()), TString::Format(";;abs #eta of calojet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, 0, 6);

    h_hlt_jet_pt[i] = fs->make<TH2F>(TString::Format("h_hlt_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of HLT PF jet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    h_hlt_jet_eta[i] = fs->make<TH2F>(TString::Format("h_hlt_jet_eta_%s", ijet.Data()), TString::Format(";;abs #eta of HLT PF jet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, 0, 6);
    h_hlt_calo_jet_pt[i] = fs->make<TH2F>(TString::Format("h_hlt_calo_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of HLT calojet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    h_hlt_calo_jet_eta[i] = fs->make<TH2F>(TString::Format("h_hlt_calo_jet_eta_%s", ijet.Data()), TString::Format(";;abs #eta of HLT calojet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, 0, 6);

    h_online_offline_pfjet_pt[i] = fs->make<TH3F>(TString::Format("h_online_offline_pfjet_pt_%s", ijet.Data()), TString::Format(";p_{T} of online PF jet #%s (GeV); p_{T} of offline PF jet #%s (GeV)", ijet.Data(), ijet.Data()), 200, 0, 1000, 200, 0, 1000, 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths);
  }

  h_jet_energy = fs->make<TH2F>("h_jet_energy", ";;jets energy (GeV)", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_jet_ht = fs->make<TH2F>("h_jet_ht", ";;H_{T} of jets", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_jet_ht_alt = fs->make<TH2F>("h_jet_ht_alt", ";;H_{T} of jets with |#eta| < 2.5", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_jet_ht_40  = fs->make<TH2F>("h_jet_ht_40", ";;H_{T} of jets with p_{T} > 40 GeV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_jet_maxdeta = fs->make<TH2F>("h_jet_maxdeta", ";;max deta btwn jets passing filter", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 63, 0, 6.28);
  h_jet_mindeta = fs->make<TH2F>("h_jet_mindeta", ";;min deta btwn jets passing filter", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 63, 0, 6.28);

  h_calo_jet_energy = fs->make<TH2F>("h_calo_jet_energy", ";;calojets energy (GeV)", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_calo_jet_ht     = fs->make<TH2F>("h_calo_jet_ht", ";;H_{T} of calojets", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_calo_jet_ht_alt = fs->make<TH2F>("h_calo_jet_ht_alt", ";;H_{T} of calojets with |#eta| < 2.5", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_calo_jet_ht_40  = fs->make<TH2F>("h_calo_jet_ht_40", ";;H_{T} of calojets with p_{T} > 40 GeV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);

  h_hlt_jet_ht = fs->make<TH2F>("h_hlt_jet_ht", ";;H_{T} of HLT PF jets", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_hlt_calo_jet_ht = fs->make<TH2F>("h_hlt_calo_jet_ht", ";;H_{T} of HLT calojets", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);

  h_bdisc_0 = fs->make<TH2F>("h_bdisc_0", ";;max jet DeepFlavour", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);
  h_bdisc_1 = fs->make<TH2F>("h_bdisc_1", ";;2nd largest jet DeepFlavour", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);
  h_bdisc_2 = fs->make<TH2F>("h_bdisc_2", ";;3rd largest jet DeepFlavour", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);

  h_thresh_bdisc_0 = fs->make<TH2F>("h_thresh_bdisc_0", ";;max threshold jet DeepFlavour", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);
  h_thresh_bdisc_1 = fs->make<TH2F>("h_thresh_bdisc_1", ";;2nd largest threshold jet DeepFlavour", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);
  h_thresh_bdisc_2 = fs->make<TH2F>("h_thresh_bdisc_2", ";;3rd largest threshold jet DeepFlavour", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);

  h_old_bdisc_0 = fs->make<TH2F>("h_old_bdisc_0", ";;max jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);
  h_old_bdisc_1 = fs->make<TH2F>("h_old_bdisc_1", ";;2nd largest jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);
  h_old_bdisc_2 = fs->make<TH2F>("h_old_bdisc_2", ";;3rd largest jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);

  h_thresh_old_bdisc_0 = fs->make<TH2F>("h_thresh_old_bdisc_0", ";;max threshold jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);
  h_thresh_old_bdisc_1 = fs->make<TH2F>("h_thresh_old_bdisc_1", ";;2nd largest threshold jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);
  h_thresh_old_bdisc_2 = fs->make<TH2F>("h_thresh_old_bdisc_2", ";;3rd largest threshold jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, 0, 1.0);


  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  h_jet_energy->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_ht->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_ht_alt->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_ht_40->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_maxdeta->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_mindeta->GetXaxis()->SetBinLabel(1, "no filter");

  h_calo_jet_energy->GetXaxis()->SetBinLabel(1, "no filter");
  h_calo_jet_ht->GetXaxis()->SetBinLabel(1, "no filter");
  h_calo_jet_ht_alt->GetXaxis()->SetBinLabel(1, "no filter");
  h_calo_jet_ht_40->GetXaxis()->SetBinLabel(1, "no filter");

  h_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");

  h_old_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_old_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");
  h_old_bdisc_2->GetXaxis()->SetBinLabel(1, "no filter");

  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_jet_energy->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_ht->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_ht_alt->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_ht_40->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_maxdeta->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_mindeta->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));

    h_calo_jet_energy->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_calo_jet_ht_alt->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_calo_jet_ht_40->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));

    h_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));

    h_old_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_old_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_old_bdisc_2->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
  }

}

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct Jet_BHelper {
    float pt  = 0.0;
    float eta = 0.0;
    float phi = 0.0;
    float csv = 0.0;
};

void MFVFilterHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;

  // Get copy of jets sorted by bscore
  Jet_BHelper jetHelper[MAX_NJETS];
  for (int i=0; i < MAX_NJETS; i++) {
    jetHelper[i].pt  = mevent->nth_jet_pt(i);
    jetHelper[i].eta = mevent->nth_jet_eta(i);
    jetHelper[i].phi = mevent->nth_jet_phi(i);
    jetHelper[i].csv = (i < (int)(mevent->jet_bdisc_old.size()) ? mevent->jet_bdisc_old[i] : -9.9);
  }
  std::sort(jetHelper, jetHelper+MAX_NJETS, [](Jet_BHelper const &a, Jet_BHelper &b) -> bool{ return a.csv > b.csv; } );

  // Shaun FIXME  -- Avoid events with poor online CaloHT
  //if (not (mevent->pass_filter(4) and mevent->pass_filter(5))) return;

  // Shaun FIXME  -- Only plot events which LOOK like the pass the hltBTagCaloCSV filter (filt #6), but don't
  //if ((mevent->pass_filter(6)) or (jetHelper[1].csv < 0.5))
  //  return;

  // Shaun FIXME  -- Only plot events which LOOK like they pass the hltBTagPFCSV filter (filt #13), but don't
  //if ((mevent->pass_filter(13)) or (jetHelper[2].csv < 0.7))
  //  return;

  // Shaun FIXME  -- Only plot events which LOOK like they pass the hltBTagPFCSV filter (filt #13), AND DO
  //if not ((mevent->pass_filter(13)) and (jetHelper[2].csv > 0.7)) 
  //  return;

  // Shaun FIXME  -- Only plot events which LOOK like they pass the hltBTagCaloCSV filter (filt #6), AND DO
  //if (not ((mevent->pass_filter(6)) and (jetHelper[1].csv > 0.5)))
  //  return;

  int require_L1  = is_dibjet ? di_bitL1 : tri_bitL1;
  int min_filtjets        = is_dibjet ? di_minfiltjets : tri_minfiltjets;
  float min_filtjetpt     = is_dibjet ? di_minfiltjetpt : tri_minfiltjetpt;
  float max_filtjeteta    = is_dibjet ? di_maxfiltjeteta : tri_maxfiltjeteta;
  float min_filtjetbscore = is_dibjet ? di_minfiltjetbdisc : tri_minfiltjetbdisc;

  const int nhltpfjets = mevent->hlt_pf_jet_pt.size();
  const int nhltcalojets = mevent->hlt_calo_jet_pt.size();

  float alt_pf_ht = 0.0;
  float alt_calo_ht = 0.0;

  float max_jetdeta = 0.0;
  float min_jetdeta = 9.9;
  int filtjet_passes = 0;
  int calofiltjet_passes = 0;
  std::vector<float> jet_bscores     = mevent->jet_bdisc;
  std::vector<float> jet_bscores_old = mevent->jet_bdisc_old;
  std::vector<float> thresh_bscores;
  std::vector<float> thresh_bscores_old;
  sort(jet_bscores_old.begin(), jet_bscores_old.end(), std::greater<float>());

  // Fill some basic hltbits/L1bits/filtbits histograms
  h_hlt_bits->Fill(0., w);
  h_l1_bits->Fill(0., w);
  h_filter_bits->Fill(0., w);
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    if (mevent->found_hlt(i)) h_hlt_bits->Fill(1+2*i,   w);
    if (mevent->pass_hlt (i)) h_hlt_bits->Fill(1+2*i+1, w);
  }
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    if (mevent->found_l1(i)) h_l1_bits->Fill(1+2*i,   w);
    if (mevent->pass_l1 (i)) h_l1_bits->Fill(1+2*i+1, w);
  }
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    if (mevent->pass_filter (i)) h_filter_bits->Fill(i+1, w);

    for (int j = 0; j < mfv::n_filter_paths; ++j) {
      if (mevent->pass_filter(i) and mevent->pass_filter(j)) {
        h_filter_bit_matrix->Fill(i, j, w);
      }
    }
  }


  // Ignore events with no bscores
  if ((std::size(jet_bscores) == 0)) return;

  for (int i = 0; i < MAX_NJETS; ++i) {
    float filtjet_pt = mevent->nth_jet_pt(i);
    float filtjet_abseta = fabs(mevent->nth_jet_eta(i));
    float filtjet_bscore = jet_bscores[i];

    // Also, calculate max and min jet deta
    if (filtjet_pt > min_pt_for_deta) {
      for (int j = i+1; j < MAX_NJETS; ++j) {
        if (mevent->nth_jet_pt(j) < min_pt_for_deta) continue;

        float temp_deta = fabs(mevent->nth_jet_eta(i) - mevent->nth_jet_eta(j));
        if (temp_deta > max_jetdeta) 
          max_jetdeta = temp_deta;

        if (temp_deta < min_jetdeta) 
          min_jetdeta = temp_deta;
      }
    }

    // Let's call a jet with |eta| < 2.5 and pT > 30 a 'threshold jet'
    // Find the HT of these threshold jets, and record their bscores.
    if ((mevent->nth_jet_pt(i) > 30.0) and (fabs(mevent->nth_jet_eta(i)) < 2.5)) {
        alt_pf_ht += mevent->nth_jet_pt(i);
        thresh_bscores.push_back(jet_bscores[i]);
        thresh_bscores_old.push_back(jet_bscores_old[i]);
    }

    // Ensure that the event passes some minimum cuts.
    if ((filtjet_pt > min_filtjetpt) && (filtjet_abseta < max_filtjeteta) && (filtjet_bscore > min_filtjetbscore)) // Do we use old_bscore or just bscore?
      filtjet_passes++;
  }

  // Do some more sorting of bscore lists
  sort(jet_bscores.begin(), jet_bscores.end(), std::greater<float>());
  sort(thresh_bscores.begin(), thresh_bscores.end(), std::greater<float>());
  sort(thresh_bscores_old.begin(), thresh_bscores_old.end(), std::greater<float>());

  // Calculate alternate CaloHT (|eta| < 2.5), and cound how many decent calojets we have
  for (int i = 0, icjets = mevent->calo_jet_pt.size(); i < icjets; i++) {
    if ((mevent->calo_jet_pt[i] > 30.0) and (fabs(mevent->calo_jet_eta[i]) < 2.5)) alt_calo_ht += mevent->calo_jet_pt[i];
    if ((mevent->calo_jet_pt[i] > min_filtjetpt) and (fabs(mevent->calo_jet_eta[i]) < max_filtjeteta)) calofiltjet_passes++;
  }


  // Don't do anything else if we don't have enough good jets or calojets
  if ((filtjet_passes < min_filtjets))// or (calofiltjet_passes < min_filtjets))
    return;

  // Begin loop that sees if the event passes a filter and fills 2D histograms
  for (int i = -1; i < mfv::n_filter_paths; ++i){
    bool passes_seq_filters = true;

    // See if event passes @ L1
    if ( (require_L1 != 0) and (not mevent->pass_l1(require_L1)) ) passes_seq_filters = false;

    // Does this event pass sequential di-bjet filters?
    else if (i > -1 and i < 4) {
      for (int j = 0; j <= i; ++j){
        if (not mevent->pass_filter(j))
          passes_seq_filters = false;
      }
    }

    // Duplicate of above conditional block. This is a kludge-y way of separating filters
    // into those that make up the tri- and di-bjet triggers. Di-bjet: [0-3], Tri-bjet: [4-13]
    // FIXME SHAUN, is there a more compact way of doing this?
    else {
      for (int j = 4; j <= i; ++j) {
        int jtemp = j;
        if ((jtemp >= 6) and (jtemp < 13)) jtemp++;   // Skip the CaloBTag filter at first
        if (j == 12) jtemp = 6;                       // Then, place it back in the 2nd-to-last spot
        if (not mevent->pass_filter(jtemp)) {
          passes_seq_filters = false;
        }
      }
    }


    // All filters on calojets only consider jets with |eta| < 2.5, 2.4, or 2.3  -  thus, we
    // need an offset that will help us fill histograms only with such jets
    int calojet_offset = 0;

    // If the event passes filters in series, then fill the 2D histograms appropriately
    if (passes_seq_filters) {
      for (int k = 0; k < MAX_NJETS; ++k) {
        h_jet_pt[k]->Fill(i+1, mevent->nth_jet_pt(k), w);
        h_jet_eta[k]->Fill(i+1, fabs(mevent->nth_jet_eta(k)), w);

        h_bsort_jet_pt[k]->Fill(i+1, jetHelper[k].pt, w);
        h_bsort_jet_eta[k]->Fill(i+1, fabs(jetHelper[k].eta), w);
        h_bsort_jet_eta[k]->Fill(i+1, jetHelper[k].csv, w);

        h_hlt_jet_pt[k]->Fill(i+1, (nhltpfjets > k ? mevent->hlt_pf_jet_pt[k] : -1.0), w);         
        h_hlt_jet_eta[k]->Fill(i+1, (nhltpfjets > k ? fabs(mevent->hlt_pf_jet_eta[k]) : -1.0), w);

        h_hlt_calo_jet_pt[k]->Fill(i+1, (nhltcalojets > k ? mevent->hlt_calo_jet_pt[k] : -1.0), w);         
        h_hlt_calo_jet_eta[k]->Fill(i+1, (nhltcalojets > k ? fabs(mevent->hlt_calo_jet_eta[k]) : -1.0), w);

        h_online_offline_pfjet_pt[k]->Fill((nhltpfjets > k ? mevent->hlt_pf_jet_pt[k] : -1.0), mevent->nth_jet_pt(k), i+1, w);

        // Fill sequential filter bit matrix. Note that the fill indices are slightly different
        // i = sequential index.   n = non-sequential index
        for (int n=0; n < mfv::n_filter_paths; ++n) {
            if (mevent->pass_filter(n)) h_seqfilt_bit_matrix->Fill(i, n, w);
        }

        if (mevent->calo_jet_pt.size() == 0) continue;

        // This is where we check if the calojet has the right eta
        if (fabs(mevent->calo_jet_eta[k]) > max_filtjeteta) {
            calojet_offset++;
        }

        // Only fill the calojet plots if the eta is right. Be sure to offset
        else {
          h_calo_jet_pt[k - calojet_offset]->Fill(i+1, mevent->calo_jet_pt[k], w);
          h_calo_jet_eta[k - calojet_offset]->Fill(i+1, fabs(mevent->calo_jet_eta[k]), w);
        }
      }

      h_jet_ht->Fill(i+1, mevent->jet_ht(30), w);
      h_jet_ht_alt->Fill(i+1, alt_pf_ht, w);
      h_jet_ht_40->Fill(i+1, mevent->jet_ht(40), w);
      h_jet_maxdeta->Fill(i+1, max_jetdeta, w);
      h_jet_mindeta->Fill(i+1, min_jetdeta, w);

      h_calo_jet_ht->Fill(i+1, mevent->calo_jet_ht(30), w);
      h_calo_jet_ht_alt->Fill(i+1, alt_calo_ht, w);
      h_calo_jet_ht_40->Fill(i+1, mevent->calo_jet_ht(40), w);

      h_hlt_calo_jet_ht->Fill(i+1, mevent->hlt_caloht, w);
      h_hlt_jet_ht->Fill(i+1, mevent->hlt_ht, w);

      h_bdisc_0->Fill(i+1, jet_bscores[0], w);
      h_bdisc_1->Fill(i+1, jet_bscores[1], w);
      h_bdisc_2->Fill(i+1, jet_bscores[2], w);

      h_thresh_bdisc_0->Fill(i+1, (thresh_bscores.size() > 0 ? thresh_bscores[0] : -0.1), w);
      h_thresh_bdisc_1->Fill(i+1, (thresh_bscores.size() > 1 ? thresh_bscores[1] : -0.1), w);
      h_thresh_bdisc_2->Fill(i+1, (thresh_bscores.size() > 2 ? thresh_bscores[2] : -0.1), w);

      h_old_bdisc_0->Fill(i+1, jet_bscores_old[0], w);
      h_old_bdisc_1->Fill(i+1, jet_bscores_old[1], w);
      h_old_bdisc_2->Fill(i+1, jet_bscores_old[2], w);

      h_thresh_old_bdisc_0->Fill(i+1, (thresh_bscores_old.size() > 0 ? thresh_bscores_old[0] : -0.1), w);
      h_thresh_old_bdisc_1->Fill(i+1, (thresh_bscores_old.size() > 1 ? thresh_bscores_old[1] : -0.1), w);
      h_thresh_old_bdisc_2->Fill(i+1, (thresh_bscores_old.size() > 2 ? thresh_bscores_old[2] : -0.1), w);

    }
  }

}

DEFINE_FWK_MODULE(MFVFilterHistos);
