#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleFiller.h"

class TrackingTreer : public edm::EDAnalyzer {
public:
  explicit TrackingTreer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  jmt::BaseSubNtupleFiller base_filler;
  jmt::BeamspotSubNtupleFiller bs_filler;
  jmt::PrimaryVerticesSubNtupleFiller pvs_filler;
  jmt::TracksSubNtupleFiller tracks_filler;
  jmt::JetsSubNtupleFiller jets_filler;

  TTree* tree;
  jmt::TrackingAndJetsNtuple nt;
};

TrackingTreer::TrackingTreer(const edm::ParameterSet& cfg)
  : base_filler(nt.base(), cfg, consumesCollector()),
    bs_filler(nt.bs(), cfg, consumesCollector()),
    pvs_filler(nt.pvs(), cfg, consumesCollector(), true, false),
    tracks_filler(nt.tracks(), cfg, consumesCollector(),
                  cfg.getParameter<bool>("track_sel") ? [](const reco::Track& tk) { return tk.pt() < 1 || tk.hitPattern().pixelLayersWithMeasurement() < 2 || tk.hitPattern().stripLayersWithMeasurement() < 6; }
                                                      : [](const reco::Track& tk) { return false; }),
    jets_filler(nt.jets(), cfg, consumesCollector())
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  nt.write_to_tree(tree);
}

void TrackingTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();

  base_filler(event);
  bs_filler(event);
  pvs_filler(event);
  tracks_filler(event);
  jets_filler(event);

  // JMTBAD tracks which pv and jet

  tree->Fill();
}

DEFINE_FWK_MODULE(TrackingTreer);
