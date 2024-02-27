#include <bitset>
#include "TH2F.h"
#include "TH3F.h"
#include "TRandom3.h"
#include "TVector2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

class MFVFilterHistos : public edm::EDAnalyzer {
    public:
        explicit MFVFilterHistos(const edm::ParameterSet&);
        void analyze(const edm::Event&, const edm::EventSetup&);

    private:
        const edm::EDGetTokenT<MFVEvent> mevent_token;
        const edm::EDGetTokenT<double> weight_token;
        const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
        const edm::EDGetTokenT<reco::TrackCollection> track_token;

        static const int MAX_NJETS = 10;
        static const int N_PROXIES = 20;
        static const int N_CAT = 2;
        const int DEN = 0;
        const int NUM = 1;
        const bool is_dibjet;

        const double offline_csv = jmt::BTagging::discriminator_min(1, 1);
        const double skew_dR_cut;
        const double btag_pt_cut;
        const bool   require_two_good_leptons;
        const bool   require_exact_ncalojets;
        const int    ncalojet_req;
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

        const int nhltcalojet_req;

        jmt::TrackRescaler track_rescaler;

        TH1F* h_hlt_bits;
        TH1F* h_l1_bits;
        TH1F* h_filter_bits;
        TH2F* h_filter_bit_matrix;
        TH2F* h_seqfilt_bit_matrix;
        TH1F* h_btag_trig_pass_all;
        TH1F* h_btag_trig_pass_kine;

        TH1F* h_jet_match_dR;
        TH1F* h_next_match_dR;

        TH1F* h_calojet_pt_den0;
        TH1F* h_calojet_pt_den1;
        TH1F* h_calojet_pt_num0;
        TH1F* h_calojet_pt_num1;
        TH1F* h_calojet_eta_den0;
        TH1F* h_calojet_eta_den1;
        TH1F* h_calojet_eta_num0;
        TH1F* h_calojet_eta_num1;
        TH1F* h_calojet_ntks;
        TH1F* h_calojet_nprompt_tks;
        TH2F* h_calojet_ntks_nprompt;
        TH1F* h_calojet_ndisp_tks;
        TH1F* h_calojet_matched_nprompt_tks;
        TH1F* h_calojet_matched_ndisp_tks;
        TH2F* h_evt_jet_prompt_multiplicity;
        TH2F* h_evt_jet_disp_multiplicity;

        TH1F* h_calojet_tk_dxybs;


        TH1F* h_filtjet_hlt_dR;

        TH1F* h_di_filter_00[N_CAT];
        TH1F* h_di_filter_01[N_CAT];
        TH1F* h_di_filter_02[N_CAT];
        TH1F* h_di_filter_03[N_CAT];

        TH1F* h_tri_filter_00[N_CAT];
        TH1F* h_tri_filter_01[N_CAT];
        TH1F* h_tri_filter_02[N_CAT];
        TH1F* h_tri_filter_03[N_CAT];
        TH1F* h_tri_filter_04[N_CAT];
        TH1F* h_tri_filter_05[N_CAT];
        TH1F* h_tri_filter_06[N_CAT];
        TH1F* h_tri_filter_07[N_CAT];
        TH1F* h_tri_filter_08[N_CAT];
        TH1F* h_tri_filter_09[N_CAT];

        TH1F* h_tri_symm_filter_00[N_CAT];
        TH1F* h_tri_symm_filter_01[N_CAT];
        TH1F* h_tri_symm_filter_02[N_CAT];

        TH1F* h_tri_skew_filter_00[N_CAT];
        TH1F* h_tri_skew_filter_01[N_CAT];
        TH1F* h_tri_skew_filter_02[N_CAT];
        TH1F* h_tri_skew_filter_03[N_CAT];
        TH1F* h_tri_skew_filter_04[N_CAT];

        TH1F* h_dd_dtk_filter_00[N_CAT];
        TH1F* h_dd_dtk_filter_alt_d_00[N_CAT];
        TH1F* h_dd_dtk_filter_01[N_CAT];
        TH1F* h_dd_dtk_filter_02[N_CAT];
        TH1F* h_dd_dtk_filter_03[N_CAT];
        TH1F* h_dd_dtk_filter_04[N_CAT];

        TH1F* h_dd_inc_filter_00[N_CAT];
        TH1F* h_dd_inc_filter_alt_d_00[N_CAT];
        TH1F* h_dd_inc_filter_01[N_CAT];
        TH1F* h_dd_inc_filter_02[N_CAT];
        TH1F* h_dd_inc_filter_03[N_CAT];


};

MFVFilterHistos::MFVFilterHistos(const edm::ParameterSet& cfg)
    : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    track_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("track_src"))),
    is_dibjet(cfg.getParameter<bool>("is_dibjet")),
    skew_dR_cut(cfg.getParameter<double>("skew_dR_cut")),
    btag_pt_cut(cfg.getParameter<double>("btag_pt_cut")),
    require_two_good_leptons(cfg.getParameter<bool>("require_two_good_leptons")),
    require_exact_ncalojets(cfg.getParameter<bool>("require_exact_ncalojets")),
    ncalojet_req(cfg.getParameter<int>("ncalojet_req")),
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
    min_pt_for_bfilter(cfg.getParameter<double>("min_pt_for_bfilter")),
    nhltcalojet_req(cfg.getParameter<int>("nhltcalojet_req"))

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

    h_calojet_pt_den0  = fs->make<TH1F>("h_calojet_pt_den0", ";p_{T} of calojets;entries", 200, 40, 640);
    h_calojet_pt_den1  = fs->make<TH1F>("h_calojet_pt_den1", ";p_{T} of calojets;entries", 200, 40, 640);
    h_calojet_pt_num0  = fs->make<TH1F>("h_calojet_pt_num0", ";p_{T} of calojets;entries", 200, 40, 640);
    h_calojet_pt_num1  = fs->make<TH1F>("h_calojet_pt_num1", ";p_{T} of calojets;entries", 200, 40, 640);
    h_calojet_eta_den0  = fs->make<TH1F>("h_calojet_eta_den0", ";abs #eta of calojets;entries", 125, 0, 2.5);
    h_calojet_eta_den1  = fs->make<TH1F>("h_calojet_eta_den1", ";abs #eta of calojets;entries", 125, 0, 2.5);
    h_calojet_eta_num0  = fs->make<TH1F>("h_calojet_eta_num0", ";abs #eta of calojets;entries", 125, 0, 2.5);
    h_calojet_eta_num1  = fs->make<TH1F>("h_calojet_eta_num1", ";abs #eta of calojets;entries", 125, 0, 2.5);
    h_calojet_ntks = fs->make<TH1F>("h_calojet_ntks", ";# of tks in calojets;entries", 100, 0, 100);
    h_calojet_nprompt_tks = fs->make<TH1F>("h_calojet_nprompt_tks", ";# of prompt tks in calojets;entries", 100, 0, 100);
    h_calojet_ntks_nprompt = fs->make<TH2F>("h_calojet_ntks_nprompt", ";# of tracks in calojets;# of prompt tracks in calojets", 100, 0, 100, 100, 0, 100);
    h_calojet_ndisp_tks  = fs->make<TH1F>("h_calojet_ndisp_tks", ";# of displaced tks in calojets;entries", 100, 0, 100);
    h_calojet_matched_nprompt_tks = fs->make<TH1F>("h_calojet_matched_nprompt_tks", ";# of prompt tks in calojets matched @ HLT;entries", 100, 0, 100);
    h_calojet_matched_ndisp_tks  = fs->make<TH1F>("h_calojet_matched_ndisp_tks", ";# of displaced tks in calojets matched @ HLT;entries", 100, 0, 100);
    h_evt_jet_prompt_multiplicity = fs->make<TH2F>("h_evt_jet_prompt_multiplicity", ";# prompt tks in calojet;evt calojet multiplicity", 40, 0, 40, 15, -0.5, 14.5);
    h_evt_jet_disp_multiplicity = fs->make<TH2F>("h_evt_jet_disp_multiplicity", ";# disp tks in calojet;evt calojet multiplicity", 40, 0, 40, 15, -0.5, 14.5);

    h_calojet_tk_dxybs = fs->make<TH1F>("h_calojet_tk_dxybs", ";abs d_{xy} of tracks in calojets (cm); entries", 200, 0, 0.2);

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

    for (int i = 0; i < mfv::n_filter_paths; ++i) {
        h_filter_bits->GetXaxis()->SetBinLabel(i+2, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_filter_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_filter_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_seqfilt_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_seqfilt_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    }

    //---------- End setting some x-axis labels

    h_filtjet_hlt_dR = fs->make<TH1F>("h_filtjet_hlt_dR", ";#DeltaR between offline jet and matching HLT jet;entries", 100, 0.0, 1.0);
    for (int i=0; i<N_CAT; i++) {

        TString bres = i == 1 ? TString("num") : TString("den");
        h_di_filter_00[i] = fs->make<TH1F>(TString::Format("h_di_filter_00_%s", bres.Data()), "CaloBJet pT Filter; p_{T} of sub-leading jet (GeV); entries",                    150, 0, 300);
        h_di_filter_01[i] = fs->make<TH1F>(TString::Format("h_di_filter_01_%s", bres.Data()), "Di-Btag Filter; 2nd-highest PFJet bscore; entries",                               50, 0, 1.0);
        h_di_filter_02[i] = fs->make<TH1F>(TString::Format("h_di_filter_02_%s", bres.Data()), "PFJet pT Filter; p_{T} of sub-leading jet (GeV); entries",                       150, 0, 300);
        h_di_filter_03[i] = fs->make<TH1F>(TString::Format("h_di_filter_03_%s", bres.Data()), "High-pT PFJet #Delta#eta Filter; Min(|#Delta#eta|) of high-p_{T} jets; entries", 100, 0, 3.0);

        h_tri_filter_00[i] = fs->make<TH1F>(TString::Format("h_tri_filter_00_%s", bres.Data()), "4-CaloJet Filter; p_{T} of 4th-leading jet (GeV); entries",              150, 0,  300);
        h_tri_filter_01[i] = fs->make<TH1F>(TString::Format("h_tri_filter_01_%s", bres.Data()), "CaloHT Filter; HT(30) (GeV); entries",                                   100, 0, 1000);
        h_tri_filter_02[i] = fs->make<TH1F>(TString::Format("h_tri_filter_02_%s", bres.Data()), "Di-Btag Filter; 2nd-highest PFJet bscore; entries",                       50, 0,  1.0);
        h_tri_filter_03[i] = fs->make<TH1F>(TString::Format("h_tri_filter_03_%s", bres.Data()), "4-PFJet Filter; p_{T} of 4th-leading jet (GeV); entries",                100, 0,  300);
        h_tri_filter_04[i] = fs->make<TH1F>(TString::Format("h_tri_filter_04_%s", bres.Data()), "1st-Leading PFJet PT Filter; p_{T} of leading jet (GeV); entries",       100, 0,  300);
        h_tri_filter_05[i] = fs->make<TH1F>(TString::Format("h_tri_filter_05_%s", bres.Data()), "2nd-Leading PFJet PT Filter; p_{T} of sub-leading jet (GeV); entries",   100, 0,  300);
        h_tri_filter_06[i] = fs->make<TH1F>(TString::Format("h_tri_filter_06_%s", bres.Data()), "3rd-Leading PFJet PT Filter; p_{T} of 3rd-leading jet (GeV); entries",   100, 0,  300);
        h_tri_filter_07[i] = fs->make<TH1F>(TString::Format("h_tri_filter_07_%s", bres.Data()), "4th-Leading PFJet PT Filter; p_{T} of 4th-leading jet (GeV); entries",   100, 0,  300);
        h_tri_filter_08[i] = fs->make<TH1F>(TString::Format("h_tri_filter_08_%s", bres.Data()), "PFHT Filter; HT(30) GeV; entries",                                       100, 0, 1000);
        h_tri_filter_09[i] = fs->make<TH1F>(TString::Format("h_tri_filter_09_%s", bres.Data()), "Tri-Btag Filter; 3rd-highest PFJet bscore; entries",                      50, 0,  1.0);

        h_tri_symm_filter_00[i] = fs->make<TH1F>(TString::Format("h_tri_symm_filter_00_%s", bres.Data()), "4th-Leading CaloJet Filter; p_{T} of 4th-leading CaloJet (GeV); entries", 100, 0, 300);
        h_tri_symm_filter_01[i] = fs->make<TH1F>(TString::Format("h_tri_symm_filter_01_%s", bres.Data()), "Di-Btag Filter; 2nd-highest PFJet bscore; entries",                        50, 0, 1.0);
        h_tri_symm_filter_02[i] = fs->make<TH1F>(TString::Format("h_tri_symm_filter_02_%s", bres.Data()), "4th-Leading PFJet Filter; p_{T} of 4th-leading PFJet (GeV); entries",     100, 0, 300);

        h_tri_skew_filter_00[i] = fs->make<TH1F>(TString::Format("h_tri_skew_filter_00_%s", bres.Data()), "4th-Leading CaloJet Filter; p_{T} of 4th-leading CaloJet (GeV); entries", 100, 0, 300);
        h_tri_skew_filter_01[i] = fs->make<TH1F>(TString::Format("h_tri_skew_filter_01_%s", bres.Data()), "2nd-Leading CaloJet Filter; p_{T} of 2nd-leading CaloJet (GeV); entries", 100, 0, 300);
        h_tri_skew_filter_02[i] = fs->make<TH1F>(TString::Format("h_tri_skew_filter_02_%s", bres.Data()), "Di-Btag Filter; 2nd-highest PFJet bscore; entries",                        50, 0, 1.0);
        h_tri_skew_filter_03[i] = fs->make<TH1F>(TString::Format("h_tri_skew_filter_03_%s", bres.Data()), "4th-Leading PFJet Filter; p_{T} of 4th-leading PFJet (GeV); entries",     100, 0, 300);
        h_tri_skew_filter_04[i] = fs->make<TH1F>(TString::Format("h_tri_skew_filter_04_%s", bres.Data()), "2nd-Leading PFJet Filter; p_{T} of 2nd-leading PFJet (GeV); entries",     100, 0, 300);

        h_dd_dtk_filter_00[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_00_%s", bres.Data()), "CaloHT430 Filter; PFHT(40) (GeV); entries",                           150, 0, 1500);
        h_dd_dtk_filter_alt_d_00[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_alt_d_00_%s", bres.Data()), "CaloHT430 Filter;CaloHT(30) (GeV); entries",               150, 0, 1500);
        h_dd_dtk_filter_01[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_01_%s", bres.Data()), "Two CaloPT>40 Filter; 2nd-highest jet pT (GeV); entries",                100, 0, 300);
        h_dd_dtk_filter_02[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_02_%s", bres.Data()), "First prompt tk filter; 2nd smallest prompt tk multiplicity; entries",     30, 0, 30);
        h_dd_dtk_filter_03[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_03_%s", bres.Data()), "Second prompt tk filter; 2nd smallest prompt tk multiplicity",             30, 0, 30);
        h_dd_dtk_filter_04[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_04_%s", bres.Data()), "Displaced tk filter; 2nd largest disp track multiplicity; entries",        30, 0, 30);

        h_dd_inc_filter_00[i] = fs->make<TH1F>(TString::Format("h_dd_inc_filter_00_%s", bres.Data()), "CaloHT650 Filter; PFHT(40) (GeV); entries",                          150, 0, 1500);
        h_dd_inc_filter_alt_d_00[i] = fs->make<TH1F>(TString::Format("h_dd_inc_filter_alt_d_00_%s", bres.Data()), "CaloHT650 Filter;CaloHT(30) (GeV); entries",               150, 0, 1500);
        h_dd_inc_filter_01[i] = fs->make<TH1F>(TString::Format("h_dd_inc_filter_01_%s", bres.Data()), "Two CaloPT>60 Filter; 2nd-highest jet pT (GeV); entries",                100, 0, 300);
        h_dd_inc_filter_02[i] = fs->make<TH1F>(TString::Format("h_dd_inc_filter_02_%s", bres.Data()), "First prompt tk filter; 2nd smallest prompt tk multiplicity; entries",     30, 0, 30);
        h_dd_inc_filter_03[i] = fs->make<TH1F>(TString::Format("h_dd_inc_filter_03_%s", bres.Data()), "Second prompt tk filter; 2nd smallest prompt tk multiplicity",             30, 0, 30);

    }

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct Jet_Track_Helper {
    float pt      = 0.;
    float eta     = 0.;
    int ntks    = 0;
    int nprompt = 0;
    int ndisp   = 0;
    bool matches_calo_jet    = false;
    bool matches_hlt_nprompt_jet = false;
    bool matches_hlt_ndisp_jet   = false;
};

struct Jet_BHelper {
    float pt  = 0.0;
    float eta = 0.0;
    float phi = 0.0;
    float bscore = 0.0;
};

struct Jet_Eta_Helper {
    float pt  =  0.0;
    float eta = 99.0;
};

void MFVFilterHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);

    edm::Handle<double> weight;
    event.getByToken(weight_token, weight);
    const double w = *weight;

    edm::Handle<MFVVertexAuxCollection> auxes;
    event.getByToken(vertex_token, auxes);

    edm::Handle<reco::TrackCollection> tracks;

    // Get a shorthand for the current year
    int ul_year = int(MFVNEUTRALINO_YEAR);

    if (require_two_good_leptons) {
        bool has_nice_muon = false;
        bool has_nice_ele  = false;
        for (size_t ilep = 0; ilep < mevent->nlep(); ++ilep) {
            if (mevent->is_electron(ilep)) {
                float ele_eta = mevent->lep_eta[ilep]; 
                float ele_pt  = mevent->lep_pt(ilep);
                if (fabs(ele_eta) > 2.4 or ele_pt < 30.0) continue;
                else if (fabs(ele_eta) < 1.479) {
                    if (mevent->lep_iso[ilep] < (0.0287+(0.506/ele_pt))) {
                        has_nice_ele = true;
                    }
                }
                else {  
                    if (mevent->lep_iso[ilep] < (0.0445+(0.963/ele_pt))) {
                        has_nice_ele = true;
                    }
                }
            }
            else if (mevent->lep_iso[ilep] < 0.15 and mevent->lep_pt(ilep) > 30.0 and fabs(mevent->lep_eta[ilep]) < 2.4) {
                has_nice_muon = true;
            }
        }

        if ((not has_nice_muon) or (not has_nice_ele) or (mevent->nbtags(1) < 2)) return;
    }

    if (require_exact_ncalojets) {
        int n_central_hltcalojets = 0;
        for (size_t i=0; i < mevent->hlt_calo_jet_pt.size(); ++i) {
            if (fabs(mevent->hlt_calo_jet_eta[i]) < 2.5) {
                n_central_hltcalojets++;
            };
        }
        if (n_central_hltcalojets != ncalojet_req) {
            return;
        }
    }

    event.getByToken(track_token, tracks);

    const int track_rescaler_which = jmt::TrackRescaler::w_JetHT; // JMTBAD which rescaling if ever a different one
    track_rescaler.setup(!event.isRealData() && track_rescaler_which != -1,
            jmt::AnalysisEras::pick(event.id().event()),
            //jmt::AnalysisEras::pick(event, this),
            track_rescaler_which);

    double bsx = mevent->bsx;
    double bsy = mevent->bsy;
    double bsz = mevent->bsz;
    const math::XYZPoint bs(bsx, bsy, bsz);

    const int nofflinepfjets   = mevent->jet_pt.size();
    const int nofflinecalojets = mevent->calo_jet_pt.size();
    //int nhltcalojets = mevent->hlt_calo_jet_pt.size();
    //if (nhltcalojet_req > 0 and nhltcalojet_req < 9 and nhltcalojets != nhltcalojet_req) return;
    //else if (nhltcalojet_req == 9 and nhltcalojets < 9) return;
    //if (not mevent->pass_hlt(mfv::b_HLT_IsoMu27)) return;

    //int ncalojets    = mevent->calo_jet_pt.size();

    double min_threshjet_deta = 99.9;
    std::vector<Jet_BHelper> bsort_helpers;
    std::vector<Jet_Track_Helper> jet_track_helper;
    std::vector<Jet_Eta_Helper> jet_eta_helper;
    std::vector<Jet_Eta_Helper> calojet_eta_helper;

    std::vector<int> jet_nprompt_counts(70, 0);
    std::vector<int> jet_ndisp_counts(70, 0);

    // Find some relevant information about prompt/seed track multiplicity
    for (int i=0; i < nofflinecalojets; i++) {
        if (mevent->calo_jet_pt[i] < 40.0 or fabs(mevent->calo_jet_eta[i]) > 2.0) continue;    

        int jet_tks              = 0;
        int jet_tks_nprompt      = 0;
        int jet_tks_ndisplaced   = 0;
        bool matches_calojet     = false;
        bool matches_promptk_jet = false;
        bool matches_disptk_jet  = false;
        double best_dR  = 0.4;
        int    best_idx = -9;
        Jet_Track_Helper tmp_track_helper;

        for (int j=0, je=mevent->hlt_calo_jet_eta.size(); j < je; j++) {
            double temp_dR = reco::deltaR(mevent->hlt_calo_jet_eta[j], mevent->hlt_calo_jet_phi[j], mevent->calo_jet_eta[i], mevent->calo_jet_phi[i]);
            if (temp_dR < best_dR) {
                matches_calojet = true;
                best_dR  = temp_dR;
                best_idx = j;
            }
        }

        if (not matches_calojet) continue;
        if (mevent->hlt_calo_jet_pt[best_idx] < 50.0 or fabs(mevent->hlt_calo_jet_eta[best_idx]) > 2.0) continue;

        for (size_t itk = 0; itk < mevent->n_jet_tracks_all(); itk++) {
            float tk_pt  = fabs(mevent->jet_track_qpt[itk]);
            float tk_eta = mevent->jet_track_eta[itk];
            float tk_phi = mevent->jet_track_phi[itk];

            if (tk_pt < 1.0) continue;

            double this_tk_dR = reco::deltaR(mevent->calo_jet_eta[best_idx], mevent->calo_jet_phi[best_idx], tk_eta, tk_phi);
            if (this_tk_dR > 0.5) continue;

            const double dxybs = fabs(mevent->jet_track_dxy[itk]);
            const double nsigmadxy = fabs(mevent->jet_track_dxy[itk]/mevent->jet_track_dxy_err[itk]);

            h_calojet_tk_dxybs->Fill(dxybs, w);

            jet_tks++;
            if (dxybs < 0.1) jet_tks_nprompt++;
            if (dxybs > 0.05 and nsigmadxy > 5.0) jet_tks_ndisplaced++;
        }

        jet_nprompt_counts[jet_tks_nprompt]  += 1;
        jet_ndisp_counts[jet_tks_ndisplaced] += 1;

        // See if this calojet matches to one which passes the prompt track tag
        for (int j=0, je=mevent->hlt_calo_jet_lowpt_fewprompt_pt.size(); j < je; j++) {
            double test_jet_eta = mevent->hlt_calo_jet_lowpt_fewprompt_eta[j];
            double test_jet_phi = mevent->hlt_calo_jet_lowpt_fewprompt_phi[j];
            if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.14) {
                matches_promptk_jet = true;
                break;
            }
        }

        // See if this calojet matches to one which passes the prompt track tag
        for (int j=0, je=mevent->hlt_calo_jet_lowpt_wdisptks_pt.size(); j < je; j++) {
            double test_jet_eta = mevent->hlt_calo_jet_lowpt_wdisptks_eta[j];
            double test_jet_phi = mevent->hlt_calo_jet_lowpt_wdisptks_phi[j];
            if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.14) {
                matches_disptk_jet = true;
                break;
            }
        }

        tmp_track_helper.pt      = mevent->calo_jet_pt[best_idx];
        tmp_track_helper.eta     = fabs(mevent->calo_jet_eta[best_idx]);
        tmp_track_helper.ntks    = jet_tks;
        tmp_track_helper.ndisp   = jet_tks_ndisplaced;
        tmp_track_helper.nprompt = jet_tks_nprompt; 
        tmp_track_helper.matches_calo_jet    = matches_calojet;
        tmp_track_helper.matches_hlt_nprompt_jet = matches_promptk_jet;
        tmp_track_helper.matches_hlt_ndisp_jet   = matches_disptk_jet; 

        jet_track_helper.push_back(tmp_track_helper);

    }

    for (int htks=0, htkse=40; htks < htkse; htks++) {
        h_evt_jet_prompt_multiplicity->Fill(htks, jet_nprompt_counts[htks], w);
        h_evt_jet_disp_multiplicity->Fill(htks, jet_ndisp_counts[htks], w);
    }

    // Calculate alt_hlt_calo_ht
    float alt_hlt_calo_ht = 0.0;
    for (int i=0, ie=mevent->hlt_calo_jet_pt.size(); i < ie; i++) {
        if (fabs(mevent->hlt_calo_jet_eta[i]) < 2.5 and mevent->hlt_calo_jet_pt[i] > 40.0) {
            alt_hlt_calo_ht += mevent->hlt_calo_jet_pt[i];
        }
    }

    // Prepare some tiny helpers to select jets in relevant eta ranges
    for (int j=0; j < nofflinepfjets; ++j) {
        Jet_Eta_Helper tmp_helper;
        tmp_helper.pt  = mevent->jet_pt[j];
        tmp_helper.eta = mevent->jet_eta[j];
        jet_eta_helper.push_back(tmp_helper);
    }

    std::vector<Jet_Eta_Helper> jets_eta2p6;
    std::vector<Jet_Eta_Helper> jets_eta2p5;
    std::vector<Jet_Eta_Helper> jets_eta2p3;
    std::vector<Jet_Eta_Helper> jets_eta2p0;
    std::copy_if(jet_eta_helper.begin(), jet_eta_helper.end(), std::back_inserter(jets_eta2p6), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.6; });
    std::copy_if(jet_eta_helper.begin(), jet_eta_helper.end(), std::back_inserter(jets_eta2p5), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.5; });
    std::copy_if(jet_eta_helper.begin(), jet_eta_helper.end(), std::back_inserter(jets_eta2p3), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.3; });
    std::copy_if(jet_eta_helper.begin(), jet_eta_helper.end(), std::back_inserter(jets_eta2p0), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.0; });
    int njets_eta2p6 = jets_eta2p6.size();
    int njets_eta2p5 = jets_eta2p5.size();
    int njets_eta2p3 = jets_eta2p3.size();
    int njets_eta2p0 = jets_eta2p0.size();


    for (int i=0, ie=mevent->calo_jet_pt.size(); i < ie; i++) {
        Jet_Eta_Helper tmp_calo_helper;
        tmp_calo_helper.pt  = mevent->calo_jet_pt[i];
        tmp_calo_helper.eta = mevent->calo_jet_eta[i];
        calojet_eta_helper.push_back(tmp_calo_helper);
    }

    std::vector<Jet_Eta_Helper> calojets_eta2p6;
    std::vector<Jet_Eta_Helper> calojets_eta2p5;
    std::vector<Jet_Eta_Helper> calojets_eta2p3;
    std::vector<Jet_Eta_Helper> calojets_eta2p0;
    std::copy_if(calojet_eta_helper.begin(), calojet_eta_helper.end(), std::back_inserter(calojets_eta2p6), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.6; });
    std::copy_if(calojet_eta_helper.begin(), calojet_eta_helper.end(), std::back_inserter(calojets_eta2p5), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.5; });
    std::copy_if(calojet_eta_helper.begin(), calojet_eta_helper.end(), std::back_inserter(calojets_eta2p3), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.3; });
    std::copy_if(calojet_eta_helper.begin(), calojet_eta_helper.end(), std::back_inserter(calojets_eta2p0), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.0; });
    int ncalojets_eta2p6 = calojets_eta2p6.size();
    int ncalojets_eta2p5 = calojets_eta2p5.size();
    int ncalojets_eta2p3 = calojets_eta2p3.size();
    //int ncalojets_eta2p0 = calojets_eta2p0.size();

    // The calo_jet_ht variable in Event.h considers ALL calojets in event; we only want those with |eta| < 2.5
    float alt_calo_ht_40 = 0.0;
    float alt_calo_ht_30 = 0.0;
    for (auto calojet : calojets_eta2p5) {
        alt_calo_ht_40 += calojet.pt * (calojet.pt > 40.0);
        alt_calo_ht_30 += calojet.pt * (calojet.pt > 30.0);
    }

    // Sort jets by DECREASING number of displaced tracks, then record the second entry 
    std::sort(jet_track_helper.begin(), jet_track_helper.end(), [](Jet_Track_Helper const &a, Jet_Track_Helper &b) -> bool{ return a.ndisp > b.ndisp; } );
    int second_most_disp_tks = jet_track_helper.size() >= 2 ? jet_track_helper[1].ndisp : -9;

    // Sort jets by INCREASING number of prompt tracks, then record the second entry
    std::sort(jet_track_helper.begin(), jet_track_helper.end(), [](Jet_Track_Helper const &a, Jet_Track_Helper &b) -> bool{ return a.nprompt < b.nprompt; } );
    int second_least_prompt_tks = jet_track_helper.size() >= 2 ? jet_track_helper[1].nprompt : 999;


    // Find min deta between pairs of threshold (high Pt) jets
    for (int i=0; i < nofflinepfjets-1; i++) {
        if (mevent->nth_jet_pt(i) < 125.0) continue;
        float eta_i = mevent->nth_jet_eta(i);

        for (int j=i+1; j < nofflinepfjets; j++) {
            if (mevent->nth_jet_pt(j) < 125.0) continue;
            float eta_j = mevent->nth_jet_eta(j);

            if (fabs(eta_i - eta_j) < min_threshjet_deta) {
                min_threshjet_deta = fabs(eta_i-eta_j);
            }
        }
    }

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
    if ((std::size(mevent->jet_bdisc_deepflav) == 0)) return;

    // Count number of btagged jets
    for(size_t i = 0, ie = mevent->jet_bdisc_deepcsv.size(); i < ie; i++) {
        // While in this loop, let's sort jets by bscore
        Jet_BHelper tmp_bsort_helper;
        if      (ul_year == 2017) tmp_bsort_helper.bscore = mevent->jet_bdisc_deepcsv[i];
        else if (ul_year == 2018) tmp_bsort_helper.bscore = mevent->jet_bdisc_deepflav[i];
        bsort_helpers.push_back(tmp_bsort_helper);

    }

    // Actually sort the jets by bscore now
    std::sort(bsort_helpers.begin(), bsort_helpers.end(), [](Jet_BHelper const &a, Jet_BHelper &b) -> bool{ return a.bscore > b.bscore; } );


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    std::vector<bool> di_filt_res;
    std::vector<bool> tri_filt_res;
    std::vector<bool> tri_filt_skew_res;
    std::vector<bool> tri_filt_symm_res;
    std::vector<bool> dd_dtk_filt_res;
    std::vector<bool> dd_inc_filt_res;

    if (ul_year == 2017) {
        di_filt_res =     { mevent->pass_filter(0), mevent->pass_filter(1), mevent->pass_filter(2), mevent->pass_filter(3) };
        tri_filt_res =    { mevent->pass_filter(7), mevent->pass_filter(8), mevent->pass_filter(9), mevent->pass_filter(10), mevent->pass_filter(11), mevent->pass_filter(12),
            mevent->pass_filter(13), mevent->pass_filter(14), mevent->pass_filter(15), mevent->pass_filter(16) };
        dd_dtk_filt_res = { mevent->pass_filter(21), mevent->pass_filter(22), mevent->pass_filter(23), mevent->pass_filter(24), mevent->pass_filter(25) };
        dd_inc_filt_res = { mevent->pass_filter(26), mevent->pass_filter(27), mevent->pass_filter(28), mevent->pass_filter(29) };
    }

    if (ul_year == 2018) {
        di_filt_res     = { mevent->pass_filter(mfv::b_hltDoubleCaloBJets100eta2p3), mevent->pass_filter(mfv::b_hltBTagCaloDeepCSV0p71Double6Jets80),
                            mevent->pass_filter(mfv::b_hltDoublePFJets116Eta2p3), mevent->pass_filter(mfv::b_hltDoublePFJets116Eta2p3MaxDeta1p6) };

        tri_filt_res    = { mevent->pass_filter(mfv::b_hltQuadCentralJet30), mevent->pass_filter(mfv::b_hltCaloQuadJet30HT320),
                            mevent->pass_filter(mfv::b_hltBTagCaloDeepCSVp17Double), mevent->pass_filter(mfv::b_hltPFCentralJetLooseIDQuad30),
                            mevent->pass_filter(mfv::b_hlt1PFCentralJetLooseID75), mevent->pass_filter(mfv::b_hlt2PFCentralJetLooseID60),
                            mevent->pass_filter(mfv::b_hlt3PFCentralJetLooseID45), mevent->pass_filter(mfv::b_hlt4PFCentralJetLooseID40),
                            mevent->pass_filter(mfv::b_hltPFCentralJetsLooseIDQuad30HT330), mevent->pass_filter(mfv::b_hltBTagPFDeepCSV4p5Triple) };

        dd_dtk_filt_res = { mevent->pass_filter(mfv::b_hltHT430), mevent->pass_filter(mfv::b_hltDoubleCentralCaloJetpt40),
                            mevent->pass_filter(mfv::b_hltTwoPromptHLTL3DisplacedDijetFullTracksHLTCaloJetTagFilterLowPt),
                            mevent->pass_filter(mfv::b_hltL4PromptDisplacedDijetFullTracksHLTCaloJetTagFilterLowPt),
                            mevent->pass_filter(mfv::b_hltL4DisplacedDijetFullTracksHLTCaloJetTagFilterLowPt) };

        dd_inc_filt_res = { mevent->pass_filter(mfv::b_hltHT650), mevent->pass_filter(mfv::b_hltDoubleCentralCaloJetpt60),
                            mevent->pass_filter(mfv::b_hltTwoPromptHLTL3DisplacedDijetFullTracksHLTCaloJetTagFilterMidPt),
                            mevent->pass_filter(mfv::b_hltL4PromptDisplacedDijetFullTracksHLTCaloJetTagFilterMidPt) };

    }

    if (ul_year == 20161 or ul_year == 20162) {

        di_filt_res       = { mevent->pass_filter(mfv::b_hltDoubleJetsC100), mevent->pass_filter(mfv::b_hltBTagCaloCSVp014DoubleWithMatching),
                              mevent->pass_filter(mfv::b_hltDoublePFJetsC100), mevent->pass_filter(mfv::b_hltDoublePFJetsC100MaxDeta1p6) };

        tri_filt_skew_res = { mevent->pass_filter(mfv::b_hltQuadCentralJet30), mevent->pass_filter(mfv::b_hltDoubleCentralJet90),  
                              mevent->pass_filter(mfv::b_hltBTagCaloCSVp087Triple), mevent->pass_filter(mfv::b_hltQuadPFCentralJetLooseID30), 
                              mevent->pass_filter(mfv::b_hltDoublePFCentralJetLooseID90) };

        tri_filt_symm_res = { mevent->pass_filter(mfv::b_hltQuadCentralJet45), mevent->pass_filter(mfv::b_hltBTagCaloCSVp087Triple),
                              mevent->pass_filter(mfv::b_hltQuadPFCentralJetLooseID45) };


        dd_dtk_filt_res   = { mevent->pass_filter(mfv::b_hltHT350), mevent->pass_filter(mfv::b_hltDoubleCentralCaloJetpt40),
                              mevent->pass_filter(mfv::b_hltTwoPromptHLTL3DisplacedDijetFullTracksHLTCaloJetTagFilterLowPt),
                              mevent->pass_filter(mfv::b_hltL4PromptDisplacedDijetFullTracksHLTCaloJetTagFilterLowPt),
                              mevent->pass_filter(mfv::b_hltL4DisplacedDijetFullTracksHLTCaloJetTagFilterLowPt) };

        dd_inc_filt_res   = { mevent->pass_filter(mfv::b_hltHT650), mevent->pass_filter(mfv::b_hltDoubleCentralCaloJetpt80),
                              mevent->pass_filter(mfv::b_hltTwoPromptHLTL3DisplacedDijetFullTracksHLTCaloJetTagFilter),
                              mevent->pass_filter(mfv::b_hltL4PromptDisplacedDijetFullTracksHLTCaloJetTagFilter) };
    }

    // Filters for 2016 di-bjet trigger (40-43, n=4)




    // Welcome to nested conditional hell >:)
    //
    // First up, all of the di-bjet filters
    if (true) {
    //if (mevent->pass_l1(mfv::b_L1_DoubleJet100er2p3_dEta_Max1p6))
        h_di_filter_00[DEN]->Fill(ncalojets_eta2p3 > 1 ? calojets_eta2p3[1].pt : -1.0, w);
        if (di_filt_res[0]) {
            h_di_filter_00[NUM]->Fill(ncalojets_eta2p3 > 1 ? calojets_eta2p3[1].pt : -1.0, w);
            h_di_filter_01[DEN]->Fill(bsort_helpers[1].bscore, w);

            if (di_filt_res[1]) {
            //if (true)
                h_di_filter_01[NUM]->Fill(bsort_helpers[1].bscore, w);
                h_di_filter_02[DEN]->Fill(njets_eta2p3 > 1 ? jets_eta2p3[1].pt : -1.0, w);

                if (di_filt_res[2]) {
                    h_di_filter_02[NUM]->Fill(njets_eta2p3 > 1 ? jets_eta2p3[1].pt : -1.0, w);
                    h_di_filter_03[DEN]->Fill(min_threshjet_deta, w);

                    if (di_filt_res[3]) {
                        h_di_filter_03[NUM]->Fill(min_threshjet_deta, w);
                    }
                }
            }
        }
    }

    // Next, all of the more complex tri-bjet filters
    // Make sure this only runs when parsing 2017/2018 conditions
    if (ul_year == 2018 or ul_year == 2017) {
    // if (mevent->pass_l1(mfv::b_L1_HTT320er)) 
        h_tri_filter_00[DEN]->Fill(ncalojets_eta2p5 > 3 ? calojets_eta2p5[3].pt : -1.0, w);
        if (tri_filt_res[0]) {
            h_tri_filter_00[NUM]->Fill(ncalojets_eta2p5 > 3 ? calojets_eta2p5[3].pt : -1.0, w);
            h_tri_filter_01[DEN]->Fill(alt_calo_ht_30, w);

            if (tri_filt_res[1]) {
                h_tri_filter_01[NUM]->Fill(alt_calo_ht_30, w);
                h_tri_filter_02[DEN]->Fill(bsort_helpers[1].bscore, w);

                if (tri_filt_res[2]) {
                //if (true) 
                    h_tri_filter_02[NUM]->Fill(bsort_helpers[1].bscore, w);
                    h_tri_filter_03[DEN]->Fill(njets_eta2p5 > 3 ? jets_eta2p5[3].pt : -1.0, w);

                    if (tri_filt_res[3]) {
                        h_tri_filter_03[NUM]->Fill(njets_eta2p5 > 3 ? jets_eta2p5[3].pt : -1.0, w);
                        h_tri_filter_04[DEN]->Fill(njets_eta2p5 > 0 ? jets_eta2p5[0].pt : -1.0, w);

                        if (tri_filt_res[4]) {
                            h_tri_filter_04[NUM]->Fill(njets_eta2p5 > 0 ? jets_eta2p5[0].pt : -1.0, w);
                            h_tri_filter_05[DEN]->Fill(njets_eta2p5 > 1 ? jets_eta2p5[1].pt : -1.0, w);

                            if (tri_filt_res[5]) {
                                h_tri_filter_05[NUM]->Fill(njets_eta2p5 > 1 ? jets_eta2p5[1].pt : -1.0, w);
                                h_tri_filter_06[DEN]->Fill(njets_eta2p5 > 2 ? jets_eta2p5[2].pt : -1.0, w);

                                if (tri_filt_res[6]) {
                                    h_tri_filter_06[NUM]->Fill(njets_eta2p5 > 2 ? jets_eta2p5[2].pt : -1.0, w);
                                    h_tri_filter_07[DEN]->Fill(njets_eta2p5 > 3 ? jets_eta2p5[3].pt : -1.0, w);

                                    if (tri_filt_res[7]) {
                                        h_tri_filter_07[NUM]->Fill(njets_eta2p5 > 3 ? jets_eta2p5[3].pt : -1.0, w);
                                        h_tri_filter_08[DEN]->Fill(mevent->jet_ht(30), w);

                                        if (tri_filt_res[8]) {
                                            h_tri_filter_08[NUM]->Fill(mevent->jet_ht(30), w);
                                            h_tri_filter_09[DEN]->Fill(bsort_helpers[2].bscore, w);

                                            if (tri_filt_res[9]) {
                                                h_tri_filter_09[NUM]->Fill(bsort_helpers[2].bscore, w);

                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Okay, now we'll look at the tri-bjet (skew) trigger filters
    // Only run this when parsing 2016(APV) files
    if (ul_year == 20161 or ul_year == 20162) {
        h_tri_skew_filter_00[DEN]->Fill(ncalojets_eta2p6 > 3 ? calojets_eta2p6[3].pt : -1.0, w);
        if (tri_filt_skew_res[0]) {
            h_tri_skew_filter_00[NUM]->Fill(ncalojets_eta2p6 > 3 ? calojets_eta2p6[3].pt : -1.0, w);
            h_tri_skew_filter_01[DEN]->Fill(ncalojets_eta2p6 > 1 ? calojets_eta2p6[1].pt : -1.0, w);

            if (tri_filt_skew_res[1]) {
                h_tri_skew_filter_01[NUM]->Fill(ncalojets_eta2p6 > 1 ? calojets_eta2p6[1].pt : -1.0, w);
                h_tri_skew_filter_02[DEN]->Fill(bsort_helpers[2].bscore, w);
        
                if (tri_filt_skew_res[2]) {
                    h_tri_skew_filter_02[NUM]->Fill(bsort_helpers[2].bscore, w);
                    h_tri_skew_filter_03[DEN]->Fill(njets_eta2p6 > 3 ? jets_eta2p6[3].pt : -1.0, w);
        
                    if (tri_filt_skew_res[3]) {
                        h_tri_skew_filter_03[NUM]->Fill(njets_eta2p6 > 3 ? jets_eta2p6[3].pt : -1.0, w);
                        h_tri_skew_filter_04[DEN]->Fill(njets_eta2p6 > 1 ? jets_eta2p6[1].pt : -1.0, w);

                        if (tri_filt_skew_res[4]) {
                            h_tri_skew_filter_04[NUM]->Fill(njets_eta2p6 > 1 ? jets_eta2p6[1].pt : -1.0, w);
                        }
                    }
                }
            }
        }
    }

    // Okay, now we'll look at the tri-bjet (symm) trigger filters
    // Only run this when parsing 2016(APV) files
    if (ul_year == 20161 or ul_year == 20162) {
        h_tri_symm_filter_00[DEN]->Fill(ncalojets_eta2p6 > 3 ? calojets_eta2p6[3].pt : -1.0, w);
        if (tri_filt_symm_res[0]) {
            h_tri_symm_filter_00[NUM]->Fill(ncalojets_eta2p6 > 3 ? calojets_eta2p6[3].pt : -1.0, w);
            h_tri_symm_filter_01[DEN]->Fill(bsort_helpers[2].bscore, w);

            if (tri_filt_symm_res[1]) {
                h_tri_symm_filter_01[NUM]->Fill(bsort_helpers[2].bscore ,w);
                h_tri_symm_filter_02[DEN]->Fill(njets_eta2p6 > 3 ? jets_eta2p6[3].pt : -1.0, w);
        
                if (tri_filt_symm_res[2]) {
                    h_tri_symm_filter_02[NUM]->Fill(njets_eta2p6 > 3 ? jets_eta2p6[3].pt : -1.0, w);
                }
            }
        }
    }



    // Now, the displaced dijet + displaced track filters:
    // if (mevent->pass_l1(mfv::b_L1_HTT320er)) 
    if (true) {
        h_dd_dtk_filter_00[DEN]->Fill(mevent->jet_ht(40), w);
        h_dd_dtk_filter_alt_d_00[DEN]->Fill(alt_calo_ht_30, w);
        if (dd_dtk_filt_res[0] ) {
            h_dd_dtk_filter_00[NUM]->Fill(mevent->jet_ht(40), w);
            h_dd_dtk_filter_alt_d_00[NUM]->Fill(alt_calo_ht_30, w);
            h_dd_dtk_filter_01[DEN]->Fill(njets_eta2p0 > 1 ? jets_eta2p0[1].pt : -1.0, w);

            if (dd_dtk_filt_res[1]) {
                h_dd_dtk_filter_01[NUM]->Fill(njets_eta2p0 > 1 ? jets_eta2p0[1].pt : -1.0, w);
                h_dd_dtk_filter_02[DEN]->Fill(second_least_prompt_tks, w);

                for (auto helper : jet_track_helper) {

                    // At this point, events pass the HT and pT filters, so now we try to
                    // figure out the track-based jet tag efficiencies
                    if (not helper.matches_calo_jet) continue;
                    h_calojet_pt_den0->Fill(helper.pt, w);
                    h_calojet_eta_den0->Fill(helper.eta, w);
                    h_calojet_ntks->Fill(helper.ntks, w);
                    h_calojet_ntks_nprompt->Fill(helper.ntks, helper.nprompt, w);
                    h_calojet_nprompt_tks->Fill(helper.nprompt, w);
                    if (helper.matches_hlt_nprompt_jet) {h_calojet_matched_nprompt_tks->Fill(helper.nprompt, w); h_calojet_pt_num0->Fill(helper.pt, w); h_calojet_eta_num0->Fill(helper.eta, w);}
                }

                if (dd_dtk_filt_res[2]) {
                    h_dd_dtk_filter_02[NUM]->Fill(second_least_prompt_tks, w);
                    h_dd_dtk_filter_03[DEN]->Fill(second_least_prompt_tks, w);


                    if (dd_dtk_filt_res[3]) {
                        h_dd_dtk_filter_03[NUM]->Fill(second_least_prompt_tks, w);
                        h_dd_dtk_filter_04[DEN]->Fill(second_most_disp_tks, w);

                        // Displaced track tag efficiency
                        for (auto helper : jet_track_helper) {
                            if (not helper.matches_calo_jet) continue;
                            h_calojet_pt_den1->Fill(helper.pt, w);
                            h_calojet_eta_den1->Fill(helper.eta, w);
                            h_calojet_ndisp_tks->Fill(helper.ndisp, w);
                            if (helper.matches_hlt_ndisp_jet) {h_calojet_matched_ndisp_tks->Fill(helper.ndisp, w); h_calojet_pt_num1->Fill(helper.pt, w); h_calojet_eta_num1->Fill(helper.eta, w);}
                        }

                        if (dd_dtk_filt_res[4]) {
                            h_dd_dtk_filter_04[NUM]->Fill(second_most_disp_tks, w);
                        }
                    }
                }
            }
        }
    }

    // Now, the inclusive displaced dijet filters:
    if (true) {
    // if (mevent->pass_l1(mfv::b_L1_HTT320er)) {
        h_dd_inc_filter_00[DEN]->Fill(mevent->jet_ht(40), w);
        h_dd_inc_filter_alt_d_00[DEN]->Fill(alt_calo_ht_30, w);
        if (dd_inc_filt_res[0]) {
            h_dd_inc_filter_00[NUM]->Fill(mevent->jet_ht(40), w);
            h_dd_inc_filter_alt_d_00[NUM]->Fill(alt_calo_ht_30, w);
            h_dd_inc_filter_01[DEN]->Fill(njets_eta2p0 > 1 ? jets_eta2p0[1].pt : -1.0, w);

            if (dd_inc_filt_res[1]) {
                h_dd_inc_filter_01[NUM]->Fill(njets_eta2p0 > 1 ? jets_eta2p0[1].pt : -1.0, w);
                h_dd_inc_filter_02[DEN]->Fill(second_least_prompt_tks, w);

                if (dd_inc_filt_res[2]) {
                    h_dd_inc_filter_02[NUM]->Fill(second_least_prompt_tks, w);
                    h_dd_inc_filter_03[DEN]->Fill(second_least_prompt_tks, w);

                    if (dd_inc_filt_res[3]) {
                        h_dd_inc_filter_03[NUM]->Fill(second_least_prompt_tks, w);
                    }
                }
            }
        }
    }

    // Done with nested conditional hell
    // SHAUN: There has got to be a better way to do all of this
}

DEFINE_FWK_MODULE(MFVFilterHistos);
