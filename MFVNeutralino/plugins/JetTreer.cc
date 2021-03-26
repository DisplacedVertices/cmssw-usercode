#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "TLorentzVector.h"
#include "TTree.h"
#include "TH1.h"

struct eventInfo
{
  int evt;
  int max_SV_ntracks;
  double weight;
  double met_pt;
  double met_phi;
  std::vector <double> jet_pt;
  std::vector <double> jet_eta;
  std::vector <double> jet_phi;
  std::vector <double> jet_energy;
};

class MFVJetTreer : public edm::EDAnalyzer {
  public:
    explicit MFVJetTreer(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&);

  private:
    virtual void beginJob() override;
    virtual void endJob() override;
    void initEventStructure();

    TTree *eventTree;
    eventInfo *evInfo;

    const edm::EDGetTokenT<MFVEvent> mevent_token;
    const edm::EDGetTokenT<MFVVertexAuxCollection> vertextight_token;
    const edm::EDGetTokenT<MFVVertexAuxCollection> vertexloose_token;

    TH1F* h_events;
};


MFVJetTreer::MFVJetTreer(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertextight_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertextight_src"))),
    vertexloose_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertexloose_src")))
{
  evInfo = new eventInfo;
}

void MFVJetTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  initEventStructure();
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<MFVVertexAuxCollection> auxes_tight;
  event.getByToken(vertextight_token, auxes_tight);

  edm::Handle<MFVVertexAuxCollection> auxes_loose;
  event.getByToken(vertexloose_token, auxes_loose);

  const int nsv_tight = int(auxes_tight->size());
  const int nsv_loose = int(auxes_loose->size());
  int nsv = 0;
  edm::Handle<MFVVertexAuxCollection> auxes;
  if (nsv_tight==0){
    nsv = nsv_loose;
    auxes = auxes_loose;
  }
  else{
    nsv = nsv_tight;
    auxes = auxes_tight;
  }

  //if (nsv_tight == 0 && nsv_loose == 0) return;
  h_events->Fill(1);

  int n_evt = event.id().event();
  evInfo->evt = n_evt;

  double max_ntrack = 0;
  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();
    if (ntracks>max_ntrack){
      max_ntrack = ntracks;
    }
  }
  evInfo->max_SV_ntracks = max_ntrack;

  for (int ij=0; ij<mevent->njets(); ij++){
    evInfo->jet_pt.push_back(mevent->jet_pt[ij]);
    evInfo->jet_eta.push_back(mevent->jet_eta[ij]);
    evInfo->jet_phi.push_back(mevent->jet_phi[ij]);
    evInfo->jet_energy.push_back(mevent->jet_energy[ij]);
  }

  evInfo->met_pt = mevent->met();
  evInfo->met_phi = mevent->metphi();
  eventTree->Fill();
}

void
MFVJetTreer::beginJob()
{
  edm::Service<TFileService> fileService;
  if(!fileService) throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");

  h_events = fileService->make<TH1F>("n_events", "n_events", 10, 0 ,10);
  eventTree = fileService->make<TTree>( "tree_DV", "tree_DV" );
  eventTree->Branch( "evt",                  &evInfo->evt);
  eventTree->Branch( "max_SV_ntracks",       &evInfo->max_SV_ntracks);
  eventTree->Branch( "met_pt",               &evInfo->met_pt);
  eventTree->Branch( "met_phi",              &evInfo->met_phi);
  eventTree->Branch( "jet_pt",               &evInfo->jet_pt);
  eventTree->Branch( "jet_eta",              &evInfo->jet_eta);
  eventTree->Branch( "jet_phi",              &evInfo->jet_phi);
  eventTree->Branch( "jet_energy",           &evInfo->jet_energy);

}

void
MFVJetTreer::endJob()
{
}

void MFVJetTreer::initEventStructure()
{
  evInfo->evt=-1;
  evInfo->max_SV_ntracks=-1;
  evInfo->met_pt=-1;
  evInfo->met_phi=-1;
  evInfo->jet_pt.clear();
  evInfo->jet_eta.clear();
  evInfo->jet_phi.clear();
  evInfo->jet_energy.clear();
}
DEFINE_FWK_MODULE(MFVJetTreer);
