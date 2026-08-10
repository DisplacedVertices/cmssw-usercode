#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

class SimPUInfo : public edm::EDAnalyzer {
 public:
  explicit SimPUInfo(const edm::ParameterSet&);
  ~SimPUInfo();
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  struct Ntuple {
    unsigned run;
    unsigned lumi;
    unsigned long long event;
    unsigned short sim_pileup_num_int[3]; // early, in-time, late (sim BX = -1, 0, 1)
    float sim_pileup_true_num_int[3]; // 
  };

  Ntuple* nt;
  TTree* tree;
};

SimPUInfo::SimPUInfo(const edm::ParameterSet& cfg) {
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");

  nt = new Ntuple;
  tree->Branch("run", &nt->run, "run/i");
  tree->Branch("lumi", &nt->lumi, "lumi/i");
  tree->Branch("event", &nt->event);
  tree->Branch("sim_pileup_num_int", nt->sim_pileup_num_int, "sim_pileup_num_int[3]/s");
  tree->Branch("sim_pileup_true_num_int", nt->sim_pileup_true_num_int, "sim_pileup_true_num_int[3]/F");

  tree->SetAlias("sample_name", cfg.getParameter<std::string>("sample_name").c_str());
}

SimPUInfo::~SimPUInfo() {
  delete nt;
}

void SimPUInfo::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  memset(nt, 0, sizeof(Ntuple));
  nt->run = event.id().run();
  nt->lumi = event.id().luminosityBlock();
  nt->event = event.id().event();

  edm::Handle<std::vector<PileupSummaryInfo> > pileup;
  event.getByLabel("addPileupInfo", pileup);
  for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi) {
    const int bx = psi->getBunchCrossing();
    if (bx < -1 || bx > 1)
      throw cms::Exception("SimPUInfo") << "pileup BX not -1, 0, or 1: " << bx << "\n";
    nt->sim_pileup_num_int     [bx+1] = psi->getPU_NumInteractions();
    nt->sim_pileup_true_num_int[bx+1] = psi->getTrueNumInteractions();
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(SimPUInfo);
