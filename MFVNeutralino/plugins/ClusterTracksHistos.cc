#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DVCode/MFVNeutralino/interface/VertexTrackClusters.h"
#include "DVCode/MFVNeutralinoFormats/interface/Event.h"
#include "DVCode/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVClusterTracksHistos : public edm::EDAnalyzer {
 public:
  explicit MFVClusterTracksHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  const double min_dbv;

  TH1F* h_w;
  TH1F* h_nsv;
  TH1F* h_ntracks;
  TH1F* h_dbv;

  TH1F* h_nclusters;
  TH2F* h_nclusters_v_ntk;
  TH1F* h_nsingleclusters;
  TH2F* h_nsingleclusters_v_ntk;
  TH1F* h_fsingleclusters;
  TH2F* h_fsingleclusters_v_ntk;
  TH1F* h_avgnconstituents;
  TH2F* h_avgnconstituents_v_ntk;
  TH1F* h_nconstle2clusters;
  TH2F* h_nconstle2clusters_v_ntk;
  TH1F* h_singleclustersdotfd;
  TH1F* h_nsingleclusterspb;
  TH2F* h_nsingleclusterspb_v_ntk;
};

MFVClusterTracksHistos::MFVClusterTracksHistos(const edm::ParameterSet& cfg)
  : event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    min_dbv(cfg.getParameter<double>("min_dbv"))
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices;arb. units", 5, 0, 5);
  h_ntracks = fs->make<TH1F>("h_ntracks", ";# of tracks;arb. units", 20, 0, 20);
  h_dbv = fs->make<TH1F>("h_dbv", ";d_{BV} (cm);arb. units", 100, 0, 0.1);

  h_nclusters               = fs->make<TH1F>("h_nclusters",                ";# clusters",                                                  20, 0, 20);
  h_nclusters_v_ntk         = fs->make<TH2F>("h_nclusters_v_ntk",          ";# tracks;# clusters",                                         20, 0, 20, 20, 0, 20);
  h_nsingleclusters         = fs->make<TH1F>("h_nsingleclusters",          ";# clusters w. 1 constituent",                                 20, 0, 20);
  h_nsingleclusters_v_ntk   = fs->make<TH2F>("h_nsingleclusters_v_ntk",    ";# tracks;# clusters w. 1 constituent",                        20, 0, 20, 20, 0, 20);
  h_fsingleclusters         = fs->make<TH1F>("h_fsingleclusters",          ";frac. clusters w. 1 constituent",                             21, 0,  1.05);
  h_fsingleclusters_v_ntk   = fs->make<TH2F>("h_fsingleclusters_v_ntk",    ";# tracks;frac. clusters w. 1 constituent",                    20, 0, 20, 21, 0,  1.05);
  h_avgnconstituents        = fs->make<TH1F>("h_avgnconstituents",         ";avg # constituents / cluster",                                20, 0, 20);
  h_avgnconstituents_v_ntk  = fs->make<TH2F>("h_avgnconstituents_v_ntk",   ";# tracks;avg # constituents / cluster",                       20, 0, 20, 20, 0, 20);
  h_nconstle2clusters       = fs->make<TH1F>("h_nconstle2clusters",        ";# clusters w. <= 2 constituents",                             20, 0, 20);
  h_nconstle2clusters_v_ntk = fs->make<TH2F>("h_nconstle2clusters_v_ntk",  ";# tracks;# clusters w. <= 2 constituents",                    20, 0, 20, 20, 0, 20);
  h_nsingleclusterspb       = fs->make<TH1F>("h_nsingleclusterspb",        ";# clusters w. 1 constituent that point back",                 20, 0, 20);
  h_nsingleclusterspb_v_ntk = fs->make<TH2F>("h_nsingleclusterspb_v_ntk",  ";# tracks;# clusters w. 1 constituent that point back",        20, 0, 20, 20, 0, 20);

  h_singleclustersdotfd = fs->make<TH1F>("h_singleclustersdotfd", ";clusters w. 1 constituent dot flight dir", 41, -1, 1.05);
}

void MFVClusterTracksHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertex_token, vertices);
  const int nsv = int(vertices->size());
  h_nsv->Fill(nsv, w);

  for (int ivtx = 0; ivtx < nsv; ++ivtx) {
    const MFVVertexAux& v = vertices->at(ivtx);
    const TVector2 flight_dir = TVector2(v.x - mevent->bsx, v.y - mevent->bsy).Unit();

    const size_t ntracks = v.ntracks();
    const double dbv = mevent->bs2ddist(v);
    h_ntracks->Fill(ntracks, w);
    h_dbv->Fill(dbv, w);

    if (dbv > min_dbv) {
      const mfv::track_clusters clusters(v);
      const size_t nclusters = clusters.size();
      const size_t nsingle = clusters.nsingle();
      const size_t nconstle2 = nsingle + clusters.ndouble();
      const double avgnconst = clusters.avgnconst();

      size_t nsinglepb = 0;
      for (const mfv::track_cluster& c : clusters) {
        if (c.size() == 1) {
          for (size_t ti : c.tracks) {
            const TVector2 track_dir = TVector2(v.track_px[ti], v.track_py[ti]).Unit();
            const double dot = track_dir * flight_dir;
            h_singleclustersdotfd->Fill(dot);
            if (dot < -0.5)
              ++nsinglepb;
          }
        }
      }

      h_nclusters->Fill(nclusters, w);
      h_nclusters_v_ntk->Fill(ntracks, nclusters, w);
      h_nsingleclusters->Fill(nsingle, w);
      h_nsingleclusters_v_ntk->Fill(ntracks, nsingle, w);
      h_fsingleclusters->Fill(nsingle / double(nclusters), w);
      h_fsingleclusters_v_ntk->Fill(ntracks, nsingle / double(nclusters), w);
      h_avgnconstituents->Fill(avgnconst, w);
      h_avgnconstituents_v_ntk->Fill(ntracks, avgnconst, w);
      h_nconstle2clusters->Fill(nconstle2, w);
      h_nconstle2clusters_v_ntk->Fill(ntracks, nconstle2, w);
      h_nsingleclusterspb->Fill(nsinglepb, w);
      h_nsingleclusterspb_v_ntk->Fill(ntracks, nsinglepb, w);
    }
  }
}

DEFINE_FWK_MODULE(MFVClusterTracksHistos);
