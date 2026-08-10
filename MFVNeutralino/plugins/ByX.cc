#include "TH1.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ByRunTH1.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVByX : public edm::EDAnalyzer {
 public:
  explicit MFVByX(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> event_token;
  const bool use_vertices;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  const bool by_run;
  const bool by_npu;

  ByRunTH1<TH1F> h_n_vertex_seed_tracks[2];
  ByRunTH1<TH1F> h_vertex_seed_track_chi2dof[2];
  ByRunTH1<TH1F> h_vertex_seed_track_q[2];
  ByRunTH1<TH1F> h_vertex_seed_track_pt[2];
  ByRunTH1<TH1F> h_vertex_seed_track_eta[2];
  ByRunTH1<TH1F> h_vertex_seed_track_phi[2];
  ByRunTH1<TH1F> h_vertex_seed_track_dxy[2];
  ByRunTH1<TH1F> h_vertex_seed_track_dz[2];
  ByRunTH1<TH1F> h_vertex_seed_track_adxy[2];
  ByRunTH1<TH1F> h_vertex_seed_track_adz[2];
  ByRunTH1<TH1F> h_vertex_seed_track_npxhits[2];
  ByRunTH1<TH1F> h_vertex_seed_track_nsthits[2];
  ByRunTH1<TH1F> h_vertex_seed_track_nhits[2];
  ByRunTH1<TH1F> h_vertex_seed_track_npxlayers[2];
  ByRunTH1<TH1F> h_vertex_seed_track_nstlayers[2];
  ByRunTH1<TH1F> h_vertex_seed_track_nlayers[2];

  ByRunTH1<TH1F> h_njets[2];
  static const int MAX_NJETS = 6;
  ByRunTH1<TH1F> h_jetpt[MAX_NJETS][2];
  ByRunTH1<TH1F> h_ht40[2];

  ByRunTH1<TH1F> h_trig[2];
  ByRunTH1<TH1F> h_ananjets[2];
  ByRunTH1<TH1F> h_anaht[2];
  ByRunTH1<TH1F> h_ana[2];

  ByRunTH1<TH1F> h_vertex_x[2];
  ByRunTH1<TH1F> h_vertex_y[2];
  ByRunTH1<TH1F> h_vertex_dbv[2];
  ByRunTH1<TH1F> h_vertex_bs2derr[2];
};

MFVByX::MFVByX(const edm::ParameterSet& cfg)
  : event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    use_vertices(cfg.getParameter<edm::InputTag>("vertex_src").label() != ""),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    by_run(cfg.existsAs<bool>("by_run") && cfg.getParameter<bool>("by_run")),
    by_npu(cfg.existsAs<bool>("by_npu") && cfg.getParameter<bool>("by_npu"))
{
  if (by_run + by_npu != 1)
    throw cms::Exception("exactly one of the by_ parameters must be 1");

  edm::Service<TFileService> fs;

  for (int i = 0; i < 2; ++i) {
    if (!use_vertices && i == 1)
      break;
    h_n_vertex_seed_tracks[i].set(&fs, TString::Format("h_n_vertex_seed_tracks_%i", i), ";# vertex seed tracks;events", 100, 0, 100);
    h_vertex_seed_track_chi2dof[i].set(&fs, TString::Format("h_vertex_seed_track_chi2dof_%i", i), ";vertex seed track #chi^{2}/dof;tracks/0.1", 100, 0, 10);
    h_vertex_seed_track_q[i].set(&fs, TString::Format("h_vertex_seed_track_q_%i", i), ";vertex seed track charge;tracks", 3, -1, 2);
    h_vertex_seed_track_pt[i].set(&fs, TString::Format("h_vertex_seed_track_pt_%i", i), ";vertex seed track p_{T} (GeV);tracks/GeV", 300, 0, 300);
    h_vertex_seed_track_eta[i].set(&fs, TString::Format("h_vertex_seed_track_eta_%i", i), ";vertex seed track #eta;tracks/0.026", 200, -2.6, 2.6);
    h_vertex_seed_track_phi[i].set(&fs, TString::Format("h_vertex_seed_track_phi_%i", i), ";vertex seed track #phi;tracks/0.032", 200, -3.15, 3.15);
    h_vertex_seed_track_dxy[i].set(&fs, TString::Format("h_vertex_seed_track_dxy_%i", i), ";vertex seed track dxy (cm);tracks/10 #mum", 2000, -1, 1);
    h_vertex_seed_track_dz[i].set(&fs, TString::Format("h_vertex_seed_track_dz_%i", i), ";vertex seed track dz (cm);tracks/10 #mum", 2000, -1, 1);
    h_vertex_seed_track_adxy[i].set(&fs, TString::Format("h_vertex_seed_track_adxy_%i", i), ";vertex seed track |dxy| (cm);tracks/10 #mum", 1000, 0, 1);
    h_vertex_seed_track_adz[i].set(&fs, TString::Format("h_vertex_seed_track_adz_%i", i), ";vertex seed track |dz| (cm);tracks/10 #mum", 1000, 0, 1);
    h_vertex_seed_track_npxhits[i].set(&fs, TString::Format("h_vertex_seed_track_npxhits_%i", i), ";vertex seed track # pixel hits;tracks", 10, 0, 10);
    h_vertex_seed_track_nsthits[i].set(&fs, TString::Format("h_vertex_seed_track_nsthits_%i", i), ";vertex seed track # strip hits;tracks", 50, 0, 50);
    h_vertex_seed_track_nhits[i].set(&fs, TString::Format("h_vertex_seed_track_nhits_%i", i), ";vertex seed track # hits;tracks", 60, 0, 60);
    h_vertex_seed_track_npxlayers[i].set(&fs, TString::Format("h_vertex_seed_track_npxlayers_%i", i), ";vertex seed track # pixel layers;tracks", 10, 0, 10);
    h_vertex_seed_track_nstlayers[i].set(&fs, TString::Format("h_vertex_seed_track_nstlayers_%i", i), ";vertex seed track # strip layers;tracks", 20, 0, 20);
    h_vertex_seed_track_nlayers[i].set(&fs, TString::Format("h_vertex_seed_track_nlayers_%i", i), ";vertex seed track # layers;tracks", 30, 0, 30);

    h_njets[i].set(&fs, TString::Format("h_njets_%i", i), ";number of jets;events", 30, 0, 30);
    for (int j = 0; j < MAX_NJETS; ++j)
      h_jetpt[j][i].set(&fs, TString::Format("h_jetpt%i_%i", j, i), TString::Format(";jet #%i p_{T} (GeV);events/10 GeV", j), 200, 0, 2000);
    h_ht40[i].set(&fs, TString::Format("h_ht40_%i", i), ";jet 40 H_{T} (GeV);events/50 GeV", 200, 0, 10000);

    h_trig[i].set(&fs, TString::Format("h_trig_%i", i), "", 1, 0, 1);
    h_ananjets[i].set(&fs, TString::Format("h_ananjets_%i", i), "", 2, 0, 2);
    h_anaht[i].set(&fs, TString::Format("h_anaht_%i", i), "", 2, 0, 2);
    h_ana[i].set(&fs, TString::Format("h_ana_%i", i), "", 2, 0, 2);
  }

  if (use_vertices) {
    h_vertex_x[1].set(&fs, "h_vertex_x_1", ";vertex x (cm);events/10 #mum", 2000, -1, 1);
    h_vertex_y[1].set(&fs, "h_vertex_y_1", ";vertex y (cm);events/10 #mum", 2000, -1, 1);
    h_vertex_dbv[1].set(&fs, "h_vertex_dbv_1", ";vertex d_{BV} (cm);events/10 #mum", 2500, 0, 2.5);
    h_vertex_bs2derr[1].set(&fs, "h_vertex_bs2derr_1", ";#sigma(vertex d_{BV}) (cm);events/0.25 #mum", 100, 0, 0.0025);
  }
}

void MFVByX::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  const unsigned by =
      by_run ? event.id().run() 
    : by_npu ? unsigned(mevent->npu)
    : 1;

  edm::Handle<MFVVertexAuxCollection> vertices;
  size_t nsv = 0;
  if (use_vertices) {
    event.getByToken(vertex_token, vertices);
    nsv = vertices->size();
    if (nsv >= 2)
      return;
  }

  h_njets[nsv][by]->Fill(mevent->njets());
  for (int i = 0; i < MAX_NJETS; ++i)
    h_jetpt[i][nsv][by]->Fill(mevent->nth_jet_pt(i));
  h_ht40[nsv][by]->Fill(mevent->jet_ht(40));

  h_trig[nsv][by]->Fill(0);
  h_ananjets[nsv][by]->Fill(mevent->njets() >= 4);
  h_anaht[nsv][by]->Fill(mevent->jet_ht(40) >= 1200);
  h_ana[nsv][by]->Fill(mevent->njets() >= 4 && mevent->jet_ht(40) >= 1200);

  const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();
  h_n_vertex_seed_tracks[nsv][by]->Fill(n_vertex_seed_tracks);
  for (size_t i = 0; i < n_vertex_seed_tracks; ++i) {
    h_vertex_seed_track_chi2dof  [nsv][by]->Fill(mevent->vertex_seed_track_chi2dof[i]);
    h_vertex_seed_track_q        [nsv][by]->Fill(mevent->vertex_seed_track_q(i));
    h_vertex_seed_track_pt       [nsv][by]->Fill(mevent->vertex_seed_track_pt(i));
    h_vertex_seed_track_eta      [nsv][by]->Fill(mevent->vertex_seed_track_eta[i]);
    h_vertex_seed_track_phi      [nsv][by]->Fill(mevent->vertex_seed_track_phi[i]);
    h_vertex_seed_track_dxy      [nsv][by]->Fill(mevent->vertex_seed_track_dxy[i]);
    h_vertex_seed_track_dz       [nsv][by]->Fill(mevent->vertex_seed_track_dz[i]);
    h_vertex_seed_track_adxy     [nsv][by]->Fill(fabs(mevent->vertex_seed_track_dxy[i]));
    h_vertex_seed_track_adz      [nsv][by]->Fill(fabs(mevent->vertex_seed_track_dz[i]));
    h_vertex_seed_track_npxhits  [nsv][by]->Fill(mevent->vertex_seed_track_npxhits(i));
    h_vertex_seed_track_nsthits  [nsv][by]->Fill(mevent->vertex_seed_track_nsthits(i));
    h_vertex_seed_track_nhits    [nsv][by]->Fill(mevent->vertex_seed_track_nhits(i));
    h_vertex_seed_track_npxlayers[nsv][by]->Fill(mevent->vertex_seed_track_npxlayers(i));
    h_vertex_seed_track_nstlayers[nsv][by]->Fill(mevent->vertex_seed_track_nstlayers(i));
    h_vertex_seed_track_nlayers  [nsv][by]->Fill(mevent->vertex_seed_track_nlayers(i));
  }

  if (use_vertices && nsv == 1) {
    const MFVVertexAux& v = vertices->at(0);
    h_vertex_x[1][by]->Fill(v.x - mevent->bsx_at_z(v.z));
    h_vertex_y[1][by]->Fill(v.y - mevent->bsy_at_z(v.z));
    h_vertex_dbv[1][by]->Fill(mevent->bs2ddist(v));
    h_vertex_bs2derr[1][by]->Fill(v.bs2derr);
  }
}

DEFINE_FWK_MODULE(MFVByX);
