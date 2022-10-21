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
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVFilterHistos : public edm::EDAnalyzer {
 public:
  explicit MFVFilterHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  static const int MAX_NJETS = 10;
  static const int N_PROXIES = 20;
  const bool is_dibjet;

  const double offline_csv;
  const double skew_dR_cut;
  const double btag_pt_cut;
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
  TH1F* h_btag_trig_pass_all;
  TH1F* h_btag_trig_pass_kine;

  TH1F* h_jet_match_dR;
  TH1F* h_next_match_dR;

  TH1F* h_filt_nsurvive;
  TH2F* h_filt_nsurvive_grid;
  
  TH1F* h_filtjet_hlt_dR;

  TH1F* h_filter_00_den;
  TH1F* h_filter_00_num;

  TH1F* h_filter_01_den;
  TH1F* h_filter_01_num;

  TH1F* h_filter_02_den;
  TH1F* h_filter_02_num;

  TH1F* h_filter_03_den;
  TH1F* h_filter_03_num;

};

MFVFilterHistos::MFVFilterHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    is_dibjet(cfg.getParameter<bool>("is_dibjet")),
    offline_csv(cfg.getParameter<double>("offline_csv")),
    skew_dR_cut(cfg.getParameter<double>("skew_dR_cut")),
    btag_pt_cut(cfg.getParameter<double>("btag_pt_cut")),
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
  h_btag_trig_pass_all = fs->make<TH1F>("h_btag_trig_pass_all", ";;nevents", 3, -1.5, 1.5);
  h_btag_trig_pass_kine = fs->make<TH1F>("h_btag_trig_pass_kine", ";;nevents", 3, -1.5, 1.5);

  h_jet_match_dR = fs->make<TH1F>("h_jet_match_dR", ";#DeltaR between matching HLT/offline jets;entries", 80, 0, 0.401);
  h_next_match_dR = fs->make<TH1F>("h_next_match_dR", ";#DeltaR between matching HLT jet and 2nd closest offline jet;entries", 80, 0, 0.401);


  h_filt_nsurvive      = fs->make<TH1F>("h_filt_nsurvive",      ";;nevents", 7, 0, 7);
  h_filt_nsurvive_grid = fs->make<TH2F>("h_filt_nsurvive_grid", ";;# HLT-btag proxies", 7, 0, 7, N_PROXIES, 0, N_PROXIES);
  

  //---------- Start setting some x-axis labels
  h_btag_trig_pass_kine->GetXaxis()->SetBinLabel(1, "Tri-btag Only");
  h_btag_trig_pass_kine->GetXaxis()->SetBinLabel(2, "Both");
  h_btag_trig_pass_kine->GetXaxis()->SetBinLabel(3, "Di-btag Only");

  h_btag_trig_pass_all->GetXaxis()->SetBinLabel(1, "Tri-btag Only");
  h_btag_trig_pass_all->GetXaxis()->SetBinLabel(2, "Both");
  h_btag_trig_pass_all->GetXaxis()->SetBinLabel(3, "Di-btag Only");

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

  h_filt_nsurvive_grid->GetXaxis()->SetBinLabel(1, "starting number");
  h_filt_nsurvive_grid->GetXaxis()->SetBinLabel(2, "after filt. presel");
  h_filt_nsurvive_grid->GetXaxis()->SetBinLabel(3, "after L1 trigger");

  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_filter_bits->GetXaxis()->SetBinLabel(i+2, TString::Format(" pass %s", mfv::filter_paths[i]));
    if (i < 4) {
      h_filt_nsurvive->GetXaxis()->SetBinLabel(i+4, TString::Format("pass %s", mfv::filter_paths[i]));
      h_filt_nsurvive_grid->GetXaxis()->SetBinLabel(i+4, TString::Format("pass %s", mfv::filter_paths[i]));
    }
    h_filter_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_filter_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_seqfilt_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    h_seqfilt_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
  }
  //---------- End setting some x-axis labels

  h_filtjet_hlt_dR = fs->make<TH1F>("h_filtjet_hlt_dR", ";#DeltaR between offline jet and matching HLT jet;entries", 100, 0.0, 1.0);

  h_filter_00_den = fs->make<TH1F>("h_filter_00_den", "before DoubleCaloBJets100eta2p3; p_{T} of sub-leading jet (GeV); entries", 150, 0, 300);
  h_filter_00_num = fs->make<TH1F>("h_filter_00_num", "after  DoubleCaloBJets100eta2p3; p_{T} of sub-leading jet (GeV); entries", 150, 0, 300);

  h_filter_01_den = fs->make<TH1F>("h_filter_01_den", "before BTagCalo80x6CSVp0p92DoubleWithMatching; 2nd highest jet CSV; entries", 100, 0, 1.0);
  h_filter_01_num = fs->make<TH1F>("h_filter_01_num", "after  BTagCalo80x6CSVp0p92DoubleWithMatching; 2nd highest jet CSV; entries", 100, 0, 1.0);

  h_filter_02_den = fs->make<TH1F>("h_filter_02_den", "before hltDoublePFJets100Eta2p3; p_{T} of sub-leading jet (GeV); entries", 150, 0, 300);
  h_filter_02_num = fs->make<TH1F>("h_filter_02_num", "after  hltDoublePFJets100Eta2p3; p_{T} of sub-leading jet (GeV); entries", 150, 0, 300);

  h_filter_03_den = fs->make<TH1F>("h_filter_03_den", "before hltDoublePFJets100Eta2p3MaxDeta1p6; min(#Delta#eta) between pair of high-p_{T} jets; entries", 125, 0, 2.50);
  h_filter_03_num = fs->make<TH1F>("h_filter_03_num", "after  hltDoublePFJets100Eta2p3MaxDeta1p6; min(#Delta#eta) between pair of high-p_{T} jets; entries", 125, 0, 2.50);

}

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct Jet_Pair_Helper {
    float off_pt  = -1.0;
    float hlt_pt  = -1.0;
    float hlt_eta = -1.0;
    float hlt_phi = -1.0;

    int off_i = -2;
};

struct Jet_Loc_Helper {
    float vtx_jet_pt  = -9.9;
    float vtx_jet_eta = -9.9;
    float vtx_jet_phi = -9.9;
    float vtx_pt   = -9.9;
    float vtx_eta  = -9.9;
    float vtx_phi  = -9.9;
    float vtx_dx  = -9.9;
    float vtx_dy  = -9.9;
    float vtx_dz  = -9.9;
};

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

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_token, auxes);
  const int nsv = int(auxes->size());

  const int nhltpfjets = mevent->hlt_pf_jet_pt.size();
  const int nofflinepfjets = mevent->jet_pt.size();
  double min_threshjet_deta = 99.9;
  std::vector<Jet_BHelper> bsort_helpers;
  std::vector<Jet_Pair_Helper> pfjethelper;

  // Do some matching of online and offline jets
  bool skinny_cone = false;
  bool use_puid    = true;
  for (int i=0; i < nhltpfjets; i++) {
    float hlt_eta    = mevent->hlt_pf_jet_eta[i];
    float hlt_phi    = mevent->hlt_pf_jet_phi[i];
    float hlt_pt     = mevent->hlt_pf_jet_pt[i];
    float match_pt  = 0.0;
    float match_eta = 0.0;
    float match_phi = 0.0;
    float match_dR  = 0.4;
    float next_dR   = -0.2;
    bool  ensure_match = false;


    for (int j=0; j < nofflinepfjets; j++) {
      bool  is_match = false;
      float off_eta = mevent->nth_jet_eta(j);
      float off_phi = mevent->nth_jet_phi(j);
      float off_pt  = mevent->nth_jet_pt(j);
      float off_pudisc = mevent->jet_pudisc[j];

      if      ((off_pt < 25.0) or (fabs(off_eta) > 2.4)) continue;
      if      ((use_puid) and (off_pt < 30.0) and (off_pudisc < 0.18)) continue;
      else if ((use_puid) and (off_pt < 50.0) and (off_pudisc < 0.61)) continue;    
    
      if (skinny_cone) { is_match = ((reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) and (off_pt > match_pt)); }
      else             { is_match = ((reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < match_dR)); }

      if (is_match) {
        match_pt  = off_pt;
        //match_eta = off_eta;
        //match_phi = off_phi;
        next_dR  = match_dR;
        match_dR = reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi);
        ensure_match = true;
      }
    }

    if (not ensure_match) continue;

    Jet_Pair_Helper temp_helper;
    temp_helper.hlt_pt  = hlt_pt;
    temp_helper.hlt_eta = hlt_eta;
    temp_helper.hlt_phi = hlt_phi;
    temp_helper.off_pt = match_pt;
    pfjethelper.push_back(temp_helper);

    h_jet_match_dR->Fill(match_dR, w);
    h_next_match_dR->Fill(next_dR, w);
  }

  // Find min deta between pairs of threshold (high Pt) jets
  for (int i=0; i < nofflinepfjets-1; i++) {
      if (mevent->nth_jet_pt(i) < 125.0) continue;
      float eta_i = mevent->nth_jet_eta(i);

      for (int j=i+1; j < nofflinepfjets; j++) {
          if (mevent->nth_jet_pt(j) < 125.0) continue;
          float eta_j = mevent->nth_jet_eta(j);

      //    printf("\nEta 0: %3.2f    Eta 1: %3.2f    dEta: %3.2f", eta_i, eta_j, fabs(eta_i - eta_j)); 
          if (fabs(eta_i - eta_j) < min_threshjet_deta) {
              min_threshjet_deta = fabs(eta_i-eta_j);
          }

      }
  }

  // Prepare the helpers which match SVs and jets
  std::vector<Jet_Loc_Helper> jet_loc_helper;
  for (int isv = 0; isv < nsv; isv++) {
      const MFVVertexAux& aux = auxes->at(isv);

      // The index [0] indicates that we're using ntracks to assoc.
      // a jet to a vertex. No need to worry about this right now.
      const std::vector<float> my_pts  = aux.jet_pt[0];
      const std::vector<float> my_etas = aux.jet_eta[0];
      const std::vector<float> my_phis = aux.jet_phi[0];
      int npt = int(my_pts.size());

      for (int ij=0; ij < npt; ij++) {
          Jet_Loc_Helper tmp_loc_helper;
          tmp_loc_helper.vtx_jet_pt  = my_pts[ij];
          tmp_loc_helper.vtx_jet_eta = my_etas[ij];
          tmp_loc_helper.vtx_jet_phi = my_phis[ij];

          // The index [2] indicates use tracks+jet to get pt/eta/phi
          tmp_loc_helper.vtx_pt  = aux.pt[2];
          tmp_loc_helper.vtx_eta = aux.eta[2];
          tmp_loc_helper.vtx_phi = aux.phi[2];

          tmp_loc_helper.vtx_dx  = aux.x - mevent->bsx_at_z(aux.z);
          tmp_loc_helper.vtx_dy  = aux.y - mevent->bsy_at_z(aux.z);
          tmp_loc_helper.vtx_dz  = aux.z - mevent->bsz;
          
          jet_loc_helper.push_back(tmp_loc_helper);
      }
  } 


  // Fill some basic hltbits/L1bits/filtbits histograms
  h_hlt_bits->Fill(0., w);
  h_l1_bits->Fill(0., w);
  h_filter_bits->Fill(0., w);
  h_filt_nsurvive->Fill(0., w);
  for (int p=0; p < N_PROXIES; p++) {
    h_filt_nsurvive_grid->Fill(0., p, w);
  }
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

  // Count number of btagged jets
  int nbtaggedjets      = 0;  // Jets which pass CSV req
  int naltbjets         = 0;  // Jets which pass CSV + angular reqs
  int nselectionjets    = 0;  // Dummy class that will take one of the above two values
  for(size_t i = 0, ie = mevent->jet_bdisc_old.size(); i < ie; i++) {
      bool passes_bscore = false;
      if (mevent->jet_bdisc_old[i] > offline_csv) { // 0.9693 is the tight WP for CSV algo
        passes_bscore = true;
      }
  
      // While here, let's get some SV information
      float closest_helper_dR  = 4.0;
      float closest_vtx_dR  = 4.0;
      for (auto helper : jet_loc_helper) {
          float temp_dR = reco::deltaR(helper.vtx_jet_eta, helper.vtx_jet_phi, mevent->nth_jet_eta(i), mevent->nth_jet_phi(i));
          if (temp_dR < closest_helper_dR) {
              closest_helper_dR = temp_dR;
              closest_vtx_dR = reco::deltaR(helper.vtx_eta, helper.vtx_phi, mevent->nth_jet_eta(i), mevent->nth_jet_phi(i));
          }
      }
  
      if (passes_bscore) {
          nbtaggedjets++;
          if (mevent->nth_jet_pt(i) > btag_pt_cut) {
              naltbjets++;
          }
          if (false) {
            std::cout << closest_vtx_dR << std::endl;
          }
      }

      // While in this loop, let's sort jets by bscore
      Jet_BHelper tmp_bsort_helper;
      tmp_bsort_helper.csv = mevent->jet_bdisc_old[i];
      bsort_helpers.push_back(tmp_bsort_helper);

  }

  // Actually sort the jets by csv now
  std::sort(bsort_helpers.begin(), bsort_helpers.end(), [](Jet_BHelper const &a, Jet_BHelper &b) -> bool{ return a.csv > b.csv; } );

  nselectionjets = naltbjets;

  int satisfy_di_btag = (mevent->nth_jet_pt(0) > 125.0 and mevent->nth_jet_pt(1) > 125.0 and min_threshjet_deta < 1.5 and mevent->pass_hlt(8));
  int satisfy_tri_btag = (mevent->nth_jet_pt(0) > 85.0 and mevent->nth_jet_pt(1) > 60.0 and mevent->nth_jet_pt(2) > 50.0 and mevent->nth_jet_pt(3) > 45.0 and mevent->pass_hlt(9));

  if (satisfy_di_btag or satisfy_tri_btag) {
    h_btag_trig_pass_kine->Fill(satisfy_di_btag - satisfy_tri_btag, w);
  }

  if ((satisfy_di_btag and nselectionjets >= 2) or (satisfy_tri_btag and nselectionjets >= 3)) {
    h_btag_trig_pass_all->Fill((satisfy_di_btag and nselectionjets >= 2) - (satisfy_tri_btag and nselectionjets >= 3), w);
  }

  // Don't do anything else if we don't have enough good jets or calojets
  bool pass_filtsel = false;
  int  filtsel_opt  = 1;   // 0 = MinSel,  1 = HalfSel,  2 = FullSel, 3 = NoSel
  if ( filtsel_opt == 0 and nofflinepfjets >= 2) { pass_filtsel = true; }

  else if ( filtsel_opt == 1
      and mevent->nth_jet_pt(0) > 125.0 
      and mevent->nth_jet_pt(1) > 125.0 
      and min_threshjet_deta < 1.5) { pass_filtsel = true; }

  else if ( filtsel_opt == 2
      and mevent->nth_jet_pt(0) > 100.0 
      and mevent->nth_jet_pt(1) > 100.0 
      and nbtaggedjets >= 2) { pass_filtsel = true; }

  else if ( filtsel_opt == 3) { pass_filtsel = true; }


  if (pass_filtsel) { 
    h_filt_nsurvive->Fill(1, w);
    h_filt_nsurvive->Fill(2, w);
    for (int p=0; p < N_PROXIES; p++) {
      if (nselectionjets != p) continue;
      h_filt_nsurvive_grid->Fill(1, p, w);
      h_filt_nsurvive_grid->Fill(2, p, w);
    }
  }
  else { 
    return;
  }

//  if (mevent->pass_l1(20)) {   // L1 bit #20 is the only seed for this trig
//    h_filt_nsurvive->Fill(2, w);
//    for (int p=0; p < N_PROXIES; p++) {
//      if (nselectionjets != p) continue;
//      h_filt_nsurvive_grid->Fill(2, p, w);
//    }
//  }
//  else {
//    return;
//  }
  

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


  // Some bools
  bool pass_00 = mevent->pass_filter(0);
  bool pass_01 = mevent->pass_filter(1);
  bool pass_02 = mevent->pass_filter(2);
  bool pass_03 = mevent->pass_filter(3);

  // Fill some floats based on which filter-passing method is used
  float pt0 = mevent->nth_jet_pt(0);
  float pt1 = mevent->nth_jet_pt(1);

  h_filter_00_den->Fill(pt1, w);

  if (pass_00) {
    h_filter_00_num->Fill(pt1, w);
    h_filter_01_den->Fill(bsort_helpers[1].csv, w);

    for (int p=0; p < N_PROXIES; p++) {
      if (nselectionjets != p) continue;
      h_filt_nsurvive_grid->Fill(3, p, w);
      h_filt_nsurvive_grid->Fill(4, p, w);
    }
    

    if (pass_01) {
      h_filter_01_num->Fill(bsort_helpers[1].csv, w);
      h_filter_02_den->Fill(pt1, w);


      for (int p=0; p < N_PROXIES; p++) {
        if (nselectionjets != p) continue;
        h_filt_nsurvive_grid->Fill(4, p, w);
      }

      if (pass_02) {
        h_filter_02_num->Fill(pt1, w);
        h_filter_03_den->Fill(min_threshjet_deta, w);

        for (int p=0; p < N_PROXIES; p++) {
          if (nselectionjets != p) continue;
          h_filt_nsurvive_grid->Fill(5, p, w);
        }


        if (pass_03) {
          h_filter_03_num->Fill(min_threshjet_deta, w);
          for (int p=0; p < N_PROXIES; p++) {
            if (nselectionjets != p) continue;
            h_filt_nsurvive_grid->Fill(6, p, w);
          }
        }
      }
    }  
  }
}

DEFINE_FWK_MODULE(MFVFilterHistos);
