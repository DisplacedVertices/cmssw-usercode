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
    //float off_eta = -1.0;
    //float off_phi = -1.0;

    float hlt_pt  = -1.0;
    //float hlt_eta = -1.0;
    //float hlt_phi = -1.0;
};

void MFVFilterHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  const int nhltpfjets = mevent->hlt_pf_jet_pt.size();
  //const int nhltcalojets = mevent->hlt_calo_jet_pt.size();
  const int nofflinepfjets = mevent->jet_pt.size();
  //const int nofflinecalojets = mevent->calo_jet_pt.size();


  // Just seeing what happens if we skip negatively-weighted events
  //if (w < 0.0) return;

  // Do some matching before online and offline stuff
  std::vector<Jet_Pair_Helper> pfjethelper;
  for (int i=0; i < nhltpfjets; i++) {
    if (pfjethelper.size() == 4) break;
    Jet_Pair_Helper temp_helper;
    float match_dR = 0.5;
    float hlt_eta = mevent->hlt_pf_jet_eta[i];
    float hlt_phi = mevent->hlt_pf_jet_phi[i];
    
    for (int j=0; j < nofflinepfjets; j++) {
      float temp_deta = fabs(mevent->jet_eta[j] - hlt_eta);
      float temp_dphi = fabs(TVector2::Phi_mpi_pi(mevent->jet_phi[j] - hlt_phi));
      float temp_dR   = std::hypot(temp_deta, temp_dphi);

      if (temp_dR < match_dR) {
        temp_helper.off_pt = mevent->jet_pt[j];
        temp_helper.hlt_pt = mevent->hlt_pf_jet_pt[i];
        match_dR = temp_dR;
      } 
    }
    if (temp_helper.hlt_pt > 1.0)
      pfjethelper.push_back(temp_helper);
  }

  
  // Initialize filter study preselection parameters
  int require_L1  = is_dibjet ? di_bitL1 : tri_bitL1;
  int min_filtjets        = is_dibjet ? di_minfiltjets : tri_minfiltjets;
  float min_filtjetpt     = is_dibjet ? di_minfiltjetpt : tri_minfiltjetpt;
  float max_filtjeteta    = is_dibjet ? di_maxfiltjeteta : tri_maxfiltjeteta;
  float min_filtjetbscore = is_dibjet ? di_minfiltjetbdisc : tri_minfiltjetbdisc;

  bool  pass_onoff_pfjet_match = true;
  //bool  pass_onoff_calojet_match = true;
  //float max_jetdeta = 0.0;
  //float min_jetdeta = 9.9;
  int filtjet_passes = 0;
  //int calofiltjet_passes = 0;

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
  if ((std::size(mevent->jet_bdisc) == 0)) return;

  for (int i = 0; i < MAX_NJETS; ++i) {
    float filtjet_pt = mevent->nth_jet_pt(i);
    float filtjet_abseta = fabs(mevent->nth_jet_eta(i));
    float filtjet_bscore = mevent->jet_bdisc[i];

     // Ensure that the event passes some minimum cuts.
    if ((filtjet_pt > min_filtjetpt) && (filtjet_abseta < max_filtjeteta) && (filtjet_bscore > min_filtjetbscore)) // Do we use old_bscore or just bscore?
      filtjet_passes++;
  }

  // Are there matches between online PFjets and offline PFjets?
//  for (int i=0, ipmax = 4; i < ipmax; i++) {
//    float hlt_eta = (nhltpfjets > i ? mevent->hlt_pf_jet_eta[i] : -99.0);
//    float hlt_phi = (nhltpfjets > i ? mevent->hlt_pf_jet_phi[i] : -99.0);
//
//    float temp_deta = fabs(mevent->jet_eta[i] - hlt_eta);
//    float temp_dphi = fabs(mevent->jet_phi[i] - hlt_phi);
//
//    if ((temp_deta > 0.33) or (temp_dphi > 0.33)){
//      pass_onoff_pfjet_match = false;
//      break;
//    }
//  }

  // Don't do anything else if we don't have enough good jets or calojets
  if ((filtjet_passes < min_filtjets) or (not pass_onoff_pfjet_match) or (not mevent->pass_l1(require_L1)))
    return;

  // Don't do anything else if not enough matches between online and offline jets
//  if (pfjethelper.size() < 4)
//    return;

//  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//  // We'll just take the easy way out for the first filters (for now)
//  for (int i = 4; i < 8; i++) { if (not (mevent->pass_filter(i))) return; }
//
//                  //jet#   0  1  2  3
//  int filter_errors = 0;
//
//  h_filter_07_den->Fill(mevent->nth_jet_pt(3), w);
//
//  if (pfjethelper[3].hlt_pt > 30.0) {
//    h_filter_07_num->Fill(mevent->nth_jet_pt(3), w);
//    h_filter_08_den->Fill(mevent->nth_jet_pt(0), w);
//
//    if (pfjethelper[0].hlt_pt > 75.0) {
//      h_filter_08_num->Fill(mevent->nth_jet_pt(0), w);
//      h_filter_09_den->Fill(mevent->nth_jet_pt(1), w);
//
//      if (mevent->nth_jet_pt(0) < 55.0) filter_errors = filter_errors ^ 1;     
//
//      if (pfjethelper[1].hlt_pt > 60.0) {
//        h_filter_09_num->Fill(mevent->nth_jet_pt(1), w);
//        h_filter_10_den->Fill(mevent->nth_jet_pt(2), w);
//
//        if (mevent->nth_jet_pt(1) < 45.0) filter_errors = filter_errors ^ 2;     
//
//        if (pfjethelper[2].hlt_pt > 45.0) {
//          h_filter_10_num->Fill(mevent->nth_jet_pt(2), w);
//          h_filter_11_den->Fill(mevent->nth_jet_pt(3), w);
//
//          if (mevent->nth_jet_pt(1) < 35.0) filter_errors = filter_errors ^ 4;     
//
//          if (pfjethelper[3].hlt_pt > 40.0) {
//            h_filter_11_num->Fill(mevent->nth_jet_pt(3), w);
//
//            if (mevent->nth_jet_pt(1) < 32.0) filter_errors = filter_errors ^ 8;
//          }
//        }
//      }
//    }
//  }

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  // We'll just take the easy way out for the first filters (for now)
  for (int i = 4; i < 8; i++) { if (not (mevent->pass_filter(i))) return; }

                  //jet#   0  1  2  3
  int filter_errors = 0;

  h_filter_07_den->Fill(mevent->nth_jet_pt(3), w);

  if (mevent->jet_hlt_pt[3] > 30.0) {
    h_filter_07_num->Fill(mevent->nth_jet_pt(3), w);
    h_filter_08_den->Fill(mevent->nth_jet_pt(0), w);

    if (mevent->jet_hlt_pt[0] > 75.0) {
      h_filter_08_num->Fill(mevent->nth_jet_pt(0), w);
      h_filter_09_den->Fill(mevent->nth_jet_pt(1), w);

//      if (mevent->nth_jet_pt(0) < 55.0) filter_errors = filter_errors ^ 1;     

      if (mevent->jet_hlt_pt[1] > 60.0) {
        h_filter_09_num->Fill(mevent->nth_jet_pt(1), w);
        h_filter_10_den->Fill(mevent->nth_jet_pt(2), w);

//        if (mevent->nth_jet_pt(1) < 45.0) filter_errors = filter_errors ^ 2;     

        if (mevent->jet_hlt_pt[2] > 45.0) {
          h_filter_10_num->Fill(mevent->nth_jet_pt(2), w);
          h_filter_11_den->Fill(mevent->nth_jet_pt(3), w);

//          if (mevent->nth_jet_pt(1) < 35.0) filter_errors = filter_errors ^ 4;     

          if (mevent->jet_hlt_pt[3] > 40.0) {
            h_filter_11_num->Fill(mevent->nth_jet_pt(3), w);

//            if (mevent->nth_jet_pt(1) < 32.0) filter_errors = filter_errors ^ 8;
          }
        }
      }
    }
  }



  // DEBUG #########################################################################################################
  if (filter_errors > 0) {
    std::cout << "\n\n-------- PF-Jet Dump --------" << std::endl;
    std::cout << "\n Misbehavior bits: " << std::bitset<4>(filter_errors) << std::endl;
    printf("#offline PFjets: %i     #online PFjets: %i \n", (int)(mevent->jet_id.size()), nhltpfjets);
  
  
    printf("\nOnline Jets\n------------------------------\n");
    for (int i=0; i < nhltpfjets; i++) {
      printf("Jet %i     pT: %5.2f   eta: %5.2f  phi: %5.2f \n", i, mevent->hlt_pf_jet_pt[i], mevent->hlt_pf_jet_eta[i], mevent->hlt_pf_jet_phi[i]);
    }
  
    printf("\nOffline Jets\n------------------------------\n");
    for (int i=0; i < nofflinepfjets; i++) {
      printf("Jet %i     pT: %5.2f   eta: %5.2f  phi: %5.2f\n", i, mevent->jet_pt[i], mevent->jet_eta[i], mevent->jet_phi[i]);
    }
  }
    
 
}

DEFINE_FWK_MODULE(MFVFilterHistos);
