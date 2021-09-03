#include "DVCode/Tools/interface/NtupleFiller.h"

class TrackingTreer : public edm::EDAnalyzer {
public:
  explicit TrackingTreer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  jmt::TrackingAndJetsNtuple nt;
  jmt::TrackingAndJetsNtupleFiller nt_filler;
};

TrackingTreer::TrackingTreer(const edm::ParameterSet& cfg)
  : nt_filler(nt, cfg, NF_CC_TrackingAndJets_v,
              jmt::TrackingAndJetsNtupleFillerParams().tracks_cut_level(cfg.getParameter<int>("track_cut_level")))
{}

void TrackingTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt_filler.fill(event, true);
}

DEFINE_FWK_MODULE(TrackingTreer);
