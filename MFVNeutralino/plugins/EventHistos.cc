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
#include "JMTucker/Tools/interface/UncertTools.h"
//#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

class MFVEventHistos : public edm::EDAnalyzer {
    public:
        explicit MFVEventHistos(const edm::ParameterSet&);
        void analyze(const edm::Event&, const edm::EventSetup&);

    private:
        const edm::EDGetTokenT<MFVEvent> mevent_token;
        //const edm::EDGetTokenT<reco::GenParticleCollection> gen_token;
        const edm::EDGetTokenT<double> weight_token;

        const double temp_caloht_cut;
        const bool   require_two_good_leptons;

        TH1F* h_w;
        TH1F* h_eventid;

        TH2F* h_gen_decay;
        TH1F* h_gen_flavor_code;

        TH1F* h_nbquarks;
        TH1F* h_bquark_pt;
        TH1F* h_bquark_eta;
        TH1F* h_bquark_phi;
        TH1F* h_bquark_energy;
        TH1F* h_bquark_pairdphi;

        TH1F* h_minlspdist2d;
        TH1F* h_lspdist2d;
        TH1F* h_lspdist3d;
        TH1F* h_gen_bs2ddist;
        TH2F* h_gen_bsxdist_bsydist;

        TH1F* h_hlt_bits;
        TH2F* h_hlt_bit_grid;
        TH1F* h_l1_bits;

        TH1F* h_npu;

        TH1F* h_bsx;
        TH1F* h_bsy;
        TH1F* h_bsz;
        TH1F* h_bsphi;

        TH1F* h_npv;
        TH1F* h_pvx;
        TH1F* h_pvy;
        TH1F* h_pvxwide;
        TH1F* h_pvywide;
        TH1F* h_pvz;
        TH1F* h_pvcxx;
        TH1F* h_pvcxy;
        TH1F* h_pvcxz;
        TH1F* h_pvcyy;
        TH1F* h_pvcyz;
        TH1F* h_pvczz;
        TH1F* h_pvrho;
        TH1F* h_pvrhowide;
        TH1F* h_pvphi;
        TH1F* h_pvntracks;
        TH1F* h_pvscore;
        TH1F* h_pvsx;
        TH1F* h_pvsy;
        TH1F* h_pvsxwide;
        TH1F* h_pvsywide;
        TH1F* h_pvsz;
        TH1F* h_pvsrho;
        TH1F* h_pvsrhowide;
        TH1F* h_pvsphi;
        TH1F* h_pvsscore;
        TH1F* h_pvsdz;
        TH1F* h_pvsmindz;
        TH1F* h_pvsmaxdz;
        TH1F* h_pvsmindz_minscore;
        TH1F* h_pvsmaxdz_minscore;
        TH1F* h_pvbs_dist;

        TH1F* h_njets;
        TH1F* h_njets20;
        TH1F* h_ncalojets;
        TH1F* h_ncalojets40;
        TH1F* h_nhltcalojets;
        TH1F* h_nhltcalojets40;
        TH1F* h_nhltbjets;
        TH1F* h_nhltcalobjets;
        TH1F* h_nhltcalobjets_low;
        static const int MAX_NJETS = 10;
        TH1F* h_jet_pt[MAX_NJETS+1];
        TH1F* h_jet_eta[MAX_NJETS+1];
        TH1F* h_jet_phi[MAX_NJETS+1];
        TH1F* h_jet_nseedtrack[MAX_NJETS+1];

        TH1F* h_jet_energy;
        TH1F* h_jet_ht;
        TH1F* h_jet_ht_40;
        TH2F* h_jet_calojet_ht;
        TH2F* h_jet_calojet_ht_40;
        TH1F* h_jet_diagnostics_lo;
        TH1F* h_jet_diagnostics_hi;

        TH1F* h_calojet_pt[MAX_NJETS+1];
        TH1F* h_calojet_eta[MAX_NJETS+1];
        TH1F* h_calojet_phi[MAX_NJETS+1];
        TH2F* h_calojet_i_pt;
        TH1F* h_calojet_ht_30;
        TH1F* h_calojet_ht_40;
        TH1F* h_calojet_diagnostics_lo;
        TH1F* h_calojet_diagnostics_hi;

        TH1F* h_jet_pairdphi;
        TH1F* h_jet_pairdr;

        TH1F* h_min_hltcalo_pfjet_dr;

        TH1F* h_met;
        TH1F* h_metphi;
        TH1F* h_metnomu;
        TH1F* h_metnomuphi;

        TH1F* h_nbtags[3];
        TH2F* h_nbtags_v_bquark_code[3];
        TH1F* h_jet_bdisc_csv;
        TH1F* h_jet_bdisc_deepcsv;
        TH1F* h_jet_bdisc_deepflav;
        TH2F* h_jet_bdisc_deepflav_v_bquark_code;
        TH1F* h_bjet_pt;
        TH1F* h_bjet_eta;
        TH1F* h_bjet_phi;
        TH1F* h_bjet_energy;
        TH1F* h_bjet_pairdphi;

        TH1F* h_thresh_csvtags;
        TH1F* h_thresh_hardcsvtags;

        TH1F* h_nmuons[2];
        TH1F* h_nelectrons[2];
        TH1F* h_nleptons[2];

        TH1F* h_leptons_pt[2][2];
        TH1F* h_leptons_eta[2][2];
        TH1F* h_leptons_phi[2][2];
        TH1F* h_leptons_dxy[2][2];
        TH1F* h_leptons_dxybs[2][2];
        TH1F* h_leptons_dz[2][2];
        TH1F* h_leptons_iso[2][2];

        TH1F* h_n_reljettks;

        TH1F* h_n_vertex_seed_tracks;
        TH1F* h_vertex_seed_track_chi2dof;
        TH1F* h_vertex_seed_track_q;
        TH1F* h_vertex_seed_track_pt;
        TH1F* h_vertex_seed_track_pt_barrel;
        TH1F* h_vertex_seed_track_pt_endcap;
        TH1F* h_vertex_seed_track_p;
        TH1F* h_vertex_seed_track_eta;
        TH1F* h_vertex_seed_track_phi;
        TH2F* h_vertex_seed_track_phi_v_eta;
        TH1F* h_vertex_seed_track_dxy;
        TH1F* h_vertex_seed_track_dz;
        TH1F* h_vertex_seed_track_err_pt;
        TH1F* h_vertex_seed_track_err_eta;
        TH1F* h_vertex_seed_track_err_phi;
        TH1F* h_vertex_seed_track_err_dxy;
        TH1F* h_vertex_seed_track_err_dz;
        TH1F* h_vertex_seed_track_npxhits;
        TH1F* h_vertex_seed_track_nsthits;
        TH1F* h_vertex_seed_track_nhits;
        TH1F* h_vertex_seed_track_npxlayers;
        TH1F* h_vertex_seed_track_nstlayers;
        TH1F* h_vertex_seed_track_nlayers;
};

MFVEventHistos::MFVEventHistos(const edm::ParameterSet& cfg)
    : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    temp_caloht_cut(cfg.getParameter<double>("temp_caloht_cut")),
    require_two_good_leptons(cfg.getParameter<bool>("require_two_good_leptons"))
{
    edm::Service<TFileService> fs;

    h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
    h_eventid = fs->make<TH1F>("h_eventid", ";eventid", 10000, 0, 10000);

    h_gen_decay = fs->make<TH2F>("h_gen_decay", "0-2=e,mu,tau, 3=h;decay code #0;decay code #1", 4, 0, 4, 4, 0, 4);
    h_gen_flavor_code = fs->make<TH1F>("h_gen_flavor_code", ";quark flavor composition;events", 3, 0, 3);

    h_nbquarks = fs->make<TH1F>("h_nbquarks", ";# of bquarks;events", 20, 0, 20);
    h_bquark_pt = fs->make<TH1F>("h_bquark_pt", ";bquarks p_{T} (GeV);bquarks/10 GeV", 100, 0, 1000);
    h_bquark_eta = fs->make<TH1F>("h_bquark_eta", ";bquarks #eta (rad);bquarks/.08", 100, -4, 4);
    h_bquark_phi = fs->make<TH1F>("h_bquark_phi", ";bquarks #phi (rad);bquarks/.063", 100, -3.1416, 3.1416);
    h_bquark_energy = fs->make<TH1F>("h_bquark_energy", ";bquarks energy (GeV);bquarks/10 GeV", 100, 0, 1000);
    h_bquark_pairdphi = fs->make<TH1F>("h_bquark_pairdphi", ";bquark pair #Delta#phi (rad);bquark pairs/.063", 100, -3.1416, 3.1416);

    h_minlspdist2d = fs->make<TH1F>("h_minlspdist2d", ";min dist2d(gen vtx #i) (cm);events/0.1 mm", 200, 0, 2);
    h_lspdist2d = fs->make<TH1F>("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
    h_lspdist3d = fs->make<TH1F>("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
    h_gen_bs2ddist = fs->make<TH1F>("h_gen_bs2ddist", ";dist2d(gen vtx, beamspot) (cm);arb. units", 500, 0, 2.5);
    h_gen_bsxdist_bsydist = fs->make<TH2F>("h_gen_bsxdist_bsydist", "; x-dist(gen vtx, beamspot) (cm); y-dist(gen vtx, beamspot)", 500, -0.5, 0.5, 500, -0.5, 0.5);

    h_hlt_bits     = fs->make<TH1F>("h_hlt_bits",     ";;events", 2*mfv::n_hlt_paths+1, 0, 2*mfv::n_hlt_paths+1);
    h_hlt_bit_grid = fs->make<TH2F>("h_hlt_bit_grid", ";;", mfv::n_hlt_paths+1, 0, mfv::n_hlt_paths+1, mfv::n_hlt_paths+1, 0, mfv::n_hlt_paths+1);
    h_l1_bits      = fs->make<TH1F>("h_l1_bits",      ";;events", 2*mfv::n_l1_paths +1, 0, 2*mfv::n_l1_paths +1);

    h_hlt_bits->GetXaxis()->SetBinLabel(1, "nevents");
    h_hlt_bit_grid->GetXaxis()->SetBinLabel(1, "nevents");
    h_hlt_bit_grid->GetYaxis()->SetBinLabel(1, "nevents");
    for (int i = 0; i < mfv::n_hlt_paths; ++i) {
        h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::hlt_paths[i]));
        h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::hlt_paths[i]));

        h_hlt_bit_grid->GetXaxis()->SetBinLabel(1+i+1, TString::Format(" pass %s", mfv::hlt_paths[i]));
        h_hlt_bit_grid->GetYaxis()->SetBinLabel(1+i+1, TString::Format(" pass %s", mfv::hlt_paths[i]));
    }
    h_l1_bits->GetXaxis()->SetBinLabel(1, "nevents");
    for (int i = 0; i < mfv::n_l1_paths; ++i) {
        h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::l1_paths[i]));
        h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::l1_paths[i]));
    }

    h_npu = fs->make<TH1F>("h_npu", ";true nPU;events", 120, 0, 120);

    h_bsx = fs->make<TH1F>("h_bsx", ";beamspot x (cm);events/10 #mum", 200, -0.1, 0.1);
    h_bsy = fs->make<TH1F>("h_bsy", ";beamspot y (cm);events/10 #mum", 200, -0.1, 0.1);
    h_bsz = fs->make<TH1F>("h_bsz", ";beamspot z (cm);events/400 #mum", 200, -4, 4);
    h_bsphi = fs->make<TH1F>("h_bsphi", ";beamspot #phi (rad);events/.063", 100, -3.1416, 3.1416);

    h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices;events", 120, 0, 120);
    h_pvx = fs->make<TH1F>("h_pvx", ";primary vertex x (cm);events/2 #mum", 200, -0.02, 0.02);
    h_pvy = fs->make<TH1F>("h_pvy", ";primary vertex y (cm);events/2 #mum", 200, -0.02, 0.02);
    h_pvxwide = fs->make<TH1F>("h_pvxwide", ";primary vertex x (cm);events/40 #mum", 50, -0.1, 0.1);
    h_pvywide = fs->make<TH1F>("h_pvywide", ";primary vertex y (cm);events/40 #mum", 50, -0.1, 0.1);
    h_pvz = fs->make<TH1F>("h_pvz", ";primary vertex z (cm);events/3.6 mm", 100, -18, 18);
    h_pvcxx = fs->make<TH1F>("h_pvcxx", ";primary vertex cxx;events", 100, 0, 5e-6);
    h_pvcyy = fs->make<TH1F>("h_pvcyy", ";primary vertex cyy;events", 100, 0, 5e-6);
    h_pvczz = fs->make<TH1F>("h_pvczz", ";primary vertex czz;events", 100, 0, 1e-5);
    h_pvcxy = fs->make<TH1F>("h_pvcxy", ";primary vertex cxy;events", 100, -1e-6, 1e-6);
    h_pvcxz = fs->make<TH1F>("h_pvcxz", ";primary vertex cxz;events", 100, -1e-6, 1e-6);
    h_pvcyz = fs->make<TH1F>("h_pvcyz", ";primary vertex cyz;events", 100, -1e-6, 1e-6);
    h_pvrho = fs->make<TH1F>("h_pvrho", ";primary vertex rho (cm);events/5 #mum", 40, 0, 0.02);
    h_pvrhowide = fs->make<TH1F>("h_pvrhowide", ";primary vertex rho (cm);events/10 #mum", 100, 0, 0.1);
    h_pvphi = fs->make<TH1F>("h_pvphi", ";primary vertex #phi (rad);events/.063", 100, -3.1416, 3.1416);
    h_pvntracks = fs->make<TH1F>("h_pvntracks", ";# of tracks in primary vertex;events/3", 100, 0, 300);
    h_pvscore = fs->make<TH1F>("h_pvscore", ";primary vertex #Sigma p_{T}^{2} (GeV^{2});events/10000 GeV^{2}", 100, 0, 1e6);
    h_pvsx = fs->make<TH1F>("h_pvsx", ";primary vertices x (cm);events/2 #mum", 200, -0.02, 0.02);
    h_pvsy = fs->make<TH1F>("h_pvsy", ";primary vertices y (cm);events/2 #mum", 200, -0.02, 0.02);
    h_pvsxwide = fs->make<TH1F>("h_pvsxwide", ";primary vertices x (cm);events/40 #mum", 50, -0.1, 0.1);
    h_pvsywide = fs->make<TH1F>("h_pvsywide", ";primary vertices y (cm);events/40 #mum", 50, -0.1, 0.1);
    h_pvsz = fs->make<TH1F>("h_pvsz", ";primary vertices z (cm);events/3.6 mm", 100, -18, 18);
    h_pvsrho = fs->make<TH1F>("h_pvsrho", ";primary vertices rho (cm);events/5 #mum", 40, 0, 0.02);
    h_pvsrhowide = fs->make<TH1F>("h_pvsrhowide", ";primary vertices rho (cm);events/10 #mum", 100, 0, 0.1);
    h_pvsphi = fs->make<TH1F>("h_pvsphi", ";primary vertices #phi (rad);events/.063", 100, -3.1416, 3.1416);
    h_pvsscore = fs->make<TH1F>("h_pvsscore", ";primary vertices #Sigma p_{T}^{2} (GeV^{2});events/10000 GeV^{2}", 100, 0, 1e6);
    h_pvsdz = fs->make<TH1F>("h_pvsdz", ";primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
    h_pvsmindz = fs->make<TH1F>("h_pvsmindz", ";min primary vertices pairs #delta z (cm);events/0.5 mm", 100, 0, 5);
    h_pvsmaxdz = fs->make<TH1F>("h_pvmaxdz", ";max primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
    h_pvsmindz_minscore = fs->make<TH1F>("h_pvmindz_minscore", ";min primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);
    h_pvsmaxdz_minscore = fs->make<TH1F>("h_pvmaxdz_minscore", ";max primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);
    h_pvbs_dist = fs->make<TH1F>("h_pvbs_dist", ";dist between PV and BS (cm);entries", 100, 0.00, 0.05);

    h_njets = fs->make<TH1F>("h_njets", ";# of jets;events", 30, 0, 30);
    h_njets20 = fs->make<TH1F>("h_njets20", ";# of jets w. p_{T} > 20 GeV;events", 20, 0, 20);
    h_ncalojets   = fs->make<TH1F>("h_ncalojets", ";# of calojets;events", 30, 0, 30);
    h_ncalojets40 = fs->make<TH1F>("h_ncalojets40", ";# of calojets with p_{T} > 40 GeV;entries", 30, 0, 30);
    h_nhltcalojets = fs->make<TH1F>("h_nhltcalojets", ";# of HLT calojets;entries", 30, 0, 30);
    h_nhltcalojets40 = fs->make<TH1F>("h_nhltcalojets40", ";# of HLT calojets with p_{T} > 40 GeV;entries", 30, 0, 30);
    h_nhltbjets = fs->make<TH1F>("h_nhltbjets", ";# of HLT bjets;entries", 20, 0, 20);
    h_nhltcalobjets = fs->make<TH1F>("h_nhltcalobjets", ";# of HLT CALO bjets;entries", 20, 0, 20);
    h_nhltcalobjets_low = fs->make<TH1F>("h_nhltcalobjets_low", ";# of low-score HLT CALO bjets;entries", 20, 0, 20);
    for (int i = 0; i < MAX_NJETS+1; ++i) {
        TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
        h_jet_pt[i] = fs->make<TH1F>(TString::Format("h_jet_pt_%s", ijet.Data()), TString::Format(";p_{T} of jet #%s (GeV);events/10 GeV", ijet.Data()), 200, 0, 2000);
        h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", ijet.Data()), TString::Format(";#eta of jet #%s (GeV);events/0.05", ijet.Data()), 120, -3, 3);
        h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", ijet.Data()), TString::Format(";#phi of jet #%s (GeV);events/0.063", ijet.Data()), 100, -3.1416, 3.1416);
        h_jet_nseedtrack[i] = fs->make<TH1F>(TString::Format("h_jet_nseedtrack_%s", ijet.Data()), TString::Format(";jet #%s number of seed tracks;arb. units", ijet.Data()), 50, 0, 50);
        h_calojet_pt[i] = fs->make<TH1F>(TString::Format("h_calojet_pt_%s", ijet.Data()), TString::Format(";p_{T} of calojet #%s (GeV);events/10 GeV", ijet.Data()), 200, 0, 2000);
        h_calojet_eta[i] = fs->make<TH1F>(TString::Format("h_calojet_eta_%s", ijet.Data()), TString::Format(";#eta of calojet #%s (GeV);events/0.05", ijet.Data()), 120, 0, 6);
        h_calojet_phi[i] = fs->make<TH1F>(TString::Format("h_calojet_phi_%s", ijet.Data()), TString::Format(";#phi of calojet #%s (GeV);events/0.063", ijet.Data()), 100, -3.1416, 3.1416);
    }
    h_calojet_i_pt = fs->make<TH2F>("h_calojet_i_pt", ";calojet index;calojet pT (GeV)", 30, 0, 30, 200, 0, 1000);
    h_calojet_ht_30 = fs->make<TH1F>("h_calojet_ht_30", ";H_{T} of calojets with p_{T} > 30 GeV (GeV);entries", 150, 0, 1500);
    h_calojet_ht_40 = fs->make<TH1F>("h_calojet_ht_40", ";H_{T} of calojets with p_{T} > 40 GeV (GeV);entries", 150, 0, 1500);
    h_calojet_diagnostics_lo = fs->make<TH1F>("h_calojet_diagnostics_lo", ";calojet diagnostic code (low-HT);entries", 4,  -0.5, 3.5);
    h_calojet_diagnostics_hi = fs->make<TH1F>("h_calojet_diagnostics_hi", ";calojet diagnostic code (high-HT);entries", 4, -0.5, 3.5);

    h_jet_energy = fs->make<TH1F>("h_jet_energy", ";jets energy (GeV);jets/10 GeV", 200, 0, 2000);
    h_jet_ht = fs->make<TH1F>("h_jet_ht", ";H_{T} of jets with p_{T} > 30 GeV (GeV);entries", 150, 0, 1500);
    h_jet_ht_40 = fs->make<TH1F>("h_jet_ht_40", ";H_{T} of jets with p_{T} > 40 GeV;entries", 150, 0, 1500);
    h_jet_calojet_ht = fs->make<TH2F>("h_jet_calojet_ht", ";H_{T} of PFJets with p_{T} > 30GeV;H_{T} of CaloJets with p_{T} > 30GeV", 150, 0, 1500, 150, 0, 1500);
    h_jet_calojet_ht_40 = fs->make<TH2F>("h_jet_calojet_ht_40", ";H_{T} of PFJets with p_{T} > 40GeV;H_{T} of CaloJets with p_{T} > 40GeV", 150, 0, 1500, 150, 0, 1500);
    h_jet_diagnostics_lo = fs->make<TH1F>("h_jet_diagnostics_lo", ";jet diagnostic code (low-HT);entries",  4, -0.5, 3.5);
    h_jet_diagnostics_hi = fs->make<TH1F>("h_jet_diagnostics_hi", ";jet diagnostic code (high-HT);entries" ,4, -0.5, 3.5);

    h_jet_pairdphi = fs->make<TH1F>("h_jet_pairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);
    h_jet_pairdr = fs->make<TH1F>("h_jet_pairdr", ";jet pair #DeltaR (rad);jet pairs/.063", 100, 0, 6.3);

    h_min_hltcalo_pfjet_dr = fs->make<TH1F>("h_min_hltcalo_pfjet_dr", ";#Delta R between HLT CaloJets and Offline PFJets;entries", 82, -0.2, 0.8);

    h_n_reljettks = fs->make<TH1F>("h_n_reljettks", ";# of jettks w/ |#eta| < 2 and p_{T} > 1;entries/bin", 80, 0, 80);

    h_n_vertex_seed_tracks = fs->make<TH1F>("h_n_vertex_seed_tracks", ";# vertex seed tracks;events", 100, 0, 100);
    h_vertex_seed_track_chi2dof = fs->make<TH1F>("h_vertex_seed_track_chi2dof", ";vertex seed track #chi^{2}/dof;tracks/1", 10, 0, 10);
    h_vertex_seed_track_q = fs->make<TH1F>("h_vertex_seed_track_q", ";vertex seed track charge;tracks", 3, -1, 2);
    h_vertex_seed_track_pt = fs->make<TH1F>("h_vertex_seed_track_pt", ";vertex seed track p_{T} (GeV);tracks/GeV", 300, 0, 300);
    h_vertex_seed_track_pt_barrel = fs->make<TH1F>("h_vertex_seed_track_pt_barrel", ";vertex seed track p_{T} (GeV) barrel;tracks/GeV", 300, 0, 300);
    h_vertex_seed_track_pt_endcap = fs->make<TH1F>("h_vertex_seed_track_pt_endcap", ";vertex seed track p_{T} (GeV) endcap;tracks/GeV", 300, 0, 300);
    h_vertex_seed_track_p = fs->make<TH1F>("h_vertex_seed_track_p", ";vertex seed track p (GeV);tracks/GeV", 300, 0, 300);
    h_vertex_seed_track_eta = fs->make<TH1F>("h_vertex_seed_track_eta", ";vertex seed track #eta;tracks/0.052", 100, -2.6, 2.6);
    h_vertex_seed_track_phi = fs->make<TH1F>("h_vertex_seed_track_phi", ";vertex seed track #phi;tracks/0.063", 100, -3.15, 3.15);
    h_vertex_seed_track_phi_v_eta = fs->make<TH2F>("h_vertex_seed_track_phi_v_eta", ";vertex seed track #eta;vertex seed track #phi", 26, -2.6, 2.6, 24, -M_PI, M_PI);
    h_vertex_seed_track_dxy = fs->make<TH1F>("h_vertex_seed_track_dxy", ";vertex seed track dxy (cm);tracks/10 #mum", 200, -0.1, 0.1);
    h_vertex_seed_track_dz = fs->make<TH1F>("h_vertex_seed_track_dz", ";vertex seed track dz (cm);tracks/10 #mum", 200, -0.1, 0.1);
    h_vertex_seed_track_err_pt = fs->make<TH1F>("h_vertex_seed_track_err_pt", ";vertex seed track #sigma(p_{T})/p_{T} (GeV);tracks/0.005", 100, 0, 0.5);
    h_vertex_seed_track_err_eta = fs->make<TH1F>("h_vertex_seed_track_err_eta", ";vertex seed track #sigma(#eta);tracks/5e-5", 100, 0, 0.005);
    h_vertex_seed_track_err_phi = fs->make<TH1F>("h_vertex_seed_track_err_phi", ";vertex seed track #sigma(#phi);tracks/5e-5", 100, 0, 0.005);
    h_vertex_seed_track_err_dxy = fs->make<TH1F>("h_vertex_seed_track_err_dxy", ";vertex seed track #sigma(dxy) (cm);tracks/3 #mum", 100, 0, 0.03);
    h_vertex_seed_track_err_dz = fs->make<TH1F>("h_vertex_seed_track_err_dz", ";vertex seed track #sigma(dz) (cm);tracks/15 #mum", 100, 0, 0.15);
    h_vertex_seed_track_npxhits = fs->make<TH1F>("h_vertex_seed_track_npxhits", ";vertex seed track # pixel hits;tracks", 10, 0, 10);
    h_vertex_seed_track_nsthits = fs->make<TH1F>("h_vertex_seed_track_nsthits", ";vertex seed track # strip hits;tracks", 50, 0, 50);
    h_vertex_seed_track_nhits = fs->make<TH1F>("h_vertex_seed_track_nhits", ";vertex seed track # hits;tracks", 60, 0, 60);
    h_vertex_seed_track_npxlayers = fs->make<TH1F>("h_vertex_seed_track_npxlayers", ";vertex seed track # pixel layers;tracks", 10, 0, 10);
    h_vertex_seed_track_nstlayers = fs->make<TH1F>("h_vertex_seed_track_nstlayers", ";vertex seed track # strip layers;tracks", 20, 0, 20);
    h_vertex_seed_track_nlayers = fs->make<TH1F>("h_vertex_seed_track_nlayers", ";vertex seed track # layers;tracks", 30, 0, 30);

    h_met = fs->make<TH1F>("h_met", ";MET (GeV);events/5 GeV", 500, 0, 2500);
    h_metphi = fs->make<TH1F>("h_metphi", ";MET #phi (rad);events/.063", 100, -3.1416, 3.1416);
    h_metnomu = fs->make<TH1F>("h_metnomu", ";METNoMu (GeV);events/5 GeV", 500, 0, 2500);
    h_metnomuphi = fs->make<TH1F>("h_metnomuphi", ";METNoMu #phi (rad);events/.063", 100, -3.1416, 3.1416);

    const char* lmt_ex[3] = {"loose", "medium", "tight"};
    const char* lep_kind[2] = {"muon", "electron"};
    for (int i = 0; i < 3; ++i) {
        h_nbtags[i] = fs->make<TH1F>(TString::Format("h_nbtags_%i", i), TString::Format(";# of %s b tags;events", lmt_ex[i]), 10, 0, 10);
        h_nbtags_v_bquark_code[i] = fs->make<TH2F>(TString::Format("h_nbtags_v_bquark_code_%i", i), TString::Format(";bquark code;# of %s b tags", lmt_ex[i]), 3, 0, 3, 3, 0, 3);
    }
    h_jet_bdisc_csv = fs->make<TH1F>("h_jet_bdisc_csv", ";jets' csv score;jets/0.02", 51, 0, 1.02);
    h_jet_bdisc_deepcsv = fs->make<TH1F>("h_jet_bdisc_deepcsv", ";jets' deepcsv score;jets/0.02", 51, 0, 1.02);
    h_jet_bdisc_deepflav = fs->make<TH1F>("h_jet_bdisc_deepflav", ";jets' deepflavour score;jets/0.02", 51, 0, 1.02);
    h_jet_bdisc_deepflav_v_bquark_code = fs->make<TH2F>("h_jet_bdisc_deepflav_v_bquark_code", ";b quark code;jets' b discriminator", 3, 0, 3, 51, 0, 1.02);
    h_bjet_pt = fs->make<TH1F>("h_bjet_pt", ";bjets p_{T} (GeV);bjets/10 GeV", 150, 0, 1500);
    h_bjet_eta = fs->make<TH1F>("h_bjet_eta", ";bjets #eta (rad);bjets/.05", 120, -3, 3);
    h_bjet_phi = fs->make<TH1F>("h_bjet_phi", ";bjets #phi (rad);bjets/.063", 100, -3.1416, 3.1416);
    h_bjet_energy = fs->make<TH1F>("h_bjet_energy", ";bjets E (GeV);bjets/10 GeV", 150, 0, 1500);
    h_bjet_pairdphi = fs->make<TH1F>("h_bjet_pairdphi", ";bjet pair #Delta#phi (rad);bjet pairs/.063", 100, -3.1416, 3.1416);

    h_thresh_csvtags = fs->make<TH1F>("h_thresh_csvtags", ";# of loose CSV btags; entries", 15, 0, 15);
    h_thresh_hardcsvtags = fs->make<TH1F>("h_thresh_hardcsvtags", ";# of loose CSV btags w/ p_{T} > 80GeV; entries", 15, 0, 15);

    const char* lep_ex[2] = {"any", "selected"};
    for (int i = 0; i < 2; ++i) {
        h_nmuons[i] = fs->make<TH1F>(TString::Format("h_nmuons_%s", lep_ex[i]), TString::Format(";# of %s muons;events", lep_ex[i]), 5, 0, 5);
        h_nelectrons[i] = fs->make<TH1F>(TString::Format("h_nelectrons_%s", lep_ex[i]), TString::Format(";# of %s electrons;events", lep_ex[i]), 5, 0, 5);
        h_nleptons[i] = fs->make<TH1F>(TString::Format("h_nleptons_%s", lep_ex[i]), TString::Format(";# of %s leptons;events", lep_ex[i]), 5, 0, 5);
        for (int j = 0; j < 2; ++j) {
            h_leptons_pt   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_pt",    lep_kind[j], lep_ex[i]), TString::Format(";%s %s p_{T} (GeV);%ss/5 GeV",     lep_ex[i], lep_kind[j], lep_kind[j]), 40, 0, 200);
            h_leptons_eta  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_eta",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #eta (rad);%ss/.104",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -2.6, 2.6);
            h_leptons_phi  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_phi",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #phi (rad);%ss/.126",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -3.1416, 3.1416);
            h_leptons_dxy  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxy",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(PV) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
            h_leptons_dxybs[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxybs", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(BS) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
            h_leptons_dz   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dz",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dz (cm);%ss/50 #mum",       lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
            h_leptons_iso  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
        }
    }
}

void MFVEventHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);

    edm::Handle<double> weight;
    event.getByToken(weight_token, weight);
    const double w = *weight;
    h_w->Fill(w);
    h_eventid->Fill(event.id().event());

    int ncalojets    = mevent->calo_jet_pt.size();
    int raw_nhltcalojets = mevent->hlt_calo_jet_pt.size(); // Has a much wider eta range than what we'll ultimately want

    //////////////////////////////////////////////////////////////////////////////

    // (Temporarily?) moving this earlier in the code for **reasons**
    int nhltcalojets   = 0;
    int nhltcalojets40 = 0;
    float hltcalojet_ht_40 = 0.0;
    for (int i=0; i < raw_nhltcalojets; ++i) {
        if (fabs(mevent->hlt_calo_jet_eta[i]) > 2.5) continue;
        float min_hltcalo_pfjet_dr = 8.0;
        nhltcalojets++;

        if (mevent->hlt_calo_jet_pt[i] > 40.0) {
            nhltcalojets40++;
            hltcalojet_ht_40 += mevent->hlt_calo_jet_pt[i];
        }
        for (int j=0; j < (int)(mevent->jet_pt.size()); j++) {
            float temp_dR = reco::deltaR(mevent->jet_eta[j], mevent->jet_phi[j], mevent->hlt_calo_jet_eta[i], mevent->hlt_calo_jet_phi[i]);
            if (temp_dR < min_hltcalo_pfjet_dr) { min_hltcalo_pfjet_dr = temp_dR; }
        }
        h_min_hltcalo_pfjet_dr->Fill( (min_hltcalo_pfjet_dr < 0.8 ? min_hltcalo_pfjet_dr : -0.19), w);
    }


    float temp_calojet_ht = 0.0; // ugh...
    for (int i=0; i < ncalojets; ++i) {
        if (fabs(mevent->calo_jet_eta[i]) > 2.5) continue;
        if (mevent->calo_jet_pt[i] > 40.0) { temp_calojet_ht += mevent->calo_jet_pt[i]; }
    }
    if (not (temp_calojet_ht > temp_caloht_cut)) return;

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

        //if ((not has_nice_muon) or (not has_nice_ele)) return;
        if ((not has_nice_muon) or (not has_nice_ele) or (mevent->nbtags(1) < 2)) return;
    }


//    bool passes_dilepton = false;
//    std::vector<int> dilepton_trigs = {mfv::b_HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL,
//                                       mfv::b_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL,
//                                       mfv::b_HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ,
//                                       mfv::b_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ};
//    for (auto trig : dilepton_trigs) {
//        if (mevent->pass_hlt(trig)) {
//            passes_dilepton = true;
//            break;
//        }
//    }
//    if (not passes_dilepton) return;

    h_gen_decay->Fill(mevent->gen_decay_type[0], mevent->gen_decay_type[1], w);
    h_gen_flavor_code->Fill(mevent->gen_flavor_code, w);

    const size_t nbquarks = mevent->gen_bquarks.size();
    h_nbquarks->Fill(nbquarks, w);
    for (size_t i = 0; i < nbquarks; ++i) {
        h_bquark_pt->Fill(mevent->gen_bquarks[i].Pt(), w);
        h_bquark_eta->Fill(mevent->gen_bquarks[i].Eta(), w);
        h_bquark_phi->Fill(mevent->gen_bquarks[i].Phi(), w);
        h_bquark_energy->Fill(mevent->gen_bquarks[i].E(), w);
        for (size_t j = i+1; j < nbquarks; ++j)
            h_bquark_pairdphi->Fill(reco::deltaPhi(mevent->gen_bquarks[i].Phi(), mevent->gen_bquarks[j].Phi()), w);
    }

    for (int igenv = 0; igenv < 2; ++igenv) {
        double genx = mevent->gen_lsp_decay[igenv*3+0];
        double geny = mevent->gen_lsp_decay[igenv*3+1];
        double genz = mevent->gen_lsp_decay[igenv*3+2];
        double genbs2ddist = mevent->mag(genx - mevent->bsx_at_z(genz),
                geny - mevent->bsy_at_z(genz) 
                );
        h_gen_bs2ddist->Fill(genbs2ddist, w);
        h_gen_bsxdist_bsydist->Fill(genx - mevent->bsx_at_z(genz), geny - mevent->bsy_at_z(genz), w);
    }

    h_minlspdist2d->Fill(mevent->minlspdist2d(), w);
    h_lspdist2d->Fill(mevent->lspdist2d(), w);
    h_lspdist3d->Fill(mevent->lspdist3d(), w);

    //////////////////////////////////////////////////////////////////////////////

    h_hlt_bits->Fill(0., w);
    h_hlt_bit_grid->Fill(0., 0., w);
    h_l1_bits->Fill(0., w);
    for (int i = 0; i < mfv::n_hlt_paths; ++i) {
        //std::cout << mfv::hlt_paths[i] << "  Found: " << mevent->found_hlt(i) << "  Pass: " << mevent->pass_hlt(i) << std::endl;
        if (mevent->found_hlt(i)) h_hlt_bits->Fill(1+2*i,   w);
        if (mevent->pass_hlt (i)) {
            h_hlt_bits->Fill(1+2*i+1, w);
            for (int j = 0; j < mfv::n_hlt_paths; ++j) {
                if (mevent->pass_hlt (j)) h_hlt_bit_grid->Fill(i+1, j+1, w);
            }
        }
    }
    for (int i = 0; i < mfv::n_l1_paths; ++i) {
        if (mevent->found_l1(i)) h_l1_bits->Fill(1+2*i,   w);
        if (mevent->pass_l1 (i)) h_l1_bits->Fill(1+2*i+1, w);
    }

    //////////////////////////////////////////////////////////////////////////////
    
    h_npu->Fill(mevent->npu, w);

    h_bsx->Fill(mevent->bsx, w);
    h_bsy->Fill(mevent->bsy, w);
    h_bsz->Fill(mevent->bsz, w);
    h_bsphi->Fill(atan2(mevent->bsy, mevent->bsx), w);

    h_npv->Fill(mevent->npv, w);
    for (auto h : { h_pvx, h_pvxwide }) h->Fill(mevent->pvx - mevent->bsx_at_z(mevent->pvz), w);
    for (auto h : { h_pvy, h_pvywide }) h->Fill(mevent->pvy - mevent->bsy_at_z(mevent->pvz), w);
    h_pvz->Fill(mevent->pvz - mevent->bsz, w);
    h_pvcxx->Fill(mevent->pvcxx, w);
    h_pvcxy->Fill(mevent->pvcxy, w);
    h_pvcxz->Fill(mevent->pvcxz, w);
    h_pvcyy->Fill(mevent->pvcyy, w);
    h_pvcyz->Fill(mevent->pvcyz, w);
    h_pvczz->Fill(mevent->pvczz, w);
    h_pvphi->Fill(atan2(mevent->pvy - mevent->bsy_at_z(mevent->pvz), mevent->pvx - mevent->bsx_at_z(mevent->pvz)), w);
    h_pvntracks->Fill(mevent->pv_ntracks, w);
    h_pvscore->Fill(mevent->pv_score, w);
    h_pvrho->Fill(mevent->pv_rho(), w);
    for (auto h : { h_pvrho, h_pvrhowide }) h->Fill(mevent->pv_rho(), w);
    for (size_t i = 0; i < mevent->npv; ++i) {
        const float z = mevent->pv_z(i);
        const float x = mevent->pv_x(i) - mevent->bsx_at_z(z);
        const float y = mevent->pv_y(i) - mevent->bsy_at_z(z);
        for (auto h : { h_pvsx, h_pvsxwide }) h->Fill(x, w);
        for (auto h : { h_pvsy, h_pvsywide }) h->Fill(y, w);
        h_pvsz->Fill(z, w);
        for (auto h : { h_pvsrho, h_pvsrhowide }) h->Fill(hypot(x,y), w);
        h_pvsphi->Fill(atan2(y,x), w);
        h_pvsscore->Fill(mevent->pv_score_(i), w);

        jmt::MinValue mindz, mindz_minscore;
        jmt::MaxValue maxdz, maxdz_minscore;
        for (size_t j = i+1; j < mevent->npv; ++j) {
            const float z2 = mevent->pv_z(j);
            //const float x2 = mevent->pv_x(j) - mevent->bsx_at_z(z);
            //const float y2 = mevent->pv_y(j) - mevent->bsy_at_z(z);
            const float dz = fabs(z-z2);
            h_pvsdz->Fill(dz, w);
            mindz(dz), maxdz(dz);
            if (mevent->pv_score_(i) > 50e3 && mevent->pv_score_(j) > 50e3)
                mindz_minscore(dz), maxdz_minscore(dz);
        }
        h_pvsmindz->Fill(mindz, w);
        h_pvsmaxdz->Fill(maxdz, w);
        h_pvsmindz_minscore->Fill(mindz_minscore, w);
        h_pvsmaxdz_minscore->Fill(maxdz_minscore, w);
    }

    h_pvbs_dist->Fill(std::hypot(mevent->pvx - mevent->bsx_at_z(mevent->pvz), mevent->pvy - mevent->bsy_at_z(mevent->pvz)));

    h_njets->Fill(mevent->njets(), w);
    h_njets20->Fill(mevent->njets(20), w);

    int n_good_lo_pfjets = 0;
    int n_good_hi_pfjets = 0;
    for (int i = 0; i < MAX_NJETS; ++i) {
        h_jet_pt[i]->Fill(mevent->nth_jet_pt(i), w);
        h_jet_eta[i]->Fill(mevent->nth_jet_eta(i), w);
        h_jet_phi[i]->Fill(mevent->nth_jet_phi(i), w);
        
        if (fabs(mevent->nth_jet_eta(i)) < 2.0 and mevent->nth_jet_pt(i) > 52.0) {
            n_good_lo_pfjets++;
            if (mevent->nth_jet_pt(i) > 72.0) {
                n_good_hi_pfjets++;
            }
        }
    }

    float calojet_ht_30 = 0.0;
    float calojet_ht_40 = 0.0;
    int   ncalojets40 = 0;
    int   n_good_lo_calojets = 0;
    int   n_good_hi_calojets = 0;
    for (int i=0; i < ncalojets; ++i) {
        if (fabs(mevent->calo_jet_eta[i]) > 2.5) continue;
        if (mevent->calo_jet_pt[i] > 40.0) {
            ncalojets40++;
            calojet_ht_40 += mevent->calo_jet_pt[i];
        }
        if (mevent->calo_jet_pt[i] > 30.0) {
            calojet_ht_30 += mevent->calo_jet_pt[i];
        }


        if (fabs(mevent->calo_jet_eta[i]) < 2.0 and mevent->calo_jet_pt[i] > 40.0) {
            n_good_lo_calojets++;
            if (mevent->calo_jet_pt[i] > 60.0) {
                n_good_hi_calojets++;
            }
        }

        h_calojet_pt[MAX_NJETS]->Fill(mevent->calo_jet_pt[i], w);
        h_calojet_eta[MAX_NJETS]->Fill(fabs(mevent->calo_jet_eta[i]), w);
        h_calojet_phi[MAX_NJETS]->Fill(mevent->calo_jet_phi[i],  w);

        if (i >= MAX_NJETS) continue;
        h_calojet_pt[i]->Fill(mevent->calo_jet_pt[i],         w);
        h_calojet_eta[i]->Fill(fabs(mevent->calo_jet_eta[i]), w);
        h_calojet_phi[i]->Fill(mevent->calo_jet_phi[i],       w);
        h_calojet_i_pt->Fill(i, mevent->calo_jet_pt[i],       w);
    }

    h_ncalojets->Fill(ncalojets, w);
    h_ncalojets40->Fill(ncalojets40, w);

    h_nhltcalojets->Fill(nhltcalojets, w);
    h_nhltcalojets40->Fill(nhltcalojets40, w);

    h_nhltbjets->Fill(mevent->hlt_pfforbtag_jet_pt.size(), w);
    h_nhltcalobjets->Fill(mevent->hlt_calo_b_jet_pt.size(), w);
    h_nhltcalobjets_low->Fill(mevent->hlt_low_calo_b_jet_pt.size(), w);

    int calojet_diag_code_lo = (1 * (calojet_ht_30 > 430)) + (2 * (n_good_lo_calojets >= 2));
    int calojet_diag_code_hi = (1 * (calojet_ht_30 > 650)) + (2 * (n_good_hi_calojets >= 2));

    int jet_diag_code_lo     = (1 * (mevent->jet_ht(30) > 560)) + (2 * (n_good_lo_pfjets >= 2));
    int jet_diag_code_hi     = (1 * (mevent->jet_ht(30) > 770)) + (2 * (n_good_hi_pfjets >= 2));

    h_calojet_ht_30->Fill(fabs(calojet_ht_30), w);
    h_calojet_ht_40->Fill(fabs(calojet_ht_40), w);
    h_jet_ht->Fill(mevent->jet_ht(30), w);
    h_jet_ht_40->Fill(mevent->jet_ht(40), w);

    h_jet_calojet_ht->Fill(mevent->jet_ht(30), fabs(calojet_ht_30), w);
    h_jet_calojet_ht_40->Fill(mevent->jet_ht(40), fabs(calojet_ht_40), w);

    h_calojet_diagnostics_lo->Fill(calojet_diag_code_lo, w);
    h_calojet_diagnostics_hi->Fill(calojet_diag_code_hi, w);
    h_jet_diagnostics_lo->Fill(jet_diag_code_lo, w);
    h_jet_diagnostics_hi->Fill(jet_diag_code_hi, w);

    for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
        if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
            continue;
        h_jet_pt[MAX_NJETS]->Fill(mevent->jet_pt[ijet], w);
        h_jet_eta[MAX_NJETS]->Fill(fabs(mevent->jet_eta[ijet]), w);
        h_jet_phi[MAX_NJETS]->Fill(mevent->jet_phi[ijet], w);
        h_jet_energy->Fill(mevent->jet_energy[ijet], w);
        for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
            if (mevent->jet_pt[jjet] < mfv::min_jet_pt)
                continue;
            h_jet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]), w);
            h_jet_pairdr->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->jet_eta[jjet], mevent->jet_phi[jjet]), w);
        }

    }

    for (int i = 0; i < 2; ++i) {
        h_nmuons[i]->Fill(mevent->nmu(i), w);
        h_nelectrons[i]->Fill(mevent->nel(i), w);
        h_nleptons[i]->Fill(mevent->nlep(i), w);
    }

    for (size_t ilep = 0; ilep < mevent->nlep(); ++ilep) {
        const size_t j = mevent->is_electron(ilep);
        for (size_t i = 0; i < 2; ++i)
            if (i == 0 || mevent->pass_lep_sel(ilep)) {
                h_leptons_pt[j][i]->Fill(mevent->lep_pt(ilep), w);
                h_leptons_eta[j][i]->Fill(mevent->lep_eta[ilep], w);
                h_leptons_phi[j][i]->Fill(mevent->lep_phi[ilep], w);
                h_leptons_dxy[j][i]->Fill(mevent->lep_dxy[ilep], w);
                h_leptons_dxybs[j][i]->Fill(mevent->lep_dxybs[ilep], w);
                h_leptons_dz[j][i]->Fill(mevent->lep_dz[ilep], w);
                h_leptons_iso[j][i]->Fill(mevent->lep_iso[ilep], w);
            }
    }

    h_met->Fill(mevent->met(), w);
    h_metphi->Fill(mevent->metphi(), w);
    h_metnomu->Fill(mevent->metNoMu(), w);
    h_metnomuphi->Fill(mevent->metNoMuphi(), w);

    for (int i = 0; i < 3; ++i) {
        h_nbtags[i]->Fill(mevent->nbtags(i), w);
        h_nbtags_v_bquark_code[i]->Fill(mevent->gen_flavor_code, mevent->nbtags(i), w);
    }
    const int ibtag = 2; // tight only
    int thresh_csvtags = 0;
    int thresh_hardcsvtags = 0;
    for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
        if (mevent->jet_pt[ijet] < mfv::min_jet_pt) continue;
        h_jet_bdisc_csv->Fill(mevent->jet_bdisc_csv[ijet], w);
        h_jet_bdisc_deepcsv->Fill(mevent->jet_bdisc_deepcsv[ijet], w);
        h_jet_bdisc_deepflav->Fill(mevent->jet_bdisc_deepflav[ijet], w);
        h_jet_bdisc_deepflav_v_bquark_code->Fill(mevent->gen_flavor_code, mevent->jet_bdisc_deepflav[ijet], w);

        if (mevent->jet_bdisc_csv[ijet] > jmt::BTagging::discriminator_min(0, 0)) {
            thresh_csvtags++;
            if (mevent->jet_pt[ijet] > 80.0) thresh_hardcsvtags++;
        }

        if (mevent->is_btagged(ijet, ibtag)) {
            h_bjet_pt->Fill(mevent->jet_pt[ijet], w);
            h_bjet_eta->Fill(mevent->jet_eta[ijet], w);
            h_bjet_phi->Fill(mevent->jet_phi[ijet], w);
            h_bjet_energy->Fill(mevent->jet_energy[ijet], w);
            for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
                if (mevent->jet_pt[jjet] < mfv::min_jet_pt)
                    continue;
                if (mevent->is_btagged(jjet, ibtag)) {
                    h_bjet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]), w);
                }
            }
        }
    }

    h_thresh_csvtags->Fill(thresh_csvtags, w);
    h_thresh_hardcsvtags->Fill(thresh_hardcsvtags, w);


    //////////////////////////////////////////////////////////////////////////////
    
    // Count number of relevant jettks in event
    int nreljettks = 0;
    for (size_t itk = 0; itk < mevent->n_jet_tracks_all(); ++itk) {
        if (fabs(mevent->jet_track_qpt[itk]) > 1.0 and fabs(mevent->jet_track_eta[itk]) < 2.0) nreljettks++;
    }

    h_n_reljettks->Fill(nreljettks, w);

    const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();
    std::vector<int> track_which_jet;
    h_n_vertex_seed_tracks->Fill(n_vertex_seed_tracks, w);
    for (size_t i = 0; i < n_vertex_seed_tracks; ++i) {
        h_vertex_seed_track_chi2dof->Fill(mevent->vertex_seed_track_chi2dof[i], w);
        h_vertex_seed_track_q->Fill(mevent->vertex_seed_track_q(i), w);
        h_vertex_seed_track_pt->Fill(mevent->vertex_seed_track_pt(i), w);
        if (abs(mevent->vertex_seed_track_eta[i])<1.4){
            h_vertex_seed_track_pt_barrel->Fill(mevent->vertex_seed_track_pt(i), w);
        }
        else{
            h_vertex_seed_track_pt_endcap->Fill(mevent->vertex_seed_track_pt(i), w);
        }
        TVector3 v;
        v.SetPtEtaPhi(mevent->vertex_seed_track_pt(i),mevent->vertex_seed_track_eta[i],mevent->vertex_seed_track_phi[i]);
        h_vertex_seed_track_p->Fill(v.Mag(), w);

        h_vertex_seed_track_eta->Fill(mevent->vertex_seed_track_eta[i], w);
        h_vertex_seed_track_phi->Fill(mevent->vertex_seed_track_phi[i], w);
        h_vertex_seed_track_phi_v_eta->Fill(mevent->vertex_seed_track_eta[i], mevent->vertex_seed_track_phi[i], w);
        h_vertex_seed_track_dxy->Fill(mevent->vertex_seed_track_dxy[i], w);
        h_vertex_seed_track_dz->Fill(mevent->vertex_seed_track_dz[i], w);
        h_vertex_seed_track_err_pt->Fill(mevent->vertex_seed_track_err_pt[i] / mevent->vertex_seed_track_pt(i), w);
        h_vertex_seed_track_err_eta->Fill(mevent->vertex_seed_track_err_eta[i], w);
        h_vertex_seed_track_err_phi->Fill(mevent->vertex_seed_track_err_phi[i], w);
        h_vertex_seed_track_err_dxy->Fill(mevent->vertex_seed_track_err_dxy[i], w);
        h_vertex_seed_track_err_dz->Fill(mevent->vertex_seed_track_err_dz[i], w);
        h_vertex_seed_track_npxhits->Fill(mevent->vertex_seed_track_npxhits(i), w);
        h_vertex_seed_track_nsthits->Fill(mevent->vertex_seed_track_nsthits(i), w);
        h_vertex_seed_track_nhits->Fill(mevent->vertex_seed_track_nhits(i), w);
        h_vertex_seed_track_npxlayers->Fill(mevent->vertex_seed_track_npxlayers(i), w);
        h_vertex_seed_track_nstlayers->Fill(mevent->vertex_seed_track_nstlayers(i), w);
        h_vertex_seed_track_nlayers->Fill(mevent->vertex_seed_track_nlayers(i), w);

        double match_threshold = 1.3;
        int jet_index = 255;
        for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
            double a = fabs(mevent->vertex_seed_track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
            double b = fabs(mevent->vertex_seed_track_eta[i] - mevent->jet_track_eta[j]) + 1;
            double c = fabs(mevent->vertex_seed_track_phi[i] - mevent->jet_track_phi[j]) + 1;
            if (a * b * c < match_threshold) {
                match_threshold = a * b * c;
                jet_index = mevent->jet_track_which_jet[j];
            }
        }
        if (jet_index != 255) {
            track_which_jet.push_back((int) jet_index);
        }
    }
    int njet_seedtrack = 0;
    for (size_t i = 0; i<mevent->jet_id.size(); ++i){
        int n_seedtrack = std::count(track_which_jet.begin(), track_which_jet.end(), i);
        njet_seedtrack += n_seedtrack;
        if (i<MAX_NJETS)
            h_jet_nseedtrack[i]->Fill(n_seedtrack, w);
    }
    h_jet_nseedtrack[MAX_NJETS]->Fill(njet_seedtrack, w);
}

DEFINE_FWK_MODULE(MFVEventHistos);
