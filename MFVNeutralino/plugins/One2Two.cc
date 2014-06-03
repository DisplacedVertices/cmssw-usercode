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
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  double svdist2d(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return mag(v0.x - v1.x, v0.y - v1.y);
  }

  double dphi(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return reco::deltaPhi(atan2(v0.y, v0.x),
			  atan2(v1.y, v1.x));
  }

  double dphi(const MFVEvent& mevent, const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return reco::deltaPhi(atan2(v0.y - mevent.bsy, v0.x - mevent.bsx),
			  atan2(v1.y - mevent.bsy, v1.x - mevent.bsx));
  }

  double dz(const MFVVertexAux& v0, const MFVVertexAux& v1) {
    return v0.z - v1.z;
  }
}

class MFVOne2Two : public edm::EDAnalyzer {
public:
  explicit MFVOne2Two(const edm::ParameterSet&);
  ~MFVOne2Two();

  bool sel_event(const MFVEvent&) const;
  bool sel_vertex(const MFVEvent&, const MFVVertexAux&) const;
  MFVVertexAux xform_vertex(const MFVEvent&, const MFVVertexAux&) const;

  TF1* f_dphi;
  TH1F* h_fcn_dphi;
  double prob_dphi(const double) const;
  double prob_dphi(const MFVVertexAux&, const MFVVertexAux&) const;

  TF1* f_dz;
  TH1F* h_fcn_dz;
  double prob_dz(const double) const;
  double prob_dz(const MFVVertexAux&, const MFVVertexAux&) const;

  void analyze(const edm::Event&, const edm::EventSetup&);
  void endJob();

  const std::string filename;
  const edm::InputTag event_src;
  const edm::InputTag vertex_src;
  const bool wrep;

  MFVVertexAuxCollection one_vertices;
  std::vector<std::pair<MFVVertexAux, MFVVertexAux> >  two_vertices;

  TH1F* h_nsv;
  TH1F* h_nsvsel;

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
  TH1F* h_2v_dphi;
  TH1F* h_2v_abs_dphi;
  TH2F* h_2v_svdz_v_dphi;

  TH1F* h_1v_bs2ddist;
  TH2F* h_1v_bs2ddist_v_bsdz;
  TH1F* h_1v_bsdz;
  TH1F* h_1v_svdist2d;
  TH1F* h_1v_svdz;
  TH1F* h_1v_svdz_all;
  TH1F* h_1v_dphi;
  TH1F* h_1v_abs_dphi;
  TH2F* h_1v_svdz_v_dphi;
  TH2F* h_1v_svdz_all_v_dphi;
};

MFVOne2Two::MFVOne2Two(const edm::ParameterSet& cfg)
  : filename(cfg.getParameter<std::string>("filename")),
    event_src(cfg.getParameter<edm::InputTag>("event_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    wrep(cfg.getParameter<bool>("wrep"))
{
  edm::Service<TFileService> fs;
  gRandom = new TRandom3(121982);

  h_nsv = new TH1F("h_nsv", "", 10, 0, 10);
  h_nsvsel = new TH1F("h_nsvsel", "", 10, 0, 10);

  f_dphi = new TF1("f_dphi", "x*x*x*x/122.4078739141", -M_PI, M_PI);
  h_fcn_dphi = fs->make<TH1F>("h_fcn_dphi", "", 10, -M_PI, M_PI);
  h_fcn_dphi->FillRandom("f_dphi", 100000);

  f_dz = new TF1("f_dz", "1/sqrt(2*3.14159265*0.01635**2)*exp(-x*x/2/0.01635**2)", -50, 50);
  h_fcn_dz = fs->make<TH1F>("h_fcn_dz", "", 10, -0.1, 0.1);
  h_fcn_dz->FillRandom("f_dz", 100000);

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
  h_2v_dphi = fs->make<TH1F>("h_2v_dphi", "", 10, -M_PI, M_PI);
  h_2v_abs_dphi = fs->make<TH1F>("h_2v_abs_dphi", "", 10, 0, M_PI);
  h_2v_svdz_v_dphi = fs->make<TH2F>("h_2v_svdz_v_dphi", "", 10, -M_PI, M_PI, 50, -0.1, 0.1);

  h_1v_bs2ddist = fs->make<TH1F>("h_1v_bs2ddist", "", 100, 0, 0.1);
  h_1v_bs2ddist_v_bsdz = fs->make<TH2F>("h_1v_bs2ddist_v_bsdz", "", 200, -20, 20, 100, 0, 0.1);
  h_1v_bsdz = fs->make<TH1F>("h_1v_bsdz", "", 200, -20, 20);
  h_1v_svdist2d = fs->make<TH1F>("h_1v_svdist2d", "", 100, 0, 0.1);
  h_1v_svdz = fs->make<TH1F>("h_1v_svdz", "", 50, -0.1, 0.1);
  h_1v_svdz_all = fs->make<TH1F>("h_1v_svdz_all", "", 200, -10, 10);
  h_1v_dphi = fs->make<TH1F>("h_1v_dphi", "", 10, -M_PI, M_PI);
  h_1v_abs_dphi = fs->make<TH1F>("h_1v_abs_dphi", "", 10, 0, M_PI);
  h_1v_svdz_v_dphi = fs->make<TH2F>("h_1v_svdz_v_dphi", "", 10, -M_PI, M_PI, 50, -0.1, 0.1);
  h_1v_svdz_all_v_dphi = fs->make<TH2F>("h_1v_svdz_all_v_dphi", "", 10, -M_PI, M_PI, 200, -10, 10);

#if 0
  h_1v_wrep_svdist2d = fs->make<TH1F>("h_1v_wrep_svdist2d", "", 100, 0, 0.1);
  h_1v_wrep_dphi = fs->make<TH1F>("h_1v_wrep_dphi", "", 10, -M_PI, M_PI);
  h_1v_wrep_abs_dphi = fs->make<TH1F>("h_1v_wrep_abs_dphi", "", 10, 0, M_PI);
#endif
}

MFVOne2Two::~MFVOne2Two() {
  delete f_dphi;
  delete f_dz;
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

double MFVOne2Two::prob_dphi(const double dphi) const {
  return f_dphi->Eval(dphi);
}

double MFVOne2Two::prob_dphi(const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  return prob_dphi(dphi(v0, v1));
}

double MFVOne2Two::prob_dz(const double dz) const {
  return f_dz->Eval(dz);
}

double MFVOne2Two::prob_dz(const MFVVertexAux& v0, const MFVVertexAux& v1) const {
  return prob_dz(dz(v0, v1));
}

void MFVOne2Two::analyze(const edm::Event& event, const edm::EventSetup&) {
  if (filename != "")
    return;

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(event_src, mevent);

  if (!sel_event(*mevent))
    return;

  edm::Handle<MFVVertexAuxCollection> input_vertices;
  event.getByLabel(vertex_src, input_vertices);

  MFVVertexAuxCollection vertices;

  for (const MFVVertexAux& v : *input_vertices)
    if (sel_vertex(*mevent, v))
      vertices.push_back(xform_vertex(*mevent, v));

  h_nsv->Fill(input_vertices->size());
  h_nsvsel->Fill(vertices.size());
  
  if (vertices.size() == 1) {
    const MFVVertexAux& v0 = vertices[0];
    one_vertices.push_back(v0);
    printf("TREETHIS1v %i %.6g %.6g %.6g\n", v0.ntracks(), v0.x, v0.y, v0.z);
  }
  else if (vertices.size() >= 2) {
    const MFVVertexAux& v0 = vertices[0];
    const MFVVertexAux& v1 = vertices[1];
    two_vertices.push_back(std::make_pair(v0, v1));
    printf("TREETHIS2v %i %.6g %.6g %.6g %i %.6g %.6g %.6g\n", v0.ntracks(), v0.x, v0.y, v0.z, v1.ntracks(), v1.x, v1.y, v1.z);
  }
}

void MFVOne2Two::endJob() {
  if (filename != "") {
    FILE* f = fopen(filename.c_str(), "rt");
    if (!f)
      throw cms::Exception("One2Two") << "could not read file " << filename;

    const bool debug = false;
    char line[1024];
    while (fgets(line, 1024, f) != 0) {
      if (debug) printf("One2Two debug: file line read: %s", line);
      int res = 0;
      int ntk0, ntk1;
      float x0,y0,z0, x1,y1,z1;
      if      ((res = sscanf(line, "TREETHIS1v %i %f %f %f",             &ntk0, &x0, &y0, &z0                      )) == 4)
	;
      else if ((res = sscanf(line, "TREETHIS2v %i %f %f %f %i %f %f %f", &ntk0, &x0, &y0, &z0, &ntk1, &x1, &y1, &z1)) == 8)
	;

      if (res == 4) {
	MFVVertexAux v0;
	v0.x = x0; v0.y = y0; v0.z = z0; v0.bs2ddist = mag(x0, y0);
	for (int i = 0; i < ntk0; ++i)
	  v0.insert_track();
	one_vertices.push_back(v0);
      }
      else if (res == 8) {
	MFVVertexAux v0, v1;
	v0.x = x0; v0.y = y0; v0.z = z0; v0.bs2ddist = mag(x0, y0);
	v1.x = x1; v1.y = y1; v1.z = z1; v1.bs2ddist = mag(x1, y1);
	for (int i = 0; i < ntk0; ++i) v0.insert_track();
	for (int i = 0; i < ntk1; ++i) v1.insert_track();
	two_vertices.push_back(std::make_pair(v0, v1));
      }
    }

    fclose(f);
  }

  printf("h_nsv:");      for (int i = 1; i <= 10; ++i) printf(" %i", int(h_nsv   ->GetBinContent(i)));
  printf("\nh_nsvsel:"); for (int i = 1; i <= 10; ++i) printf(" %i", int(h_nsvsel->GetBinContent(i)));
  printf("\n# 1v: %i  # 2v: %i\n", int(one_vertices.size()), int(two_vertices.size()));

  if (filename == "")
    return;

  for (const auto& pair : two_vertices) {
    const MFVVertexAux& v0 = pair.first;
    const MFVVertexAux& v1 = pair.second;
    
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
    h_2v_svdz->Fill(dz(v0, v1));
    h_2v_dphi->Fill(dphi(v0, v1));
    h_2v_abs_dphi->Fill(fabs(dphi(v0, v1)));
    h_2v_svdz_v_dphi->Fill(dphi(v0, v1), dz(v0, v1));
  }

  const int nonevertices = int(one_vertices.size());
  const int giveup = 20*nonevertices;

  std::vector<bool> used(nonevertices, 0);
  const int npairs = nonevertices/2;
  for (int ipair = 0; ipair < npairs; ++ipair) {
    int iv = -1;
    while (iv == -1) {
      int x = gRandom->Integer(nonevertices);
      if (wrep || !used[x]) {
	iv = x;
	used[x] = true;
	break;
      }
    }

    const MFVVertexAux& v0 = one_vertices[iv];
    int tries = 0;

    int jv = -1;
    while (jv == -1) {
      int x = gRandom->Integer(nonevertices);
      if (x != iv && (wrep || !used[x])) {
	const MFVVertexAux& vx = one_vertices[x];
	const double p_dphi = prob_dphi(v0, vx);
	const double p_dz   = prob_dz  (v0, vx);
	const double u1 = gRandom->Rndm();
	const double u2 = gRandom->Rndm();

	if (p_dphi > u1 && p_dz > u2) {
	  jv = x;
	  used[x] = true;
	  printf("\r%200s\r", "");
	  fflush(stdout);
	  break;
	}

	if (++tries % 20000 == 0) {
	  printf("\rtry %12i on pair %6i with v0 = %i (%f, %f, %f)   vx = %i (%f, %f, %f)  p_dphi %f  p_dz %f  u1 %f  u2 %f", tries, ipair, v0.ntracks(), v0.x, v0.y, v0.z, vx.ntracks(), vx.x, vx.y, vx.z, p_dphi, p_dz, u1, u2);
	  fflush(stdout);
	}

	if (tries == giveup)
	  break;
      }
    }

    if (jv == -1) { // tries == giveup, forget about this guy.
      --ipair;
      continue;
    }

    const MFVVertexAux& v1 = one_vertices[jv];

    h_1v_bs2ddist->Fill(v0.bs2ddist);
    h_1v_bs2ddist->Fill(v1.bs2ddist);
    h_1v_bs2ddist_v_bsdz->Fill(v0.z, v0.bs2ddist);
    h_1v_bs2ddist_v_bsdz->Fill(v1.z, v1.bs2ddist);
    h_1v_bsdz->Fill(v0.z);
    h_1v_bsdz->Fill(v1.z);

    h_1v_svdist2d->Fill(svdist2d(v0, v1));
    h_1v_svdz->Fill(dz(v0, v1));
    h_1v_svdz_all->Fill(dz(v0, v1));
    h_1v_dphi->Fill(dphi(v0, v1));
    h_1v_abs_dphi->Fill(fabs(dphi(v0, v1)));
    h_1v_svdz_v_dphi->Fill(dphi(v0, v1), dz(v0, v1));
    h_1v_svdz_all_v_dphi->Fill(dphi(v0, v1), dz(v0, v1));
  }
}

DEFINE_FWK_MODULE(MFVOne2Two);
