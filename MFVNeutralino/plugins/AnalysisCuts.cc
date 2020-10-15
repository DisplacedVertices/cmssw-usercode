#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/Tools/interface/BTagging.h"

class MFVAnalysisCuts : public edm::EDFilter {
public:
  explicit MFVAnalysisCuts(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  bool satisfiesTrigger(edm::Handle<MFVEvent>, size_t) const;

  bool jet_hlt_match(edm::Handle<MFVEvent> mevent, int i, float min_jet_pt=20.) const {
    // an offline jet with a successful HLT match will have a nonzero jet_hlt_pt;
    // all others have the default value of 0
    return mevent->jet_hlt_pt[i] > min_jet_pt;
  }
  bool displaced_jet_hlt_match(edm::Handle<MFVEvent> mevent, int i, float min_jet_pt=20.) const {
    // an offline jet with a successful HLT match will have a nonzero displaced_jet_hlt_pt;
    // all others have the default value of 0
    return mevent->displaced_jet_hlt_pt[i] > min_jet_pt;
  }

  const edm::InputTag mevent_src;
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  const bool use_mevent;

  const int apply_presel;

  const bool require_bquarks;
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
    use_mevent(mevent_src.label() != ""),
    apply_presel(cfg.getParameter<int>("apply_presel")),
    require_bquarks(cfg.getParameter<bool>("require_bquarks")),
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

bool MFVAnalysisCuts::filter(edm::Event& event, const edm::EventSetup&) {
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
        if(satisfiesTrigger(mevent, trig)){
          success = true;
          break;
        }
      }
      if(!success) return false;
    }

    // Bjet or DisplacedDijet trigger && offline presel orthogonal with HT trigger && offline
    if (apply_presel == 4) {

      // Veto events which pass HT trigger and offline HT > 1200 GeV, to keep orthogonal with apply_presel == 1
      if(satisfiesTrigger(mevent, mfv::b_HLT_PFHT1050)) return false;

      bool success = false;
      for(size_t trig : mfv::HTOrBjetOrDisplacedDijetTriggers){

        // skip HT trigger
        if(trig == mfv::b_HLT_PFHT1050) continue;

        if(satisfiesTrigger(mevent, trig)){
          success = true;
          break;
        }
      }
      if(!success) return false;
    }

    // MET trigger

    if (apply_presel == 5) {
      return satisfiesTrigger(mevent, mfv::b_HLT_PFMET120_PFMHT120_IDTight);
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

bool MFVAnalysisCuts::satisfiesTrigger(edm::Handle<MFVEvent> mevent, size_t trig) const {
  if(!mevent->pass_hlt(trig)) return false;

  // note that if these weren't pT ordered, we'd have to be more careful in the loops...
  int njets = mevent->njets(20);

  // note that this could be loosened if desired
  int nbtaggedjets = mevent->nbtags(jmt::BTagging::tight);

  // for the trigger chains where we need to do any detailed matching
  bool passed_kinematics = false;

  switch(trig){
    case mfv::b_HLT_PFHT1050 :
      return mevent->jet_ht(40) >= 1200 && mevent->njets(20) >= 4;
    case mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33 :
      {
        if(njets < 4) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 140) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 140) continue;

            if(fabs(mevent->jet_eta[j0] - mevent->jet_eta[j1]) < 1.6){
              passed_kinematics = true;
            }
          }
        }
        return passed_kinematics;
      }
    case mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0 :
      {
        if(mevent->jet_ht(30) < 450 || njets < 4) return false;
        if(nbtaggedjets < 3) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 115) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 100) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(mevent, j2) || mevent->jet_pt[j2] < 85) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(mevent, j3) || mevent->jet_pt[j3] < 80) continue;

                passed_kinematics = true;
              }
            }
          }
        }
        return passed_kinematics;
      }
      case mfv::b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71 :
      {
        if(njets < 4) return false;
        if(nbtaggedjets < 2) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 156) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 156) continue;

            if(fabs(mevent->jet_eta[j0] - mevent->jet_eta[j1]) < 1.6){
              passed_kinematics = true;
            }
          }
        }
        return passed_kinematics;
      }
      case mfv::b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 :
      {
        if(mevent->jet_ht(30) < 480 || njets < 4) return false;
        if(nbtaggedjets < 3) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 115) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 100) continue;

            for(int j2 = j1+1; j2 < njets; ++j2){
              if(!jet_hlt_match(mevent, j2) || mevent->jet_pt[j2] < 85) continue;

              for(int j3 = j2+1; j3 < njets; ++j3){
                if(!jet_hlt_match(mevent, j3) || mevent->jet_pt[j3] < 80) continue;

                passed_kinematics = true;
              }
            }
          }
        }
        return passed_kinematics;
      }
      case mfv::b_HLT_HT430_DisplacedDijet40_DisplacedTrack :
      {
        if(mevent->jet_ht(40) < 580 || njets < 4) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!displaced_jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 80) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!displaced_jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 80) continue;
            passed_kinematics = true;
          }
        }
        return passed_kinematics;
      }
      case mfv::b_HLT_HT650_DisplacedDijet60_Inclusive :
      {
        if(mevent->jet_ht(40) < 800 || njets < 4) return false;

        for(int j0 = 0; j0 < njets; ++j0){
          if(!displaced_jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 100) continue;

          for(int j1 = j0+1; j1 < njets; ++j1){
            if(!displaced_jet_hlt_match(mevent, j1) || mevent->jet_pt[j1] < 100) continue;
            passed_kinematics = true;
          }
        }
        return passed_kinematics;
      }
      case mfv::b_HLT_PFMET120_PFMHT120_IDTight :
      {
        if(mevent->met() < 200 || njets < 4) return false; // cut on MET to avoid turn-on region, maybe cut value need to be determined
        return true;
      }
      default :
      {
        throw std::invalid_argument(std::string(mfv::hlt_paths[trig]) + " not implemented in satisfiesTrigger");
      }
  }

  return false;
}

DEFINE_FWK_MODULE(MFVAnalysisCuts);
