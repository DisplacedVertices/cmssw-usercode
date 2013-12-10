#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

class MFVAnalysisCuts : public edm::EDFilter {
public:
  explicit MFVAnalysisCuts(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag mevent_src;
  const int trigger_bit;
  const bool re_trigger;
  const double min_4th_jet_pt;
  const double min_5th_jet_pt;
  const double min_6th_jet_pt;
  const int min_njets;
  const int max_njets;
  const std::vector<int> min_nbtags;
  const std::vector<int> max_nbtags;
  const double min_sumht;
  const int min_nmuons;
  const int min_nsemilepmuons;
  const int min_nleptons;

  const bool apply_vertex_cuts;
  const edm::InputTag vertex_src;
  const int min_nvertex;
  const int min_ntracks01;
  const double min_maxtrackpt01;
  const int min_njetsntks01;
  const double min_tkonlymass01;
  const double min_jetsntkmass01;
  const double min_tksjetsntkmass01;
};

MFVAnalysisCuts::MFVAnalysisCuts(const edm::ParameterSet& cfg) 
  : mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    trigger_bit(cfg.getParameter<int>("trigger_bit")),
    re_trigger(cfg.getParameter<bool>("re_trigger")),
    min_4th_jet_pt(cfg.getParameter<double>("min_4th_jet_pt")),
    min_5th_jet_pt(cfg.getParameter<double>("min_5th_jet_pt")),
    min_6th_jet_pt(cfg.getParameter<double>("min_6th_jet_pt")),
    min_njets(cfg.getParameter<int>("min_njets")),
    max_njets(cfg.getParameter<int>("max_njets")),
    min_nbtags(cfg.getParameter<std::vector<int> >("min_nbtags")),
    max_nbtags(cfg.getParameter<std::vector<int> >("max_nbtags")),
    min_sumht(cfg.getParameter<double>("min_sumht")),
    min_nmuons(cfg.getParameter<int>("min_nmuons")),
    min_nsemilepmuons(cfg.getParameter<int>("min_nsemilepmuons")),
    min_nleptons(cfg.getParameter<int>("min_nleptons")),
    apply_vertex_cuts(cfg.getParameter<bool>("apply_vertex_cuts")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    min_nvertex(cfg.getParameter<int>("min_nvertex")),
    min_ntracks01(cfg.getParameter<int>("min_ntracks01")),
    min_maxtrackpt01(cfg.getParameter<double>("min_maxtrackpt01")),
    min_njetsntks01(cfg.getParameter<int>("min_njetsntks01")),
    min_tkonlymass01(cfg.getParameter<double>("min_tkonlymass01")),
    min_jetsntkmass01(cfg.getParameter<double>("min_jetsntkmass01")),
    min_tksjetsntkmass01(cfg.getParameter<double>("min_tksjetsntkmass01"))
{
}

bool MFVAnalysisCuts::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);

  if (trigger_bit >= 0) {
    if (re_trigger) {
      bool pass_trigger[mfv::n_trigger_paths] = { 0 };
      TriggerHelper trig_helper(event, edm::InputTag("TriggerResults", "", "HLT"));
      mfv::trigger_decision(trig_helper, pass_trigger);
      if (!pass_trigger[trigger_bit])
        return false;
    }
    else if (!mevent->pass_trigger[trigger_bit])
      return false;
  }

  if (mevent->nmu[0] < min_nmuons)
    return false;

  if (mevent->nmu[1] < min_nsemilepmuons)
    return false;

  if (mevent->nlep(0) < min_nleptons)
    return false;

  if (mevent->njets < min_njets || mevent->njets > max_njets)
    return false;

  if((min_4th_jet_pt > 0 && mevent->jetpt4 < min_4th_jet_pt) ||
     (min_5th_jet_pt > 0 && mevent->jetpt5 < min_5th_jet_pt) ||
     (min_6th_jet_pt > 0 && mevent->jetpt6 < min_6th_jet_pt))
    return false;

  for (int i = 0; i < 3; ++i)
    if (mevent->nbtags[i] < min_nbtags[i] || mevent->nbtags[i] > max_nbtags[i])
      return false;

  if (mevent->jet_sum_ht < min_sumht)
    return false;

  if (apply_vertex_cuts) {
    edm::Handle<MFVVertexAuxCollection> vertices;
    event.getByLabel(vertex_src, vertices);

    const int nsv = int(vertices->size());
    if (nsv < min_nvertex)
      return false;

    if (min_ntracks01 > 0 || min_maxtrackpt01 > 0 || min_njetsntks01 > 0 || min_tkonlymass01 > 0 || min_jetsntkmass01 > 0 || min_tksjetsntkmass01 > 0) {
      if (nsv < 2)
        return false;

      const MFVVertexAux& v0 = vertices->at(0);
      const MFVVertexAux& v1 = vertices->at(1);

      if (v0.ntracks + v1.ntracks < min_ntracks01)
        return false;
      if (v0.maxtrackpt + v1.maxtrackpt < min_maxtrackpt01)
        return false;
      if (v0.njets[mfv::JByNtracks] + v1.njets[mfv::JByNtracks] < min_njetsntks01)
        return false;
      if (v0.mass[mfv::PTracksOnly] + v1.mass[mfv::PTracksOnly] < min_tkonlymass01)
        return false;
      if (v0.mass[mfv::PJetsByNtracks] + v1.mass[mfv::PJetsByNtracks] < min_jetsntkmass01)
        return false;
      if (v0.mass[mfv::PTracksPlusJetsByNtracks] + v1.mass[mfv::PTracksPlusJetsByNtracks] < min_tksjetsntkmass01)
        return false;
    }
  }

  return true;
}

DEFINE_FWK_MODULE(MFVAnalysisCuts);
