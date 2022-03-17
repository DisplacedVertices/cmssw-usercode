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
  const int require_L1;
  const int min_filtjets;
  const double min_filtjetpt;
  const double max_filtjeteta;
  const double min_filtjetbscore;
  const double min_pt_for_deta;
  const double min_pt_for_bfilter;

  TH1F* h_hlt_bits;
  TH1F* h_l1_bits;
  TH1F* h_filter_bits;

  TH2F* h_jet_pt[MAX_NJETS+1];
  TH2F* h_jet_energy;
  TH2F* h_jet_ht;
  TH2F* h_jet_ht_40;
  TH2F* h_jet_maxdeta;
  TH2F* h_jet_mindeta;

  TH2F* h_calo_jet_pt[MAX_NJETS+1];
  TH2F* h_calo_jet_energy;
  TH2F* h_calo_jet_ht;
  TH2F* h_calo_jet_ht_40;

  TH2F* h_thresh_jet_bsc[MAX_NJETS+1];
  TH2F* h_thresh_jet_old_bsc[MAX_NJETS+1];

  TH2F* h_bdisc_0;
  TH2F* h_bdisc_1;
  TH2F* h_pt_by_bdisc_0;
  TH2F* h_pt_by_bdisc_1;
  TH2F* h_threshold_bdisc_0;
  TH2F* h_threshold_bdisc_1;

  TH2F* h_old_bdisc_0;
  TH2F* h_old_bdisc_1;
  TH2F* h_pt_by_old_bdisc_0;
  TH2F* h_pt_by_old_bdisc_1;
  TH2F* h_threshold_old_bdisc_0;
  TH2F* h_threshold_old_bdisc_1;

};

MFVFilterHistos::MFVFilterHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    require_L1(cfg.getParameter<int>("require_L1")),
    min_filtjets(cfg.getParameter<int>("min_filtjets")),
    min_filtjetpt(cfg.getParameter<double>("min_filtjetpt")),
    max_filtjeteta(cfg.getParameter<double>("max_filtjeteta")),
    min_filtjetbscore(cfg.getParameter<double>("min_filtjetbscore")),
    min_pt_for_deta(cfg.getParameter<double>("min_pt_for_deta")),
    min_pt_for_bfilter(cfg.getParameter<double>("min_pt_for_bfilter"))
    
{
  edm::Service<TFileService> fs;

 
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  h_hlt_bits = fs->make<TH1F>("h_hlt_bits", ";;events", 2*mfv::n_hlt_paths+1, 0, 2*mfv::n_hlt_paths+1);
  h_l1_bits  = fs->make<TH1F>("h_l1_bits",  ";;events", 2*mfv::n_l1_paths +1, 0, 2*mfv::n_l1_paths +1);
  h_filter_bits  = fs->make<TH1F>("h_filter_bits",  ";;events", mfv::n_filter_paths +1, 0, mfv::n_filter_paths +1);

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
  }

  for (int i = 0; i < MAX_NJETS+1; ++i) {

    TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
    h_jet_pt[i] = fs->make<TH2F>(TString::Format("h_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of jet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    //h_jet_eta[i] = fs->make<TH2F>(TString::Format("h_jet_eta_%s", ijet.Data()), TString::Format(";;eta of jet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, -3, 3);
    //h_jet_phi[i] = fs->make<TH2F>(TString::Format("h_jet_phi_%s", ijet.Data()), TString::Format(";;phi of jet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, -3.1416, 3.1416);

    h_calo_jet_pt[i] = fs->make<TH2F>(TString::Format("h_calo_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of calojet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    //h_calo_jet_eta[i] = fs->make<TH2F>(TString::Format("h_calo_jet_eta_%s", ijet.Data()), TString::Format(";;eta of calojet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 120, -3, 3);
    //h_calo_jet_phi[i] = fs->make<TH2F>(TString::Format("h_calo_jet_phi_%s", ijet.Data()), TString::Format(";;phi of calojet #%s", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 100, -3.1416, 3.1416);

    //h_thresh_jet_pt[i] = fs->make<TH2F>(TString::Format( "h_thresh_jet_pt_%s", ijet.Data()), TString::Format(";;p_{T} of thresholdjet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
    h_thresh_jet_bsc[i] = fs->make<TH2F>(TString::Format( "h_thresh_jet_bsc_%s", ijet.Data()), TString::Format(";;DeepCSV of thresholdjet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 20, 0, 1.0);
    h_thresh_jet_old_bsc[i] = fs->make<TH2F>(TString::Format( "h_thresh_jet_old_bsc_%s", ijet.Data()), TString::Format(";;CSVv2 of thresholdjet #%s (GeV)", ijet.Data()), 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 20, 0, 1.0);
  }

  h_jet_energy = fs->make<TH2F>("h_jet_energy", ";;jets energy (GeV)", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_jet_ht = fs->make<TH2F>("h_jet_ht", ";;H_{T} of jets", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_jet_ht_40 = fs->make<TH2F>("h_jet_ht_40", ";;H_{T} of jets with p_{T} > 40 GeV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_jet_maxdeta = fs->make<TH2F>("h_jet_maxdeta", ";;max deta btwn jets passing filter", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 63, 0, 6.28);
  h_jet_mindeta = fs->make<TH2F>("h_jet_mindeta", ";;min deta btwn jets passing filter", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 63, 0, 6.28);

  h_calo_jet_energy = fs->make<TH2F>("h_calo_jet_energy", ";;calojets energy (GeV)", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_calo_jet_ht = fs->make<TH2F>("h_calo_jet_ht", ";;H_{T} of calojets", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);
  h_calo_jet_ht_40 = fs->make<TH2F>("h_calo_jet_ht_40", ";;H_{T} of calojets with p_{T} > 40 GeV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 300, 0, 1200);

  h_bdisc_0 = fs->make<TH2F>("h_bdisc_0", ";;max jet DeepCSV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);
  h_bdisc_1 = fs->make<TH2F>("h_bdisc_1", ";;2nd largest jet DeepCSV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);

  h_pt_by_bdisc_0 = fs->make<TH2F>("h_pt_by_bdisc_0", ";;pT of jet with max jet DeepCSV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
  h_pt_by_bdisc_1 = fs->make<TH2F>("h_pt_by_bdisc_1", ";;pT of jet with 2nd largest jet DeepCSV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);

  h_threshold_bdisc_0 = fs->make<TH2F>("h_threshold_bdisc_0", ";;max ThresholdJet DeepCSV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);
  h_threshold_bdisc_1 = fs->make<TH2F>("h_threshold_bdisc_1", ";;2nd largest ThresholdJet DeepCSV", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);

  h_old_bdisc_0 = fs->make<TH2F>("h_old_bdisc_0", ";;max jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);
  h_old_bdisc_1 = fs->make<TH2F>("h_old_bdisc_1", ";;2nd largest jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);

  h_pt_by_old_bdisc_0 = fs->make<TH2F>("h_pt_by_old_bdisc_0", ";;pT of jet with max jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);
  h_pt_by_old_bdisc_1 = fs->make<TH2F>("h_pt_by_old_bdisc_1", ";;pT of jet with 2nd largest jet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 200, 0, 400);

  h_threshold_old_bdisc_0 = fs->make<TH2F>("h_threshold_old_bdisc_0", ";;max ThresholdJet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);
  h_threshold_old_bdisc_1 = fs->make<TH2F>("h_threshold_old_bdisc_1", ";;2nd largest ThresholdJet CSVv2", 1+mfv::n_filter_paths, 0, 1+mfv::n_filter_paths, 50, 0, 1.0);

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  h_jet_energy->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_ht->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_ht_40->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_maxdeta->GetXaxis()->SetBinLabel(1, "no filter");
  h_jet_mindeta->GetXaxis()->SetBinLabel(1, "no filter");

  h_calo_jet_energy->GetXaxis()->SetBinLabel(1, "no filter");
  h_calo_jet_ht->GetXaxis()->SetBinLabel(1, "no filter");
  h_calo_jet_ht_40->GetXaxis()->SetBinLabel(1, "no filter");

  h_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");
  h_pt_by_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_pt_by_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");
  h_threshold_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_threshold_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");

  h_old_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_old_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");
  h_pt_by_old_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_pt_by_old_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");
  h_threshold_old_bdisc_0->GetXaxis()->SetBinLabel(1, "no filter");
  h_threshold_old_bdisc_1->GetXaxis()->SetBinLabel(1, "no filter");

  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_jet_energy->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_ht->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_ht_40->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_maxdeta->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_jet_mindeta->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));

    h_calo_jet_energy->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_calo_jet_ht->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_calo_jet_ht_40->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));

    h_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_pt_by_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_pt_by_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_threshold_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_threshold_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));

    h_old_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_old_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_pt_by_old_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_pt_by_old_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_threshold_old_bdisc_0->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
    h_threshold_old_bdisc_1->GetXaxis()->SetBinLabel(i+2, TString::Format("  %s", mfv::filter_paths[i]));
  }

}

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void MFVFilterHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;

  float bscore_0 = 0.0;
  float bscore_1 = 0.0;
  float pt_by_bscore_0 = -1.0;
  float pt_by_bscore_1 = -1.0;
  float threshold_bscore_0 = -0.5;
  float threshold_bscore_1 = -0.5;

  float old_bscore_0 = 0.0;
  float old_bscore_1 = 0.0;
  float pt_by_old_bscore_0 = -1.0;
  float pt_by_old_bscore_1 = -1.0;
  float threshold_old_bscore_0 = -0.5;
  float threshold_old_bscore_1 = -0.5;

  float max_jetdeta = 0.0;
  float min_jetdeta = 9.9;
  int filtjet_passes = 0;
  std::vector<float> jet_bscores     = mevent->jet_bdisc;
  std::vector<float> jet_bscores_old = mevent->jet_bdisc_old;

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
  }


  // Negatively-weighted events throw off future code. Disable for now
  // Also, if no b-tagged jets, skip
  if ((w < 0) || (std::size(jet_bscores_old) == 0)) return;

  for (int i = 0; i < MAX_NJETS; ++i) {
    float filtjet_pt = mevent->nth_jet_pt(i);
    float filtjet_abseta = fabs(mevent->nth_jet_eta(i));
    float filtjet_bscore = jet_bscores[i]; // This line is breaking??
    float filtjet_old_bscore = jet_bscores_old[i]; // This line is breaking??

    if (filtjet_pt > min_pt_for_bfilter) { 
      if (filtjet_bscore > threshold_bscore_0){
        threshold_bscore_1 = threshold_bscore_0;
        threshold_bscore_0 = filtjet_bscore;
      }

      if (filtjet_old_bscore > threshold_old_bscore_0){
        threshold_old_bscore_1 = threshold_old_bscore_0;
        threshold_old_bscore_0 = filtjet_old_bscore;
      }
    }

    if (filtjet_bscore > bscore_0) {
      bscore_1 = bscore_0;
      bscore_0 = filtjet_bscore;

      pt_by_bscore_1 = pt_by_bscore_0;
      pt_by_bscore_0 = filtjet_pt;
    }

    if (filtjet_old_bscore > bscore_0) {
      old_bscore_1 = old_bscore_0;
      old_bscore_0 = filtjet_old_bscore;

      pt_by_old_bscore_1 = pt_by_old_bscore_0;
      pt_by_old_bscore_0 = filtjet_pt;
    }


    // Also, calculate max jet deta
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

    // Ensure that the event passes some minimum cuts.
    if ((filtjet_pt > min_filtjetpt) && (filtjet_abseta < max_filtjeteta) && (filtjet_old_bscore > min_filtjetbscore)) // Do we use old_bscore or just bscore?
      filtjet_passes++;
  }

  if (filtjet_passes < min_filtjets)
    return;

  for (int i = -1; i < mfv::n_filter_paths; ++i){
    bool passes_seq_filters = true;

    //l1 bit number 18 corresponds to L1 trigger for HLT_PFHT300PT30_QuadPFJet_75_60_45_40
    //l1 bit number 20 corresponds to L1 trigger for di-bjet trigger
    if ( (require_L1 != 0) and (not mevent->pass_l1(require_L1)) ) passes_seq_filters = false;

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
        if (not mevent->pass_filter(j)) {
          passes_seq_filters = false;
        }
      }
    }

    if (passes_seq_filters) {
      for (int k = 0; k < MAX_NJETS; ++k) {
        h_jet_pt[k]->Fill(i+1, mevent->nth_jet_pt(k), w);
        //h_jet_eta[k]->Fill(i+1, mevent->nth_jet_eta(k), w);
        //h_jet_phi[k]->Fill(i+1, mevent->nth_jet_phi(k), w);
        
        if (mevent->nth_jet_pt(k) > min_pt_for_bfilter) {
          h_thresh_jet_bsc[k]->Fill(i+1, jet_bscores[k], w);
          h_thresh_jet_old_bsc[k]->Fill(i+1, jet_bscores_old[k], w);
        }
        else {
          h_thresh_jet_bsc[k]->Fill(i+1, -999.0, w);
          h_thresh_jet_old_bsc[k]->Fill(i+1, -999.0, w);
        }

        if (mevent->calo_jet_pt.size() == 0) continue;
        h_calo_jet_pt[k]->Fill(i+1, mevent->calo_jet_pt[k], w);
        //h_calo_jet_eta[k]->Fill(i+1, mevent->calo_jet_eta[k], w);
        //h_calo_jet_phi[k]->Fill(i+1, mevent->calo_jet_phi[k], w);
      }

      h_jet_ht->Fill(i+1, mevent->jet_ht(30), w);
      h_jet_ht_40->Fill(i+1, mevent->jet_ht(40), w);
      h_jet_maxdeta->Fill(i+1, max_jetdeta, w);
      h_jet_mindeta->Fill(i+1, min_jetdeta, w);

      h_calo_jet_ht->Fill(i+1, mevent->calo_jet_ht(30), w);
      h_calo_jet_ht_40->Fill(i+1, mevent->calo_jet_ht(40), w);

      h_bdisc_0->Fill(i+1, bscore_0, w);
      h_bdisc_1->Fill(i+1, bscore_1, w);

      h_old_bdisc_0->Fill(i+1, old_bscore_0, w);
      h_old_bdisc_1->Fill(i+1, old_bscore_1, w);

      if (bscore_0 > 0.85)
        h_pt_by_bdisc_0->Fill(i+1, pt_by_bscore_0, w);
      else
        h_pt_by_bdisc_0->Fill(i+1, -1.0, w);

      if (bscore_1 > 0.85)
        h_pt_by_bdisc_1->Fill(i+1, pt_by_bscore_1, w);
      else
        h_pt_by_bdisc_1->Fill(i+1, -1.0, w);

      if (old_bscore_0 > 0.85)
        h_pt_by_old_bdisc_0->Fill(i+1, pt_by_old_bscore_0, w);
      else
        h_pt_by_old_bdisc_0->Fill(i+1, -1.0, w);

      if (bscore_1 > 0.85)
        h_pt_by_old_bdisc_1->Fill(i+1, pt_by_old_bscore_1, w);
      else
        h_pt_by_old_bdisc_1->Fill(i+1, -1.0, w);

      h_threshold_bdisc_0->Fill(i+1, threshold_bscore_0, w);
      h_threshold_bdisc_1->Fill(i+1, threshold_bscore_1, w);

      h_threshold_old_bdisc_0->Fill(i+1, threshold_old_bscore_0, w);
      h_threshold_old_bdisc_1->Fill(i+1, threshold_old_bscore_1, w);
    }
  }

}

DEFINE_FWK_MODULE(MFVFilterHistos);
