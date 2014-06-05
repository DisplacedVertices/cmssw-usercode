#include "TF1.h"
#include "TH2F.h"
#include "TRandom3.h"
#include "TTree.h"
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
  bool sel_vertex_aft(const MFVVertexAux&) const;
  MFVVertexAux xform_vertex(const MFVEvent&, const MFVVertexAux&) const;

  double prob_dphi(const double) const;
  double prob_dphi(const MFVVertexAux&, const MFVVertexAux&) const;

  double prob_dz(const double) const;
  double prob_dz(const MFVVertexAux&, const MFVVertexAux&) const;

  void analyze(const edm::Event&, const edm::EventSetup&);
  void endJob();

  const edm::InputTag event_src;
  const edm::InputTag vertex_src;
  const int min_ntracks;

  const std::string tree_path;
  const std::string filename;
  const std::vector<std::string> filenames;
  const std::vector<int> n1vs;
  const std::vector<double> weights;
  const std::vector<int> npairses;
  const bool wrep;
  const int npairs;
  const int min_ntracks_aft;
  const bool use_f_dz;
  const double max_1v_dz;
  const int max_1v_ntracks;

  const std::string form_dphi;
  const std::string form_dz;
  TF1* f_dphi;
  TF1* f_dz;
  TH1F* h_fcn_dphi;
  TH1F* h_fcn_dz;

  MFVVertexAuxCollection one_vertices;
  std::vector<std::pair<MFVVertexAux, MFVVertexAux> >  two_vertices;

  TH1F* h_nsv;
  TH1F* h_nsvsel;

  TH2F* h_2v_xy;
  TH1F* h_2v_bs2ddist;
  TH2F* h_2v_bs2ddist_v_bsdz;
  TH1F* h_2v_bsdz;
  TH1F* h_2v_bs2ddist_0;
  TH2F* h_2v_bs2ddist_v_bsdz_0;
  TH1F* h_2v_bsdz_0;
  TH1F* h_2v_bs2ddist_1;
  TH2F* h_2v_bs2ddist_v_bsdz_1;
  TH1F* h_2v_bsdz_1;
  TH2F* h_2v_ntracks;
  TH1F* h_2v_ntracks01;
  TH1F* h_2v_svdist2d;
  TH1F* h_2v_svdz;
  TH1F* h_2v_dphi;
  TH1F* h_2v_abs_dphi;
  TH1F* h_2v_lt35_dphi;
  TH1F* h_2v_lt35_abs_dphi;
  TH1F* h_2v_gt35_dphi;
  TH1F* h_2v_gt35_abs_dphi;
  TH2F* h_2v_svdz_v_dphi;

  TH2F* h_1v_xy;
  TH1F* h_1v_bs2ddist;
  TH2F* h_1v_bs2ddist_v_bsdz;
  TH1F* h_1v_bsdz;
  TH2F* h_1v_ntracks;
  TH1F* h_1v_ntracks01;
  TH1F* h_1v_svdist2d;
  TH1F* h_1v_svdz;
  TH1F* h_1v_svdz_all;
  TH1F* h_1v_dphi;
  TH1F* h_1v_abs_dphi;
  TH2F* h_1v_svdz_v_dphi;
  TH2F* h_1v_svdz_all_v_dphi;

  struct tree_t {
    unsigned run;
    unsigned lumi;
    unsigned event;
    unsigned char nvtx;
    unsigned char ntk0;
    float x0;
    float y0;
    float z0;
    unsigned char ntk1;
    float x1;
    float y1;
    float z1;
  };
  tree_t nt;
  TTree* tree;
};

MFVOne2Two::MFVOne2Two(const edm::ParameterSet& cfg)
  : event_src(cfg.getParameter<edm::InputTag>("event_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    min_ntracks(cfg.getParameter<int>("min_ntracks")),

    tree_path(cfg.getParameter<std::string>("tree_path")),
    filename(cfg.getParameter<std::string>("filename")),
    filenames(cfg.getParameter<std::vector<std::string> >("filenames")),
    n1vs(cfg.getParameter<std::vector<int> >("n1vs")),
    weights(cfg.getParameter<std::vector<double> >("weights")),
    npairses(cfg.getParameter<std::vector<int> >("npairses")),
    wrep(cfg.getParameter<bool>("wrep")),
    npairs(cfg.getParameter<int>("npairs")),
    min_ntracks_aft(cfg.getParameter<int>("min_ntracks_aft")),
    use_f_dz(cfg.getParameter<bool>("use_f_dz")),
    max_1v_dz(cfg.getParameter<double>("max_1v_dz")),
    max_1v_ntracks(cfg.getParameter<int>("max_1v_ntracks")),
    form_dphi(cfg.getParameter<std::string>("form_dphi")),
    form_dz(cfg.getParameter<std::string>("form_dz")),
    f_dphi(0),
    f_dz(0)
{
  edm::Service<TFileService> fs;

  h_nsv = new TH1F("h_nsv", "", 10, 0, 10);
  h_nsvsel = new TH1F("h_nsvsel", "", 10, 0, 10);

  if (filename == "") {
    tree = fs->make<TTree>("t", "");
    tree->Branch("run", &nt.run, "run/i");
    tree->Branch("lumi", &nt.lumi, "lumi/i");
    tree->Branch("event", &nt.event, "event/i");
    tree->Branch("nvtx", &nt.nvtx, "nvtx/b");
    tree->Branch("ntk0", &nt.ntk0, "ntk0/b");
    tree->Branch("x0", &nt.x0, "x0/F");
    tree->Branch("y0", &nt.y0, "y0/F");
    tree->Branch("z0", &nt.z0, "z0/F");
    tree->Branch("ntk1", &nt.ntk1, "ntk1/b");
    tree->Branch("x1", &nt.x1, "x1/F");
    tree->Branch("y1", &nt.y1, "y1/F");
    tree->Branch("z1", &nt.z1, "z1/F");
  }
  else {
    f_dphi = new TF1("f_dphi", form_dphi.c_str(), -M_PI, M_PI);
    h_fcn_dphi = fs->make<TH1F>("h_fcn_dphi", "", 10, -M_PI, M_PI);
    h_fcn_dphi->FillRandom("f_dphi", 100000);

    f_dz = new TF1("f_dz", form_dz.c_str(), -50, 50);
    h_fcn_dz = fs->make<TH1F>("h_fcn_dz", "", 10, -0.1, 0.1);
    h_fcn_dz->FillRandom("f_dz", 100000);

    h_2v_xy = fs->make<TH2F>("h_2v_xy", "", 100, -0.05, 0.05, 100, 0.05, 0.05);
    h_2v_bs2ddist = fs->make<TH1F>("h_2v_bs2ddist", "", 100, 0, 0.1);
    h_2v_bs2ddist_v_bsdz = fs->make<TH2F>("h_2v_bs2ddist_v_bsdz", "", 200, -20, 20, 100, 0, 0.1);
    h_2v_bsdz = fs->make<TH1F>("h_2v_bsdz", "", 200, -20, 20);
    h_2v_bs2ddist_0 = fs->make<TH1F>("h_2v_bs2ddist_0", "", 100, 0, 0.1);
    h_2v_bs2ddist_v_bsdz_0 = fs->make<TH2F>("h_2v_bs2ddist_v_bsdz_0", "", 200, -20, 20, 100, 0, 0.1);
    h_2v_bsdz_0 = fs->make<TH1F>("h_2v_bsdz_0", "", 200, -20, 20);
    h_2v_bs2ddist_1 = fs->make<TH1F>("h_2v_bs2ddist_1", "", 100, 0, 0.1);
    h_2v_bs2ddist_v_bsdz_1 = fs->make<TH2F>("h_2v_bs2ddist_v_bsdz_1", "", 200, -20, 20, 100, 0, 0.1);
    h_2v_bsdz_1 = fs->make<TH1F>("h_2v_bsdz_1", "", 200, -20, 20);
    h_2v_ntracks = fs->make<TH2F>("h_2v_ntracks", "", 20, 0, 20, 20, 0, 20);
    h_2v_ntracks01 = fs->make<TH1F>("h_2v_ntracks01", "", 30, 0, 30);
    h_2v_svdist2d = fs->make<TH1F>("h_2v_svdist2d", "", 100, 0, 0.1);
    h_2v_svdz = fs->make<TH1F>("h_2v_svdz", "", 50, -0.1, 0.1);
    h_2v_dphi = fs->make<TH1F>("h_2v_dphi", "", 10, -M_PI, M_PI);
    h_2v_abs_dphi = fs->make<TH1F>("h_2v_abs_dphi", "", 10, 0, M_PI);
    h_2v_lt35_dphi = fs->make<TH1F>("h_2v_lt35_dphi", "", 10, -M_PI, M_PI);
    h_2v_lt35_abs_dphi = fs->make<TH1F>("h_2v_lt35_abs_dphi", "", 10, 0, M_PI);
    h_2v_gt35_dphi = fs->make<TH1F>("h_2v_gt35_dphi", "", 10, -M_PI, M_PI);
    h_2v_gt35_abs_dphi = fs->make<TH1F>("h_2v_gt35_abs_dphi", "", 10, 0, M_PI);
    h_2v_svdz_v_dphi = fs->make<TH2F>("h_2v_svdz_v_dphi", "", 10, -M_PI, M_PI, 50, -0.1, 0.1);

    h_1v_xy = fs->make<TH2F>("h_1v_xy", "", 100, -0.05, 0.05, 100, 0.05, 0.05);
    h_1v_bs2ddist = fs->make<TH1F>("h_1v_bs2ddist", "", 100, 0, 0.1);
    h_1v_bs2ddist_v_bsdz = fs->make<TH2F>("h_1v_bs2ddist_v_bsdz", "", 200, -20, 20, 100, 0, 0.1);
    h_1v_bsdz = fs->make<TH1F>("h_1v_bsdz", "", 200, -20, 20);
    h_1v_ntracks = fs->make<TH2F>("h_1v_ntracks", "", 20, 0, 20, 20, 0, 20);
    h_1v_ntracks01 = fs->make<TH1F>("h_1v_ntracks01", "", 30, 0, 30);
    h_1v_svdist2d = fs->make<TH1F>("h_1v_svdist2d", "", 100, 0, 0.1);
    h_1v_svdz = fs->make<TH1F>("h_1v_svdz", "", 50, -0.1, 0.1);
    h_1v_svdz_all = fs->make<TH1F>("h_1v_svdz_all", "", 200, -10, 10);
    h_1v_dphi = fs->make<TH1F>("h_1v_dphi", "", 10, -M_PI, M_PI);
    h_1v_abs_dphi = fs->make<TH1F>("h_1v_abs_dphi", "", 10, 0, M_PI);
    h_1v_svdz_v_dphi = fs->make<TH2F>("h_1v_svdz_v_dphi", "", 10, -M_PI, M_PI, 50, -0.1, 0.1);
    h_1v_svdz_all_v_dphi = fs->make<TH2F>("h_1v_svdz_all_v_dphi", "", 10, -M_PI, M_PI, 200, -10, 10);
  }
}

MFVOne2Two::~MFVOne2Two() {
  delete f_dphi;
  delete f_dz;
}

bool MFVOne2Two::sel_event(const MFVEvent&) const {
  return true;
}

bool MFVOne2Two::sel_vertex(const MFVEvent&, const MFVVertexAux& v) const {
  return v.ntracks() >= min_ntracks;
}

bool MFVOne2Two::sel_vertex_aft(const MFVVertexAux& v) const {
  return v.ntracks() >= min_ntracks_aft;
}

MFVVertexAux MFVOne2Two::xform_vertex(const MFVEvent& mevent, const MFVVertexAux& v) const {
  MFVVertexAux v2(v);
  v2.x -= mevent.bsx;
  v2.y -= mevent.bsy;
  v2.z -= mevent.bsz;
  return v2;
}

double MFVOne2Two::prob_dphi(const double dphi) const {
  return f_dphi->Eval(fabs(dphi));
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

  memset(&nt, 0, sizeof(tree_t));
  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();

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

    nt.nvtx = 1;
    nt.ntk0 = v0.ntracks();
    nt.x0 = v0.x;
    nt.y0 = v0.y;
    nt.z0 = v0.z;
  }
  else if (vertices.size() >= 2) {
    const MFVVertexAux& v0 = vertices[0];
    const MFVVertexAux& v1 = vertices[1];
    two_vertices.push_back(std::make_pair(v0, v1));

    nt.nvtx = 2;
    nt.ntk0 = v0.ntracks();
    nt.ntk1 = v1.ntracks();
    nt.x0 = v0.x; nt.y0 = v0.y; nt.z0 = v0.z;
    nt.x1 = v1.x; nt.y1 = v1.y; nt.z1 = v1.z;
  }
  else {
    if (vertices.size() != 0)
      throw cms::Exception("CheckYourPremises") << "more than two vertices (" << vertices.size() << ") in this event";
    return;
  }

  tree->Fill();
}

void MFVOne2Two::endJob() {
  if (filename != "") {
    TFile* f = new TFile(filename.c_str());
    if (!f)
      throw cms::Exception("One2Two") << "could not read file " << filename;
    tree = (TTree*)f->Get(tree_path.c_str());
    if (!tree)
      throw cms::Exception("One2Two") << "could not get " << tree_path << " from file " << filename;
    tree->SetBranchAddress("run", &nt.run);
    tree->SetBranchAddress("lumi", &nt.lumi);
    tree->SetBranchAddress("event", &nt.event);
    tree->SetBranchAddress("nvtx", &nt.nvtx);
    tree->SetBranchAddress("ntk0", &nt.ntk0);
    tree->SetBranchAddress("x0", &nt.x0);
    tree->SetBranchAddress("y0", &nt.y0);
    tree->SetBranchAddress("z0", &nt.z0);
    tree->SetBranchAddress("ntk1", &nt.ntk1);
    tree->SetBranchAddress("x1", &nt.x1);
    tree->SetBranchAddress("y1", &nt.y1);
    tree->SetBranchAddress("z1", &nt.z1);

    int j = 0, je = tree->GetEntries();
    for (; j < je; ++j) {
      if (tree->LoadTree(j) < 0) break;
      if (tree->GetEntry(j) <= 0) continue;

      if (nt.nvtx == 1) {
	MFVVertexAux v0;
	v0.x = nt.x0; v0.y = nt.y0; v0.z = nt.z0; v0.bs2ddist = mag(nt.x0, nt.y0);
	for (int i = 0; i < nt.ntk0; ++i)
	  v0.insert_track();
	if (sel_vertex_aft(v0))
	  one_vertices.push_back(v0);
      }
      else if (nt.nvtx == 2) {
	MFVVertexAux v0, v1;
	v0.x = nt.x0; v0.y = nt.y0; v0.z = nt.z0; v0.bs2ddist = mag(nt.x0, nt.y0);
	v1.x = nt.x1; v1.y = nt.y1; v1.z = nt.z1; v1.bs2ddist = mag(nt.x1, nt.y1);
	for (int i = 0; i < nt.ntk0; ++i) v0.insert_track();
	for (int i = 0; i < nt.ntk1; ++i) v1.insert_track();
	bool sel0 = sel_vertex_aft(v0);
	bool sel1 = sel_vertex_aft(v1);
	if (sel0 && sel1)
	  two_vertices.push_back(std::make_pair(v0, v1));
	else if (sel0)
	  one_vertices.push_back(v0);
	else if (sel1)
	  one_vertices.push_back(v1);
      }
    }

    f->Close();
    delete f;
  }

  printf("h_nsv:");      for (int i = 1; i <= 10; ++i) printf(" %i", int(h_nsv   ->GetBinContent(i)));
  printf("\nh_nsvsel:"); for (int i = 1; i <= 10; ++i) printf(" %i", int(h_nsvsel->GetBinContent(i)));
  printf("\n# 1v: %i  # 2v: %i\n", int(one_vertices.size()), int(two_vertices.size()));

  if (filename == "")
    return;

  for (const auto& pair : two_vertices) {
    const MFVVertexAux& v0 = pair.first;
    const MFVVertexAux& v1 = pair.second;
    
    h_2v_xy->Fill(v0.x, v0.y);
    h_2v_xy->Fill(v1.x, v1.y);
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

    h_2v_ntracks->Fill(v0.ntracks(), v1.ntracks());
    h_2v_ntracks01->Fill(v0.ntracks() + v1.ntracks());
    h_2v_svdist2d->Fill(svdist2d(v0, v1));
    h_2v_svdz->Fill(dz(v0, v1));
    h_2v_dphi->Fill(dphi(v0, v1));
    h_2v_abs_dphi->Fill(fabs(dphi(v0, v1)));
    if (svdist2d(v0, v1) < 0.035) {
      h_2v_lt35_dphi->Fill(dphi(v0, v1));
      h_2v_lt35_abs_dphi->Fill(fabs(dphi(v0, v1)));
    }
    else {
      h_2v_gt35_dphi->Fill(dphi(v0, v1));
      h_2v_gt35_abs_dphi->Fill(fabs(dphi(v0, v1)));
    }
    h_2v_svdz_v_dphi->Fill(dphi(v0, v1), dz(v0, v1));
  }

  const int nonevertices = int(one_vertices.size());
  const int giveup = 20*nonevertices;
  TRandom3* rand = new TRandom3(121982);

  std::vector<bool> used(nonevertices, 0);
  const int npairsuse = npairs > 0 ? npairs : nonevertices/2;
  for (int ipair = 0; ipair < npairsuse; ++ipair) {
    int iv = -1;
    while (iv == -1) {
      int x = rand->Integer(nonevertices);
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
      int x = rand->Integer(nonevertices);
      if (x != iv && (wrep || !used[x])) {
	const MFVVertexAux& vx = one_vertices[x];
	const bool phi_ok = prob_dphi(v0, vx) > rand->Rndm();
	const bool dz_ok = use_f_dz ? prob_dz(v0, vx) > rand->Rndm() : fabs(v0.z - vx.z) < max_1v_dz;
	const bool ntracks_ok = v0.ntracks() + vx.ntracks() < max_1v_ntracks;
        ++tries;

	if (phi_ok && dz_ok && ntracks_ok) {
	  jv = x;
	  used[x] = true;
	  break;
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

    h_1v_xy->Fill(v0.x, v0.y);
    h_1v_xy->Fill(v1.x, v1.y);
    h_1v_bs2ddist->Fill(v0.bs2ddist);
    h_1v_bs2ddist->Fill(v1.bs2ddist);
    h_1v_bs2ddist_v_bsdz->Fill(v0.z, v0.bs2ddist);
    h_1v_bs2ddist_v_bsdz->Fill(v1.z, v1.bs2ddist);
    h_1v_bsdz->Fill(v0.z);
    h_1v_bsdz->Fill(v1.z);

    int ntk0 = v0.ntracks();
    int ntk1 = v1.ntracks();
    if (ntk1 > ntk0)
      h_1v_ntracks->Fill(ntk1, ntk0);
    else
      h_1v_ntracks->Fill(ntk0, ntk1);
    h_1v_ntracks01->Fill(v0.ntracks() + v1.ntracks());
    h_1v_svdist2d->Fill(svdist2d(v0, v1));
    h_1v_svdz->Fill(dz(v0, v1));
    h_1v_svdz_all->Fill(dz(v0, v1));
    h_1v_dphi->Fill(dphi(v0, v1));
    h_1v_abs_dphi->Fill(fabs(dphi(v0, v1)));
    h_1v_svdz_v_dphi->Fill(dphi(v0, v1), dz(v0, v1));
    h_1v_svdz_all_v_dphi->Fill(dphi(v0, v1), dz(v0, v1));
  }

  delete rand;
}

DEFINE_FWK_MODULE(MFVOne2Two);
