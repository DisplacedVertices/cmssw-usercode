#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVRefitDistance : public edm::EDAnalyzer {
 public:
  explicit MFVRefitDistance(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  const bool require_genmatch;

  TH1D* h_genvalid;
  TH1D* h_nsv;
  TH1D* h_nsvmatch;
  TH1D* h_nrefitbad;
  TH1D* h_dist3;
  TH1D* h_dist2;
  TH1D* h_distz;
  TH1D* h_maxdist3;
  TH1D* h_maxdist2;
  TH1D* h_maxdistz;
  TH2F* h_maxdist3_v_dbv;
  TH2F* h_maxdist2_v_dbv;
  TH2F* h_maxdistz_v_dbv;
  TH2F* h_maxdist3_v_bs2derr;
  TH2F* h_maxdist2_v_bs2derr;
  TH2F* h_maxdistz_v_bs2derr;
};

MFVRefitDistance::MFVRefitDistance(const edm::ParameterSet& cfg)
  : weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    require_genmatch(cfg.getParameter<bool>("require_genmatch"))
{
  edm::Service<TFileService> fs;
  h_genvalid = fs->make<TH1D>("h_genvalid", "", 2, 0, 2);
  h_nsv = fs->make<TH1D>("h_nsv", "", 10,0,10);
  h_nsvmatch = fs->make<TH1D>("h_nsvmatch", "", 10,0,10);
  h_nrefitbad = fs->make<TH1D>("h_nrefitbad", "", 10,0,10);
  h_dist3 = fs->make<TH1D>("h_dist3", "", 1000, 0, 1);
  h_dist2 = fs->make<TH1D>("h_dist2", "", 1000, 0, 1);
  h_distz = fs->make<TH1D>("h_distz", "", 1000, 0, 1);
  h_maxdist3 = fs->make<TH1D>("h_maxdist3", "", 1000, 0, 1);
  h_maxdist2 = fs->make<TH1D>("h_maxdist2", "", 1000, 0, 1);
  h_maxdistz = fs->make<TH1D>("h_maxdistz", "", 1000, 0, 1);
  h_maxdist3_v_dbv = fs->make<TH2F>("h_maxdist3_v_dbv", "", 100, 0, 2.5, 100, 0, 0.1);
  h_maxdist2_v_dbv = fs->make<TH2F>("h_maxdist2_v_dbv", "", 100, 0, 2.5, 100, 0, 0.1);
  h_maxdistz_v_dbv = fs->make<TH2F>("h_maxdistz_v_dbv", "", 100, 0, 2.5, 100, 0, 0.1);
  h_maxdist3_v_bs2derr = fs->make<TH2F>("h_maxdist3_v_bs2derr", "", 100, 0, 0.0025, 100, 0, 0.1);
  h_maxdist2_v_bs2derr = fs->make<TH2F>("h_maxdist2_v_bs2derr", "", 100, 0, 0.0025, 100, 0, 0.1);
  h_maxdistz_v_bs2derr = fs->make<TH2F>("h_maxdistz_v_bs2derr", "", 100, 0, 0.0025, 100, 0, 0.1);
}

void MFVRefitDistance::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;

  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  h_genvalid->Fill(mevent->gen_valid, w);

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertex_token, vertices);
  const size_t nsv = vertices->size();
  int nsvmatch = 0;

  h_nsv->Fill(nsv, w);

  for (size_t isv = 0; isv < nsv; ++isv) {
    const auto& v = (*vertices)[isv];
    if (require_genmatch && mevent->gen_valid && mevent->lspmatches(v) == -1)
      continue;
    ++nsvmatch;

    const double dbv = mevent->bs2ddist(v);
    int nrefitbad = 0;
    //    printf("vtx %lu with dbv %f\n", isv, dbv);

    jmt::MaxValue maxdist3, maxdist2, maxdistz;
    for (size_t i = 0, ie = v.nnm1(); i < ie; ++i) {
      if (v.nm1_chi2[i] < 0) {
        ++nrefitbad;
        continue;
      }

      const double dist3 = mag(v.nm1_x[i] - v.x, v.nm1_y[i] - v.y, v.nm1_z[i] - v.z);
      const double dist2 = mag(v.nm1_x[i] - v.x, v.nm1_y[i] - v.y);
      const double distz = fabs(v.nm1_z[i] - v.z);
      h_dist3->Fill(dist3, w);
      h_dist2->Fill(dist2, w);
      h_distz->Fill(distz, w);

      maxdist3(dist3);
      maxdist2(dist2);
      maxdistz(distz);
    }

    if (event.isRealData() && dbv >= 0.1 && maxdist3 < 0.01) {
      std::cout << "r,l,e " << event.id().run() << "," << event.luminosityBlock() << "," << event.id().event() << " dbv " << dbv << " maxdist3 " << maxdist3 << "\n";
      printf("  vertex at %f %f %f with %i tracks and chi2 = %f\n", v.x, v.y, v.z, v.ntracks(), v.chi2);
      for (int i = 0; i < v.ntracks(); ++i) {
        printf("  tk #%i: chi2: %11.3g ndof: %11.3g  q*pt: %11.3g +- %11.3g eta: %11.3g +- %11.3g phi: %11.3g +- %11.3g dxy: %11.3g +- %11.3g dz: %11.3g +- %11.3g\n", i, v.track_chi2[i], v.track_ndof[i], v.track_q(i) * v.track_pt(i), v.track_pt_err[i], v.track_eta[i], v.track_eta_err(i), v.track_phi[i], v.track_phi_err(i), v.track_dxy[i], v.track_dxy_err(i), v.track_dz[i], v.track_dz_err(i));
        const double dist3 = mag(v.nm1_x[i] - v.x, v.nm1_y[i] - v.y, v.nm1_z[i] - v.z);
        const double dist2 = mag(v.nm1_x[i] - v.x, v.nm1_y[i] - v.y);
        const double distz = fabs(v.nm1_z[i] - v.z);
        printf("     remove and get vtx at %f %f %f with chi2 = %f and bs2derr %f, dist3 = %f, dist2 = %f, distz = %f\n", v.nm1_x[i], v.nm1_y[i], v.nm1_z[i], v.nm1_chi2[i], v.nm1_bs2derr[i], dist3, dist2, distz);
      }
    }
    h_nrefitbad->Fill(nrefitbad, w);
    h_maxdist3->Fill(maxdist3, w);
    h_maxdist2->Fill(maxdist2, w);
    h_maxdistz->Fill(maxdistz, w);
    h_maxdist3_v_dbv->Fill(dbv, maxdist3, w);
    h_maxdist2_v_dbv->Fill(dbv, maxdist2, w);
    h_maxdistz_v_dbv->Fill(dbv, maxdistz, w);
    h_maxdist3_v_bs2derr->Fill(v.bs2derr, maxdist3, w);
    h_maxdist2_v_bs2derr->Fill(v.bs2derr, maxdist2, w);
    h_maxdistz_v_bs2derr->Fill(v.bs2derr, maxdistz, w);
  }

  h_nsvmatch->Fill(nsvmatch, w);
}

DEFINE_FWK_MODULE(MFVRefitDistance);
