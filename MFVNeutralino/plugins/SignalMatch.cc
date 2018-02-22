#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVSignalMatch : public edm::EDAnalyzer {
 public:
  explicit MFVSignalMatch(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertices_token;
  const edm::EDGetTokenT<MFVEvent> event_token;
  const double max_dist;

  TH1D* h_valid;
  TH1D* h_gendist;
  TH1D* h_nvtx;
  TH1D* h_nmatch;
  TH2D* h_nmatch_v_nvtx;
  TH1D* h_nmatch_nge2;
  TH1D* h_nmatch_neq2;
  TH1D* h_nmatch_ngt2;
  TH1D* h_nmatch_dvvzero;
  TH1D* h_samematch;
  TH1D* h_samematch_dvvzero;

  TH1D* h_gendvv_all;
  TH1D* h_dvv;
  TH1D* h_gendvv;
  TH1D* h_dvv_nmatch[4];
  TH1D* h_gendvv_nmatch[4];
  TH1D* h_dvv_samematch;
  TH1D* h_gendvv_samematch;
  TH1D* h_dvvzero;
  TH1D* h_dvvzero_samematch;
  TH1D* h_gendvv_dvvzero;

  TH1D* h_genrho;
  TH1D* h_genrho_notmatched;
  TH1D* h_genrho_notmatched_nge2;
};

MFVSignalMatch::MFVSignalMatch(const edm::ParameterSet& cfg)
  : vertices_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    max_dist(cfg.getParameter<double>("max_dist"))
{
  edm::Service<TFileService> fs;

  h_valid = fs->make<TH1D>("h_valid", ";gen_valid flag set?;events", 2, 0, 2);
  h_gendist = fs->make<TH1D>("h_gendist", ";3D distance between decay vertices (cm);events/50 #mum", 2000, 0, 10);
  h_nvtx = fs->make<TH1D>("h_nvtx", ";# of selected vertices;events", 10, 0, 10);
  h_nmatch = fs->make<TH1D>("h_nmatch", ";# of selected vertices matching a decay vertex;events", 10, 0, 10);
  h_nmatch_v_nvtx = fs->make<TH2D>("h_nmatch_v_nvtx", ";# of selected vertices;# of selected vertices matching a decay vertex", 10, 0, 10, 10, 0, 10);
  h_nmatch_nge2 = fs->make<TH1D>("h_nmatch_nge2", "events with at least two selected vertices;# of selected vertices matching a decay vertex;events", 10, 0, 10);
  h_nmatch_neq2 = fs->make<TH1D>("h_nmatch_neq2", "events with exactly two selected vertices;# of selected vertices matching a decay vertex;events", 10, 0, 10);
  h_nmatch_ngt2 = fs->make<TH1D>("h_nmatch_ngt2", "events with more than two selected vertices;# of selected vertices matching a decay vertex;events", 10, 0, 10);
  h_nmatch_dvvzero = fs->make<TH1D>("h_nmatch_dvvzero", "d_{VV} ~ 0;# of selected vertices matching a decay vertex;events", 10, 0, 10);
  h_samematch = fs->make<TH1D>("h_samematch", "# of selected vertices at least 2;same decay vertex matched?;events", 2, 0, 2);
  h_samematch_dvvzero = fs->make<TH1D>("h_samematch_dvvzero", "# of selected vertices at least 2 and d_{VV} ~ 0;same decay vertex matched?;events", 2, 0, 2);
  h_gendvv_all = fs->make<TH1D>("h_gendvv_all", "all not-skipped events;generated d_{VV} (cm);events/50 #mum", 800, 0, 4);
  h_dvv = fs->make<TH1D>("h_dvv", ";d_{VV} (cm);events/50 #mum", 800, 0, 4);
  h_gendvv = fs->make<TH1D>("h_gendvv", "events with at least two vertices;generated d_{VV} (cm);events/50 #mum", 800, 0, 4);
  for (int i = 0; i < 4; ++i) {
    h_dvv_nmatch[i] = fs->make<TH1D>(TString::Format("h_dvv_nmatch%i", i), TString::Format("%i matching a decay vertex;d_{VV} (cm);events/50 #mum", i), 800, 0, 4);
    h_gendvv_nmatch[i] = fs->make<TH1D>(TString::Format("h_gendvv_nmatch%i", i), TString::Format("%i matching a decay vertex;generated d_{VV} (cm);events/50 #mum", i), 800, 0, 4);
  }
  h_dvv_samematch = fs->make<TH1D>("h_dvv_samematch", "both vertices match the same decay vertex;d_{VV} (cm);events/50 #mum", 800, 0, 4);
  h_gendvv_samematch = fs->make<TH1D>("h_gendvv_samematch", "both vertices match the same decay vertex;generated d_{VV} (cm);events/50 #mum", 800, 0, 4);
  h_dvvzero = fs->make<TH1D>("h_dvvzero", ";d_{VV} ~ 0?;events", 2, 0, 2);
  h_dvvzero_samematch = fs->make<TH1D>("h_dvvzero_samematch", "both vertices match the same decay vertex;d_{VV} ~ 0?;events", 2, 0, 2);
  h_gendvv_dvvzero = fs->make<TH1D>("h_gendvv_dvvzero", "d_{VV} ~ 0;generated d_{VV} (cm);events/50 #mum", 800, 0, 4);
  h_genrho = fs->make<TH1D>("h_genrho", ";generated #rho (cm);events/50 #mum", 2000, 0, 10);
  h_genrho_notmatched = fs->make<TH1D>("h_genrho_notmatched", "decay vertex not matched;generated #rho (cm) ;events/50 #mum", 2000, 0, 10);
  h_genrho_notmatched_nge2 = fs->make<TH1D>("h_genrho_notmatched_nge2", "decay vertex not matched and at least two selected vertices;generated #rho (cm) ;events/50 #mum", 2000, 0, 10);
}

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }
}

void MFVSignalMatch::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  h_valid->Fill(mevent->gen_valid);
  if (!mevent->gen_valid)
    return;

  const double gendist = mevent->lspdist3d();
  h_gendist->Fill(gendist);
  if (gendist < max_dist)
    return;

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);

  const size_t nvtx = vertices->size();
  h_nvtx->Fill(nvtx);

  std::vector<int> match_ivtx(2, -1);
  std::vector<int> match_igen(nvtx, -1);
  int nmatch = 0;
  for (size_t ivtx = 0; ivtx < nvtx; ++ivtx) {
    const MFVVertexAux& vtx = (*vertices)[ivtx];

    double min_dist = max_dist;
    int igen = -1;
    for (int i = 0; i < 2; ++i) {
      const double dist = mag(mevent->gen_lsp_decay[i*3+0] - vtx.x,
                              mevent->gen_lsp_decay[i*3+1] - vtx.y,
                              mevent->gen_lsp_decay[i*3+2] - vtx.z);
      if (dist < min_dist) {
        min_dist = dist;
        igen = i;
      }
    }

    if (igen > -1) {
      ++nmatch;
      match_ivtx[igen] = ivtx;
      match_igen[ivtx] = igen;
    }
  }

  const int nmatch_max3 = std::min(nmatch, 3);

  h_nmatch->Fill(nmatch);
  h_nmatch_v_nvtx->Fill(nvtx, nmatch);
  if (nvtx >= 2) h_nmatch_nge2->Fill(nmatch);
  if (nvtx == 2) h_nmatch_neq2->Fill(nmatch);
  if (nvtx >  2) h_nmatch_ngt2->Fill(nmatch);

  const double genrho[2] = {
    mag(mevent->gen_lsp_decay[0*3+0] - mevent->gen_pv[0], mevent->gen_lsp_decay[0*3+1] - mevent->gen_pv[1]),
    mag(mevent->gen_lsp_decay[1*3+0] - mevent->gen_pv[0], mevent->gen_lsp_decay[1*3+1] - mevent->gen_pv[1])
  };
  const double gendvv = mevent->lspdist2d();

  h_gendvv_all->Fill(gendvv);
  if (nvtx >= 2) {
    const MFVVertexAux& v0 = (*vertices)[0];
    const MFVVertexAux& v1 = (*vertices)[1];
    const int i0 = match_igen[0];
    const int i1 = match_igen[1];
    const bool samematch = i0 == i1 && i0 != -1;
    const double dvv = mag(v0.x - v1.x, v0.y - v1.y);
    const bool dvvzero = dvv < 0.03;

    h_dvv->Fill(dvv);
    h_gendvv->Fill(gendvv);
    h_dvv_nmatch[nmatch_max3]->Fill(dvv);
    h_gendvv_nmatch[nmatch_max3]->Fill(gendvv);
    h_samematch->Fill(samematch);
    h_dvvzero->Fill(dvvzero);

    if (samematch) {
      h_dvvzero_samematch->Fill(dvvzero);
      h_dvv_samematch->Fill(dvv);
      h_gendvv_samematch->Fill(gendvv);
    }

    if (dvvzero) {
      h_nmatch_dvvzero->Fill(nmatch);
      h_gendvv_dvvzero->Fill(gendvv);
      h_samematch_dvvzero->Fill(samematch);
    }
  }

  for (int i = 0; i < 2; ++i) {
    h_genrho->Fill(genrho[i]);
    if (match_ivtx[i] == -1) {
      h_genrho_notmatched->Fill(genrho[i]);
      if (nvtx >= 2)
        h_genrho_notmatched_nge2->Fill(genrho[i]);
    }
  }
}

DEFINE_FWK_MODULE(MFVSignalMatch);
