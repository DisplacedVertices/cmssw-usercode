#include "TF1.h"
#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

namespace {
  struct RLE {
    unsigned run;
    unsigned lumi;
    unsigned event;

    RLE(const edm::Event& event) : run(event.id().run()), lumi(event.luminosityBlock()), event(event.id().event()) {}
  };

  bool operator<(const RLE& a, const RLE& b) {
    if (a.run == b.run) {
      if (a.lumi == b.lumi)
	return a.event < b.event;
      else
	return a.lumi < b.lumi;
    }
    else
      return a.run < b.run;
  }

  std::ostream& operator<<(std::ostream& o, const RLE& rle) {
    o << "(" << rle.run << "," << rle.lumi << "," << rle.event << ")";
    return o;
  }    

  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  double svdist2d(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return mag(v0.x - v1.x, v0.y - v1.y);
  }

  double delta_phi(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return reco::deltaPhi(atan2(v0.y, v0.x),
			  atan2(v1.y, v1.x));
  }

  double delta_phi(const MFVEvent& mevent, const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return reco::deltaPhi(atan2(v0.y - mevent.bsy, v0.x - mevent.bsx),
			  atan2(v1.y - mevent.bsy, v1.x - mevent.bsx));
  }
}

class MFVOne2Two : public edm::EDAnalyzer {
public:
  explicit MFVOne2Two(const edm::ParameterSet&);
  ~MFVOne2Two();

  bool sel_event(const MFVEvent&) const;
  bool sel_vertex(const MFVEvent&, const MFVVertexAux&) const;
  MFVVertexAux xform_vertex(const MFVEvent&, const MFVVertexAux&) const;

  TF1* f_delta_phi;
  TH1F* h_fcn_delta_phi;
  double prob_delta_phi(const double) const;
  double prob_delta_phi(const MFVVertexAux&, const MFVVertexAux&) const;

  void analyze(const edm::Event&, const edm::EventSetup&);
  void endJob();

  const edm::InputTag event_src;
  const edm::InputTag vertex_src;

  std::map<RLE, MFVEvent> mevents;
  std::map<RLE, MFVVertexAuxCollection> all_vertices;
  MFVVertexAuxCollection one_vertices;

  TH1F* h_2v_bs2ddist;
  TH2F* h_2v_bs2ddist_v_bsdz;
  TH1F* h_2v_bsdz;
  TH1F* h_2v_bs2ddist_0;
  TH2F* h_2v_bs2ddist_v_bsdz_0;
  TH1F* h_2v_bsdz_0;
  TH1F* h_2v_bs2ddist_1;
  TH2F* h_2v_bs2ddist_v_bsdz_1;
  TH1F* h_2v_bsdz_1;
  TH1F* h_2v_svdist2d;
  TH1F* h_2v_svdz;
  TH1F* h_2v_delta_phi;
  TH1F* h_2v_abs_delta_phi;
  TH2F* h_2v_svdz_v_delta_phi;

  TH1F* h_1v_worep_bs2ddist;
  TH2F* h_1v_worep_bs2ddist_v_bsdz;
  TH1F* h_1v_worep_bsdz;
  TH1F* h_1v_worep_svdist2d;
  TH1F* h_1v_worep_svdz;
  TH1F* h_1v_worep_svdz_all;
  TH1F* h_1v_worep_delta_phi;
  TH1F* h_1v_worep_abs_delta_phi;
  TH2F* h_1v_worep_svdz_v_delta_phi;

  TH1F* h_1v_wrep_svdist2d;
  TH1F* h_1v_wrep_delta_phi;
  TH1F* h_1v_wrep_abs_delta_phi;
};

MFVOne2Two::MFVOne2Two(const edm::ParameterSet& cfg)
  : event_src(cfg.getParameter<edm::InputTag>("event_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src"))
{
  edm::Service<TFileService> fs;
  gRandom = new TRandom3(121982);

  f_delta_phi = new TF1("f_delta_phi", "x*x*x*x/122.4078739141", -M_PI, M_PI);
  h_fcn_delta_phi = fs->make<TH1F>("h_fcn_delta_phi", "", 10, -M_PI, M_PI);
  h_fcn_delta_phi->FillRandom("f_delta_phi", 100000);

  h_2v_bs2ddist = fs->make<TH1F>("h_2v_bs2ddist", "", 100, 0, 0.1);
  h_2v_bs2ddist_v_bsdz = fs->make<TH2F>("h_2v_bs2ddist_v_bsdz", "", 200, -20, 20, 100, 0, 0.1);
  h_2v_bsdz = fs->make<TH1F>("h_2v_bsdz", "", 200, -20, 20);
  h_2v_bs2ddist_0 = fs->make<TH1F>("h_2v_bs2ddist_0", "", 100, 0, 0.1);
  h_2v_bs2ddist_v_bsdz_0 = fs->make<TH2F>("h_2v_bs2ddist_v_bsdz_0", "", 200, -20, 20, 100, 0, 0.1);
  h_2v_bsdz_0 = fs->make<TH1F>("h_2v_bsdz_0", "", 200, -20, 20);
  h_2v_bs2ddist_1 = fs->make<TH1F>("h_2v_bs2ddist_1", "", 100, 0, 0.1);
  h_2v_bs2ddist_v_bsdz_1 = fs->make<TH2F>("h_2v_bs2ddist_v_bsdz_1", "", 200, -20, 20, 100, 0, 0.1);
  h_2v_bsdz_1 = fs->make<TH1F>("h_2v_bsdz_1", "", 200, -20, 20);
  h_2v_svdist2d = fs->make<TH1F>("h_2v_svdist2d", "", 100, 0, 0.1);
  h_2v_svdz = fs->make<TH1F>("h_2v_svdz", "", 50, -0.1, 0.1);
  h_2v_delta_phi = fs->make<TH1F>("h_2v_delta_phi", "", 10, -M_PI, M_PI);
  h_2v_abs_delta_phi = fs->make<TH1F>("h_2v_abs_delta_phi", "", 10, 0, M_PI);
  h_2v_svdz_v_delta_phi = fs->make<TH2F>("h_2v_svdz_v_delta_phi", "", 10, -M_PI, M_PI, 50, -0.1, 0.1);

  h_1v_worep_bs2ddist = fs->make<TH1F>("h_1v_worep_bs2ddist", "", 100, 0, 0.1);
  h_1v_worep_bs2ddist_v_bsdz = fs->make<TH2F>("h_1v_worep_bs2ddist_v_bsdz", "", 200, -20, 20, 100, 0, 0.1);
  h_1v_worep_bsdz = fs->make<TH1F>("h_1v_worep_bsdz", "", 200, -20, 20);
  h_1v_worep_svdist2d = fs->make<TH1F>("h_1v_worep_svdist2d", "", 100, 0, 0.1);
  h_1v_worep_svdz = fs->make<TH1F>("h_1v_worep_svdz", "", 50, -0.1, 0.1);
  h_1v_worep_svdz_all = fs->make<TH1F>("h_1v_worep_svdz_all", "", 200, -10, 10);
  h_1v_worep_delta_phi = fs->make<TH1F>("h_1v_worep_delta_phi", "", 10, -M_PI, M_PI);
  h_1v_worep_abs_delta_phi = fs->make<TH1F>("h_1v_worep_abs_delta_phi", "", 10, 0, M_PI);
  h_1v_worep_svdz_v_delta_phi = fs->make<TH2F>("h_1v_worep_svdz_v_delta_phi", "", 10, -M_PI, M_PI, 50, -0.1, 0.1);

  h_1v_wrep_svdist2d = fs->make<TH1F>("h_1v_wrep_svdist2d", "", 100, 0, 0.1);
  h_1v_wrep_delta_phi = fs->make<TH1F>("h_1v_wrep_delta_phi", "", 10, -M_PI, M_PI);
  h_1v_wrep_abs_delta_phi = fs->make<TH1F>("h_1v_wrep_abs_delta_phi", "", 10, 0, M_PI);
}

MFVOne2Two::~MFVOne2Two() {
  delete f_delta_phi;
}

bool MFVOne2Two::sel_event(const MFVEvent&) const {
  return true;
}

bool MFVOne2Two::sel_vertex(const MFVEvent&, const MFVVertexAux& v) const {
  return v.ntracks() >= 6;
}

MFVVertexAux MFVOne2Two::xform_vertex(const MFVEvent& mevent, const MFVVertexAux& v) const {
  MFVVertexAux v2(v);
  v2.x -= mevent.bsx;
  v2.y -= mevent.bsy;
  v2.z -= mevent.bsz;
  return v2;
}

double MFVOne2Two::prob_delta_phi(const double delta_phi) const {
  return f_delta_phi->Eval(delta_phi);
}

double MFVOne2Two::prob_delta_phi(const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  return prob_delta_phi(delta_phi(v0, v1));
}

void MFVOne2Two::analyze(const edm::Event& event, const edm::EventSetup&) {
  RLE rle(event); 
  //std::cout << "RLE: " << rle << std::endl;

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(event_src, mevent);

  if (!sel_event(*mevent))
    return;

  mevents[rle] = *mevent;

  edm::Handle<MFVVertexAuxCollection> input_vertices;
  event.getByLabel(vertex_src, input_vertices);

  MFVVertexAuxCollection& vertices = all_vertices[rle];

  for (const MFVVertexAux& v : *input_vertices)
    if (sel_vertex(*mevent, v))
      vertices.push_back(xform_vertex(*mevent, v));

  if (vertices.size() == 1) {
    one_vertices.push_back(vertices[0]);
  }
  else if (vertices.size() >= 2) {
    const MFVVertexAux& v0 = vertices.at(0);
    const MFVVertexAux& v1 = vertices.at(1);

    h_2v_bs2ddist->Fill(v0.bs2ddist);
    h_2v_bs2ddist->Fill(v1.bs2ddist);
    h_2v_bs2ddist_0->Fill(v0.bs2ddist);
    h_2v_bs2ddist_1->Fill(v1.bs2ddist);
    h_2v_bs2ddist_v_bsdz->Fill(v0.z, v0.bs2ddist);
    h_2v_bs2ddist_v_bsdz->Fill(v1.z, v1.bs2ddist);
    h_2v_bs2ddist_v_bsdz_0->Fill(v0.z, v0.bs2ddist);
    h_2v_bs2ddist_v_bsdz_1->Fill(v1.z, v1.bs2ddist);
    h_2v_bsdz->Fill(v0.z);
    h_2v_bsdz->Fill(v1.z);
    h_2v_bsdz_0->Fill(v0.z);
    h_2v_bsdz_1->Fill(v1.z);

    h_2v_svdist2d->Fill(svdist2d(v0, v1));
    h_2v_svdz->Fill(v0.z - v1.z);
    h_2v_delta_phi->Fill(delta_phi(v0, v1));
    h_2v_abs_delta_phi->Fill(fabs(delta_phi(v0, v1)));
    h_2v_svdz_v_delta_phi->Fill(delta_phi(v0, v1), v0.z - v1.z);
  }
}

void MFVOne2Two::endJob() {
  assert(mevents.size() == all_vertices.size());
  const int nevents = int(mevents.size());
  int nallvertices = 0;
  int nonevertices = 0;
  for (const auto& it : all_vertices) {
    //const RLE& rle = it.first;
    const MFVVertexAuxCollection& vertices = it.second;
    nallvertices += int(vertices.size());
    if (vertices.size() == 1)
      ++nonevertices;
  }

  printf("hi in endJob: %i events processed, with %i vertices (avg %f/event)\n# one-vertex events: %i", nevents, nallvertices, float(nallvertices)/nevents, nonevertices);
  assert(int(one_vertices.size()) == nonevertices);

  // sample without replacement
  std::vector<bool> used(one_vertices.size(), 0);
  const int npairs = nonevertices/2;
  for (int ipair = 0; ipair < npairs; ++ipair) {
    int iv = -1;
    while (iv == -1) {
      int x = gRandom->Integer(nonevertices);
      if (!used[x]) {
	iv = x;
	used[x] = true;
	break;
      }
    }

    const MFVVertexAux& v0 = one_vertices[iv];

    int jv = -1;
    while (jv == -1) {
      int x = gRandom->Integer(nonevertices);
      if (!used[x]) {
	const MFVVertexAux& vx = one_vertices[x];
	if (prob_delta_phi(v0, vx) > gRandom->Rndm()) {
	  jv = x;
	  used[x] = true;
	  break;
	}
      }
    }
    
    const MFVVertexAux& v1 = one_vertices[jv];

    h_1v_worep_bs2ddist->Fill(v0.bs2ddist);
    h_1v_worep_bs2ddist->Fill(v1.bs2ddist);
    h_1v_worep_bs2ddist_v_bsdz->Fill(v0.z, v0.bs2ddist);
    h_1v_worep_bs2ddist_v_bsdz->Fill(v1.z, v1.bs2ddist);
    h_1v_worep_bsdz->Fill(v0.z);
    h_1v_worep_bsdz->Fill(v1.z);

    h_1v_worep_svdist2d->Fill(svdist2d(v0, v1));
    h_1v_worep_svdz->Fill(v0.z - v1.z);
    h_1v_worep_svdz_all->Fill(v0.z - v1.z);
    h_1v_worep_delta_phi->Fill(delta_phi(v0, v1));
    h_1v_worep_abs_delta_phi->Fill(fabs(delta_phi(v0, v1)));
    h_1v_worep_svdz_v_delta_phi->Fill(delta_phi(v0, v1), v0.z - v1.z);
  }

  // sample with replacement
  for (int ipair = 0; ipair < npairs; ++ipair) {
    int iv = gRandom->Integer(nonevertices);
    const MFVVertexAux& v0 = one_vertices[iv];

    int jv = -1;
    while (jv == -1) {
      int x = gRandom->Integer(nonevertices);
      const MFVVertexAux& vx = one_vertices[x];
      if (prob_delta_phi(v0, vx) > gRandom->Rndm()) {
	jv = x;
	break;
      }
    }
    
    const MFVVertexAux& v1 = one_vertices[jv];

    h_1v_wrep_svdist2d->Fill(svdist2d(v0, v1));
    h_1v_wrep_delta_phi->Fill(delta_phi(v0, v1));
    h_1v_wrep_abs_delta_phi->Fill(fabs(delta_phi(v0, v1)));
  }
}

DEFINE_FWK_MODULE(MFVOne2Two);
