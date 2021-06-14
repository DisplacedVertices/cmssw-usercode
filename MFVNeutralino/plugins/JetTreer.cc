#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/MFVNeutralinoFormats/interface/JetVertexAssociation.h"
#include "TLorentzVector.h"
#include "TTree.h"
#include "TH1.h"

struct eventInfo
{
  int evt;
  double weight;
  double met_pt;
  double met_phi;
  int nsv;
  int vtx_ntk;
  double vtx_dBV;
  double vtx_dBVerr;
  double vtx_mass_track;
  double vtx_mass_jet;
  double vtx_mass_trackjet;
  std::vector <float> vtx_tk_pt;
  std::vector <float> vtx_tk_eta;
  std::vector <float> vtx_tk_phi;
  std::vector <float> vtx_tk_dxy;
  std::vector <float> vtx_tk_dxy_err;
  std::vector <float> vtx_tk_nsigmadxy;
  std::vector <float> vtx_tk_dz;
  std::vector <float> vtx_tk_dz_err;
  std::vector <float> vtx_tk_nsigmadz;
  std::vector <double> jet_pt;
  std::vector <double> jet_eta;
  std::vector <double> jet_phi;
  std::vector <double> jet_energy;
  std::vector <double> tk_pt;
  std::vector <double> tk_eta;
  std::vector <double> tk_phi;
  std::vector <double> tk_dxybs;
  std::vector <double> tk_dxybs_sig;
  std::vector <double> tk_dxybs_err;
  std::vector <double> tk_dz;
  std::vector <double> tk_dz_sig;
  std::vector <double> tk_dz_err;
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
    const edm::EDGetTokenT<double> weight_token;
    const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
    const edm::EDGetTokenT<MFVVertexAuxCollection> vertextight_token;
    const edm::EDGetTokenT<MFVVertexAuxCollection> vertexloose_token;
    const edm::EDGetTokenT<MFVVertexAuxCollection> vertexextraloose_token;

    const bool use_vtx_tight;
    const bool use_vtx_othogonal;

    jmt::TrackRescaler track_rescaler;

    TH1F* h_events;
};


MFVJetTreer::MFVJetTreer(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    vertextight_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertextight_src"))),
    vertexloose_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertexloose_src"))),
    vertexextraloose_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertexextraloose_src"))),
    use_vtx_tight(cfg.getParameter<bool>("use_vtx_tight")),         // whether to use vertices passing dBV and dBVerr cut
    use_vtx_othogonal(cfg.getParameter<bool>("use_vtx_othogonal"))  // whether to use vertices othogonal to tight vertices (not passing dBV or not passing dBVerr)
{
  if (!(use_vtx_tight || use_vtx_othogonal))
    throw cms::Exception("MFVJetTreer") << "One and only one of use_vtx_tight and use_vtx_othogonal must be true";

  evInfo = new eventInfo;
}

void MFVJetTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  initEventStructure();
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  int nsv = 0;
  edm::Handle<MFVVertexAuxCollection> auxes;

  if (use_vtx_tight){
    edm::Handle<MFVVertexAuxCollection> auxes_tight;
    event.getByToken(vertextight_token, auxes_tight);

    edm::Handle<MFVVertexAuxCollection> auxes_loose;
    event.getByToken(vertexloose_token, auxes_loose);

    const int nsv_tight = int(auxes_tight->size());
    const int nsv_loose = int(auxes_loose->size());
    if (nsv_tight==0){
      nsv = nsv_loose;
      auxes = auxes_loose;
    }
    else{
      nsv = nsv_tight;
      auxes = auxes_tight;
    }
  }
  else if (use_vtx_othogonal){
    edm::Handle<MFVVertexAuxCollection> auxes_extraloose;
    event.getByToken(vertexextraloose_token, auxes_extraloose);
    auxes = auxes_extraloose;
    for (size_t isv = 0; isv < auxes->size(); ++isv) {
      const MFVVertexAux& aux = auxes->at(isv);
      if ((aux.bs2ddist>=0.01) and (aux.bs2derr<=0.0025) )
        continue;
      ++nsv;
    }
  }

  //if (nsv_tight == 0 && nsv_loose == 0) return;
  if (nsv==0) return;
  if (mevent->met()<150) return;
  //if (mevent->met()<150) return;
  //if (mevent->met()>=150) return;

  int n_evt = event.id().event();
  evInfo->evt = n_evt;
  evInfo->weight = w;
  evInfo->nsv = nsv;

  for (int ij=0; ij<mevent->njets(); ij++){
    evInfo->jet_pt.push_back(mevent->jet_pt[ij]);
    evInfo->jet_eta.push_back(mevent->jet_eta[ij]);
    evInfo->jet_phi.push_back(mevent->jet_phi[ij]);
    evInfo->jet_energy.push_back(mevent->jet_energy[ij]);
  }

  evInfo->met_pt = mevent->met();
  evInfo->met_phi = mevent->metphi();

  double max_ntrack = 0;
  size_t best_SV_idx = -1;

  for (size_t isv = 0; isv < auxes->size(); ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();
    if (use_vtx_othogonal)
      if ((aux.bs2ddist>=0.01) and (aux.bs2derr<=0.0025) )
        continue;
    if (ntracks>max_ntrack){
      max_ntrack = ntracks;
      best_SV_idx = isv;
    }
  }
  h_events->Fill(best_SV_idx);
  const MFVVertexAux& aux = auxes->at(best_SV_idx);
  evInfo->vtx_ntk = aux.ntracks();
  evInfo->vtx_dBV = aux.bs2ddist;
  evInfo->vtx_dBVerr = aux.bs2derr;
  evInfo->vtx_mass_track = aux.mass[mfv::PTracksOnly];
  evInfo->vtx_mass_jet = aux.mass[mfv::PJetsByNtracks];
  evInfo->vtx_mass_trackjet = aux.mass[mfv::PTracksPlusJetsByNtracks];
  evInfo->vtx_tk_pt = aux.track_pts();
  evInfo->vtx_tk_eta = aux.track_eta;
  evInfo->vtx_tk_phi = aux.track_phi;
  evInfo->vtx_tk_dxy = aux.track_dxy;
  evInfo->vtx_tk_dxy_err = aux.track_dxy_errs();
  evInfo->vtx_tk_nsigmadxy = aux.track_dxy_nsigmas();
  evInfo->vtx_tk_dz = aux.track_dz;
  evInfo->vtx_tk_dz_err = aux.track_dz_errs();
  std::vector<float> vtx_tk_dz_sig ({});
  for (int itk=0; itk<aux.ntracks(); ++itk){
    vtx_tk_dz_sig.push_back(aux.track_dz[itk] / aux.track_dz_err(itk) );
  }
  evInfo->vtx_tk_nsigmadz = vtx_tk_dz_sig;

  double bsx = mevent->bsx;
  double bsy = mevent->bsy;
  double bsz = mevent->bsz;
  const math::XYZPoint bs(bsx, bsy, bsz);

  double min_track_pt = 1.0;
  double min_track_nhits = 0;
  double min_track_npxhits = 0;
  double min_track_npxlayers = 2;
  double min_track_nstlayers = 6;
  double min_track_hit_r = 1;
  
  const int track_rescaler_which = jmt::TrackRescaler::w_JetHT; // JMTBAD which rescaling if ever a different one
  track_rescaler.setup(!event.isRealData() && track_rescaler_which != -1,
                       jmt::AnalysisEras::pick(event.id().event()),
                       //jmt::AnalysisEras::pick(event, this),
                       track_rescaler_which);

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i){
    const reco::TrackRef& tk = reco::TrackRef(tracks, i);
    const auto rs = track_rescaler.scale(*tk);

    const double pt = tk->pt();
    const double dxybs = tk->dxy(bs);
    const double rescaled_dxyerr = rs.rescaled_tk.dxyError();
    const double rescaled_sigmadxybs = dxybs / rescaled_dxyerr;
    const double dzbs = tk->dz(bs);
    const double rescaled_dzerr = rs.rescaled_tk.dzError();
    const double rescaled_sigmadzbs = dzbs / rescaled_dzerr;
    const int nhits = tk->hitPattern().numberOfValidHits();
    const int npxhits = tk->hitPattern().numberOfValidPixelHits();
    //const int nsthits = tk->hitPattern().numberOfValidStripHits();
    const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
    int min_r = 2000000000;
    for (int i = 1; i <= 4; ++i)
      if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
        min_r = i;
        break;
      }

    const bool use =
      pt > min_track_pt &&
      nhits >= min_track_nhits &&
      npxhits >= min_track_npxhits &&
      npxlayers >= min_track_npxlayers &&
      nstlayers >= min_track_nstlayers &&
      (min_track_hit_r == 999 || min_r <= min_track_hit_r);

    if (use) {
      evInfo->tk_pt.push_back(pt);
      evInfo->tk_eta.push_back(tk->eta());
      evInfo->tk_phi.push_back(tk->phi());
      evInfo->tk_dxybs.push_back(dxybs);
      evInfo->tk_dxybs_err.push_back(rescaled_dxyerr);
      evInfo->tk_dxybs_sig.push_back(rescaled_sigmadxybs);
      evInfo->tk_dz.push_back(dzbs);
      evInfo->tk_dz_err.push_back(rescaled_dzerr);
      evInfo->tk_dz_sig.push_back(rescaled_sigmadzbs);
    }
  }

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
  eventTree->Branch( "weight",               &evInfo->weight);
  eventTree->Branch( "met_pt",               &evInfo->met_pt);
  eventTree->Branch( "met_phi",              &evInfo->met_phi);
  eventTree->Branch( "nsv",                  &evInfo->nsv);
  eventTree->Branch( "vtx_ntk",              &evInfo->vtx_ntk);
  eventTree->Branch( "vtx_dBV",              &evInfo->vtx_dBV);
  eventTree->Branch( "vtx_dBVerr",           &evInfo->vtx_dBVerr);
  eventTree->Branch( "vtx_mass_track",       &evInfo->vtx_mass_track);
  eventTree->Branch( "vtx_mass_jet",         &evInfo->vtx_mass_jet);
  eventTree->Branch( "vtx_mass_trackjet",    &evInfo->vtx_mass_trackjet);
  eventTree->Branch( "vtx_tk_pt",            &evInfo->vtx_tk_pt);
  eventTree->Branch( "vtx_tk_eta",           &evInfo->vtx_tk_eta);
  eventTree->Branch( "vtx_tk_phi",           &evInfo->vtx_tk_phi);
  eventTree->Branch( "vtx_tk_dxy",           &evInfo->vtx_tk_dxy);
  eventTree->Branch( "vtx_tk_dxy_err",           &evInfo->vtx_tk_dxy_err);
  eventTree->Branch( "vtx_tk_nsigmadxy",     &evInfo->vtx_tk_nsigmadxy);
  eventTree->Branch( "vtx_tk_dz",           &evInfo->vtx_tk_dz);
  eventTree->Branch( "vtx_tk_dz_err",           &evInfo->vtx_tk_dz_err);
  eventTree->Branch( "vtx_tk_nsigmadz",     &evInfo->vtx_tk_nsigmadz);
  eventTree->Branch( "jet_pt",               &evInfo->jet_pt);
  eventTree->Branch( "jet_eta",              &evInfo->jet_eta);
  eventTree->Branch( "jet_phi",              &evInfo->jet_phi);
  eventTree->Branch( "jet_energy",           &evInfo->jet_energy);
  eventTree->Branch( "tk_pt",                &evInfo->tk_pt);
  eventTree->Branch( "tk_eta",               &evInfo->tk_eta);
  eventTree->Branch( "tk_phi",               &evInfo->tk_phi);
  eventTree->Branch( "tk_dxybs",             &evInfo->tk_dxybs);
  eventTree->Branch( "tk_dxybs_sig",         &evInfo->tk_dxybs_sig);
  eventTree->Branch( "tk_dxybs_err",         &evInfo->tk_dxybs_err);
  eventTree->Branch( "tk_dz",                &evInfo->tk_dz);
  eventTree->Branch( "tk_dz_sig",            &evInfo->tk_dz_sig);
  eventTree->Branch( "tk_dz_err",            &evInfo->tk_dz_err);

}

void
MFVJetTreer::endJob()
{
}

void MFVJetTreer::initEventStructure()
{
  evInfo->evt=-1;
  evInfo->weight=-1;
  evInfo->met_pt=-1;
  evInfo->met_phi=-1;
  evInfo->nsv=-1;
  evInfo->vtx_ntk=-1;
  evInfo->vtx_dBV=-1;
  evInfo->vtx_dBVerr=-1;
  evInfo->vtx_mass_track=-1;
  evInfo->vtx_mass_jet=-1;
  evInfo->vtx_mass_trackjet=-1;
  evInfo->vtx_tk_pt.clear();
  evInfo->vtx_tk_eta.clear();
  evInfo->vtx_tk_phi.clear();
  evInfo->vtx_tk_dxy.clear();
  evInfo->vtx_tk_dxy_err.clear();
  evInfo->vtx_tk_nsigmadxy.clear();
  evInfo->vtx_tk_dz.clear();
  evInfo->vtx_tk_dz_err.clear();
  evInfo->vtx_tk_nsigmadz.clear();
  evInfo->jet_pt.clear();
  evInfo->jet_eta.clear();
  evInfo->jet_phi.clear();
  evInfo->jet_energy.clear();
  evInfo->tk_pt.clear();
  evInfo->tk_eta.clear();
  evInfo->tk_phi.clear();
  evInfo->tk_dxybs.clear();
  evInfo->tk_dxybs_sig.clear();
  evInfo->tk_dxybs_err.clear();
  evInfo->tk_dz.clear();
  evInfo->tk_dz_sig.clear();
  evInfo->tk_dz_err.clear();
}
DEFINE_FWK_MODULE(MFVJetTreer);
