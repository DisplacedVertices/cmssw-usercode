#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DVCode/Tools/interface/Utilities.h"

class MFVOverlayVertexHistos : public edm::EDAnalyzer {
 public:
  explicit MFVOverlayVertexHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<std::vector<double>> truth_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;

  const double dz_true_max;
  const int min_ntracks;
  const double found_dist;
  const bool debug;

  TH1F* h_dz_true;

  TH1F* h_dvv_true;
  TH1F* h_dvv_pass_anytwo;
  TH1F* h_dvv_pass_twominntk;
  TH1F* h_dvv_pass_foundv0andv1;
  TH1F* h_dvv_pass_foundv0andv1samentk;
  TH1F* h_dvv_pass_foundv0andv1asmanyntk;
  TH1F* h_dvv_pass_foundv0andv1bytracks;

  TH1F* h_d3d_true;
  TH1F* h_d3d_pass_anytwo;
  TH1F* h_d3d_pass_twominntk;
  TH1F* h_d3d_pass_foundv0andv1;
  TH1F* h_d3d_pass_foundv0andv1samentk;
  TH1F* h_d3d_pass_foundv0andv1asmanyntk;
  TH1F* h_d3d_pass_foundv0andv1bytracks;

  TH1F* h_min_track_vertex_dist[2];
  TH1F* h_min_track_vertex_sig[2];

  struct _track {
    _track() {}
    _track(double x, double y, double z) : px(x), py(y), pz(z), p(mag(x,y,z)) {}
    double dist(const reco::TrackBaseRef& t) { return mag(t->px() - px, t->py() - py, t->pz() - pz); }
    double fracdist(const reco::TrackBaseRef& t) { return dist(t) / p - 1; }
    double px;
    double py;
    double pz;
    double p;
  };
};

MFVOverlayVertexHistos::MFVOverlayVertexHistos(const edm::ParameterSet& cfg)
  : truth_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("truth_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    dz_true_max(cfg.getParameter<double>("dz_true_max")),
    min_ntracks(cfg.getParameter<int>("min_ntracks")),
    found_dist(cfg.getParameter<double>("found_dist")),
    debug(cfg.getParameter<bool>("debug"))
{
  edm::Service<TFileService> fs;

  h_dz_true = fs->make<TH1F>("h_dz_true", "", 100, -0.1, 0.1);

  h_dvv_true                       = fs->make<TH1F>("h_dvv_true",                       "", 4000, 0, 4);
  h_dvv_pass_anytwo                = fs->make<TH1F>("h_dvv_pass_anytwo",                "", 4000, 0, 4);
  h_dvv_pass_twominntk             = fs->make<TH1F>("h_dvv_pass_twominntk",             "", 4000, 0, 4);
  h_dvv_pass_foundv0andv1          = fs->make<TH1F>("h_dvv_pass_foundv0andv1",          "", 4000, 0, 4);
  h_dvv_pass_foundv0andv1samentk   = fs->make<TH1F>("h_dvv_pass_foundv0andv1samentk",   "", 4000, 0, 4);
  h_dvv_pass_foundv0andv1asmanyntk = fs->make<TH1F>("h_dvv_pass_foundv0andv1asmanyntk", "", 4000, 0, 4);
  h_dvv_pass_foundv0andv1bytracks  = fs->make<TH1F>("h_dvv_pass_foundv0andv1bytracks",  "", 4000, 0, 4);

  h_d3d_true                       = fs->make<TH1F>("h_d3d_true",                       "", 4000, 0, 4);
  h_d3d_pass_anytwo                = fs->make<TH1F>("h_d3d_pass_anytwo",                "", 4000, 0, 4);
  h_d3d_pass_twominntk             = fs->make<TH1F>("h_d3d_pass_twominntk",             "", 4000, 0, 4);
  h_d3d_pass_foundv0andv1          = fs->make<TH1F>("h_d3d_pass_foundv0andv1",          "", 4000, 0, 4);
  h_d3d_pass_foundv0andv1samentk   = fs->make<TH1F>("h_d3d_pass_foundv0andv1samentk",   "", 4000, 0, 4);
  h_d3d_pass_foundv0andv1asmanyntk = fs->make<TH1F>("h_d3d_pass_foundv0andv1asmanyntk", "", 4000, 0, 4);
  h_d3d_pass_foundv0andv1bytracks  = fs->make<TH1F>("h_d3d_pass_foundv0andv1bytracks",  "", 4000, 0, 4);

  for (int i = 0; i < 2; ++i) {
    h_min_track_vertex_dist[i] = fs->make<TH1F>(TString::Format("h_min_track_vertex_dist_%i", i), "", 1000, 0, 1);
    h_min_track_vertex_sig[i] = fs->make<TH1F>(TString::Format("h_min_track_vertex_sig_%i", i), "", 1000, 0, 100);
  }
}

void MFVOverlayVertexHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  assert(!event.isRealData()); // JMTBAD lots of reasons this dosen't work on data yet, beamspot is one

  edm::Handle<std::vector<double>> truth;
  event.getByToken(truth_token, truth);

  const int ntk0 = int(truth->at(0));
  const double x0 = truth->at(1);
  const double y0 = truth->at(2);
  const double z0 = truth->at(3);
  const int ntk1 = int(truth->at(4));
  const double x1 = truth->at(5);
  const double y1 = truth->at(6);
  const double z1 = truth->at(7);
  const double x1_0 = truth->at(8); // 1_0 = 1 in 0's "frame"
  const double y1_0 = truth->at(9);
  const double z1_0 = truth->at(10);

  const double min_track_vertex_dist = truth->at(11);
  const double min_track_vertex_sig = truth->at(12);

  const double dvv_true = mag(x0 - x1_0, y0 - y1_0);
  const double d3d_true = mag(x0 - x1_0, y0 - y1_0, z0 - z1_0);
  const double dz_true = z0 - z1_0;
  h_dvv_true->Fill(dvv_true);
  h_d3d_true->Fill(d3d_true);
  h_dz_true->Fill(dz_true);

  if (fabs(dz_true) > dz_true_max)
    return;

  assert(int(truth->size()) - 13 == (ntk0 + ntk1) * 3);

  const int ntks[2] = { ntk0, ntk1 };
  std::vector<_track> tracks[2];
  for (int j = 0; j < 2; ++j) {
    tracks[j].resize(ntks[j]);

    const int offset = 13 + j*3*ntks[0];
    for (int i = 0; i < ntks[j]; ++i)
      tracks[j][i] = _track(truth->at(offset + 3*i), truth->at(offset + 3*i+1), truth->at(offset + 3*i+2));
  }
    
  if (debug) {
    printf("OverlayVertexHistos: truth: ntk0 %i v0 %f, %f, %f ntk1 %i v1 %f, %f, %f v1_0 %f, %f, %f -> dvv_true %f, d3d_true %f | min tk-v dist %f sig %f\n",
           ntk0, x0, y0, z0, ntk1, x1, y1, z1, x1_0, y1_0, z1_0, dvv_true, d3d_true, min_track_vertex_dist, min_track_vertex_sig);
    for (int j = 0; j < 2; ++j)
      for (int i = 0; i < ntks[j]; ++i)
        printf("v%i tk%i  %f, %f, %f  p = %f\n", j, i, tracks[j][i].px, tracks[j][i].py, tracks[j][i].pz, tracks[j][i].p);
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const double bsx = beamspot->x0();
  const double bsy = beamspot->y0();
  const double bsz = beamspot->z0();
  const double bsdxdz = beamspot->dxdz();
  const double bsdydz = beamspot->dydz();

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);

  int nvtx = int(vertices->size());
  if (debug) printf("%i reco vertices:\n", nvtx);

  int nvtx_minntk = 0;
  bool found[2] = {0};
  int found_ntk[2] = {0};
  int found_by_tracks[2] = {-1,-1};

  for (int iv = 0; iv < nvtx; ++iv) {
    const reco::Vertex& v = vertices->at(iv);
    const int ntk = v.tracksSize();

    if (ntk >= min_ntracks)
      ++nvtx_minntk;

    const double vx = v.x() - (bsx + bsdxdz * (v.z() - bsz));
    const double vy = v.y() - (bsy + bsdydz * (v.z() - bsz));
    const double vz = v.z() - bsz;

    const double d0   = mag(vx - x0,   vy - y0,   vz - z0);
    const double d1_0 = mag(vx - x1_0, vy - y1_0, vz - z1_0);
    
    bool this_found[2] = {0};

    if (d0 < found_dist) {
      this_found[0] = found[0] = true;
      found_ntk[0] = ntk;
    }

    if (d1_0 < found_dist) {
      this_found[1] = found[1] = true;
      found_ntk[1] = ntk;
    }

    if (debug) printf("vertex at %f, %f, %f with %i tracks:  d0 %f -> found0? %i  d1_0 %f -> found1? %i \n",
                      v.x(), v.y(), v.z(), ntk, d0, this_found[0], d1_0, this_found[1]);

    for (int j = 0; j < 2; ++j) {
      if (ntk >= ntks[j]) {
        std::vector<bool> track_found(ntks[j], false);
        for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
          if (debug) printf("reco track %f, %f, %f p %f\n", (*it)->px(), (*it)->py(), (*it)->pz(), (*it)->p());
          for (int i = 0; i < ntks[j]; ++i) {
            const double dist = tracks[j][i].dist(*it);
            if (debug) printf("truth v%i track %i  %f, %f, %f, p %f  dist %f\n", j, i, tracks[j][i].px, tracks[j][i].py, tracks[j][i].pz, tracks[j][i].p, dist);

            if (dist < 0.01) {
              if (debug) printf("  found!\n");
              track_found[i] = true;
            }
          }
        }

        if (std::all_of(track_found.begin(), track_found.end(), [](bool v) { return v; }))
          found_by_tracks[j] = iv;

        if (debug) {
          printf("found decisions for truth v%i: ", j);
          for (int i = 0; i < ntks[j]; ++i)
            printf("tk%i? %i  ", i, int(track_found[i]));
          printf("overall: %i\n", found_by_tracks[j]);
        }
      }
    }
  } 

  if (debug) printf("decisions:\n");

  auto fillit = [&](double v, TH1F* h, bool cond) {
    if (debug) printf("%s: %i\n", h->GetName(), cond);
    if (cond) h->Fill(v);
  };

  const bool pass_anytwo                = nvtx >= 2;
  const bool pass_twominntk             = nvtx >= 2 && nvtx_minntk >= 2;
  const bool pass_foundv0andv1          = nvtx >= 2 && found[0] && found[1];
  const bool pass_foundv0andv1samentk   = nvtx >= 2 && found[0] && found[1] && found_ntk[0] == ntk0 && found_ntk[1] == ntk1;
  const bool pass_foundv0andv1asmanyntk = nvtx >= 2 && found[0] && found[1] && found_ntk[0] >= ntk0 && found_ntk[1] >= ntk1;
  const bool pass_foundv0andv1bytracks  = nvtx >= 2 && found_by_tracks[0] != -1 && found_by_tracks[1] != -1 && found_by_tracks[0] != found_by_tracks[1];

  fillit(dvv_true, h_dvv_pass_anytwo,                 pass_anytwo);
  fillit(dvv_true, h_dvv_pass_twominntk,              pass_twominntk);
  fillit(dvv_true, h_dvv_pass_foundv0andv1,           pass_foundv0andv1);
  fillit(dvv_true, h_dvv_pass_foundv0andv1samentk,    pass_foundv0andv1samentk);
  fillit(dvv_true, h_dvv_pass_foundv0andv1asmanyntk,  pass_foundv0andv1asmanyntk);
  fillit(dvv_true, h_dvv_pass_foundv0andv1bytracks,   pass_foundv0andv1bytracks);

  fillit(d3d_true, h_d3d_pass_anytwo,                 pass_anytwo);
  fillit(d3d_true, h_d3d_pass_twominntk,              pass_twominntk);
  fillit(d3d_true, h_d3d_pass_foundv0andv1,           pass_foundv0andv1);
  fillit(d3d_true, h_d3d_pass_foundv0andv1samentk,    pass_foundv0andv1samentk);
  fillit(d3d_true, h_d3d_pass_foundv0andv1asmanyntk,  pass_foundv0andv1asmanyntk);
  fillit(d3d_true, h_d3d_pass_foundv0andv1bytracks,   pass_foundv0andv1bytracks);

  if (dvv_true > 0.1) {
    h_min_track_vertex_dist[pass_foundv0andv1bytracks]->Fill(min_track_vertex_dist);
    h_min_track_vertex_sig [pass_foundv0andv1bytracks]->Fill(min_track_vertex_sig);
  }
}

DEFINE_FWK_MODULE(MFVOverlayVertexHistos);
