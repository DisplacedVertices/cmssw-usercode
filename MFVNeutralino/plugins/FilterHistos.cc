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
        const int ul_year;
        const bool is_dibjet;

        const double offline_csv = jmt::BTagging::discriminator_min(1, 1);
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

        TH1F* h_filt_nsurvive;

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
    ul_year(cfg.getParameter<int>("ul_year")),
    is_dibjet(cfg.getParameter<bool>("is_dibjet")),
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

    h_filt_nsurvive      = fs->make<TH1F>("h_filt_nsurvive", ";;entries", 24, 0, 24);


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

    std::vector<TString> xlabels = {TString("starting number"),  TString("after calojet pt"), TString("after di-btag"), TString("after pfjet pt"), TString("after pfjet dEta"), TString("after first pT3"), TString("after CaloHT"), TString("after di-btag"), TString("after second pT3"), TString("after pT0"), TString("after pT1"), TString("after pT2"), TString("after third pT4"), TString("after PFHT"), TString("after tri-btag"), TString("after CaloHT430"), TString("after calo pT1"), TString("after pmpt_tk_0"), TString("after pmpt_tk_1"), TString("after disp_tk"), TString("after CaloHT650"), TString("after calo pT1"), TString("after pmpt_tk_0"), TString("after pmpt_tk_1")};

    for (int i = 0; i < mfv::n_filter_paths; ++i) {
        h_filter_bits->GetXaxis()->SetBinLabel(i+2, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_filter_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_filter_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_seqfilt_bit_matrix->GetXaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
        h_seqfilt_bit_matrix->GetYaxis()->SetBinLabel(i+1, TString::Format(" pass %s", mfv::filter_paths[i]));
    }

    int ilabel = 1;
    for (auto mystring : xlabels) {
        h_filt_nsurvive->GetXaxis()->SetBinLabel(ilabel, mystring);
        ilabel++;
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

        h_dd_dtk_filter_00[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_00_%s", bres.Data()), "CaloHT430 Filter; CaloHT(40) (GeV); entries",                           100, 0, 1000);
        h_dd_dtk_filter_alt_d_00[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_alt_d_00_%s", bres.Data()), "CaloHT430 Filter;CaloHT(30) (GeV); entries",               100, 0, 1000);
        h_dd_dtk_filter_01[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_01_%s", bres.Data()), "Two CaloPT>40 Filter; 2nd-highest jet pT (GeV); entries",                100, 0, 300);
        h_dd_dtk_filter_02[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_02_%s", bres.Data()), "First prompt tk filter; 2nd smallest prompt tk multiplicity; entries",     30, 0, 30);
        h_dd_dtk_filter_03[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_03_%s", bres.Data()), "Second prompt tk filter; 2nd smallest prompt tk multiplicity",             30, 0, 30);
        h_dd_dtk_filter_04[i] = fs->make<TH1F>(TString::Format("h_dd_dtk_filter_04_%s", bres.Data()), "Displaced tk filter; 2nd largest disp track multiplicity; entries",        30, 0, 30);

        h_dd_inc_filter_00[i] = fs->make<TH1F>(TString::Format("h_dd_inc_filter_00_%s", bres.Data()), "CaloHT650 Filter; CaloHT(40) (GeV); entries",                          100, 0, 1000);
        h_dd_inc_filter_alt_d_00[i] = fs->make<TH1F>(TString::Format("h_dd_inc_filter_alt_d_00_%s", bres.Data()), "CaloHT650 Filter;CaloHT(30) (GeV); entries",               100, 0, 1000);
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

struct CaloJet_Central_Helper {
    float pt = 0.0;
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

    std::vector<Jet_Eta_Helper> jets_eta2p5;
    std::vector<Jet_Eta_Helper> jets_eta2p3;
    std::vector<Jet_Eta_Helper> jets_eta2p0;
    std::copy_if(jet_eta_helper.begin(), jet_eta_helper.end(), std::back_inserter(jets_eta2p5), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.5; });
    std::copy_if(jet_eta_helper.begin(), jet_eta_helper.end(), std::back_inserter(jets_eta2p3), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.3; });
    std::copy_if(jet_eta_helper.begin(), jet_eta_helper.end(), std::back_inserter(jets_eta2p0), [](Jet_Eta_Helper const &a) { return fabs(a.eta) < 2.0; });
    int njets_eta2p5 = jets_eta2p5.size();
    int njets_eta2p3 = jets_eta2p3.size();
    int njets_eta2p0 = jets_eta2p0.size();

    // The calo_jet_ht variable in Event.h considers ALL calojets in event; we only want those with |eta| < 2.5
    float alt_calo_ht_40 = 0.0;
    float alt_calo_ht_30 = 0.0;
    std::vector<CaloJet_Central_Helper> calojet_central_helper;
    for (int i=0, ie=mevent->calo_jet_pt.size(); i < ie; i++) {
        // Calculating alt_calo_ht_40, 35, 40
        float this_pt = mevent->calo_jet_pt[i];
        CaloJet_Central_Helper temp_helper;
        if (fabs(mevent->calo_jet_eta[i]) > 2.5) continue;
        alt_calo_ht_40 += this_pt * (this_pt > 40.0);
        alt_calo_ht_30 += this_pt * (this_pt > 30.0);
        temp_helper.pt = this_pt;
        calojet_central_helper.push_back(temp_helper);
    }

    // Get the second-highest pT calo jet within |eta| < 2.0 (for dd triggers)
    float scnd_leading_cent_calo_pt = -2.0;
    bool  skip_first = true;
    for (int i=0, ie=mevent->calo_jet_pt.size(); i < ie; i++) {
        // Getting second-leading central calojet pT
        if (fabs(mevent->calo_jet_eta[i]) > 2.0) continue;     // skip if not a central jet
        if (skip_first) { skip_first = false; continue; }      // skip if this is the leading central calojet
        else            { scnd_leading_cent_calo_pt = mevent->calo_jet_pt[i]; break; }
    }

    // Get the second-highest pT calo jet within |eta| < 2.3 (for dd triggers)
    float scnd_leading_bjet_trig_calo_pt = -2.0;
    bool  skip_first_bjet_trig = true;
    for (int i=0, ie=mevent->calo_jet_pt.size(); i < ie; i++) {
        // Getting second-leading central calojet pT
        if (fabs(mevent->calo_jet_eta[i]) > 2.3) continue;                      // skip if not a central jet
        if (skip_first_bjet_trig) { skip_first_bjet_trig = false; continue; }   // skip if this is the leading central calojet
        else { scnd_leading_bjet_trig_calo_pt = mevent->calo_jet_pt[i]; break; }
    }

    // Sort jets by DECREASING number of displaced tracks, then record the second entry 
    std::sort(jet_track_helper.begin(), jet_track_helper.end(), [](Jet_Track_Helper const &a, Jet_Track_Helper &b) -> bool{ return a.ndisp > b.ndisp; } );
    int second_most_disp_tks = jet_track_helper.size() >= 2 ? jet_track_helper[1].ndisp : -9;

    // Sort jets by INCREASING number of prompt tracks, then record the second entry
    std::sort(jet_track_helper.begin(), jet_track_helper.end(), [](Jet_Track_Helper const &a, Jet_Track_Helper &b) -> bool{ return a.nprompt < b.nprompt; } );
    int second_least_prompt_tks = jet_track_helper.size() >= 2 ? jet_track_helper[1].nprompt : 999;

    // Sort CaloJet_Central_Helper entries by descending pT (they should already be in this order, but let's be safe)
    std::sort(calojet_central_helper.begin(), calojet_central_helper.end(), [](CaloJet_Central_Helper const &a, CaloJet_Central_Helper &b) -> bool{ return a.pt > b.pt; } );
    float fourth_central_calojet_pt = calojet_central_helper.size() >= 4 ? calojet_central_helper[3].pt : -9.9;


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
        di_filt_res     = { mevent->pass_filter(0), mevent->pass_filter(4), mevent->pass_filter(5), mevent->pass_filter(6) };
        tri_filt_res    = { mevent->pass_filter(7), mevent->pass_filter(17), mevent->pass_filter(18), mevent->pass_filter(10), mevent->pass_filter(11), mevent->pass_filter(12),
            mevent->pass_filter(13), mevent->pass_filter(14), mevent->pass_filter(19), mevent->pass_filter(20) };
        dd_dtk_filt_res = { mevent->pass_filter(21), mevent->pass_filter(22), mevent->pass_filter(23), mevent->pass_filter(24), mevent->pass_filter(25) };
        dd_inc_filt_res = { mevent->pass_filter(26), mevent->pass_filter(27), mevent->pass_filter(28), mevent->pass_filter(29) };
    }


    //FIXME delete this garbage
    if (scnd_leading_cent_calo_pt and false) {
        std::cout << "hello I'm garbage" << std::endl;
    }

    // Fill the starting bin of h_filt_nsurvive
    h_filt_nsurvive->Fill(0.1, w);

    // Fill the di-bjet bins in h_filt_nsurvive
    for (int ibin=2; ibin <= 5; ibin++) {
        if (di_filt_res[ibin-2]) { h_filt_nsurvive->Fill(ibin-1, w); }
        else break;
    }

    // Fill the tri-bjet bins in h_filt_nsurvive
    for (int ibin=6; ibin <= 15; ibin++) {
        if (tri_filt_res[ibin-6]) { h_filt_nsurvive->Fill(ibin-1, w); }
        else break;
    }

    // Fill the low-HT displaced dijet bins in h_filt_nsurvive
    for (int ibin=16; ibin <= 20; ibin++) {
        if (dd_dtk_filt_res[ibin-16]) { h_filt_nsurvive->Fill(ibin-1, w); }
        else break;
    }

    // Fill the high-HT displaced dijet bins in h_filt_nsurvive
    for (int ibin=21; ibin <= 24; ibin++) {
        if (dd_inc_filt_res[ibin-21]) { h_filt_nsurvive->Fill(ibin-1, w); }
        else break;
    }


    // Welcome to nested conditional hell >:)
    //
    // First up, all of the di-bjet filters
    if (mevent->pass_l1(mfv::b_L1_DoubleJet100er2p3_dEta_Max1p6)) {
        h_di_filter_00[DEN]->Fill(scnd_leading_bjet_trig_calo_pt, w);
        if (di_filt_res[0]) {
            h_di_filter_00[NUM]->Fill(scnd_leading_bjet_trig_calo_pt, w);
            h_di_filter_01[DEN]->Fill(bsort_helpers[1].bscore, w);
    
            //if (di_filt_res[1]) {
            if (true) {
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

    // Next, all of the tri-bjet filters
    if (mevent->pass_l1(mfv::b_L1_HTT320er)) {
        h_tri_filter_00[DEN]->Fill(fourth_central_calojet_pt, w);
        if (tri_filt_res[0]) {
            h_tri_filter_00[NUM]->Fill(fourth_central_calojet_pt, w);
            h_tri_filter_01[DEN]->Fill(alt_calo_ht_30, w);
    
            if (tri_filt_res[1]) {
                h_tri_filter_01[NUM]->Fill(alt_calo_ht_30, w);
                h_tri_filter_02[DEN]->Fill(bsort_helpers[1].bscore, w);
    
                //if (tri_filt_res[2]) {
                if (true) {
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

    // Now, the displaced dijet + displaced track filters:
    h_dd_dtk_filter_00[DEN]->Fill(mevent->jet_ht(40), w);
    h_dd_dtk_filter_alt_d_00[DEN]->Fill(mevent->jet_ht(30), w);
    if (dd_dtk_filt_res[0] ) {
    //if (dd_dtk_filt_res[0] and mevent->pass_l1(mfv::b_L1_HTT380er)) {
        h_dd_dtk_filter_00[NUM]->Fill(mevent->jet_ht(40), w);
        h_dd_dtk_filter_alt_d_00[NUM]->Fill(mevent->jet_ht(30), w);
        h_dd_dtk_filter_01[DEN]->Fill(njets_eta2p0 > 1 ? jets_eta2p5[1].pt : -1.0, w);

        if (dd_dtk_filt_res[1]) {
            h_dd_dtk_filter_01[NUM]->Fill(njets_eta2p0 > 1 ? jets_eta2p5[1].pt : -1.0, w);
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

    // Now, the inclusive displaced dijet filters:
    h_dd_inc_filter_00[DEN]->Fill(mevent->jet_ht(40), w);
    h_dd_inc_filter_alt_d_00[DEN]->Fill(mevent->jet_ht(30), w);
    if (dd_inc_filt_res[0]) {
    //if (dd_inc_filt_res[0] and mevent->pass_l1(mfv::b_L1_HTT380er)) {
        h_dd_inc_filter_00[NUM]->Fill(mevent->jet_ht(40), w);
        h_dd_inc_filter_alt_d_00[NUM]->Fill(mevent->jet_ht(40), w);
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
    
    // Done with nested conditional hell
    // SHAUN: There has got to be a better way to do all of this
}

DEFINE_FWK_MODULE(MFVFilterHistos);
