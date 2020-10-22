#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "DataFormats/Common/interface/ValueMap.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"

#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "TH1.h"

class TriggerEffStudy_StandAlone : public edm::EDAnalyzer {
  public:
    explicit TriggerEffStudy_StandAlone(const edm::ParameterSet&);
    ~TriggerEffStudy_StandAlone();

    virtual void beginJob() override;
    virtual void beginRun(edm::Run const &, edm::EventSetup const&) override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    bool analyzeTrig(const edm::Event&, std::string);
    void trigAvaliabilityCheck(std::string);
  private:
  
    std::string   processName_;
    std::string   triggerMETName_;
    std::string   triggerMETnoMuName_;
    std::string   triggerPFHTName_;
    //std::string   refTriggerName_;
    //istd::string   sigTriggerName_;
    edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
    edm::Handle<edm::TriggerResults>           triggerResultsHandle_;
    //edm::EDGetTokenT<edm::View<pat::MET> > pfMetToken_;
    bool verbose_;
  
    HLTConfigProvider hltConfig_;
  
    TH1F* h_trig_cutflow_;
};

TriggerEffStudy_StandAlone::TriggerEffStudy_StandAlone(const edm::ParameterSet& iConfig)
  :
    processName_(iConfig.getUntrackedParameter<std::string>("processName")),
    triggerMETName_(iConfig.getUntrackedParameter<std::string>("triggerMETTag")),
    triggerMETnoMuName_(iConfig.getUntrackedParameter<std::string>("triggerMETnoMuTag")),
    triggerPFHTName_(iConfig.getUntrackedParameter<std::string>("triggerPFHTTag")),
    triggerResultsToken_(consumes<edm::TriggerResults>(iConfig.getUntrackedParameter<edm::InputTag>("triggerTag"))),
    verbose_(iConfig.getUntrackedParameter<bool>("verbose"))
{}

void TriggerEffStudy_StandAlone::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // load Trigger paths
  iEvent.getByToken(triggerResultsToken_, triggerResultsHandle_);

  h_trig_cutflow_->Fill("all", 1);

  if (!triggerResultsHandle_.isValid()) {
    std::cout << "****Error in getting TriggerResults product from Event!" << std::endl;
    return;
  }
  if (analyzeTrig(iEvent, triggerPFHTName_)){
    h_trig_cutflow_->Fill("PFHT", 1);
    if(verbose_){
      std::cout << "event pass PFHT trigger!" << std::endl;
    }
  }

  if (analyzeTrig(iEvent, triggerMETName_)){
    h_trig_cutflow_->Fill("MET", 1);
    if(verbose_){
      std::cout << "event pass MET trigger!" << std::endl;
    }
  }

  if (analyzeTrig(iEvent, triggerMETnoMuName_)){
    h_trig_cutflow_->Fill("METnoMu", 1);
    if(verbose_){
      std::cout << "event pass METnoMu trigger!" << std::endl;
    }
  }
}

bool TriggerEffStudy_StandAlone::analyzeTrig(const edm::Event& iEvent, std::string trigName){
  assert(triggerResultsHandle_->size()==hltConfig_.size());
  const unsigned int ntrigs(hltConfig_.size());
  const unsigned int trigIdx(hltConfig_.triggerIndex(trigName));
  assert(trigIdx==iEvent.triggerNames(*triggerResultsHandle_).triggerIndex(trigName));
  if(trigIdx>=ntrigs){
    std::cout << "Trigger path: " << trigName << " not available! " << std::endl;
  }
  bool accept = triggerResultsHandle_->accept(trigIdx);
  return accept;

}

TriggerEffStudy_StandAlone::~TriggerEffStudy_StandAlone()
{
}

void TriggerEffStudy_StandAlone::beginJob(){
  edm::Service<TFileService> fileService;
  if(!fileService) throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");

  h_trig_cutflow_ = fileService->make<TH1F>("h_trig_cutflow","h_trig_cutflow",10,0,10);
}

void TriggerEffStudy_StandAlone::trigAvaliabilityCheck(std::string triggerName){
  const unsigned int n(hltConfig_.size());
  unsigned int triggerIdx(hltConfig_.triggerIndex(triggerName));
  if (triggerIdx>=n) {
    std::cout << "TriggerName: " << triggerName << " not available in config!" << std::endl;
  }

}

void TriggerEffStudy_StandAlone::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
  bool changed(true);
  if(hltConfig_.init(iRun, iSetup, processName_, changed)){
    if(changed) {
      trigAvaliabilityCheck(triggerPFHTName_);
      trigAvaliabilityCheck(triggerMETName_);
      trigAvaliabilityCheck(triggerMETnoMuName_);

      //const unsigned int n(hltConfig_.size());
      //unsigned int triggerIdx(hltConfig_.triggerIndex(trigName_));
      //if (triggerIdx>=n) {
      //  std::cout << "TriggerName: " << triggerName_ << " not available in config!" << std::endl;
      //}
    }
  }
  else {
    std::cout << "Warning, didn't find trigger process HLT,\t" << processName_ << std::endl;
  }
}


DEFINE_FWK_MODULE(TriggerEffStudy_StandAlone);
