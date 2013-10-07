#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralino/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/VertexAux.h"

class MFVAnalysisCuts : public edm::EDFilter {
public:
  explicit MFVAnalysisCuts(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag mevent_src;
  const int trigger_bit;
  const double min_4th_jet_pt;
  const double min_5th_jet_pt;
  const double min_6th_jet_pt;
  const int min_njets;
  const int max_njets;
  const int min_nbtags;
  const double min_sum_ht;
  const int min_nleptons;

  const edm::InputTag vertex_src;
  const int min_nvertex;
  const int min_ntracks01;
  const double min_maxtrackpt01;
};

MFVAnalysisCuts::MFVAnalysisCuts(const edm::ParameterSet& cfg) 
  : mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    trigger_bit(cfg.getParameter<int>("trigger_bit")),
    min_4th_jet_pt(cfg.getParameter<double>("min_4th_jet_pt")),
    min_5th_jet_pt(cfg.getParameter<double>("min_5th_jet_pt")),
    min_6th_jet_pt(cfg.getParameter<double>("min_6th_jet_pt")),
    min_njets(cfg.getParameter<int>("min_njets")),
    max_njets(cfg.getParameter<int>("max_njets")),
    min_nbtags(cfg.getParameter<int>("min_nbtags")),
    min_sum_ht(cfg.getParameter<double>("min_sum_ht")),
    min_nleptons(cfg.getParameter<int>("min_nleptons")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    min_nvertex(cfg.getParameter<int>("min_nvertex")),
    min_ntracks01(cfg.getParameter<int>("min_ntracks01")),
    min_maxtrackpt01(cfg.getParameter<int>("min_maxtrackpt01"))
{
}

bool MFVAnalysisCuts::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);

  if (!mevent->pass_trigger[trigger_bit])
    return false;

  if (mevent->nlep(0) < min_nleptons)
    return false;

  if (mevent->njets < min_njets || mevent->njets > max_njets)
    return false;

  if (mevent->jetpt4 < min_4th_jet_pt ||
      mevent->jetpt5 < min_5th_jet_pt ||
      mevent->jetpt6 < min_6th_jet_pt)
    return false;

  if (mevent->nbtags < min_nbtags)
    return false;

  if (mevent->jet_sum_ht < min_sum_ht)
    return false;

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  const int nsv = int(vertices->size());
  if (nsv < min_nvertex)
    return false;

  if (min_ntracks01 > 0 || min_maxtrackpt01 > 0) {
    if (nsv < 2)
      return false;

    const MFVVertexAux& v0 = vertices->at(0);
    const MFVVertexAux& v1 = vertices->at(1);

    if (v0.ntracks + v1.ntracks < min_ntracks01)
      return false;

    if (v0.maxtrackpt + v1.maxtrackpt < min_maxtrackpt01)
      return false;
  }

  return true;
}

DEFINE_FWK_MODULE(MFVAnalysisCuts);
