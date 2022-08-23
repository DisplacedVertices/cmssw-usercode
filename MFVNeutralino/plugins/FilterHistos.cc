#include <bitset>
#include "TH2F.h"
#include "TH3F.h"
#include "TRandom3.h"
#include "TVector2.h"
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

  TH1F* h_jet_match_dR;
  TH1F* h_next_match_dR;

  TH1F* h_filt_nsurvive;
  TH1F* h_reused_jets;
  
  TH1F* h_filtjet_hlt_dR;

  TH1F* h_filter_07_den;
  TH1F* h_filter_07_num;

  TH1F* h_filter_08_den;
  TH1F* h_filter_08_num;

  TH1F* h_filter_09_den;
  TH1F* h_filter_09_num;

  TH1F* h_filter_10_den;
  TH1F* h_filter_10_num;

  TH1F* h_filter_11_den;
  TH1F* h_filter_11_num;

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

  h_jet_match_dR = fs->make<TH1F>("h_jet_match_dR", ";#DeltaR between matching HLT/offline jets;entries", 80, 0, 0.401);
  h_next_match_dR = fs->make<TH1F>("h_next_match_dR", ";#DeltaR between matching HLT jet and 2nd closest offline jet;entries", 80, 0, 0.401);


  h_filt_nsurvive = fs->make<TH1F>("h_filt_nsurvive", ";;nevents", mfv::n_filter_paths+3-4, 0, mfv::n_filter_paths+3-4);
  h_reused_jets = fs->make<TH1F>("h_reused_jets", ";reused offline jet in evt?; nevents", 2, 0, 1.1);
  

  //---------- Start setting some x-axis labels
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

  h_filt_nsurvive->GetXaxis()->SetBinLabel(1, "starting number");
  h_filt_nsurvive->GetXaxis()->SetBinLabel(2, "after filt. presel");
  h_filt_nsurvive->GetXaxis()->SetBinLabel(3, "after L1 trigger");

  h_reused_jets->GetXaxis()->SetBinLabel(1, "No");
  h_reused_jets->GetXaxis()->SetBinLabel(2, "Yes");
  
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_filter_bits->GetXaxis()->SetBinLabel(i+2, TString::Format(" pass %s", mfv::filter_paths[i]));
    if (i >= 4) {
      h_filt_nsurvive->GetXaxis()->SetBinLabel(i+4-4, TString::Format("pass %s", mfv::filter_paths[i]));
    }
    h_filter_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_filter_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_seqfilt_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_seqfilt_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
  }
  //---------- End setting some x-axis labels

  h_filtjet_hlt_dR = fs->make<TH1F>("h_filtjet_hlt_dR", ";#DeltaR between offline jet and matching HLT jet;entries", 100, 0.0, 1.0);

  h_filter_07_den = fs->make<TH1F>("h_filter_07_den", "before PFCentralLooseJetIDQuad30; p_{T} of 4th-leading jet (GeV); entries", 200, 0, 300);
  h_filter_07_num = fs->make<TH1F>("h_filter_07_num", "after  PFCentralLooseJetIDQuad30; p_{T} of 4th-leading jet (GeV); entries", 200, 0, 300);

  h_filter_08_den = fs->make<TH1F>("h_filter_08_den", "before 1PFCentralLooseJetID75; p_{T} of leading jet (GeV); entries", 200, 0, 300);
  h_filter_08_num = fs->make<TH1F>("h_filter_08_num", "after  1PFCentralLooseJetID75; p_{T} of leading jet (GeV); entries", 200, 0, 300);

  h_filter_09_den = fs->make<TH1F>("h_filter_09_den", "before 2PFCentralLooseJetID60; p_{T} of 2nd-leading jet (GeV); entries", 200, 0, 300);
  h_filter_09_num = fs->make<TH1F>("h_filter_09_num", "after  2PFCentralLooseJetID60; p_{T} of 2nd-leading jet (GeV); entries", 200, 0, 300);

  h_filter_10_den = fs->make<TH1F>("h_filter_10_den", "before 3PFCentralLooseJetID45; p_{T} of 3rd-leading jet (GeV); entries", 200, 0, 300);
  h_filter_10_num = fs->make<TH1F>("h_filter_10_num", "after  3PFCentralLooseJetID45; p_{T} of 3rd-leading jet (GeV); entries", 200, 0, 300);

  h_filter_11_den = fs->make<TH1F>("h_filter_11_den", "before 4PFCentralLooseJetID40; p_{T} of 4th-leading jet (GeV); entries", 200, 0, 300);
  h_filter_11_num = fs->make<TH1F>("h_filter_11_num", "after  4PFCentralLooseJetID40; p_{T} of 4th-leading jet (GeV); entries", 200, 0, 300);

}

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct Jet_Pair_Helper {
    float off_pt  = -1.0;
    float hlt_pt  = -1.0;
    float hlt_eta = -1.0;
    float hlt_phi = -1.0;
};

void MFVFilterHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  const int nhltpfjets = mevent->hlt_pf_jet_pt.size();
  const int nofflinepfjets = mevent->jet_pt.size();

  // Do some matching of online and offline jets
  std::vector<Jet_Pair_Helper> pfjethelper;
  bool skinny_cone = false;
  bool use_puid    = false;
  for (int i=0; i < nofflinepfjets; i++) {
    float off_eta = mevent->nth_jet_eta(i);
    float off_phi = mevent->nth_jet_phi(i);
    float off_pt  = mevent->nth_jet_pt(i);
    float off_pudisc = mevent->jet_pudisc[i];
    float match_pt  = 0.0;
    float match_eta = 0.0;
    float match_phi = 0.0;
    float match_dR  = 0.4;
    float next_dR   = -0.2;
    bool  ensure_match = false;

    if      ((use_puid) and (off_pt < 30.0) and (off_pudisc < 0.18)) continue;
    else if ((use_puid) and (off_pt < 50.0) and (off_pudisc < 0.61)) continue;    

    for (int j=0; j < nhltpfjets; j++) {
      bool  is_match = false;
      float hlt_eta    = mevent->hlt_pf_jet_eta[j];
      float hlt_phi    = mevent->hlt_pf_jet_phi[j];
      float hlt_pt     = mevent->hlt_pf_jet_pt[j];
    
      if (skinny_cone) { is_match = ((reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) and (off_pt > match_pt)); }
      else             { is_match = ((reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < match_dR)); }

      if (is_match) {
        match_pt  = hlt_pt;
        match_eta = hlt_eta;
        match_phi = hlt_phi;
        next_dR  = match_dR;
        match_dR = reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi);
        ensure_match = true;
      }
    }

    if (not ensure_match) continue;

    Jet_Pair_Helper temp_helper;
    temp_helper.hlt_pt  = match_pt;
    temp_helper.hlt_eta = match_eta;
    temp_helper.hlt_phi = match_phi;
    temp_helper.off_pt = off_pt;
    pfjethelper.push_back(temp_helper);

    h_jet_match_dR->Fill(match_dR, w);
    h_next_match_dR->Fill(next_dR, w);
  }

  // Initialize filter study preselection parameters
  int require_L1  = is_dibjet ? di_bitL1 : tri_bitL1;
  int min_filtjets        = is_dibjet ? di_minfiltjets : tri_minfiltjets;
  float min_filtjetpt     = is_dibjet ? di_minfiltjetpt : tri_minfiltjetpt;
  float max_filtjeteta    = is_dibjet ? di_maxfiltjeteta : tri_maxfiltjeteta;
  float min_filtjetbscore = is_dibjet ? di_minfiltjetbdisc : tri_minfiltjetbdisc;


  // Fill some basic hltbits/L1bits/filtbits histograms
  h_hlt_bits->Fill(0., w);
  h_l1_bits->Fill(0., w);
  h_filter_bits->Fill(0., w);
  h_filt_nsurvive->Fill(0., w);
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
  if ((std::size(mevent->jet_bdisc) == 0)) return;

  // Don't do anything else if we don't have enough good jets or calojets
  if (pfjethelper.size() >= 4) {
    h_filt_nsurvive->Fill(1, w);
  }
  else {
    return;
  }

  // See if an offline jet is the best match to multiple online jets
  int reused_jet = 0;
  for (unsigned int i=0; i < 3; i++) {
    float phi0 = pfjethelper[i].hlt_phi;
    float eta0 = pfjethelper[i].hlt_eta;
    for (unsigned int j=i+1; j < 4; j++) {
      float phi1 = pfjethelper[j].hlt_phi;
      float eta1 = pfjethelper[j].hlt_eta;
      float tmp_dR = reco::deltaR(eta0, phi0, eta1, phi1);

      if (tmp_dR < 0.01) {
        reused_jet = 1;
      } 
    }
  }
  h_reused_jets->Fill(reused_jet, w);

  h_filt_nsurvive->Fill(2, w);

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


  // We'll just take the easy way out for the first filters (for now)
  for (int i = 4; i < 7; i++) {
    if (not (mevent->pass_filter(i))) return;
    h_filt_nsurvive->Fill(i-1, w);
  }

  for (int i = 7; i < mfv::n_filter_paths; i++) {
    if (not (mevent->pass_filter(i))) break;
    h_filt_nsurvive->Fill(i-1, w);
  }

  h_filter_07_den->Fill(pfjethelper[3].off_pt, w);

  if (mevent->pass_filter(7)) {
  //if (pfjethelper[3].hlt_pt > 30.0) {
    h_filter_07_num->Fill(pfjethelper[3].off_pt, w);
    h_filter_08_den->Fill(pfjethelper[0].off_pt, w);

    if (mevent->pass_filter(8)) {
    //if (pfjethelper[0].hlt_pt > 75.0) {
      h_filter_08_num->Fill(pfjethelper[0].off_pt, w);
      h_filter_09_den->Fill(pfjethelper[1].off_pt, w);

      if (mevent->pass_filter(9)) {
      //if (pfjethelper[1].hlt_pt > 60.0) {
        h_filter_09_num->Fill(pfjethelper[1].off_pt, w);
        h_filter_10_den->Fill(pfjethelper[2].off_pt, w);

        if (mevent->pass_filter(10)) {
        //if (pfjethelper[2].hlt_pt > 45.0) {
          h_filter_10_num->Fill(pfjethelper[2].off_pt, w);
          h_filter_11_den->Fill(pfjethelper[3].off_pt, w);

          if (mevent->pass_filter(11)) {
          //if (pfjethelper[3].hlt_pt > 40.0) {
            h_filter_11_num->Fill(pfjethelper[3].off_pt, w);

          }
        }
      }
    }
  }
}

DEFINE_FWK_MODULE(MFVFilterHistos);
