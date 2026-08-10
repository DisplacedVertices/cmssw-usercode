#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"


class MFVMETTrigFilter : public edm::EDFilter {
public:
  explicit MFVMETTrigFilter(const edm::ParameterSet&);

private:
  virtual void beginRun(edm::Run const &, edm::EventSetup const&);
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  std::string   processName_;
  std::string   sigTriggerName_;
  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
  edm::EDGetTokenT<pat::METCollection> pfMetToken_;
  double met_thresh_;
  bool verbose_;

  /// additional class data memebers
  edm::Handle<edm::TriggerResults>           triggerResultsHandle_;
  HLTConfigProvider hltConfig_;

  
};
MFVMETTrigFilter::MFVMETTrigFilter(const edm::ParameterSet& ps)
{
  using namespace std;
  using namespace edm;

  processName_ = ps.getUntrackedParameter<std::string>("processName","HLT");
  sigTriggerName_ = ps.getUntrackedParameter<std::string>("sigTriggerName","HLT_PFMET120_PFMHT120_IDTight_v*");
  triggerResultsToken_ = consumes<edm::TriggerResults> (ps.getUntrackedParameter<edm::InputTag>("triggerResultsTag", edm::InputTag("TriggerResults", "", "HLT")));
  pfMetToken_ = consumes<pat::METCollection>(ps.getUntrackedParameter<edm::InputTag>("pfMetInputTag_", edm::InputTag("slimmedMETs")));
  met_thresh_ = ps.getUntrackedParameter<double>("met_thresh",150.0);
  verbose_ = ps.getUntrackedParameter<bool>("verbose",false);
}

void
MFVMETTrigFilter::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  using namespace std;
  using namespace edm;

  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      const unsigned int n(hltConfig_.size());
      // check if trigger names in (new) config
      unsigned int sigTriggerIndex(hltConfig_.triggerIndex(sigTriggerName_));
      if (sigTriggerIndex>=n) {
  cout << "MFVMETTrigFilter::filter:"
       << " TriggerName " << sigTriggerName_ 
       << " not available in config!" << endl;
      }
    } // if changed
  } else {
    cout << "MFVMETTrigFilter::filter:"
   << " config extraction failure with process name "
   << processName_ << endl;
  }

}


bool
MFVMETTrigFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace std;
  using namespace edm;
  using namespace reco;
  using namespace trigger;

  if (verbose_) cout << endl;

  // get event products
  iEvent.getByToken(triggerResultsToken_,triggerResultsHandle_);
  if (!triggerResultsHandle_.isValid()) {
    cout << "MFVMETTrigFilter::filter: Error in getting TriggerResults product from Event!" << endl;
    return false;
  }

  // sanity check
  assert(triggerResultsHandle_->size()==hltConfig_.size());

  // retrieve necessary containers
  Handle<pat::METCollection > pfMetHandle_;
  iEvent.getByToken( pfMetToken_ , pfMetHandle_ );

  if (verbose_) cout << endl;

  const unsigned int ntrigs(hltConfig_.size());
  const unsigned int sigTriggerIndex(hltConfig_.triggerIndex(sigTriggerName_));
  assert(sigTriggerIndex==iEvent.triggerNames(*triggerResultsHandle_).triggerIndex(sigTriggerName_));

  // abort on invalid trigger name
  if (sigTriggerIndex>=ntrigs) {
    cout << "MFVMETTrigFilter::filter: path "
   << sigTriggerName_ << " - not found!" << endl;
    return false;
  }

  if (verbose_) {
    cout << "MFVMETTrigFilter::filter: signal path "
   << sigTriggerName_ << " [" << sigTriggerIndex << "]" << endl;
  }
  
  // modules on this trigger path
  bool sigAccept = triggerResultsHandle_->accept(sigTriggerIndex);

  float met = ( pfMetHandle_->at(0) ).pt();
  if (verbose_) cout << "met: " << met << endl;
  bool evtAccept = sigAccept || (met<met_thresh_) ;

  if (verbose_) cout << "event pass " << evtAccept << " trigger " << sigAccept << " met " << met << std::endl;
  if (verbose_) cout << endl;
  return evtAccept;
}
DEFINE_FWK_MODULE(MFVMETTrigFilter);
