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

struct eventInfo
{
  int evt;
  double weight;
  std::vector <int> vtx_ntrack;
  std::vector <double> vtx_dBV;
  std::vector <double> vtx_err_dBV;
  std::vector <double> vtx_x;
  std::vector <double> vtx_y;
  std::vector <double> vtx_z;
  std::vector <double> vtx_px;
  std::vector <double> vtx_py;
  std::vector <double> vtx_pz;
  std::vector <double> vtx_E;
  std::vector <std::vector<float>> vtx_tk_dxy;
  std::vector <std::vector<float>> vtx_tk_dxyerr;
  std::vector <std::vector<float>> vtx_tk_dxynsigma;
  std::vector <double> gen_vtx_x;
  std::vector <double> gen_vtx_y;
  std::vector <double> gen_vtx_z;
  std::vector <double> gen_dBV;
  std::vector <double> gen_pt;
};

class MFVVertexTreer : public edm::EDAnalyzer {
  public:
    explicit MFVVertexTreer(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&);

  private:
    virtual void beginJob() override;
    virtual void endJob() override;
    void initEventStructure();

    TTree *eventTree;
    eventInfo *evInfo;

    const edm::EDGetTokenT<MFVEvent> mevent_token;
    const edm::EDGetTokenT<double> weight_token;
    const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
};


MFVVertexTreer::MFVVertexTreer(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src")))
{
  evInfo = new eventInfo;
}

void MFVVertexTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  evInfo->weight = w;

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_token, auxes);

  const int nsv = int(auxes->size());
  initEventStructure();

  int n_evt = event.id().event();
  evInfo->evt = n_evt;

  size_t lsp_high_pt_idx = mevent->gen_lsp_pt[0]>=mevent->gen_lsp_pt[1]? 0 : 1;
  size_t lsp_low_pt_idx = lsp_high_pt_idx==0? 1 : 0;
  std::vector<size_t> lsp_idx = {lsp_high_pt_idx, lsp_low_pt_idx};
  for (size_t igenv : lsp_idx) {
    double genx = mevent->gen_lsp_decay[igenv*3+0];
    double geny = mevent->gen_lsp_decay[igenv*3+1];
    double genz = mevent->gen_lsp_decay[igenv*3+2];
    double genpt = mevent->gen_lsp_pt[igenv];
    double genbs2ddist = mevent->mag(genx - mevent->bsx_at_z(genz),
                                     geny - mevent->bsy_at_z(genz) 
        );
    evInfo->gen_dBV.push_back(genbs2ddist);
    evInfo->gen_vtx_x.push_back(genx);
    evInfo->gen_vtx_y.push_back(geny);
    evInfo->gen_vtx_z.push_back(genz);
    evInfo->gen_pt.push_back(genpt);
    
  }
  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();
    evInfo->vtx_ntrack.push_back(ntracks);
    evInfo->vtx_x.push_back(aux.x);
    evInfo->vtx_y.push_back(aux.y);
    evInfo->vtx_z.push_back(aux.z);
    evInfo->vtx_dBV.push_back(aux.bs2ddist);
    evInfo->vtx_err_dBV.push_back(aux.bs2derr);
    TLorentzVector p = aux.p4();
    evInfo->vtx_px.push_back(p.Px());
    evInfo->vtx_py.push_back(p.Py());
    evInfo->vtx_pz.push_back(p.Pz());
    evInfo->vtx_E.push_back(p.E());
    evInfo->vtx_tk_dxy.push_back(aux.track_dxy);
    evInfo->vtx_tk_dxyerr.push_back(aux.track_dxy_errs());
    evInfo->vtx_tk_dxynsigma.push_back(aux.track_dxy_nsigmas());
  }



  eventTree->Fill();
}

void
MFVVertexTreer::beginJob()
{
  edm::Service<TFileService> fileService;
  if(!fileService) throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");

  eventTree = fileService->make<TTree>( "tree_DV", "tree_DV" );
  eventTree->Branch( "evt",                  &evInfo->evt);
  eventTree->Branch( "weight",               &evInfo->weight);
  eventTree->Branch( "vtx_ntrack",           &evInfo->vtx_ntrack);
  eventTree->Branch( "vtx_dBV",              &evInfo->vtx_dBV);
  eventTree->Branch( "vtx_err_dBV",          &evInfo->vtx_err_dBV);
  eventTree->Branch( "vtx_x",                &evInfo->vtx_x);
  eventTree->Branch( "vtx_y",                &evInfo->vtx_y);
  eventTree->Branch( "vtx_z",                &evInfo->vtx_z);
  eventTree->Branch( "vtx_px",               &evInfo->vtx_px);
  eventTree->Branch( "vtx_py",               &evInfo->vtx_py);
  eventTree->Branch( "vtx_pz",               &evInfo->vtx_pz);
  eventTree->Branch( "vtx_E",                &evInfo->vtx_E);
  eventTree->Branch( "vtx_tk_dxy",           &evInfo->vtx_tk_dxy);
  eventTree->Branch( "vtx_tk_dxyerr",        &evInfo->vtx_tk_dxyerr);
  eventTree->Branch( "vtx_tk_dxynsigma",     &evInfo->vtx_tk_dxynsigma);
  eventTree->Branch( "gen_vtx_x",            &evInfo->gen_vtx_x);
  eventTree->Branch( "gen_vtx_y",            &evInfo->gen_vtx_y);
  eventTree->Branch( "gen_vtx_z",            &evInfo->gen_vtx_z);
  eventTree->Branch( "gen_dBV",              &evInfo->gen_dBV);
  eventTree->Branch( "gen_pt",               &evInfo->gen_pt);

}

void
MFVVertexTreer::endJob()
{
}

void MFVVertexTreer::initEventStructure()
{
  evInfo->evt=-1;
  evInfo->weight=-1;
  evInfo->vtx_ntrack.clear();
  evInfo->vtx_dBV.clear();
  evInfo->vtx_err_dBV.clear();
  evInfo->vtx_x.clear();
  evInfo->vtx_y.clear();
  evInfo->vtx_z.clear();
  evInfo->vtx_px.clear();
  evInfo->vtx_py.clear();
  evInfo->vtx_pz.clear();
  evInfo->vtx_E.clear();
  evInfo->vtx_tk_dxy.clear();
  evInfo->vtx_tk_dxyerr.clear();
  evInfo->vtx_tk_dxynsigma.clear();
  evInfo->gen_vtx_x.clear();
  evInfo->gen_vtx_y.clear();
  evInfo->gen_vtx_z.clear();
  evInfo->gen_dBV.clear();
  evInfo->gen_pt.clear();
}
DEFINE_FWK_MODULE(MFVVertexTreer);
