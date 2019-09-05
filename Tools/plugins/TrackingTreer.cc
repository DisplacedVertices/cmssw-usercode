#include "JMTucker/Tools/interface/NtupleFiller.h"

class TrackingTreer : public edm::EDAnalyzer {
public:
  explicit TrackingTreer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  TTree* t;
  jmt::TrackingAndJetsNtuple nt;
  jmt::TrackingAndJetsNtupleFiller nt_filler;
};

TrackingTreer::TrackingTreer(const edm::ParameterSet& cfg)
  : t(NtupleFiller_setup(nt)),
    nt_filler(nt, cfg, NF_CC_TrackingAndJets_v,
              jmt::TrackingAndJetsNtupleFillerParams().tracks_cut_level(cfg.getParameter<int>("track_cut_level")))
{}

void TrackingTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();
  nt_filler(event);
  t->Fill();
}

DEFINE_FWK_MODULE(TrackingTreer);
