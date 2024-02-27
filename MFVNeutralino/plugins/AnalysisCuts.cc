#include <random>
#include <stdio.h>
#include <math.h>
#include "DataFormats/Math/interface/deltaPhi.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"
#include "JMTucker/Tools/interface/UncertTools.h"

class MFVAnalysisCuts : public edm::EDFilter {
    public:
        explicit MFVAnalysisCuts(const edm::ParameterSet&);

    private:
        virtual bool filter(edm::Event&, const edm::EventSetup&);
        bool satisfiesTrigger(edm::Handle<MFVEvent>, size_t, const edm::EventSetup&);

        bool jet_hlt_match(edm::Handle<MFVEvent> mevent, int i, float min_jet_pt=20.) const {
            // an offline jet with a successful HLT match will have a nonzero jet_hlt_pt;
            // all others have the default value of 0
            return mevent->jet_hlt_pt.at(i) > min_jet_pt;
        }
        bool displaced_jet_hlt_match(edm::Handle<MFVEvent> mevent, int i, float min_jet_pt=20.) const {
            // an offline jet with a successful HLT match will have a nonzero displaced_jet_hlt_pt;
            // all others have the default value of 0
            return mevent->displaced_jet_hlt_pt.at(i) > min_jet_pt;
        }

        // Helper function to see whether a MC btag would've been rejected if it was in data

        const edm::InputTag mevent_src;
        const edm::EDGetTokenT<MFVEvent> mevent_token;
        const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

        std::mt19937 rng;
        std::uniform_real_distribution<float> distribution;

        const bool use_mevent;

        const int apply_presel;

        const bool require_bquarks;
        const bool require_trigbit;
        const bool require_gen_sumdbv;
        const bool require_bjet_psel;
        const bool study_btag_sf;
        const int  study_btag_sfvar;
        const bool dijet_agnostic;
        const bool bjet_agnostic;
        const bool bjet_veto;
        const bool study_jer;
        const bool study_jes;
        const bool jes_jer_var_up;
        const int btagger_choice;
        const int btag_wp;
        const int  trigbit_tostudy;
        const int l1_bit;
        const int trigger_bit;
        const int apply_trigger;
        const bool apply_cleaning_filters;
        const int min_npv;
        const int max_npv;
        const double min_npu;
        const double max_npu;
        const int max_pv_ntracks;
        const int min_njets;
        const int max_njets;
        const std::vector<int> min_nbtags;
        const std::vector<int> max_nbtags;
        const double min_ht;
        const double max_ht;
        const int min_nleptons;
        const int min_nselleptons;

        const bool apply_vertex_cuts;
        const int min_nvertex;
        const int max_nvertex;
        const int ntracks01_0;
        const int ntracks01_1;
        const int min_ntracks01;
        const int max_ntracks01;
        const double min_maxtrackpt01;
        const double max_maxtrackpt01;
        const int min_njetsntks01;
        const double min_tkonlymass01;
        const double min_jetsntkmass01;
        const double min_tksjetsntkmass01;
        const double min_absdeltaphi01;
        const double min_bs2ddist01;
        const double min_bs2dsig01;
        const double min_pv2ddist01;
        const double min_pv3ddist01;
        const double min_pv2dsig01;
        const double min_pv3dsig01;
        const double min_svdist2d;
        const double max_svdist2d;
        const double min_svdist3d;
        const int max_ntrackssharedwpv01;
        const int max_ntrackssharedwpvs01;
        const int max_fractrackssharedwpv01;
        const int max_fractrackssharedwpvs01;
};

MFVAnalysisCuts::MFVAnalysisCuts(const edm::ParameterSet& cfg) 
    : mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    mevent_token(consumes<MFVEvent>(mevent_src)),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    rng(259),
    distribution(0.0f, 1.0f),
    use_mevent(mevent_src.label() != ""),
    apply_presel(cfg.getParameter<int>("apply_presel")),
    require_bquarks(cfg.getParameter<bool>("require_bquarks")),
    require_trigbit(cfg.getParameter<bool>("require_trigbit")),
    require_gen_sumdbv(cfg.getParameter<bool>("require_gen_sumdbv")),
    require_bjet_psel(cfg.getParameter<bool>("require_bjet_psel")),
    study_btag_sf(cfg.getParameter<bool>("study_btag_sf")),
    study_btag_sfvar(cfg.getParameter<int>("study_btag_sfvar")),
    dijet_agnostic(cfg.getParameter<bool>("dijet_agnostic")),
    bjet_agnostic(cfg.getParameter<bool>("bjet_agnostic")),
    bjet_veto(cfg.getParameter<bool>("bjet_veto")),
    study_jer(cfg.getParameter<bool>("study_jer")),
    study_jes(cfg.getParameter<bool>("study_jes")),
    jes_jer_var_up(cfg.getParameter<bool>("jes_jer_var_up")),
    btagger_choice(cfg.getParameter<int>("btagger_choice")),
    btag_wp(cfg.getParameter<int>("btag_wp")),
    trigbit_tostudy(cfg.getParameter<int>("trigbit_tostudy")),
    l1_bit(apply_presel ? -1 : cfg.getParameter<int>("l1_bit")),
    trigger_bit(apply_presel ? -1 : cfg.getParameter<int>("trigger_bit")),
    apply_trigger(apply_presel ? 0 : cfg.getParameter<int>("apply_trigger")),
    apply_cleaning_filters(cfg.getParameter<bool>("apply_cleaning_filters")),
    min_npv(cfg.getParameter<int>("min_npv")),
    max_npv(cfg.getParameter<int>("max_npv")),
    min_npu(cfg.getParameter<double>("min_npu")),
    max_npu(cfg.getParameter<double>("max_npu")),
    max_pv_ntracks(cfg.getParameter<int>("max_pv_ntracks")),
    min_njets(cfg.getParameter<int>("min_njets")),
    max_njets(cfg.getParameter<int>("max_njets")),
    min_nbtags(cfg.getParameter<std::vector<int> >("min_nbtags")),
    max_nbtags(cfg.getParameter<std::vector<int> >("max_nbtags")),
    min_ht(cfg.getParameter<double>("min_ht")),
    max_ht(cfg.getParameter<double>("max_ht")),
    min_nleptons(cfg.getParameter<int>("min_nleptons")),
    min_nselleptons(cfg.getParameter<int>("min_nselleptons")),
    apply_vertex_cuts(cfg.getParameter<bool>("apply_vertex_cuts")),
    min_nvertex(cfg.getParameter<int>("min_nvertex")),
    max_nvertex(cfg.getParameter<int>("max_nvertex")),
    ntracks01_0(cfg.getParameter<int>("ntracks01_0")),
    ntracks01_1(cfg.getParameter<int>("ntracks01_1")),
    min_ntracks01(cfg.getParameter<int>("min_ntracks01")),
    max_ntracks01(cfg.getParameter<int>("max_ntracks01")),
    min_maxtrackpt01(cfg.getParameter<double>("min_maxtrackpt01")),
    max_maxtrackpt01(cfg.getParameter<double>("max_maxtrackpt01")),
    min_njetsntks01(cfg.getParameter<int>("min_njetsntks01")),
    min_tkonlymass01(cfg.getParameter<double>("min_tkonlymass01")),
    min_jetsntkmass01(cfg.getParameter<double>("min_jetsntkmass01")),
    min_tksjetsntkmass01(cfg.getParameter<double>("min_tksjetsntkmass01")),
    min_absdeltaphi01(cfg.getParameter<double>("min_absdeltaphi01")),
    min_bs2ddist01(cfg.getParameter<double>("min_bs2ddist01")),
    min_bs2dsig01(cfg.getParameter<double>("min_bs2dsig01")),
    min_pv2ddist01(cfg.getParameter<double>("min_pv2ddist01")),
    min_pv3ddist01(cfg.getParameter<double>("min_pv3ddist01")),
    min_pv2dsig01(cfg.getParameter<double>("min_pv2dsig01")),
    min_pv3dsig01(cfg.getParameter<double>("min_pv3dsig01")),
    min_svdist2d(cfg.getParameter<double>("min_svdist2d")),
    max_svdist2d(cfg.getParameter<double>("max_svdist2d")),
    min_svdist3d(cfg.getParameter<double>("min_svdist3d")),
    max_ntrackssharedwpv01(cfg.getParameter<int>("max_ntrackssharedwpv01")),
    max_ntrackssharedwpvs01(cfg.getParameter<int>("max_ntrackssharedwpvs01")),
    max_fractrackssharedwpv01(cfg.getParameter<double>("max_fractrackssharedwpv01")),
    max_fractrackssharedwpvs01(cfg.getParameter<double>("max_fractrackssharedwpvs01"))
{
    if (apply_cleaning_filters)
        throw cms::Exception("NotImplemented", "cleaning filters not yet implemented");
}

namespace {
    template <typename T>
        T mag(T x, T y) {
            return sqrt(x*x + y*y);
        }

    template <typename T>
        T mag(T x, T y, T z) {
            return sqrt(x*x + y*y + z*z);
        }
}

bool MFVAnalysisCuts::filter(edm::Event& event, const edm::EventSetup& setup) {
    edm::Handle<MFVEvent> mevent;

    if (use_mevent) {
        event.getByToken(mevent_token, mevent);

        if (apply_presel == 1 && (!mevent->pass_hlt(mfv::b_HLT_PFHT1050) || mevent->jet_ht(40) < 1200 || mevent->njets(20) < 4))
            return false;

        if (apply_presel == 2) {
            if (!mevent->pass_hlt(mfv::b_HLT_Ele35_WPTight_Gsf) && !mevent->pass_hlt(mfv::b_HLT_IsoMu27))
                return false;

            // JMTBAD match to lepton that triggered
            // JMTBAD real turnon value
            if (mevent->pass_hlt(mfv::b_HLT_Ele35_WPTight_Gsf) && mevent->first_lep_pass(MFVEvent::lep_el).Pt() < 35)
                return false;

            if (mevent->pass_hlt(mfv::b_HLT_IsoMu27) && mevent->first_lep_pass(MFVEvent::lep_mu).Pt() < 27)
                return false;
        }

        // HT or Bjet or DisplacedDijet trigger && offline presel
        if (apply_presel == 3) {

            bool success = false;
            for(size_t trig : mfv::HTOrBjetOrDisplacedDijetTriggers){
                if(satisfiesTrigger(mevent, trig, setup)){
                    success = true;
                    break;
                }
            }
            if(!success) return false;
        }

        // Bjet or DisplacedDijet trigger && offline presel orthogonal with HT trigger && offline
        if (apply_presel == 4) {

            // Veto events which pass HT trigger and offline HT > 1200 GeV, to keep orthogonal with apply_presel == 1
            if(satisfiesTrigger(mevent, mfv::b_HLT_PFHT1050, setup)) return false;

            bool success = false;
            for(size_t trig : mfv::HTOrBjetOrDisplacedDijetTriggers){

                if(satisfiesTrigger(mevent, trig, setup)){
                    success = true;
                    break;
                }
            }
            if(!success) return false;
        }

        if (apply_presel == 6) {
            bool success = false;

            double gen_sumdbv = 0.0;
            for (int igenv = 0; igenv < 2; ++igenv) {
                double genx = mevent->gen_lsp_decay[igenv*3+0];
                double geny = mevent->gen_lsp_decay[igenv*3+1];
                double genz = mevent->gen_lsp_decay[igenv*3+2];
                double genbs2ddist = mevent->mag(genx - mevent->bsx_at_z(genz), geny - mevent->bsy_at_z(genz));
                gen_sumdbv += genbs2ddist;  
            }
            if (require_gen_sumdbv and gen_sumdbv < 0.7) return false;

            if (bjet_veto and satisfiesTrigger(mevent, mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33, setup)) return false;
            if (bjet_veto and satisfiesTrigger(mevent, mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0, setup)) return false;

            for(size_t trig : mfv::HTOrBjetOrDisplacedDijetTriggers){

                // remain agnostic to the HT1050 trigger
                if (trig == mfv::b_HLT_PFHT1050) continue;
                if (trigbit_tostudy < 999 and int(trig) != trigbit_tostudy) continue;

                if (bjet_agnostic and trig == mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33) continue;
                if (bjet_agnostic and trig == mfv::b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71) continue;
                if (bjet_agnostic and trig == mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0) continue;
                if (bjet_agnostic and trig == mfv::b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5) continue;
                if (bjet_agnostic and trig == mfv::b_HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6) continue;
                if (bjet_agnostic and trig == mfv::b_HLT_DoubleJet90_Double30_TripleBTagCSV_p087) continue;
                if (bjet_agnostic and trig == mfv::b_HLT_QuadJet45_TripleBTagCSV_p087) continue;

                if (dijet_agnostic and trig == mfv::b_HLT_HT430_DisplacedDijet40_DisplacedTrack) continue;
                if (dijet_agnostic and trig == mfv::b_HLT_HT650_DisplacedDijet60_Inclusive) continue;
                if (dijet_agnostic and trig == mfv::b_HLT_HT350_DisplacedDijet40_DisplacedTrack) continue;
                if (dijet_agnostic and trig == mfv::b_HLT_HT650_DisplacedDijet80_Inclusive) continue;

                if(satisfiesTrigger(mevent, trig, setup)){
                    success = true;
                    break;
                }
            }
            if(!success) return false;
        }

        if (require_bquarks && mevent->gen_flavor_code != 2)
            return false;

        if (l1_bit >= 0 && !mevent->pass_l1(l1_bit))
            return false;

        if (trigger_bit >= 0 && !mevent->pass_hlt(trigger_bit))
            return false;

        if (apply_trigger == 1 && !mevent->pass_hlt(mfv::b_HLT_PFHT1050))
            return false;

        if (apply_trigger == 2 && !mevent->pass_hlt(mfv::b_HLT_Ele35_WPTight_Gsf) && !mevent->pass_hlt(mfv::b_HLT_IsoMu27))
            return false;

        if (apply_trigger == 3){
            bool at_least_one_trigger_passed = false;
            for(size_t trig : mfv::HTOrBjetOrDisplacedDijetTriggers){
                if(mevent->pass_hlt(trig)){
                    at_least_one_trigger_passed = true;
                    break;
                }
            }
            if(!at_least_one_trigger_passed) return false;
        }

        if (apply_trigger == 4){
            bool at_least_one_trigger_passed = false;
            for(size_t trig : mfv::HTOrBjetOrDisplacedDijetTriggers){

                // skip HT trigger
                if(trig == mfv::b_HLT_PFHT1050) continue;

                if(mevent->pass_hlt(trig)){
                    at_least_one_trigger_passed = true;
                    break;
                }
            }
            if(!at_least_one_trigger_passed) return false;
        }

        if (mevent->npv < min_npv || mevent->npv > max_npv)
            return false;

        if (mevent->npu < min_npu || mevent->npu > max_npu)
            return false;

        if (mevent->pv_ntracks > max_pv_ntracks)
            return false;

        if (mevent->nlep(false) < min_nleptons)
            return false;

        if (mevent->nlep(true) < min_nselleptons)
            return false;

        if (mevent->njets(20) < min_njets || mevent->njets(20) > max_njets)
            return false;

        for (int i = 0; i < 3; ++i)
            if (mevent->nbtags(i) < min_nbtags[i] || mevent->nbtags(i) > max_nbtags[i])
                return false;

        if (mevent->jet_ht(40) < min_ht)
            return false;

        if (mevent->jet_ht(40) > max_ht)
            return false;
    }

    if (apply_vertex_cuts) {
        edm::Handle<MFVVertexAuxCollection> vertices;
        event.getByToken(vertex_token, vertices);

        const int nsv = int(vertices->size());
        if (nsv < min_nvertex || nsv > max_nvertex)
            return false;

        const bool two_vertex_cuts_on =
            ntracks01_0 > 0 ||
            ntracks01_1 > 0 ||
            min_ntracks01 > 0 ||
            max_ntracks01 < 100000 || // for ints
            min_maxtrackpt01 > 0 ||
            max_maxtrackpt01 < 1e6 || // for floats
            min_njetsntks01 > 0 ||
            min_tkonlymass01 > 0 ||
            min_jetsntkmass01 > 0 ||
            min_tksjetsntkmass01 > 0 ||
            min_absdeltaphi01 > 0 ||
            min_bs2ddist01 > 0 ||
            min_bs2dsig01 > 0 ||
            min_pv2ddist01 > 0 ||
            min_pv3ddist01 > 0 ||
            min_pv2dsig01 > 0 ||
            min_pv3dsig01 > 0 ||
            min_svdist2d > 0 ||
            max_svdist2d < 1e6 ||
            min_svdist3d > 0 ||
            max_ntrackssharedwpv01 < 100000 ||
            max_ntrackssharedwpvs01 < 100000 ||
            max_fractrackssharedwpv01 < 1e6 ||
            max_fractrackssharedwpvs01 < 1e6;

        if (two_vertex_cuts_on) {
            if (nsv < 2)
                return false;

            const MFVVertexAux& v0 = vertices->at(0);
            const MFVVertexAux& v1 = vertices->at(1);

            if (ntracks01_0 > 0 || ntracks01_1 > 0) {
                assert(ntracks01_0 > 0 && ntracks01_1 > 0);
                assert(v0.ntracks() >= v1.ntracks());
                if (v0.ntracks() != ntracks01_0 || v1.ntracks() != ntracks01_1)
                    return false;
            }
            if (v0.ntracks() + v1.ntracks() < min_ntracks01)
                return false;
            if (v0.ntracks() + v1.ntracks() > max_ntracks01)
                return false;
            if (v0.maxtrackpt() + v1.maxtrackpt() < min_maxtrackpt01)
                return false;
            if (v0.maxtrackpt() + v1.maxtrackpt() > max_maxtrackpt01)
                return false;
            if (v0.njets[mfv::JByNtracks] + v1.njets[mfv::JByNtracks] < min_njetsntks01)
                return false;
            if (v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly] < min_tkonlymass01)
                return false;
            if (v0.mass[mfv::PJetsByNtracks] + v1.mass[mfv::PJetsByNtracks] < min_jetsntkmass01)
                return false;
            if (v0.mass[mfv::PTracksPlusJetsByNtracks] + v1.mass[mfv::PTracksPlusJetsByNtracks] < min_tksjetsntkmass01)
                return false;

            if (use_mevent) {
                const double phi0 = atan2(v0.y - mevent->bsy, v0.x - mevent->bsx);
                const double phi1 = atan2(v1.y - mevent->bsy, v1.x - mevent->bsx);
                if (fabs(reco::deltaPhi(phi0, phi1)) < min_absdeltaphi01)
                    return false;
            }

            if (v0.bs2ddist + v1.bs2ddist < min_bs2ddist01)
                return false;

            if (v0.bs2dsig() + v1.bs2dsig() < min_bs2dsig01)
                return false;

            if (v0.pv2ddist + v1.pv2ddist < min_pv2ddist01)
                return false;

            if (v0.pv3ddist + v1.pv3ddist < min_pv3ddist01)
                return false;

            if (v0.pv2dsig() + v1.pv2dsig() < min_pv2dsig01)
                return false;

            if (v0.pv3dsig() + v1.pv3dsig() < min_pv3dsig01)
                return false;

            const double svdist2d = mag(v0.x - v1.x,
                    v0.y - v1.y);
            const double svdist3d = mag(v0.x - v1.x,
                    v0.y - v1.y,
                    v0.z - v1.z);

            if (svdist2d < min_svdist2d || svdist2d > max_svdist2d)
                return false;

            if (svdist3d < min_svdist3d)
                return false;

            if (v0.ntrackssharedwpv()  + v1.ntrackssharedwpv()  > max_ntrackssharedwpv01)
                return false;
            if (v0.ntrackssharedwpvs() + v1.ntrackssharedwpvs() > max_ntrackssharedwpvs01)
                return false;
            if (float(v0.ntrackssharedwpv()  + v1.ntrackssharedwpv ())/(v0.ntracks() + v1.ntracks()) > max_fractrackssharedwpv01)
                return false;
            if (float(v0.ntrackssharedwpvs() + v1.ntrackssharedwpvs())/(v0.ntracks() + v1.ntracks()) > max_fractrackssharedwpvs01)
                return false;
        }
    }

    return true;
}

bool MFVAnalysisCuts::satisfiesTrigger(edm::Handle<MFVEvent> mevent, size_t trig, const edm::EventSetup& setup) {
    if(require_trigbit and !mevent->pass_hlt(trig)) return false;

    edm::ESHandle<JetCorrectorParametersCollection> jet_corr;
    setup.get<JetCorrectionsRecord>().get("AK4PF", jet_corr);
    JetCorrectionUncertainty jec_unc((*jet_corr)["Uncertainty"]);

    // Container for JER/JES-corrected jet pT's
    std::vector<float> jet_pt_checks;

    // Get a shorthand for the current year
    int year = int(MFVNEUTRALINO_YEAR);

    // note that if these weren't pT ordered, we'd have to be more careful in the loops...
    int njets     = mevent->njets(20);
    int ncalojets = mevent->calo_jet_pt.size();

    // note that this could be loosened/tightened if desired
    int sel_btags      = 0;
    int sel_btags_hard = 0;
    std::vector<int> calojet_ngood(2, 0); // Two entries (for different pT cuts, each start at 0)
    std::vector<int> pfjet_ngood(2, 0); // Two entries (for different pT cuts, each start at 0) //FIXME might be temporary

    std::vector<float> jettk_dxys;
    std::vector<float> jettk_nsigmadxys;

    float alt_calo_ht = 0.0; // To account for the fact that calo_jet_ht uses jets up to eta 5.0. We don't want that

    // FIXME Fix this comment once the code is done
    for (int ic=0; ic < ncalojets; ic++) {
        float cj_pt = mevent->calo_jet_pt[ic];
        float cj_aeta = fabs(mevent->calo_jet_eta[ic]);

        // Do this loop if we want to study correction for JER
        if (study_jer) {
            float cj_E  = mevent->calo_jet_energy[ic];
            float closest_pf_dR = 9.9;
            int   closest_pf_idx = 999;

            for (int ip=0; ip < njets; ip++) {
                float temp_dR = reco::deltaR(mevent->jet_eta[ip], mevent->jet_phi[ip], mevent->calo_jet_eta[ic], mevent->calo_jet_phi[ic]);
                if (temp_dR < closest_pf_dR) {
                    closest_pf_dR = temp_dR;
                    closest_pf_idx = ip;
                }
            }

            cj_pt = jmt::UncertTools::jer_pt(mevent->jet_gen_energy[closest_pf_idx], cj_E, cj_pt, cj_aeta, jes_jer_var_up);

        }

        else if (study_jes) {
            jec_unc.setJetEta(mevent->calo_jet_eta[ic]);
            jec_unc.setJetPt(mevent->calo_jet_pt[ic]);
            if (    jes_jer_var_up) { cj_pt *= (1 + jec_unc.getUncertainty(true)); }
            if (not jes_jer_var_up) { cj_pt *= (1 - jec_unc.getUncertainty(false)); }
        }

        if (cj_pt > 30.0 and cj_aeta < 2.5) alt_calo_ht += mevent->calo_jet_pt[ic];

        // Don't do the following CPU-intensive for loop if it's not a relevant jet
        if (cj_pt < 40.0 or fabs(mevent->calo_jet_eta[ic]) > 2.0) continue;

        // If you made it here, the CaloJet is good enough for the low HT trigger. Record this & check if it's good enough for High HT trig
        calojet_ngood[0]++;
        if (cj_pt > 60.0) calojet_ngood[1]++;

    }

    for(int j0 = 0; j0 < njets; j0++) {
        float rand_y = distribution(rng);
        float pf_pt = mevent->jet_pt[j0];

        if (study_jer) {
            pf_pt = jmt::UncertTools::jer_pt_alt(mevent->jet_gen_energy[j0], mevent->jet_p4(j0), jes_jer_var_up);
        }

        else if (study_jes) {
            jec_unc.setJetEta(mevent->jet_eta[j0]);
            jec_unc.setJetPt(mevent->jet_pt[j0]);
            if (    jes_jer_var_up) { pf_pt *= (1 + jec_unc.getUncertainty(true)); }
            if (not jes_jer_var_up) { pf_pt *= (1 - jec_unc.getUncertainty(false)); }
        }

        jet_pt_checks.push_back(pf_pt);

        if (pf_pt > 75.0 and fabs(mevent->jet_eta[j0]) < 2.0) {
            pfjet_ngood[0]++;
            if (pf_pt > 90.0) {
                pfjet_ngood[1]++;
            }
        }

        switch(btagger_choice) {
            case 0:
                if (mevent->jet_bdisc_csv[j0] > jmt::BTagging::discriminator_min(0, btag_wp)){
                    sel_btags++;
                    if (pf_pt > 80.0) sel_btags_hard++;
                }
                break;
            case 1:
                if (mevent->jet_bdisc_deepcsv[j0] > jmt::BTagging::discriminator_min(1, btag_wp)){
                    sel_btags++;
                    if (pf_pt > 80.0) sel_btags_hard++;
                }
                break;
            case 2:
                if (mevent->jet_bdisc_deepflav[j0] > jmt::BTagging::discriminator_min(2, btag_wp)){
                    // If we're applying SFs and this jet gets demoted, skip it
                    if (study_btag_sf and jmt::UncertTools::reject_btag_sf(pf_pt, rand_y, study_btag_sfvar, year)) {
                        break;
                    }
                    sel_btags++;
                    if (pf_pt > 80.0) sel_btags_hard++;
                }
                // If we're applying SFs and this otherwise untagged jet gets promoted, make sure we count it
                else if (study_btag_sf and jmt::UncertTools::admit_btag_sf(pf_pt, rand_y, mevent->jet_hadron_flavor(j0), study_btag_sfvar, year)) {
                    sel_btags++;
                    if (pf_pt > 80.0) sel_btags_hard++;
                }
                break;
        }
    }

    // For the tri-bjet trigger
    float ht_thresh_lo = 30.0;
    float jet_ht_check_30 = std::accumulate(jet_pt_checks.begin(), jet_pt_checks.end(), 0.f,
            [ht_thresh_lo](float init, float b) { if (b > ht_thresh_lo) init += b; return init; });

    // For the tri-bjet trigger
    float ht_thresh_hi = 40.0;
    float jet_ht_check_40 = std::accumulate(jet_pt_checks.begin(), jet_pt_checks.end(), 0.f,
            [ht_thresh_hi](float init, float b) { if (b > ht_thresh_hi) init += b; return init; });

    // for the trigger chains where we need to do any detailed matching
    bool passed_kinematics = false;

    switch(trig){
        case mfv::b_HLT_PFHT1050 :
            return mevent->jet_ht(40) >= 1200 && mevent->njets(20) >= 4;

        case mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33 :
            {
                if(year != 2017) return false;
                if(require_bjet_psel and sel_btags_hard < 2) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 125) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 125) continue;

                        if(fabs(mevent->jet_eta[j0] - mevent->jet_eta[j1]) < 1.6){
                            passed_kinematics = true;
                        }
                    }
                }
                return passed_kinematics;
            }

        case mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0 :
            {
                if(year != 2017) return false;
                if(jet_ht_check_30 < 350 || njets < 4) return false;
                if(require_bjet_psel and sel_btags < 3) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(!jet_hlt_match(mevent, j0) || jet_pt_checks[j0] < 90) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(!jet_hlt_match(mevent, j1) || jet_pt_checks[j1] < 75) continue;

                        for(int j2 = j1+1; j2 < njets; ++j2){
                            if(!jet_hlt_match(mevent, j2) || jet_pt_checks[j2] < 55) continue;

                            for(int j3 = j2+1; j3 < njets; ++j3){
                                if(!jet_hlt_match(mevent, j3) || jet_pt_checks[j3] < 55) continue;

                                passed_kinematics = true;
                            }
                        }
                    }
                }
                return passed_kinematics;
            }

        case mfv::b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71 :
            {
                if(year != 2018) return false;
                if(require_bjet_psel and sel_btags_hard < 2) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(!jet_hlt_match(mevent, j0) || jet_pt_checks[j0] < 140) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(!jet_hlt_match(mevent, j1) || jet_pt_checks[j1] < 140) continue;

                        if(fabs(mevent->jet_eta[j0] - mevent->jet_eta[j1]) < 1.6){
                            passed_kinematics = true;
                        }
                    }
                }
                return passed_kinematics;
            }

        case mfv::b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 :
            {
                if(year != 2018) return false;
                if(jet_ht_check_30 < 425 || njets < 4) return false;
                if(require_bjet_psel and sel_btags < 3) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(!jet_hlt_match(mevent, j0) || jet_pt_checks[j0] < 95) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(!jet_hlt_match(mevent, j1) || jet_pt_checks[j1] < 65) continue;

                        for(int j2 = j1+1; j2 < njets; ++j2){
                            if(!jet_hlt_match(mevent, j2) || jet_pt_checks[j2] < 60) continue;

                            for(int j3 = j2+1; j3 < njets; ++j3){
                                if(!jet_hlt_match(mevent, j3) || jet_pt_checks[j3] < 55) continue;

                                passed_kinematics = true;
                            }
                        }
                    }
                }
                return passed_kinematics;
            }

        case mfv::b_HLT_HT430_DisplacedDijet40_DisplacedTrack :
            {
                if(year != 2018 and year != 2017) return false;
                if(jet_ht_check_40 < 557 || pfjet_ngood[0] < 2) return false;

                passed_kinematics = true;
                return passed_kinematics;
            }

        case mfv::b_HLT_HT650_DisplacedDijet60_Inclusive :
            {
                if(year != 2018 and year != 2017) return false;
                if(jet_ht_check_40 < 846 || pfjet_ngood[1] < 2) return false;
                //if(jet_ht_check_40 < 750 || pfjet_ngood[1] < 2) return false;

                passed_kinematics = true;
                return passed_kinematics;
            }

            // Start 2016 bjet and displaced dijet triggers here
        case mfv::b_HLT_HT350_DisplacedDijet40_DisplacedTrack :
            {
                if(year != 20161 and year != 20162) return false;
                if(jet_ht_check_40 < 470 || njets < 2 || pfjet_ngood[1] < -2 || jet_ht_check_30 < -2) return false; // Can delete the pfjet_ngood part... it's a dummy thing for now

                for(int j0 = 0; j0 < njets; ++j0){
                    if(mevent->jet_pt[j0] < 50) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(mevent->jet_pt[j1] < 50) continue;
                        passed_kinematics = true;
                    }
                }
                return passed_kinematics;
            }
        case mfv::b_HLT_HT650_DisplacedDijet80_Inclusive :
            {
                if(year != 20161 and year != 20162) return false;
                if(jet_ht_check_40 < 800 || njets < 2) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(mevent->jet_pt[j0] < 100) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(mevent->jet_pt[j1] < 100) continue;
                        passed_kinematics = true;
                    }
                }
                return passed_kinematics;
            }

        case mfv::b_HLT_QuadJet45_TripleBTagCSV_p087 :
            {
                if(year != 20161 and year != 20162) return false;
                if(njets < 4) return false;
                if(sel_btags < 3) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 50) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 50) continue;

                        for(int j2 = j1+1; j2 < njets; ++j2){
                            if(!jet_hlt_match(mevent, j2) || mevent->jet_pt[j2] < 50) continue;

                            for(int j3 = j2+1; j3 < njets; ++j3){
                                if(!jet_hlt_match(mevent, j3) || mevent->jet_pt[j3] < 50) continue;

                                passed_kinematics = true;
                            }
                        }
                    }
                }
                return passed_kinematics;

            }

        case mfv::b_HLT_DoubleJet90_Double30_TripleBTagCSV_p087 :
            {
                if(year != 20161 and year != 20162) return false;
                if(njets < 4) return false;
                if(sel_btags < 3) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 100) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 100) continue;

                        for(int j2 = j1+1; j2 < njets; ++j2){
                            if(!jet_hlt_match(mevent, j2) || mevent->jet_pt[j2] < 35) continue;

                            for(int j3 = j2+1; j3 < njets; ++j3){
                                if(!jet_hlt_match(mevent, j3) || mevent->jet_pt[j3] < 35) continue;

                                passed_kinematics = true;
                            }
                        }
                    }
                }
                return passed_kinematics;
            }

        case mfv::b_HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6 :
            {
                if(year != 20161 and year != 20162) return false;
                if(sel_btags_hard < 2) return false;

                for(int j0 = 0; j0 < njets; ++j0){
                    if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 110) continue;

                    for(int j1 = j0+1; j1 < njets; ++j1){
                        if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 110) continue;

                        if(fabs(mevent->jet_eta[j0] - mevent->jet_eta[j1]) < 1.6){
                            passed_kinematics = true;
                        }
                    }
                }
                return passed_kinematics;
            }

        default :
            {
                throw std::invalid_argument(std::string(mfv::hlt_paths[trig]) + " not implemented in satisfiesTrigger");
            }
    }

    return false;
}

DEFINE_FWK_MODULE(MFVAnalysisCuts);
